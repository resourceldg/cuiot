class NotFoundException(Exception):
    """Excepción para recursos no encontrados"""
    pass

class ValidationException(Exception):
    """Excepción para errores de validación"""
    pass

class AuthenticationException(Exception):
    """Excepción para errores de autenticación"""
    pass

class AuthorizationException(Exception):
    """Excepción para errores de autorización"""
    pass

class BusinessLogicException(Exception):
    """Excepción para errores de lógica de negocio"""
    pass 