import random
from datetime import datetime
from app.core.database import get_db
from app.models.package import Package

SAMPLE_PACKAGES = [
    # Individual packages
    {
        "package_type": "individual",
        "name": "Básico Individual",
        "description": "Plan básico para una persona con monitoreo esencial y alertas básicas.",
        "price_monthly": 5000,  # 50 ARS
        "price_yearly": 50000,  # 500 ARS
        "currency": "ARS",
        "max_users": 1,
        "max_devices": 3,
        "max_storage_gb": 5,
        "features": ["monitoreo_basico", "alertas_emergencia", "app_movil"],
        "limitations": ["sin_analiticas", "sin_integraciones"],
        "customizable_options": ["dispositivos_adicionales"],
        "add_ons_available": ["storage_extra", "analytics_basic"],
        "base_configuration": {"alertas": True, "monitoreo": True},
        "is_customizable": True,
        "support_level": "basic",
        "response_time_hours": 24,
        "is_active": True,
        "is_featured": False
    },
    {
        "package_type": "individual",
        "name": "Familiar Premium",
        "description": "Plan familiar con monitoreo avanzado, múltiples usuarios y análisis detallado.",
        "price_monthly": 12000,  # 120 ARS
        "price_yearly": 120000,  # 1200 ARS
        "currency": "ARS",
        "max_users": 5,
        "max_devices": 10,
        "max_storage_gb": 20,
        "features": ["monitoreo_avanzado", "alertas_inteligentes", "analytics_basico", "app_movil", "dashboard_web"],
        "limitations": ["sin_integraciones_avanzadas"],
        "customizable_options": ["usuarios_adicionales", "dispositivos_adicionales", "storage_extra"],
        "add_ons_available": ["analytics_advanced", "integrations_basic", "support_priority"],
        "base_configuration": {"alertas": True, "monitoreo": True, "analytics": True},
        "is_customizable": True,
        "support_level": "standard",
        "response_time_hours": 12,
        "is_active": True,
        "is_featured": True
    },
    # Professional packages
    {
        "package_type": "professional",
        "name": "Profesional Básico",
        "description": "Plan para profesionales de la salud con herramientas de monitoreo y reportes.",
        "price_monthly": 25000,  # 250 ARS
        "price_yearly": 250000,  # 2500 ARS
        "currency": "ARS",
        "max_users": 10,
        "max_devices": 25,
        "max_storage_gb": 50,
        "features": ["monitoreo_profesional", "reportes_detallados", "analytics_avanzado", "integraciones_basicas", "api_access"],
        "limitations": ["sin_soporte_24h"],
        "customizable_options": ["usuarios_adicionales", "dispositivos_adicionales", "storage_extra", "integraciones_avanzadas"],
        "add_ons_available": ["support_24h", "integrations_advanced", "white_label"],
        "base_configuration": {"alertas": True, "monitoreo": True, "analytics": True, "reportes": True},
        "is_customizable": True,
        "support_level": "standard",
        "response_time_hours": 8,
        "is_active": True,
        "is_featured": False
    },
    {
        "package_type": "professional",
        "name": "Profesional Plus",
        "description": "Plan profesional avanzado con soporte prioritario y herramientas especializadas.",
        "price_monthly": 45000,  # 450 ARS
        "price_yearly": 450000,  # 4500 ARS
        "currency": "ARS",
        "max_users": 25,
        "max_devices": 50,
        "max_storage_gb": 100,
        "features": ["monitoreo_profesional", "reportes_avanzados", "analytics_enterprise", "integraciones_avanzadas", "api_access", "white_label"],
        "limitations": [],
        "customizable_options": ["usuarios_adicionales", "dispositivos_adicionales", "storage_extra", "integraciones_avanzadas", "soporte_dedicado"],
        "add_ons_available": ["support_dedicated", "custom_integrations", "training_sessions"],
        "base_configuration": {"alertas": True, "monitoreo": True, "analytics": True, "reportes": True, "integraciones": True},
        "is_customizable": True,
        "support_level": "premium",
        "response_time_hours": 4,
        "is_active": True,
        "is_featured": True
    },
    # Institutional packages
    {
        "package_type": "institutional",
        "name": "Institucional Básico",
        "description": "Plan para instituciones pequeñas con monitoreo centralizado y gestión de múltiples usuarios.",
        "price_monthly": 80000,  # 800 ARS
        "price_yearly": 800000,  # 8000 ARS
        "currency": "ARS",
        "max_users": 50,
        "max_devices": 100,
        "max_storage_gb": 200,
        "features": ["monitoreo_institucional", "gestion_usuarios", "reportes_institucionales", "analytics_avanzado", "integraciones_basicas", "api_access"],
        "limitations": ["sin_soporte_dedicado"],
        "customizable_options": ["usuarios_adicionales", "dispositivos_adicionales", "storage_extra", "integraciones_avanzadas"],
        "add_ons_available": ["support_dedicated", "integrations_advanced", "custom_development"],
        "base_configuration": {"alertas": True, "monitoreo": True, "analytics": True, "reportes": True, "gestion": True},
        "is_customizable": True,
        "support_level": "premium",
        "response_time_hours": 6,
        "is_active": True,
        "is_featured": False
    },
    {
        "package_type": "institutional",
        "name": "Institucional Enterprise",
        "description": "Plan enterprise para grandes instituciones con soporte dedicado y personalización completa.",
        "price_monthly": 150000,  # 1500 ARS
        "price_yearly": 1500000,  # 15000 ARS
        "currency": "ARS",
        "max_users": None,  # Unlimited
        "max_devices": None,  # Unlimited
        "max_storage_gb": 500,
        "features": ["monitoreo_enterprise", "gestion_avanzada", "reportes_enterprise", "analytics_enterprise", "integraciones_avanzadas", "api_access", "white_label", "custom_development"],
        "limitations": [],
        "customizable_options": ["personalizacion_completa", "desarrollo_custom", "integraciones_especializadas"],
        "add_ons_available": ["support_enterprise", "custom_integrations", "training_program", "consulting_services"],
        "base_configuration": {"alertas": True, "monitoreo": True, "analytics": True, "reportes": True, "gestion": True, "integraciones": True},
        "is_customizable": True,
        "support_level": "enterprise",
        "response_time_hours": 2,
        "is_active": True,
        "is_featured": True
    }
]

def populate_packages():
    db = next(get_db())
    created = 0
    for data in SAMPLE_PACKAGES:
        pkg = db.query(Package).filter_by(name=data["name"]).first()
        if not pkg:
            pkg = Package(**data)
            db.add(pkg)
            created += 1
    db.commit()
    print(f"✅ Paquetes creados: {created} (idempotente)")
    db.close()

if __name__ == "__main__":
    populate_packages() 