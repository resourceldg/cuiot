from typing import List, Optional, Dict, Any, Tuple
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from datetime import datetime, date, timedelta

from app.models.package import Package, UserPackage, PackageAddOn, UserPackageAddOn
from app.models.user import User
from app.models.cared_person import CaredPerson
from app.schemas.package import (
    PackageCreate, PackageUpdate, UserPackageCreate, UserPackageUpdate,
    PackageAddOnCreate, PackageAddOnUpdate, UserPackageAddOnCreate,
    LegalCapacityVerification, PackageRecommendationRequest
)
from app.services.referral import ReferralService
from app.models.care_type import CareType

class PackageService:
    """Service for managing packages and subscriptions"""
    
    @staticmethod
    def get_available_packages(
        db: Session, 
        package_type: Optional[str] = None,
        is_active: bool = True,
        is_featured: Optional[bool] = None
    ) -> List[Package]:
        query = db.query(Package)
        if is_active:
            query = query.filter(Package.is_active == True)
        if package_type:
            query = query.filter(Package.package_type == package_type)
        if is_featured is not None:
            query = query.filter(Package.is_featured == is_featured)
        return query.order_by(Package.price_monthly).all()

    @staticmethod
    def get_package_by_id(db: Session, package_id: UUID) -> Optional[Package]:
        return db.query(Package).filter(Package.id == package_id).first()

    @staticmethod
    def create_package(db: Session, package_data: PackageCreate) -> Package:
        db_package = Package(**package_data.model_dump())
        db.add(db_package)
        db.commit()
        db.refresh(db_package)
        return db_package

    @staticmethod
    def update_package(db: Session, package_id: UUID, package_data: PackageUpdate) -> Optional[Package]:
        package = PackageService.get_package_by_id(db, package_id)
        if not package:
            return None
        update_data = package_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(package, field, value)
        db.commit()
        db.refresh(package)
        return package

    @staticmethod
    def delete_package(db: Session, package_id: UUID) -> bool:
        package = PackageService.get_package_by_id(db, package_id)
        if not package:
            return False
        package.is_active = False
        db.commit()
        return True

    @staticmethod
    def validate_legal_capacity(db: Session, user_id: UUID, package_id: UUID) -> Dict[str, Any]:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {
                "can_contract": False,
                "requires_representative": False,
                "verification_status": "error",
                "message": "Usuario no encontrado"
            }
        
        # Buscar el ID del tipo de cuidado "delegated"
        delegated_care_type = db.query(CareType).filter(CareType.name == "delegated").first()
        if not delegated_care_type:
            return {
                "can_contract": True,
                "requires_representative": False,
                "verification_status": "verified",
                "message": "Usuario puede contratar directamente"
            }
        
        cared_persons = db.query(CaredPerson).filter(
            and_(CaredPerson.user_id == user_id, CaredPerson.care_type_id == delegated_care_type.id)
        ).all()
        if cared_persons:
            return {
                "can_contract": False,
                "requires_representative": True,
                "verification_status": "required",
                "message": "Usuario tiene personas bajo cuidado delegado. Se requiere verificación de capacidad legal."
            }
        cared_person = db.query(CaredPerson).filter(
            and_(CaredPerson.user_id == user_id, CaredPerson.care_type_id == delegated_care_type.id)
        ).first()
        if cared_person:
            return {
                "can_contract": False,
                "requires_representative": True,
                "verification_status": "required",
                "message": "Usuario bajo cuidado delegado. Debe contratar a través de su representante legal."
            }
        return {
            "can_contract": True,
            "requires_representative": False,
            "verification_status": "verified",
            "message": "Usuario puede contratar directamente"
        }

    @staticmethod
    def subscribe_to_package(db: Session, user_id: UUID, subscription_data: UserPackageCreate) -> Tuple[Optional[UserPackage], str]:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None, "Usuario no encontrado"
        # Validar roles permitidos
        allowed_roles = [
            "institution_admin",  # Solo admin institucional puede contratar
            "cared_person_self",
            "family", "family_member"
        ]
        user_roles = [r.name for r in user.roles if getattr(r, 'is_active', True)]
        # Si es staff institucional y no admin, solo puede ver
        if "institution_staff" in user_roles and not any(r in user_roles for r in ["institution_admin"]):
            return None, "Solo el administrador de la institución puede contratar paquetes. El staff solo puede visualizar."
        if not any(role in allowed_roles for role in user_roles):
            return None, "Solo instituciones (admin), personas auto-cuidantes y familias pueden contratar paquetes."
        # Validar capacidad legal
        legal_check = PackageService.validate_legal_capacity(db, user_id, subscription_data.package_id)
        if not legal_check["can_contract"]:
            return None, legal_check["message"]
        package = PackageService.get_package_by_id(db, subscription_data.package_id)
        if not package:
            return None, "Paquete no encontrado"
        if not package.is_active:
            return None, "Paquete no está disponible"
        base_price = package.price_monthly if subscription_data.billing_cycle == "monthly" else package.price_yearly
        if not base_price:
            return None, "Precio no disponible para el ciclo de facturación seleccionado"
        final_price = base_price
        referral_applied = False
        referral_code = getattr(subscription_data, "referral_code", None)
        if referral_code:
            referral_result = ReferralService.validate_referral_code(
                db, referral_code, "user@example.com"
            )
            if referral_result.get("is_valid"):
                discount_percentage = 0.10
                final_price = int(base_price * (1 - discount_percentage))
                referral_applied = True
        today = date.today()
        if subscription_data.billing_cycle == "monthly":
            next_billing = today + timedelta(days=30)
        else:
            next_billing = today + timedelta(days=365)
        user_package_data = subscription_data.model_dump()
        user_package_data.pop("add_ons", None)
        user_package_data.pop("referral_code", None)
        
        # Buscar el ID del status_type "active"
        from app.models.status_type import StatusType
        active_status = db.query(StatusType).filter(StatusType.name == "active").first()
        
        db_user_package = UserPackage(
            **user_package_data,
            user_id=user_id,
            start_date=today,
            current_amount=final_price,
            next_billing_date=next_billing,
            status_type_id=active_status.id if active_status else None,
            referral_code_used=getattr(subscription_data, "referral_code", None),
            referral_commission_applied=referral_applied,
            legal_capacity_verified=legal_check["verification_status"] == "verified"
        )
        db.add(db_user_package)
        db.commit()
        db.refresh(db_user_package)
        return db_user_package, "Suscripción creada exitosamente"

    @staticmethod
    def get_user_subscriptions(db: Session, user_id: UUID, status: Optional[str] = None) -> List[UserPackage]:
        query = db.query(UserPackage).filter(UserPackage.user_id == user_id)
        if status:
            # Buscar el ID del status_type correspondiente
            from app.models.status_type import StatusType
            status_type = db.query(StatusType).filter(StatusType.name == status).first()
            if status_type:
                query = query.filter(UserPackage.status_type_id == status_type.id)
        return query.all()

    @staticmethod
    def update_subscription(db: Session, subscription_id: UUID, update_data: UserPackageUpdate) -> Optional[UserPackage]:
        subscription = db.query(UserPackage).filter(UserPackage.id == subscription_id).first()
        if not subscription:
            return None
        update_dict = update_data.model_dump(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(subscription, field, value)
        db.commit()
        db.refresh(subscription)
        return subscription

    @staticmethod
    def cancel_subscription(db: Session, subscription_id: UUID) -> bool:
        subscription = db.query(UserPackage).filter(UserPackage.id == subscription_id).first()
        if not subscription:
            return False
        subscription.cancel_subscription()
        db.commit()
        return True

    @staticmethod
    def add_add_on_to_subscription(db: Session, subscription_id: UUID, add_on_data: Dict[str, Any]) -> Optional[UserPackageAddOn]:
        subscription = db.query(UserPackage).filter(UserPackage.id == subscription_id).first()
        if not subscription:
            return None
        add_on = db.query(PackageAddOn).filter(PackageAddOn.id == add_on_data["add_on_id"]).first()
        if not add_on or not add_on.is_active:
            return None
        add_on_price = add_on.price_monthly if add_on_data.get("billing_cycle") == "monthly" else add_on.price_yearly
        if not add_on_price:
            return None
        total_price = add_on_price * add_on_data.get("quantity", 1)
        
        # Buscar el ID del status_type "active"
        from app.models.status_type import StatusType
        active_status = db.query(StatusType).filter(StatusType.name == "active").first()
        
        db_user_add_on = UserPackageAddOn(
            user_package_id=subscription_id,
            add_on_id=add_on_data["add_on_id"],
            quantity=add_on_data.get("quantity", 1),
            custom_configuration=add_on_data.get("custom_configuration"),
            billing_cycle=add_on_data.get("billing_cycle", "monthly"),
            current_amount=total_price,
            status_type_id=active_status.id if active_status else None
        )
        db.add(db_user_add_on)
        db.commit()
        db.refresh(db_user_add_on)
        return db_user_add_on

    @staticmethod
    def remove_add_on_from_subscription(db: Session, user_add_on_id: UUID) -> bool:
        user_add_on = db.query(UserPackageAddOn).filter(UserPackageAddOn.id == user_add_on_id).first()
        if not user_add_on:
            return False
        
        # Buscar el ID del status_type "cancelled"
        from app.models.status_type import StatusType
        cancelled_status = db.query(StatusType).filter(StatusType.name == "cancelled").first()
        if cancelled_status:
            user_add_on.status_type_id = cancelled_status.id
        else:
            # Fallback: usar el campo status legacy si no existe el status_type
            user_add_on.status = "cancelled"
        
        db.commit()
        return True

    @staticmethod
    def get_package_recommendations(db: Session, request: PackageRecommendationRequest) -> Dict[str, Any]:
        packages = PackageService.get_available_packages(db, request.user_type)
        if not packages:
            return {
                "user_type": request.user_type,
                "recommended_package": None,
                "alternative_packages": [],
                "reasoning": "No hay paquetes disponibles para este tipo de usuario",
                "customization_suggestions": None
            }
        recommended = packages[0]
        if request.budget_monthly:
            affordable_packages = [p for p in packages if p.price_monthly <= request.budget_monthly]
            if affordable_packages:
                recommended = affordable_packages[0]
        if request.required_features:
            feature_compatible = []
            for package in packages:
                if package.features:
                    package_features = package.features.get("features", [])
                    if all(feature in package_features for feature in request.required_features):
                        feature_compatible.append(package)
            if feature_compatible:
                recommended = feature_compatible[0]
        alternatives = [p for p in packages if p.id != recommended.id][:3]
        return {
            "user_type": request.user_type,
            "recommended_package": recommended,
            "alternative_packages": alternatives,
            "reasoning": f"Recomendado basado en tipo de usuario '{request.user_type}' y necesidades especificadas",
            "customization_suggestions": None
        }

    @staticmethod
    def calculate_customization_price(db: Session, package_id: UUID, custom_configuration: Dict[str, Any], add_ons: List[Dict[str, Any]]) -> Dict[str, Any]:
        package = PackageService.get_package_by_id(db, package_id)
        if not package:
            return {"error": "Paquete no encontrado"}
        base_price = package.price_monthly
        total_add_ons_price = 0
        for add_on_data in add_ons:
            add_on = db.query(PackageAddOn).filter(PackageAddOn.id == add_on_data["add_on_id"]).first()
            if add_on and add_on.is_active:
                add_on_price = add_on.price_monthly
                quantity = add_on_data.get("quantity", 1)
                total_add_ons_price += add_on_price * quantity
        customization_multiplier = 1.0
        if custom_configuration.get("premium_support"):
            customization_multiplier += 0.2
        if custom_configuration.get("advanced_analytics"):
            customization_multiplier += 0.15
        final_price = int((base_price + total_add_ons_price) * customization_multiplier)
        return {
            "base_price": base_price,
            "add_ons_price": total_add_ons_price,
            "customization_multiplier": customization_multiplier,
            "final_price": final_price,
            "final_price_ars": final_price / 100
        }

    @staticmethod
    def get_package_statistics(db: Session) -> Dict[str, Any]:
        total_packages = db.query(Package).filter(Package.is_active == True).count()
        
        # Buscar el ID del status_type "active"
        from app.models.status_type import StatusType
        active_status = db.query(StatusType).filter(StatusType.name == "active").first()
        
        if active_status:
            total_subscriptions = db.query(UserPackage).filter(UserPackage.status_type_id == active_status.id).count()
            active_subscriptions = db.query(UserPackage).filter(UserPackage.status_type_id == active_status.id).all()
            package_types = db.query(
                Package.package_type,
                func.count(UserPackage.id)
            ).join(UserPackage).filter(
                UserPackage.status_type_id == active_status.id
            ).group_by(Package.package_type).all()
        else:
            total_subscriptions = 0
            active_subscriptions = []
            package_types = []
        
        total_revenue = sum(sub.current_amount for sub in active_subscriptions)
        return {
            "total_packages": total_packages,
            "total_subscriptions": total_subscriptions,
            "total_revenue_cents": total_revenue,
            "total_revenue_ars": total_revenue / 100,
            "package_type_distribution": dict(package_types)
        }
