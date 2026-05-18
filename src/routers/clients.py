from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import get_db
from schemas import client as client_schema
from repositories import ClientRepository

router = APIRouter()

@router.get("/", response_model=list[client_schema.ClientRead])
def list_clients(db: Session = Depends(get_db)):
    return db.query(models.Client).all()

@router.post("/", response_model=client_schema.ClientRead)
def create_client(client: client_schema.ClientCreate, db: Session = Depends(get_db)):
    repo = ClientRepository(db)
    # Convert Pydantic to dict here   
    return repo.create(client.model_dump())

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
    repo = ClientRepository(db)
    # Only send fields that were actually sent in the request
    update_data = client.model_dump(exclude_unset=True)
    return repo.update(client_id, update_data)