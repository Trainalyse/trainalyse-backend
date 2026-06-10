from fastapi import Request, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


# Consider the security scheme like a machine
# on execution fastapi passes the request object to it internally and automatically
# it checks for existence of Authorization header in request object otherwise error (auto_error=True)
# it updates the docs UI to ask for authentication token and show result, otherwise the docs UI will simply error 403
# it returns HTTPAuthorizationCredentials object which contains scheme and credentials attributes
# incoming http header > "Authorization= Bearer 1234"
# security_scheme.scheme = "Bearer", security_scheme.credentials = "1234"
security_scheme = HTTPBearer(auto_error=True)


async def check_dev_token(
    request: Request,  # when executed via fastapi's Depends, the request object is passed automatically if the type hint is Request
    # since security_scheme is an internal function of FastAPI and OpenAPI which requires internal passing of data like the request object,
    # we need to execute it via FastAPI's Depends method
    auth_token_info: HTTPAuthorizationCredentials = Depends(security_scheme),
):
    """
    Interceptors incoming requests, extracts the Bearer token,
    and cross-examines it against the Cloudflare environment secret.
    """
    # Pull the credentials string parsed by HTTPBearer
    client_token = auth_token_info.credentials

    # asgi wraps the cloudflare's env variable and request object into "scope" object
    # fastapi wraps the scope object into its "Request" object and passes it to any paramter which has type hint as "Request" (when executed via Depends)
    env = request.scope.get("env")
    expected_token = getattr(env, "DEV_API_TOKEN", None) if env else None

    # Fail-safe check if the token environment configuration is completely missing
    if not expected_token:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server Configuration Error: SECURE_TOKEN is unconfigured.",
        )

    # Compare strings securely. If they mismatch, throw a 401 Unauthorized execution break
    if client_token != expected_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access Denied: Invalid or corrupted authentication token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return True
