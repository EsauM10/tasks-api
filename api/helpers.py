from typing import Any

from api.protocols import HttpResponse

def error(message: str = 'Internal server error') -> dict[str, str]:
    return {'error': message}

def bad_request(body: dict[str, Any]) -> HttpResponse:
    return HttpResponse(status_code=400, body=body)

def conflict(body: dict[str, Any]) -> HttpResponse:
    return HttpResponse(status_code=409, body=body)

def created(body: dict[str, Any]) -> HttpResponse:
    return HttpResponse(status_code=201, body=body)

def internal_server_error(body: dict[str, Any]) -> HttpResponse:
    return HttpResponse(status_code=500, body=body)

def not_found(body: dict[str, Any]) -> HttpResponse:
    return HttpResponse(status_code=404, body=body)

def success(body: dict[str, Any]) -> HttpResponse:
    return HttpResponse(status_code=200, body=body)

def unauthorized(body: dict[str, Any]) -> HttpResponse:
    return HttpResponse(status_code=401, body=body)

            