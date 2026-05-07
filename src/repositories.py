from typing import List, Optional
from sqlalchemy.orm import Session
from . import models


class BaseRepository:
    def __init__(self, db: Session):
        self.db = db


class ClientRepository(BaseRepository):
    def create(self, data):
        obj = models.Client(**data.dict())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def get(self, client_id: int) -> Optional[models.Client]:
        return self.db.get(models.Client, client_id)

    def list(self) -> List[models.Client]:
        return self.db.query(models.Client).all()

    def delete(self, client_id: int) -> None:
        obj = self.get(client_id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
            
    def update(self, client_id: int, data) -> Optional[models.Client]:
        obj = self.get(client_id)
        if not obj:
            return None
        
        for field, value in data.items():
            setattr(obj, field, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj


class ProductRepository(BaseRepository):
    def create(self, data):
        obj = models.Product(**data.dict())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def get(self, product_id: int) -> Optional[models.Product]:
        return self.db.get(models.Product, product_id)

    def list(self) -> List[models.Product]:
        return self.db.query(models.Product).all()

    def delete(self, product_id: int) -> None:
        obj = self.get(product_id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
    
    def update(self, product_id: int, data) -> Optional[models.Product]:
        obj = self.get(product_id)
        if not obj:
            return None
        
        for field, value in data.items():
            setattr(obj, field, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj


class AddressRepository(BaseRepository):
    def create(self, data):
        obj = models.Address(**data.dict())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def get(self, address_id: int) -> Optional[models.Address]:
        return self.db.get(models.Address, address_id)

    def list(self) -> List[models.Address]:
        return self.db.query(models.Address).all()

    def delete(self, address_id: int) -> None:
        obj = self.get(address_id)
        if obj:
            self.db.delete(obj)
            self.db.commit()

    def update(self, address_id: int, data) -> Optional[models.Address]:
        obj = self.get(address_id)
        if not obj:
            return None
        
        for field, value in data.items():
            setattr(obj, field, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj