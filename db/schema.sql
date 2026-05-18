-- Reference schema (Catalog: clients, addresses, products are independent flat entities).
-- The running app uses SQLAlchemy `Base.metadata.create_all` — this file is only documentation.

DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS addresses;
DROP TABLE IF EXISTS clients;

CREATE TABLE clients (
    id SERIAL PRIMARY KEY,
    rfc VARCHAR(13) NOT NULL UNIQUE,
    razon_social VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    comercial_name VARCHAR(255),
    telefono VARCHAR(20)
);

CREATE TABLE addresses (
    id SERIAL PRIMARY KEY,
    domicilio TEXT NOT NULL,
    colonia VARCHAR(100),
    municipio VARCHAR(100),
    estado VARCHAR(100),
    address_type VARCHAR(20) NOT NULL,
    CONSTRAINT chk_address_type CHECK (address_type IN ('FACTURACIÓN', 'ENVÍO'))
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    unit VARCHAR(50),
    base_price NUMERIC(10,2) NOT NULL
);
