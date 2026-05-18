from fastapi import FastAPI
from database import engine, Base
from routers import clients, products, addresses

# Generate tables (for local dev)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Catalog Service")

# Include Routers BEFORE the run block
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(clients.router, prefix="/clients", tags=["Clients"])
app.include_router(addresses.router, prefix="/addresses", tags=["Addresses"])

@app.get("/")
def health_check():
    return {"status": "healthy", "service": "catalog"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)