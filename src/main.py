import logging
import time

from fastapi import FastAPI, Request
from database import engine, Base
from routers import clients, products, addresses

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)

# Generate tables (for local dev)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Catalog Service")

app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(clients.router, prefix="/clients", tags=["Clients"])
app.include_router(addresses.router, prefix="/addresses", tags=["Addresses"])

_inbound_logger = logging.getLogger("catalog.inbound")


@app.middleware("http")
async def log_catalog_api(request: Request, call_next):
    """Log inbound API calls (including from Sales) to CloudWatch via Docker awslogs."""
    started = time.perf_counter()
    response = await call_next(request)
    path = request.url.path
    if path.startswith(("/clients", "/products", "/addresses")):
        ms = (time.perf_counter() - started) * 1000
        client_host = request.client.host if request.client else "?"
        _inbound_logger.info(
            "inbound %s %s status=%s duration_ms=%.1f remote=%s",
            request.method,
            path,
            response.status_code,
            ms,
            client_host,
        )
    return response


@app.get("/")
def health_check():
    return {"status": "healthy", "service": "catalog"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
