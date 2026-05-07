from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from ..schemas import client as client_schema

router = APIRouter(
    prefix="/clients",
    tags=["clients"]
)

@router.get("/", response_model=list[client_schema.ClientRead])
def list_clients(db: Session = Depends(get_db)):
    return db.query(models.Client).all()

@router.post("/", response_model=client_schema.ClientRead)
def create_client(client: client_schema.ClientCreate, db: Session = Depends(get_db)):
    db_client = models.Client(**client.model_dump())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

@router.get("/{client_id}", response_model=client_schema.ClientRead)
def get_client(client_id: int, db: Session = Depends(get_db)):
    db_client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")
    return db_client

@router.delete("/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    db_client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")
    db.delete(db_client)
    db.commit()
    return {"ok": True}

@router.put("/{client_id}", response_model=client_schema.ClientRead)
def update_client(client_id: int, client: client_schema.ClientUpdate, db: Session = Depends(get_db)):
    db_client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    # Update only the fields provided in the request
    update_data = client.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_client, key, value)
    
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client