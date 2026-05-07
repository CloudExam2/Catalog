from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from .. import models
from ..schemas import product as product_schema

router = APIRouter(
    prefix="/products",
    tags=["products"]
)

@router.get("/", response_model=list[product_schema.ProductRead])
def list_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()

@router.post("/", response_model=product_schema.ProductRead)
def create_product(product: product_schema.ProductCreate, db: Session = Depends(get_db)):
    # Replaced .dict() with .model_dump() per Pydantic v2
    new_product = models.Product(**product.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

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