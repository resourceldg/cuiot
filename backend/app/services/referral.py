from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from datetime import datetime, timedelta
import secrets
import string

from app.models.referral import Referral, ReferralCommission
from app.models.user import User
from app.models.cared_person import CaredPerson
from app.models.institution import Institution
from app.schemas.referral import (
    ReferralCreate, ReferralUpdate, ReferralCommissionCreate,
    ReferralStats, ReferralCodeGenerate, ReferralValidation
)

class ReferralService:
    """Service for managing referrals and commissions"""
    
    # Commission rates by referrer type
    COMMISSION_RATES = {
        "caregiver": {
            "first_month": 0.15,  # 15% of first month
            "recurring": 0.05,    # 5% of recurring months
            "bonus": 0.10         # 10% bonus for high performers
        },
        "institution": {
            "first_month": 0.10,  # 10% of first month
            "recurring": 0.03,    # 3% of recurring months
            "bonus": 0.05         # 5% bonus for high performers
        },
        "family": {
            "first_month": 0.05,  # 5% of first month
            "recurring": 0.02,    # 2% of recurring months
            "bonus": 0.03         # 3% bonus for high performers
        },
        "cared_person": {
            "first_month": 0.05,  # 5% of first month
            "recurring": 0.02,    # 2% of recurring months
            "bonus": 0.03         # 3% bonus for high performers
        }
    }
    
    # Referral expiry days
    REFERRAL_EXPIRY_DAYS = 30
    
    # Minimum referrals for bonus
    MIN_REFERRALS_FOR_BONUS = 5
    
    @staticmethod
    def generate_referral_code(length: int = 8) -> str:
        """Generate a unique referral code"""
        alphabet = string.ascii_uppercase + string.digits
        while True:
            code = ''.join(secrets.choice(alphabet) for _ in range(length))
            # Check if code already exists (would need to be implemented with DB check)
            return code
    
    @staticmethod
    def create_referral(db: Session, referral_data: ReferralCreate) -> Referral:
        """Create a new referral"""
        # Generate referral code if not provided
        if not referral_data.referral_code:
            referral_data.referral_code = ReferralService.generate_referral_code()
        
        # Create referral
        db_referral = Referral(**referral_data.model_dump())
        db.add(db_referral)
        db.commit()
        db.refresh(db_referral)
        
        return db_referral
    
    @staticmethod
    def get_referral_by_code(db: Session, referral_code: str) -> Optional[Referral]:
        """Get referral by code"""
        return db.query(Referral).filter(Referral.referral_code == referral_code).first()
    
    @staticmethod
    def get_referrals_by_referrer(
        db: Session, 
        referrer_type: str, 
        referrer_id: UUID,
        skip: int = 0,
        limit: int = 100
    ) -> List[Referral]:
        """Get referrals by referrer"""
        return db.query(Referral).filter(
            and_(
                Referral.referrer_type == referrer_type,
                Referral.referrer_id == referrer_id
            )
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_referral_status(
        db: Session, 
        referral_id: UUID, 
        status: str,
        commission_amount: Optional[float] = None
    ) -> Optional[Referral]:
        """Update referral status"""
        referral = db.query(Referral).filter(Referral.id == referral_id).first()
        if not referral:
            return None
        
        referral.status = status
        
        if status == "registered":
            referral.registered_at = datetime.utcnow()
        elif status == "converted":
            referral.converted_at = datetime.utcnow()
            if commission_amount:
                referral.commission_amount = commission_amount
        elif status == "expired":
            referral.expired_at = datetime.utcnow()
        
        db.commit()
        db.refresh(referral)
        return referral
    
    @staticmethod
    def validate_referral_code(
        db: Session, 
        referral_code: str, 
        referred_email: str
    ) -> Dict[str, Any]:
        """Validate a referral code"""
        referral = ReferralService.get_referral_by_code(db, referral_code)
        
        if not referral:
            return {
                "is_valid": False,
                "error_message": "Código de referido inválido"
            }
        
        if referral.status == "expired":
            return {
                "is_valid": False,
                "error_message": "Código de referido expirado"
            }
        
        if referral.status == "converted":
            return {
                "is_valid": False,
                "error_message": "Código de referido ya utilizado"
            }
        
        # Check if email already exists
        existing_user = db.query(User).filter(User.email == referred_email).first()
        if existing_user:
            return {
                "is_valid": False,
                "error_message": "El email ya está registrado"
            }
        
        # Get referrer info
        referrer_name = ReferralService._get_referrer_name(db, referral.referrer_type, referral.referrer_id)
        commission_info = ReferralService.COMMISSION_RATES.get(referral.referrer_type, {})
        
        return {
            "is_valid": True,
            "referrer_name": referrer_name,
            "referrer_type": referral.referrer_type,
            "commission_info": commission_info
        }
    
    @staticmethod
    def _get_referrer_name(db: Session, referrer_type: str, referrer_id: UUID) -> Optional[str]:
        """Get referrer name by type and ID"""
        if referrer_type == "caregiver":
            user = db.query(User).filter(User.id == referrer_id).first()
            return f"{user.first_name} {user.last_name}" if user else None
        elif referrer_type == "institution":
            institution = db.query(Institution).filter(Institution.id == referrer_id).first()
            return institution.name if institution else None
        elif referrer_type == "family":
            user = db.query(User).filter(User.id == referrer_id).first()
            return f"{user.first_name} {user.last_name}" if user else None
        elif referrer_type == "cared_person":
            cared_person = db.query(CaredPerson).filter(CaredPerson.id == referrer_id).first()
            return cared_person.full_name if cared_person else None
        return None
    
    @staticmethod
    def create_commission(
        db: Session, 
        referral_id: UUID,
        recipient_type: str,
        recipient_id: UUID,
        amount: float,
        commission_type: str,
        percentage: float
    ) -> ReferralCommission:
        """Create a new commission"""
        commission_data = ReferralCommissionCreate(
            referral_id=referral_id,
            recipient_type=recipient_type,
            recipient_id=recipient_id,
            amount=amount,
            commission_type=commission_type,
            percentage=percentage
        )
        
        db_commission = ReferralCommission(**commission_data.model_dump())
        db.add(db_commission)
        db.commit()
        db.refresh(db_commission)
        
        return db_commission
    
    @staticmethod
    def get_commissions_by_recipient(
        db: Session,
        recipient_type: str,
        recipient_id: UUID,
        skip: int = 0,
        limit: int = 100
    ) -> List[ReferralCommission]:
        """Get commissions by recipient"""
        return db.query(ReferralCommission).filter(
            and_(
                ReferralCommission.recipient_type == recipient_type,
                ReferralCommission.recipient_id == recipient_id
            )
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def pay_commission(db: Session, commission_id: UUID) -> Optional[ReferralCommission]:
        """Mark commission as paid"""
        commission = db.query(ReferralCommission).filter(ReferralCommission.id == commission_id).first()
        if not commission:
            return None
        
        commission.mark_as_paid()
        db.commit()
        db.refresh(commission)
        return commission
    
    @staticmethod
    def get_referral_stats(
        db: Session,
        referrer_type: Optional[str] = None,
        referrer_id: Optional[UUID] = None
    ) -> ReferralStats:
        """Get referral statistics"""
        query = db.query(Referral)
        
        if referrer_type and referrer_id:
            query = query.filter(
                and_(
                    Referral.referrer_type == referrer_type,
                    Referral.referrer_id == referrer_id
                )
            )
        
        total_referrals = query.count()
        pending_referrals = query.filter(Referral.status == "pending").count()
        registered_referrals = query.filter(Referral.status == "registered").count()
        converted_referrals = query.filter(Referral.status == "converted").count()
        expired_referrals = query.filter(Referral.status == "expired").count()
        
        conversion_rate = (converted_referrals / total_referrals * 100) if total_referrals > 0 else 0
        
        # Commission stats
        commission_query = db.query(ReferralCommission)
        if referrer_type and referrer_id:
            commission_query = commission_query.filter(
                and_(
                    ReferralCommission.recipient_type == referrer_type,
                    ReferralCommission.recipient_id == referrer_id
                )
            )
        
        total_commissions_paid = commission_query.filter(ReferralCommission.status == "paid").with_entities(
            func.sum(ReferralCommission.amount)
        ).scalar() or 0
        
        total_commissions_pending = commission_query.filter(ReferralCommission.status == "pending").with_entities(
            func.sum(ReferralCommission.amount)
        ).scalar() or 0
        
        avg_commission_amount = commission_query.with_entities(
            func.avg(ReferralCommission.amount)
        ).scalar() or 0
        
        return ReferralStats(
            total_referrals=total_referrals,
            pending_referrals=pending_referrals,
            registered_referrals=registered_referrals,
            converted_referrals=converted_referrals,
            expired_referrals=expired_referrals,
            conversion_rate=conversion_rate,
            total_commissions_paid=total_commissions_paid,
            total_commissions_pending=total_commissions_pending,
            avg_commission_amount=avg_commission_amount
        )
    
    @staticmethod
    def expire_old_referrals(db: Session) -> int:
        """Expire referrals older than REFERRAL_EXPIRY_DAYS"""
        expiry_date = datetime.utcnow() - timedelta(days=ReferralService.REFERRAL_EXPIRY_DAYS)
        
        expired_count = db.query(Referral).filter(
            and_(
                Referral.status == "pending",
                Referral.created_at < expiry_date
            )
        ).update({"status": "expired", "expired_at": datetime.utcnow()})
        
        db.commit()
        return expired_count
    
    @staticmethod
    def calculate_commission_amount(
        subscription_amount: float,
        referrer_type: str,
        commission_type: str
    ) -> float:
        """Calculate commission amount"""
        rates = ReferralService.COMMISSION_RATES.get(referrer_type, {})
        percentage = rates.get(commission_type, 0)
        return subscription_amount * percentage
    
    @staticmethod
    def check_bonus_eligibility(
        db: Session,
        referrer_type: str,
        referrer_id: UUID
    ) -> bool:
        """Check if referrer is eligible for bonus"""
        converted_count = db.query(Referral).filter(
            and_(
                Referral.referrer_type == referrer_type,
                Referral.referrer_id == referrer_id,
                Referral.status == "converted"
            )
        ).count()
        
        return converted_count >= ReferralService.MIN_REFERRALS_FOR_BONUS 