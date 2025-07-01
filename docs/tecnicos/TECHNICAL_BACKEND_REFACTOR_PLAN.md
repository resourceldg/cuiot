# CUIOT Backend Refactor Plan

## Overview
Complete backend redesign aligned with business rules and documentation to ensure consistency and scalability.

## Phase 1: Foundation & Core Models

### 1.1 Base Models & Database Setup
- [ ] Create new base models (User, Role, Institution, CaredPerson)
- [ ] Set up proper SQLAlchemy relationships
- [ ] Generate initial migration
- [ ] Test database connectivity

### 1.2 Authentication & Authorization
- [ ] Implement JWT authentication
- [ ] Role-based access control
- [ ] User management endpoints
- [ ] Security middleware

## Phase 2: Business Domain Models

### 2.1 Care Management
- [ ] CaregiverAssignment model
- [ ] CaregiverInstitution model (freelance support)
- [ ] Emergency protocols
- [ ] Service subscriptions

### 2.2 Device & IoT Integration
- [ ] Device models with proper relationships
- [ ] Device configuration
- [ ] Location tracking
- [ ] Geofencing

### 2.3 Monitoring & Alerts
- [ ] Event system
- [ ] Alert management
- [ ] Reminder system
- [ ] Debug/test support

## Phase 3: API & Services

### 3.1 Core API Endpoints
- [ ] User management
- [ ] Institution management
- [ ] Cared person management
- [ ] Device management

### 3.2 Business Logic Services
- [ ] Authentication service
- [ ] User service
- [ ] Device service
- [ ] Alert service

### 3.3 Debug & Testing
- [ ] Debug endpoints
- [ ] Test data generation
- [ ] Health checks
- [ ] API documentation

## Phase 4: Integration & Testing

### 4.1 Frontend Integration
- [ ] CORS configuration
- [ ] API client updates
- [ ] Authentication flow
- [ ] Error handling

### 4.2 Testing & Validation
- [ ] Unit tests
- [ ] Integration tests
- [ ] API tests
- [ ] Performance testing

## Current Status
- ✅ Legacy code cleaned
- ✅ Docker containers restarted
- ✅ Database reset
- 🔄 Ready to start Phase 1

## Next Steps
1. Define new base models
2. Create initial migration
3. Test database setup
4. Proceed with authentication

## Success Criteria
- [ ] All models align with business rules
- [ ] No legacy references remain
- [ ] Clean migration history
- [ ] All tests pass
- [ ] API documentation complete
- [ ] Frontend integration working 