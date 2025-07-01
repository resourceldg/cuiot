## Diagnósticos clínicos con adjuntos

### Crear diagnóstico con adjuntos

**POST** `/api/v1/diagnoses/`

Crea un nuevo diagnóstico clínico para una persona bajo cuidado, permitiendo adjuntar archivos médicos (PDFs, imágenes, etc.) junto con los datos estructurados del diagnóstico.

**Tipo de contenido:** `multipart/form-data`

**Campos esperados:**

| Campo             | Tipo         | Requerido | Descripción                                      |
|-------------------|--------------|-----------|--------------------------------------------------|
| diagnosis_name    | string       | Sí        | Nombre estandarizado del diagnóstico             |
| description       | string       | No        | Descripción clínica detallada                    |
| severity_level    | string       | No        | Gravedad (mild, moderate, severe, etc.)          |
| diagnosis_date    | string (ISO) | No        | Fecha del diagnóstico (YYYY-MM-DD)               |
| doctor_name       | string       | No        | Nombre del profesional que realiza el diagnóstico|
| medical_notes     | string       | No        | Notas adicionales                                |
| cie10_code        | string       | No        | Código CIE-10                                    |
| cared_person_id   | UUID         | Sí        | ID de la persona bajo cuidado                    |
| is_active         | boolean      | No        | Estado del diagnóstico (por defecto: true)       |
| files             | archivo(s)   | No        | Uno o más archivos adjuntos (PDF, imagen, etc.)  |

**Ejemplo de request (cURL):**

```bash
curl -X POST "https://tuservidor/api/v1/diagnoses/" \
  -H "Authorization: Bearer <token>" \
  -F "diagnosis_name=Diabetes tipo 2" \
  -F "description=Paciente con diabetes y antecedentes familiares" \
  -F "severity_level=moderate" \
  -F "diagnosis_date=2024-07-01" \
  -F "doctor_name=Dr. House" \
  -F "cared_person_id=123e4567-e89b-12d3-a456-426614174000" \
  -F "is_active=true" \
  -F "files=@/ruta/al/archivo1.pdf" \
  -F "files=@/ruta/al/imagen1.jpg"
```

**Respuesta exitosa (`200` o `201`):**

```json
{
  "id": "uuid-del-diagnostico",
  "diagnosis_name": "Diabetes tipo 2",
  "description": "Paciente con diabetes y antecedentes familiares",
  "severity_level": "moderate",
  "diagnosis_date": "2024-07-01T00:00:00",
  "doctor_name": "Dr. House",
  "medical_notes": null,
  "cie10_code": null,
  "attachments": [
    {
      "filename": "archivo1.pdf",
      "url": "/static/diagnoses/uuid_archivo1.pdf",
      "content_type": "application/pdf",
      "size": 123456
    },
    {
      "filename": "imagen1.jpg",
      "url": "/static/diagnoses/uuid_imagen1.jpg",
      "content_type": "image/jpeg",
      "size": 234567
    }
  ],
  "is_active": true,
  "cared_person_id": "123e4567-e89b-12d3-a456-426614174000",
  "created_by_id": "uuid-del-usuario",
  "created_at": "2024-07-01T12:34:56",
  "updated_by_id": null,
  "updated_at": null
}
```

**Notas:**
- Los archivos adjuntos se almacenan en el servidor y se exponen como URLs accesibles.
- El endpoint requiere autenticación (`Bearer token`).
- Los campos adicionales y la estructura pueden adaptarse según necesidades clínicas o regulatorias.

## Endpoints de Reportes Clínicos y de Cuidado

### Crear reporte

**POST** `/api/v1/reports/`

- Soporta `multipart/form-data` para adjuntar archivos.
- Campos principales:
  - `title` (str, requerido): Título del reporte.
  - `description` (str, opcional): Descripción detallada.
  - `report_type` (str, requerido): Tipo de reporte. Valores sugeridos:
    - higiene
    - alimentacion
    - evacuacion
    - conducta
    - estado_animo
    - incidente
    - turno
    - clinico
    - general
    - otro
  - `is_autocuidado` (bool, opcional): Si es un reporte de autocuidado.
  - `cared_person_id` (UUID, requerido si no es autocuidado): Persona bajo cuidado asociada.
  - `files` (uno o varios archivos, opcional): Adjuntos (imágenes, PDFs, etc.).

#### Ejemplo de request (cURL)

```bash
curl -X POST "http://localhost:8000/api/v1/reports/" \
  -H "Authorization: Bearer <token>" \
  -F "title=Reporte de higiene matutina" \
  -F "description=Baño y cambio de ropa realizado sin incidentes." \
  -F "report_type=higiene" \
  -F "cared_person_id=..." \
  -F "files=@/ruta/a/imagen1.jpg" \
  -F "files=@/ruta/a/nota.pdf"
```

#### Ejemplo de response

```json
{
  "id": "...",
  "title": "Reporte de higiene matutina",
  "description": "Baño y cambio de ropa realizado sin incidentes.",
  "report_type": "higiene",
  "attached_files": [
    {
      "filename": "imagen1.jpg",
      "url": "/static/reports/uuid_imagen1.jpg",
      "content_type": "image/jpeg",
      "size": 123456
    },
    {
      "filename": "nota.pdf",
      "url": "/static/reports/uuid_nota.pdf",
      "content_type": "application/pdf",
      "size": 45678
    }
  ],
  "is_autocuidado": false,
  "cared_person_id": "...",
  "created_by_id": "...",
  "created_at": "2024-06-01T10:00:00Z",
  "updated_at": null
}
```

### Validación de tipos de reporte

- El campo `report_type` debe ser uno de los valores sugeridos.
- Si usas Pydantic v1, valida manualmente con:
  ```python
  ReportBase.validate_report_type(report_type)
  ```
- Si usas Pydantic v2, puedes activar la validación automática con `@field_validator`.

### Formato de adjuntos

- Cada adjunto debe tener los metadatos: `filename`, `url`, `content_type`, `size`.
- Los archivos se almacenan en `/static/reports/` y se acceden por URL relativa.

## Endpoints de Protocolos de Sujeción y Prevención de Incidentes

### Crear protocolo de sujeción

**POST** `/api/v1/restraint-protocols/`

- Soporta `multipart/form-data` para adjuntar archivos.
- Campos principales:
  - `protocol_type` (str, requerido): Tipo de protocolo:
    - physical: Sujeción física (cinturones, chalecos, etc.)
    - chemical: Sujeción química (medicamentos)
    - environmental: Sujeción ambiental (cerraduras, alarmas)
    - behavioral: Protocolos conductuales
    - mechanical: Dispositivos mecánicos
    - electronic: Dispositivos electrónicos
    - social: Protocolos sociales
    - other: Otros tipos
  - `title` (str, requerido): Título del protocolo
  - `justification` (str, requerido): Justificación clínica requerida
  - `start_date` (str, requerido): Fecha de inicio (ISO format)
  - `responsible_professional` (str, requerido): Profesional responsable
  - `cared_person_id` (str, requerido): ID de la persona bajo cuidado
  - `files` (archivos, opcional): Adjuntos (documentos, imágenes, etc.)

#### Ejemplo de request (cURL)

```bash
curl -X POST "http://localhost:8000/api/v1/restraint-protocols/" \
  -H "Authorization: Bearer <token>" \
  -F "protocol_type=physical" \
  -F "title=Protocolo de sujeción física para prevención de caídas" \
  -F "description=Protocolo para prevenir caídas durante la noche" \
  -F "justification=Paciente con historial de caídas nocturnas y riesgo de lesiones graves" \
  -F "risk_assessment=Alto riesgo de caída durante la noche, especialmente entre 2-4 AM" \
  -F "start_date=2024-06-01T10:00:00Z" \
  -F "review_frequency=weekly" \
  -F "next_review_date=2024-06-08T10:00:00Z" \
  -F "responsible_professional=Dr. María González" \
  -F "professional_license=MED-12345" \
  -F "supervising_doctor=Dr. Carlos Rodríguez" \
  -F "status=active" \
  -F "compliance_status=compliant" \
  -F "notes=Protocolo implementado con consentimiento familiar" \
  -F "cared_person_id=..." \
  -F "files=@/ruta/a/documento.pdf"
```

#### Ejemplo de response

```json
{
  "id": "...",
  "protocol_type": "physical",
  "title": "Protocolo de sujeción física para prevención de caídas",
  "description": "Protocolo para prevenir caídas durante la noche",
  "justification": "Paciente con historial de caídas nocturnas y riesgo de lesiones graves",
  "risk_assessment": "Alto riesgo de caída durante la noche, especialmente entre 2-4 AM",
  "start_date": "2024-06-01T10:00:00Z",
  "end_date": null,
  "review_frequency": "weekly",
  "next_review_date": "2024-06-08T10:00:00Z",
  "responsible_professional": "Dr. María González",
  "professional_license": "MED-12345",
  "supervising_doctor": "Dr. Carlos Rodríguez",
  "status": "active",
  "compliance_status": "compliant",
  "attached_files": [
    {
      "filename": "documento.pdf",
      "url": "/static/restraint_protocols/uuid_documento.pdf",
      "content_type": "application/pdf",
      "size": 123456
    }
  ],
  "notes": "Protocolo implementado con consentimiento familiar",
  "cared_person_id": "...",
  "institution_id": null,
  "created_by_id": "...",
  "updated_by_id": null,
  "last_compliance_check": null,
  "created_at": "2024-06-01T10:00:00Z",
  "updated_at": null
}
```

### Obtener protocolos

**GET** `/api/v1/restraint-protocols/`

- Query parameters:
  - `cared_person_id` (UUID, opcional): Filtrar por persona bajo cuidado
  - `institution_id` (int, opcional): Filtrar por institución
  - `protocol_type` (str, opcional): Filtrar por tipo de protocolo
  - `status` (str, opcional): Filtrar por estado
  - `active_only` (bool, opcional): Solo protocolos activos

### Obtener protocolos por persona

**GET** `/api/v1/restraint-protocols/cared-person/{cared_person_id}`

### Suspender protocolo

**POST** `/api/v1/restraint-protocols/{protocol_id}/suspend`

- Requiere `reason` (str): Razón de la suspensión

### Finalizar protocolo

**POST** `/api/v1/restraint-protocols/{protocol_id}/complete`

- Requiere `completion_notes` (str): Notas de finalización

### Actualizar cumplimiento

**POST** `/api/v1/restraint-protocols/{protocol_id}/compliance`

- Requiere `compliance_status` (str): Nuevo estado de cumplimiento
- Estados permitidos: compliant, non_compliant, under_review, pending_assessment

### Protocolos que requieren revisión

**GET** `/api/v1/restraint-protocols/requiring-review`

### Resumen estadístico

**GET** `/api/v1/restraint-protocols/summary/overview`

### Validación y cumplimiento

- Los protocolos requieren justificación clínica obligatoria
- Se valida que las fechas sean coherentes (start_date < end_date, etc.)
- Se mantiene trazabilidad completa de cambios y actualizaciones
- Los protocolos pueden ser suspendidos, completados o actualizados en cumplimiento
- Se requiere supervisión profesional y documentación de responsabilidades 