from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.auth import AuthService
from app.models.user import User
from app.services.referral import ReferralService
from app.schemas.referral import (
    ReferralCreate, ReferralResponse, ReferralUpdate,
    ReferralCommissionResponse, ReferralStats,
    ReferralCodeGenerate, ReferralCodeResponse,
    ReferralValidation, ReferralValidationResponse
)

router = APIRouter()

@router.post("/generate-code", response_model=ReferralCodeResponse)
def generate_referral_code(
    code_data: ReferralCodeGenerate,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """Generate a referral code for the current user"""
    # Validate referrer type and ID
    if code_data.referrer_type not in ["caregiver", "institution", "family", "cared_person"]:
        raise HTTPException(status_code=400, detail="Tipo de referente inválido")
    
    # Check if user can generate codes for this type
    if code_data.referrer_type == "caregiver" and not current_user.has_role("caregiver"):
        raise HTTPException(status_code=403, detail="Solo los cuidadores pueden generar códigos de cuidador")
    
    if code_data.referrer_type == "family" and not current_user.has_role("family"):
        raise HTTPException(status_code=403, detail="Solo las familias pueden generar códigos de familia")
    
    # Generate referral code
    referral_code = code_data.custom_code or ReferralService.generate_referral_code()
    
    # Get commission rates
    commission_rates = ReferralService.COMMISSION_RATES.get(code_data.referrer_type, {})
    
    # Get usage count and earnings (simplified)
    usage_count = 0
    total_earnings = 0.0
    
    return ReferralCodeResponse(
        referral_code=referral_code,
        referrer_type=code_data.referrer_type,
        referrer_id=code_data.referrer_id,
        commission_rates=commission_rates,
        expiry_days=ReferralService.REFERRAL_EXPIRY_DAYS,
        usage_count=usage_count,
        total_earnings=total_earnings
    )

@router.post("/validate", response_model=ReferralValidationResponse)
def validate_referral_code(
    validation_data: ReferralValidation,
    db: Session = Depends(get_db)
):
    """Validate a referral code"""
    result = ReferralService.validate_referral_code(
        db, validation_data.referral_code, validation_data.referred_email
    )
    
    return ReferralValidationResponse(**result)

@router.post("/create", response_model=ReferralResponse)
def create_referral(
    referral_data: ReferralCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """Create a new referral"""
    # Validate referrer permissions
    if referral_data.referrer_type == "caregiver" and not current_user.has_role("caregiver"):
        raise HTTPException(status_code=403, detail="Solo los cuidadores pueden crear referidos de cuidador")
    
    if referral_data.referrer_type == "family" and not current_user.has_role("family"):
        raise HTTPException(status_code=403, detail="Solo las familias pueden crear referidos de familia")
    
    # Create referral
    referral = ReferralService.create_referral(db, referral_data)
    
    # Convert to response format
    return ReferralResponse(
        **referral.__dict__,
        days_since_created=referral.days_since_created,
        is_expirable=referral.is_expirable,
        total_commissions=0.0  # Will be calculated separately
    )

@router.get("/my-referrals", response_model=List[ReferralResponse])
def get_my_referrals(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """Get referrals created by current user"""
    # Get primary role (first active role)
    roles = current_user.roles
    referrer_type = roles[0].name if roles else "user"
    referrals = ReferralService.get_referrals_by_referrer(
        db, referrer_type, current_user.id, skip, limit
    )
    
    return [
        ReferralResponse(
            **referral.__dict__,
            days_since_created=referral.days_since_created,
            is_expirable=referral.is_expirable,
            total_commissions=0.0  # Will be calculated separately
        )
        for referral in referrals
    ]

@router.get("/my-commissions", response_model=List[ReferralCommissionResponse])
def get_my_commissions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """Get commissions for current user"""
    # Get primary role (first active role)
    roles = current_user.roles
    recipient_type = roles[0].name if roles else "user"
    commissions = ReferralService.get_commissions_by_recipient(
        db, recipient_type, current_user.id, skip, limit
    )
    
    return [ReferralCommissionResponse(**commission.__dict__) for commission in commissions]

@router.get("/stats", response_model=ReferralStats)
def get_referral_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """Get referral statistics for current user"""
    # Get primary role (first active role)
    roles = current_user.roles
    referrer_type = roles[0].name if roles else "user"
    stats = ReferralService.get_referral_stats(db, referrer_type, current_user.id)
    return stats

@router.get("/stats/all", response_model=ReferralStats)
def get_all_referral_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """Get all referral statistics (admin only)"""
    if not current_user.has_role("admin"):
        raise HTTPException(status_code=403, detail="Solo administradores pueden ver estadísticas globales")
    
    stats = ReferralService.get_referral_stats(db)
    return stats

@router.put("/{referral_id}/status")
def update_referral_status(
    referral_id: UUID,
    status_update: ReferralUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """Update referral status (admin only)"""
    if not current_user.has_role("admin"):
        raise HTTPException(status_code=403, detail="Solo administradores pueden actualizar estados")
    
    if not status_update.status:
        raise HTTPException(status_code=400, detail="El estado es requerido")
    
    referral = ReferralService.update_referral_status(
        db, referral_id, status_update.status, status_update.commission_amount
    )
    
    if not referral:
        raise HTTPException(status_code=404, detail="Referido no encontrado")
    
    return {"message": "Estado actualizado correctamente", "referral_id": referral_id}

@router.post("/commissions/{commission_id}/pay")
def pay_commission(
    commission_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """Mark commission as paid (admin only)"""
    if not current_user.has_role("admin"):
        raise HTTPException(status_code=403, detail="Solo administradores pueden pagar comisiones")
    
    commission = ReferralService.pay_commission(db, commission_id)
    
    if not commission:
        raise HTTPException(status_code=404, detail="Comisión no encontrada")
    
    return {"message": "Comisión marcada como pagada", "commission_id": commission_id}

@router.post("/expire-old")
def expire_old_referrals(
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """Expire old referrals (admin only)"""
    if not current_user.has_role("admin"):
        raise HTTPException(status_code=403, detail="Solo administradores pueden expirar referidos")
    
    expired_count = ReferralService.expire_old_referrals(db)
    
    return {
        "message": f"{expired_count} referidos expirados",
        "expired_count": expired_count
    }

@router.get("/bonus-eligibility")
def check_bonus_eligibility(
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """Check if current user is eligible for bonus"""
    # Get primary role (first active role)
    roles = current_user.roles
    referrer_type = roles[0].name if roles else "user"
    is_eligible = ReferralService.check_bonus_eligibility(
        db, referrer_type, current_user.id
    )
    
    return {
        "is_eligible": is_eligible,
        "min_referrals_required": ReferralService.MIN_REFERRALS_FOR_BONUS,
        "referrer_type": referrer_type
    } 