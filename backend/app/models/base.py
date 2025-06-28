# Importar todos los modelos para que SQLAlchemy los reconozca
from app.models.user import User
from app.models.elderly_person import ElderlyPerson
from app.models.device import Device
from app.models.event import Event
from app.models.alert import Alert
from app.models.reminder import Reminder
from app.models.device_config import DeviceConfig

# Agregar las relaciones faltantes
from sqlalchemy.orm import relationship

# Relación en User
User.elderly_persons = relationship("ElderlyPerson", back_populates="user", cascade="all, delete-orphan") 