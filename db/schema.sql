-- 1. DROP CHILD TABLES FIRST (Prevents dependency errors)
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS addresses;

-- 2. DROP PARENT TABLE LAST
DROP TABLE IF EXISTS clients;

-- 3. CREATE CLIENTS
CREATE TABLE clients (
    id SERIAL PRIMARY KEY,
    rfc VARCHAR(13) NOT NULL UNIQUE,
    razon_social VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    comercial_name VARCHAR(255),
    telefono VARCHAR(20)
);

-- 4. CREATE ADDRESSES (Linked to Client)
CREATE TABLE addresses (
    id SERIAL PRIMARY KEY,
    client_id INTEGER NOT NULL,
    domicilio TEXT NOT NULL,
    colonia VARCHAR(100),
    municipio VARCHAR(100),
    estado VARCHAR(100),
    address_type VARCHAR(20),
    CONSTRAINT fk_client_address FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE
);

-- 5. CREATE PRODUCTS (Linked to Client/Seller)
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    seller_id INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    unit VARCHAR(50),
    base_price NUMERIC(10,2) NOT NULL,
    CONSTRAINT fk_seller_product FOREIGN KEY (seller_id) REFERENCES clients(id) ON DELETE CASCADE
);