import pytest
from main import app

def test_app_import():
    """Test that the app can be imported without hanging"""
    assert app is not None
    assert app.title == "Sistema Integral de Monitoreo API"

def test_app_routes():
    """Test that app routes are accessible"""
    routes = [route.path for route in app.routes]
    assert "/" in routes
    assert "/health" in routes
    assert "/api/v1/health/" in routes 