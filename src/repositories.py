from typing import List, Optional
from sqlalchemy.orm import Session
import models

class BaseRepository:
    def __init__(self, db: Session):
        self.db = db

class ClientRepository(BaseRepository):
    # 'data' should now be a dictionary passed from the router
    def create(self, data: dict):
        obj = models.Client(**data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def get(self, client_id: int) -> Optional[models.Client]:
        return self.db.get(models.Client, client_id)

    def list(self) -> List[models.Client]:
        return self.db.query(models.Client).all()

    def delete(self, client_id: int) -> bool:
        obj = self.get(client_id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
            return True
        return False
            
    def update(self, client_id: int, data: dict) -> Optional[models.Client]:
        obj = self.get(client_id)
        if not obj:
            return None
        
        for field, value in data.items():
            setattr(obj, field, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

class ProductRepository(BaseRepository):
    def create(self, data: dict):
        obj = models.Product(**data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def get(self, product_id: int) -> Optional[models.Product]:
        return self.db.get(models.Product, product_id)

    def list(self) -> List[models.Product]:
        return self.db.query(models.Product).all()

    def delete(self, product_id: int) -> bool:
        obj = self.get(product_id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
            return True
        return False
    
    def update(self, product_id: int, data: dict) -> Optional[models.Product]:
        obj = self.get(product_id)
        if not obj:
            return None
        
        for field, value in data.items():
            setattr(obj, field, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

# AddressRepository follows the exact same pattern as ProductRepository
class AddressRepository(BaseRepository):
    def create(self, data: dict):
        obj = models.Address(**data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def get(self, address_id: int) -> Optional[models.Address]:
        return self.db.get(models.Address, address_id)

    def list(self) -> List[models.Address]:
        return self.db.query(models.Address).all()

    def delete(self, address_id: int) -> bool:
        obj = self.get(address_id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
            return True
        return False
    
    def update(self, address_id: int, data: dict) -> Optional[models.Address]:
        obj = self.get(address_id)
        if not obj:
            return None
        
        for field, value in data.items():
            setattr(obj, field, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj