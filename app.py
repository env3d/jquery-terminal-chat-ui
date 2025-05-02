from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
import httpx
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response as StarletteResponse

app = FastAPI()

# Proxy server address
TARGET_SERVER = "http://localhost:8080"  # Replace with your target server

# Create an HTTP client for httpx
client = httpx.AsyncClient()

# Custom Middleware to proxy requests starting with /v1
class ProxyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Check if the request path starts with /v1
        
        if request.url.path.startswith("/v1"):

            target_url = f"{TARGET_SERVER}{request.url.path}"

            async with httpx.AsyncClient(timeout=60) as client:
                proxied_response = await client.request(
                    method=request.method,
                    url=target_url,
                    headers=dict(request.headers),
                    content=await request.body(),
                )

            # Return a non-async response with appropriate status code and headers
            return StarletteResponse(
                content=proxied_response.content,
                status_code=proxied_response.status_code,
                headers=dict(proxied_response.headers),
                media_type=proxied_response.headers.get("content-type")
            )

        # If path does not start with /v1, proceed with the original request
        return await call_next(request)

# Add the custom middleware to the app
app.add_middleware(ProxyMiddleware)

app.mount("/", StaticFiles(directory="static", html=True), name="static")
