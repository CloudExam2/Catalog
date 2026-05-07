from sqlalchemy import Column, Integer, String, Text, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from .database import Base

class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    rfc = Column(String(13), unique=True, nullable=False)
    razon_social = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    comercial_name = Column(String(255))
    telefono = Column(String(20))

    # Relationships within the same service
    addresses = relationship("Address", back_populates="client")
    products = relationship("Product", back_populates="seller")

class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id")) # Ownership added
    domicilio = Column(Text, nullable=False)
    colonia = Column(String(100))
    municipio = Column(String(100))
    estado = Column(String(100))
    address_type = Column(String(20)) # 'BILLING'/'SHIPPING'

    client = relationship("Client", back_populates="addresses")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("clients.id")) # Ownership added
    name = Column(String(255), nullable=False)
    unit = Column(String(50))
    base_price = Column(DECIMAL(10, 2), nullable=False)

    seller = relationship("Client", back_populates="products")