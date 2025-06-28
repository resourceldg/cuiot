# Viejos Son Los Trapos - Sistema de Monitoreo para Adultos Mayores

Un sistema completo de monitoreo y cuidado para adultos mayores que incluye dispositivos IoT, aplicación web, API backend y comunicación MQTT en tiempo real.

## 🚀 Estado del Proyecto

✅ **Funcionando correctamente**
- Backend FastAPI con PostgreSQL
- Frontend SvelteKit con TypeScript
- Base de datos PostgreSQL
- Redis para cache
- MQTT Broker para IoT
- Docker Compose para desarrollo

## 🏗️ Arquitectura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   Dispositivos  │
│   SvelteKit     │◄──►│   FastAPI       │◄──►│      IoT        │
│   (Puerto 3000) │    │  (Puerto 8000)  │    │   (MQTT 1883)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   PostgreSQL    │
                       │   (Puerto 5432) │
                       └─────────────────┘
```

## 🛠️ Tecnologías Utilizadas

### Backend
- **FastAPI** - Framework web moderno y rápido
- **PostgreSQL** - Base de datos principal
- **Redis** - Cache y sesiones
- **SQLAlchemy** - ORM
- **Alembic** - Migraciones de base de datos
- **Pydantic** - Validación de datos

### Frontend
- **SvelteKit** - Framework web reactivo
- **TypeScript** - Tipado estático
- **Tailwind CSS** - Framework CSS
- **Vite** - Build tool y dev server
- **Chart.js** - Gráficos
- **FullCalendar** - Calendario de eventos

### DevOps
- **Docker** - Containerización
- **Docker Compose** - Orquestación
- **MQTT** - Comunicación IoT
- **Adminer** - Gestión de base de datos

## 🚀 Inicio Rápido

### Prerrequisitos
- Docker
- Docker Compose

### Instalación y Ejecución

1. **Clonar el repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd viejos_son_los_trapos
   ```

2. **Iniciar el entorno de desarrollo**
   ```bash
   ./start-dev.sh
   ```

   O manualmente:
   ```bash
   docker-compose up --build -d
   ```

3. **Acceder a los servicios**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Documentación API: http://localhost:8000/docs
   - Adminer (DB): http://localhost:8080

## 📁 Estructura del Proyecto

```
viejos_son_los_trapos/
├── backend/                 # API FastAPI
│   ├── app/
│   │   ├── api/            # Endpoints de la API
│   │   ├── core/           # Configuración y utilidades
│   │   ├── models/         # Modelos de base de datos
│   │   ├── schemas/        # Esquemas Pydantic
│   │   └── services/       # Lógica de negocio
│   ├── alembic/            # Migraciones
│   └── requirements.txt    # Dependencias Python
├── web-panel/              # Frontend SvelteKit
│   ├── src/
│   │   ├── components/     # Componentes Svelte
│   │   ├── lib/           # Utilidades y tipos
│   │   └── routes/        # Páginas de la aplicación
│   └── package.json       # Dependencias Node.js
├── docker/                 # Configuración Docker
├── docker-compose.yml      # Orquestación de servicios
└── start-dev.sh           # Script de inicio
```

## 🔧 Desarrollo

### Comandos Útiles

```bash
# Ver logs de un servicio específico
docker-compose logs -f backend
docker-compose logs -f web-panel

# Reiniciar un servicio
docker-compose restart backend

# Parar todos los servicios
docker-compose down

# Reconstruir un servicio
docker-compose build web-panel

# Ejecutar comandos dentro de un contenedor
docker-compose exec backend python -m pytest
docker-compose exec web-panel npm run test
```

### Hot Reload

- **Frontend**: Los cambios en `web-panel/src/` se reflejan automáticamente
- **Backend**: Los cambios en `backend/app/` reinician automáticamente el servidor

### Base de Datos

- **Acceso directo**: `docker-compose exec postgres psql -U viejos_trapos_user -d viejos_trapos_db`
- **Interfaz web**: http://localhost:8080 (Adminer)
- **Migraciones**: `docker-compose exec backend alembic upgrade head`

## 📊 Funcionalidades

### Gestión de Adultos Mayores
- Registro y edición de perfiles
- Información médica y de contacto
- Estado de actividad en tiempo real

### Dispositivos IoT
- Registro y configuración de dispositivos
- Monitoreo de estado y conectividad
- Configuración de alertas

### Sistema de Alertas
- Alertas en tiempo real
- Diferentes niveles de severidad
- Notificaciones push y sonoras

### Eventos y Calendario
- Programación de eventos médicos
- Recordatorios de medicación
- Visitas familiares y actividades

### Dashboard
- Vista general del sistema
- Métricas en tiempo real
- Gráficos y estadísticas

## 🔒 Seguridad

- Autenticación JWT
- Validación de datos con Pydantic
- CORS configurado
- Variables de entorno para configuración

## 🧪 Testing

```bash
# Tests del backend
docker-compose exec backend python -m pytest

# Tests del frontend
docker-compose exec web-panel npm run test:ui
docker-compose exec web-panel npm run test:e2e
```

## 📝 API Documentation

La documentación completa de la API está disponible en:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 🆘 Soporte

Si encuentras algún problema:

1. Verifica que Docker esté ejecutándose
2. Revisa los logs: `docker-compose logs`
3. Reconstruye los contenedores: `docker-compose up --build -d`
4. Abre un issue en el repositorio

## 🎯 Roadmap

- [ ] Aplicación móvil React Native
- [ ] Integración con wearables
- [ ] Machine Learning para detección de anomalías
- [ ] Integración con servicios médicos
- [ ] Sistema de reportes avanzados
- [ ] Multi-tenancy
- [ ] API pública para desarrolladores 