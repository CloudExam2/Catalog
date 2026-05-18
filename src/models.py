import enum

from sqlalchemy import Column, DECIMAL, Enum as SAEnum, Integer, String, Text
from database import Base


class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    rfc = Column(String(13), unique=True, nullable=False)
    razon_social = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    comercial_name = Column(String(255))
    telefono = Column(String(20))


class AddressType(str, enum.Enum):
    FACTURACION = "FACTURACIÓN"
    ENVIO = "ENVÍO"


class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True, index=True)
    domicilio = Column(Text, nullable=False)
    colonia = Column(String(100))
    municipio = Column(String(100))
    estado = Column(String(100))
    address_type = Column(SAEnum(AddressType), nullable=False)


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    unit = Column(String(50))
    base_price = Column(DECIMAL(10, 2), nullable=False)
