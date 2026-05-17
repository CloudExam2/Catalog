from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src import models
from src.database import get_db
from src.schemas import product as product_schema
from src.repositories import ProductRepository

router = APIRouter()

@router.get("/", response_model=list[product_schema.ProductRead])
def list_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()

@router.post("/", response_model=product_schema.ProductRead)
def create_product(product: product_schema.ProductCreate, db: Session = Depends(get_db)):
    repo = ProductRepository(db)
    # Convert Pydantic to dict here
    return repo.create(product.model_dump())

@router.get("/{product_id}", response_model=product_schema.ProductRead)
def get_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return {"ok": True}

@router.put("/{product_id}", response_model=product_schema.ProductRead)
def update_product(product_id: int, product: product_schema.ProductUpdate, db: Session = Depends(get_db)):
    repo = ProductRepository(db)
    # Only send fields that were actually sent in the request
    update_data = product.model_dump(exclude_unset=True)
    return repo.update(product_id, update_data)