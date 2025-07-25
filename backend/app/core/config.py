from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    """Configuración de la aplicación"""
    
    # Configuración de la aplicación
    app_name: str = "Sistema Integral de Monitoreo API"
    version: str = "1.0.0"
    environment: str = "development"
    
    # Base de datos - Configuración por entorno
    database_url: str = "postgresql://viejos_trapos_user:viejos_trapos_pass@postgres:5432/viejos_trapos_db"
    test_database_url: str = "postgresql://viejos_trapos_user:viejos_trapos_pass@postgres:5432/viejos_trapos_test_db"
    
    # Determinar URL de base de datos según entorno
    @property
    def get_database_url(self) -> str:
        """Retorna la URL de base de datos según el entorno"""
        if self.environment == "test":
            return self.test_database_url
        return self.database_url
    
    # Redis
    redis_url: str = "redis://redis:6379"
    
    # Seguridad
    secret_key: str = "viejos_trapos_secret_key_dev"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 480  # 8 horas para desarrollo
    
    # MQTT
    mqtt_broker: str = "mqtt"
    mqtt_port: int = 1883
    mqtt_username: Optional[str] = None
    mqtt_password: Optional[str] = None
    
    # Configuración de alertas
    movement_timeout_hours: int = 3  # Horas sin movimiento para alertar
    heartbeat_timeout_minutes: int = 5  # Minutos sin heartbeat para alertar
    
    # Configuración de notificaciones
    enable_email_notifications: bool = False
    enable_push_notifications: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Instancia global de configuración
settings = Settings() 