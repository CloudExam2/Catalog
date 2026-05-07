from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import get_db
from schemas import address as address_schema
from repositories import AddressRepository

router = APIRouter(
    prefix="/addresses",
    tags=["addresses"]
)

@router.get("/", response_model=list[address_schema.AddressRead])
def list_addresses(db: Session = Depends(get_db)):
    return db.query(models.Address).all()

@router.post("/", response_model=address_schema.AddressRead)
def create_address(address: address_schema.AddressCreate, db: Session = Depends(get_db)):
    repo = AddressRepository(db)
    # Convert Pydantic to dict here
    return repo.create(address.model_dump())

@router.get("/{address_id}", response_model=address_schema.AddressRead)
def get_address(address_id: int, db: Session = Depends(get_db)):
    db_address = db.query(models.Address).filter(models.Address.id == address_id).first()
    if not db_address:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address

@router.delete("/{address_id}")
def delete_address(address_id: int, db: Session = Depends(get_db)):
    db_address = db.query(models.Address).filter(models.Address.id == address_id).first()
    if not db_address:
        raise HTTPException(status_code=404, detail="Address not found")
    db.delete(db_address)
    db.commit()
    return {"ok": True}

@router.put("/{address_id}", response_model=address_schema.AddressRead)
def update_address(address_id: int, address: address_schema.AddressUpdate, db: Session = Depends(get_db)):
    repo = AddressRepository(db)
    # Only send fields that were actually sent in the request
    update_data = address.model_dump(exclude_unset=True)
    return repo.update(address_id, update_data)