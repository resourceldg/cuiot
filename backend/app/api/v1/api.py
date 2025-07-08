from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, debug, health, cared_persons, devices, alerts, events, reminders, reports, referrals, packages, diagnoses_router, medical_profile, medication_schedule, medication_log, restraint_protocols, shift_observations, status_types_router, caregiver_assignments, service_subscriptions, care_types, relationship_types, report_types, reminder_types, shift_observation_types, referral_types, caregiver_assignment_types, service_types, alert_types, event_types, device_types, catalogs, dashboard_router

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(debug.router, prefix="/debug", tags=["debug"])
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(cared_persons.router, prefix="/cared-persons", tags=["cared-persons"])
api_router.include_router(devices.router, prefix="/devices", tags=["devices"])
api_router.include_router(alerts.router, prefix="/alerts", tags=["alerts"])
api_router.include_router(events.router, prefix="/events", tags=["events"])
api_router.include_router(reminders.router, prefix="/reminders", tags=["reminders"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(referrals.router, prefix="/referrals", tags=["referrals"])
api_router.include_router(packages.router, prefix="/packages", tags=["packages"])
api_router.include_router(diagnoses_router, prefix="/diagnoses", tags=["diagnoses"])
api_router.include_router(medical_profile.router, prefix="/medical-profiles", tags=["medical-profiles"])
api_router.include_router(medication_schedule.router, prefix="/medication-schedules", tags=["medication-schedules"])
api_router.include_router(medication_log.router, prefix="/medication-logs", tags=["medication-logs"])
api_router.include_router(restraint_protocols.router, prefix="/restraint-protocols", tags=["restraint-protocols"])
api_router.include_router(shift_observations.router, prefix="/shift-observations", tags=["shift-observations"])
api_router.include_router(status_types_router, prefix="/status-types", tags=["status-types"])
api_router.include_router(caregiver_assignments.router, prefix="/caregiver-assignments", tags=["caregiver-assignments"])
api_router.include_router(service_subscriptions.router, prefix="/service-subscriptions", tags=["service-subscriptions"])
api_router.include_router(care_types.router, prefix="/care-types", tags=["care-types"])
api_router.include_router(relationship_types.router, prefix="/relationship-types", tags=["relationship-types"])
api_router.include_router(report_types.router, prefix="/report-types", tags=["report-types"])

# New normalized entity endpoints
api_router.include_router(reminder_types.router, prefix="/reminder-types", tags=["reminder-types"])
api_router.include_router(alert_types.router, prefix="/alert-types", tags=["alert-types"])
api_router.include_router(event_types.router, prefix="/event-types", tags=["event-types"])
api_router.include_router(device_types.router, prefix="/device-types", tags=["device-types"])
api_router.include_router(shift_observation_types.router, prefix="/shift-observation-types", tags=["shift-observation-types"])
api_router.include_router(referral_types.router, prefix="/referral-types", tags=["referral-types"])
api_router.include_router(caregiver_assignment_types.router, prefix="/caregiver-assignment-types", tags=["caregiver-assignment-types"])
api_router.include_router(service_types.router, prefix="/service-types", tags=["service-types"])
api_router.include_router(catalogs.router, prefix="/catalogs", tags=["catalogs"])

# Dashboard summary endpoint
api_router.include_router(dashboard_router, prefix="/dashboard", tags=["dashboard"])
