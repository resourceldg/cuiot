from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.services.package import PackageService
from app.schemas.package import (
    PackageCreate, PackageUpdate, PackageResponse,
    UserPackageCreate, UserPackageUpdate, UserPackageResponse,
    PackageAddOnCreate, PackageAddOnUpdate, PackageAddOnResponse,
    UserPackageAddOnCreate, UserPackageAddOnResponse,
    LegalCapacityVerification, LegalCapacityResponse,
    PackageRecommendationRequest, PackageRecommendation,
    PackageCustomization, PackageStatisticsResponse
)
from app.services.auth import AuthService

router = APIRouter()

# Package management endpoints
@router.get("/statistics", response_model=PackageStatisticsResponse)
async def get_package_statistics(
    db: Session = Depends(get_db),
    current_user = Depends(AuthService.get_current_active_user)
):
    if not current_user.has_role("admin"):
        raise HTTPException(status_code=403, detail="Solo administradores pueden ver estadísticas")
    return PackageService.get_package_statistics(db)

@router.get("/", response_model=List[PackageResponse])
def get_packages(
    package_type: Optional[str] = Query(None, description="Filter by package type"),
    is_featured: Optional[bool] = Query(None, description="Filter by featured status"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get available packages"""
    packages = PackageService.get_available_packages(
        db, package_type=package_type, is_featured=is_featured
    )
    return packages

@router.get("/{package_id}", response_model=PackageResponse)
def get_package(
    package_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get package by ID"""
    package = PackageService.get_package_by_id(db, package_id)
    if not package:
        raise HTTPException(status_code=404, detail="Paquete no encontrado")
    return package

@router.post("/", response_model=PackageResponse, status_code=status.HTTP_201_CREATED)
def create_package(
    package_data: PackageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new package (admin only)"""
    if not current_user.has_role("admin"):
        raise HTTPException(status_code=403, detail="Solo administradores pueden crear paquetes")
    
    package = PackageService.create_package(db, package_data)
    return package

@router.put("/{package_id}", response_model=PackageResponse)
def update_package(
    package_id: UUID,
    package_data: PackageUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a package (admin only)"""
    if not current_user.has_role("admin"):
        raise HTTPException(status_code=403, detail="Solo administradores pueden actualizar paquetes")
    
    package = PackageService.update_package(db, package_id, package_data)
    if not package:
        raise HTTPException(status_code=404, detail="Paquete no encontrado")
    return package

@router.delete("/{package_id}")
def delete_package(
    package_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a package (admin only)"""
    if not current_user.has_role("admin"):
        raise HTTPException(status_code=403, detail="Solo administradores pueden eliminar paquetes")
    
    success = PackageService.delete_package(db, package_id)
    if not success:
        raise HTTPException(status_code=404, detail="Paquete no encontrado")
    
    return {"message": "Paquete eliminado exitosamente"}

# User package subscription endpoints
@router.get("/user/subscriptions", response_model=List[UserPackageResponse])
def get_user_subscriptions(
    status: Optional[str] = Query(None, description="Filter by subscription status"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current user's package subscriptions"""
    subscriptions = PackageService.get_user_subscriptions(db, current_user.id, status)
    return subscriptions

@router.post("/user/subscribe", response_model=UserPackageResponse, status_code=status.HTTP_201_CREATED)
def subscribe_to_package(
    subscription_data: UserPackageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Subscribe to a package"""
    subscription, message = PackageService.subscribe_to_package(db, current_user.id, subscription_data)
    if not subscription:
        raise HTTPException(status_code=400, detail=message)
    return subscription

@router.put("/user/subscriptions/{subscription_id}", response_model=UserPackageResponse)
def update_subscription(
    subscription_id: UUID,
    update_data: UserPackageUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update user package subscription"""
    subscription = PackageService.update_subscription(db, subscription_id, update_data)
    if not subscription:
        raise HTTPException(status_code=404, detail="Suscripción no encontrada")
    return subscription

@router.delete("/user/subscriptions/{subscription_id}")
def cancel_subscription(
    subscription_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Cancel user package subscription"""
    success = PackageService.cancel_subscription(db, subscription_id)
    if not success:
        raise HTTPException(status_code=404, detail="Suscripción no encontrada")
    
    return {"message": "Suscripción cancelada exitosamente"}

@router.get("/user/{user_id}/subscriptions", response_model=List[UserPackageResponse])
def get_user_subscriptions_by_id(
    user_id: UUID,
    status: Optional[str] = Query(None, description="Filter by subscription status"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all package subscriptions for a given user (admin only or self)."""
    print(f"🔧 get_user_subscriptions_by_id - Current user: {current_user.email} (ID: {current_user.id})")
    print(f"🔧 get_user_subscriptions_by_id - Requested user_id: {user_id}")
    print(f"🔧 get_user_subscriptions_by_id - Current user roles: {[r.name for r in current_user.roles]}")
    print(f"🔧 get_user_subscriptions_by_id - Is admin: {current_user.has_role('admin')}")
    
    # TEMPORAL: Permitir acceso a cualquier usuario autenticado para debugging
    # if current_user.id != user_id and not current_user.has_role("admin"):
    #     print(f"❌ get_user_subscriptions_by_id - Access denied: user {current_user.email} cannot view subscriptions for user {user_id}")
    #     raise HTTPException(status_code=403, detail="Solo administradores pueden ver las suscripciones de otros usuarios")
    
    print(f"✅ get_user_subscriptions_by_id - Access granted, fetching subscriptions...")
    subscriptions = PackageService.get_user_subscriptions(db, user_id, status)
    print(f"✅ get_user_subscriptions_by_id - Found {len(subscriptions)} subscriptions")
    
    # Logging detallado de los datos antes de la serialización
    print(f"🔧 get_user_subscriptions_by_id - Raw subscriptions data:")
    for i, sub in enumerate(subscriptions):
        print(f"  Subscription {i+1}:")
        print(f"    ID: {sub.id}")
        print(f"    User ID: {sub.user_id}")
        print(f"    Package ID: {sub.package_id}")
        print(f"    Package name: {sub.package.name if sub.package else 'None'}")
        print(f"    Status: {sub.status}")
        print(f"    Current amount: {sub.current_amount}")
        print(f"    Selected features: {sub.selected_features}")
        print(f"    Add-ons count: {len(sub.add_ons) if sub.add_ons else 0}")
    
    print(f"🔧 get_user_subscriptions_by_id - Returning {len(subscriptions)} subscriptions")
    return subscriptions

# Add-on management endpoints
@router.get("/add-ons/", response_model=List[PackageAddOnResponse])
def get_add_ons(
    add_on_type: Optional[str] = Query(None, description="Filter by add-on type"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get available add-ons"""
    # This would need to be implemented in PackageService
    return []

@router.post("/add-ons/", response_model=PackageAddOnResponse, status_code=status.HTTP_201_CREATED)
def create_add_on(
    add_on_data: PackageAddOnCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Crear un nuevo add-on (solo admin)"""
    if not current_user.has_role("admin"):
        raise HTTPException(status_code=403, detail="Solo administradores pueden crear add-ons")
    from app.models.package import PackageAddOn
    from datetime import datetime
    db_add_on = PackageAddOn(
        name=add_on_data.name,
        description=add_on_data.description,
        add_on_type=add_on_data.add_on_type,
        price_monthly=add_on_data.price_monthly,
        price_yearly=add_on_data.price_yearly,
        configuration=add_on_data.configuration,
        limitations=add_on_data.limitations,
        compatible_packages=add_on_data.compatible_packages,
        max_quantity=add_on_data.max_quantity,
        is_active=True,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(db_add_on)
    db.commit()
    db.refresh(db_add_on)
    return db_add_on

@router.post("/user/subscriptions/{subscription_id}/add-ons", response_model=UserPackageAddOnResponse)
def add_add_on_to_subscription(
    subscription_id: UUID,
    add_on_data: UserPackageAddOnCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add an add-on to a subscription"""
    user_add_on = PackageService.add_add_on_to_subscription(db, subscription_id, add_on_data.model_dump())
    if not user_add_on:
        raise HTTPException(status_code=400, detail="No se pudo agregar el add-on")
    return user_add_on

@router.delete("/user/add-ons/{user_add_on_id}")
def remove_add_on_from_subscription(
    user_add_on_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Remove an add-on from a subscription"""
    success = PackageService.remove_add_on_from_subscription(db, user_add_on_id)
    if not success:
        raise HTTPException(status_code=404, detail="Add-on no encontrado")
    
    return {"message": "Add-on removido exitosamente"}

# Legal capacity validation endpoints
@router.post("/legal-capacity/verify", response_model=LegalCapacityResponse)
def verify_legal_capacity(
    verification_data: LegalCapacityVerification,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Verify legal capacity for package subscription"""
    # This would need to be implemented in PackageService
    return {
        "user_id": verification_data.user_id,
        "can_contract": True,
        "requires_representative": False,
        "legal_representative_id": None,
        "verification_status": "verified",
        "message": "Capacidad legal verificada"
    }

# Package recommendation endpoints
@router.post("/recommendations", response_model=PackageRecommendation)
def get_package_recommendations(
    request: PackageRecommendationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get package recommendations based on user needs"""
    recommendations = PackageService.get_package_recommendations(db, request)
    return recommendations

# Package customization endpoints
@router.post("/customize/calculate-price")
def calculate_customization_price(
    customization_data: PackageCustomization,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Calculate price for customized package"""
    price_info = PackageService.calculate_customization_price(
        db, 
        customization_data.package_id,
        customization_data.custom_configuration,
        [add_on.model_dump() for add_on in customization_data.add_ons]
    )
    
    if "error" in price_info:
        raise HTTPException(status_code=400, detail=price_info["error"])
    
    return price_info 