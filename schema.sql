-- =====================================================================
-- schema.sql  -  Data Definition Language (DDL)
-- Pharmacy Management System  (SQLite)
--
-- Creates 7 related tables, normalized up to 3NF, with primary keys,
-- foreign keys, data types and integrity constraints.
-- =====================================================================

PRAGMA foreign_keys = ON;

-- Drop in reverse dependency order so the script can be re-run safely.
DROP TABLE IF EXISTS Sale_Item;
DROP TABLE IF EXISTS Sale;
DROP TABLE IF EXISTS Medicine;
DROP TABLE IF EXISTS Employee;
DROP TABLE IF EXISTS Customer;
DROP TABLE IF EXISTS Supplier;
DROP TABLE IF EXISTS Category;

-- ---------------------------------------------------------------------
-- 1. Category : the group a medicine belongs to (Antibiotics, etc.)
-- ---------------------------------------------------------------------
CREATE TABLE Category (
    category_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT    NOT NULL UNIQUE,
    description   TEXT
);

-- ---------------------------------------------------------------------
-- 2. Supplier : companies that supply medicines to the pharmacy
-- ---------------------------------------------------------------------
CREATE TABLE Supplier (
    supplier_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    supplier_name  TEXT    NOT NULL,
    contact_person TEXT,
    phone          TEXT,
    email          TEXT,
    address        TEXT
);

-- ---------------------------------------------------------------------
-- 3. Medicine : products in stock.  Each medicine belongs to one
--    Category and is provided by one Supplier (two foreign keys).
-- ---------------------------------------------------------------------
CREATE TABLE Medicine (
    medicine_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    medicine_name  TEXT    NOT NULL,
    category_id    INTEGER NOT NULL,
    supplier_id    INTEGER NOT NULL,
    unit_price     REAL    NOT NULL CHECK (unit_price >= 0),
    stock_quantity INTEGER NOT NULL DEFAULT 0 CHECK (stock_quantity >= 0),
    expiry_date    TEXT,
    batch_no       TEXT,
    FOREIGN KEY (category_id) REFERENCES Category(category_id),
    FOREIGN KEY (supplier_id) REFERENCES Supplier(supplier_id)
);

-- ---------------------------------------------------------------------
-- 4. Customer : people who buy medicines
-- ---------------------------------------------------------------------
CREATE TABLE Customer (
    customer_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT    NOT NULL,
    phone         TEXT,
    email         TEXT,
    address       TEXT
);

-- ---------------------------------------------------------------------
-- 5. Employee : pharmacy staff who handle the sales
-- ---------------------------------------------------------------------
CREATE TABLE Employee (
    employee_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_name TEXT    NOT NULL,
    role          TEXT,
    phone         TEXT,
    salary        REAL    CHECK (salary >= 0),
    hire_date     TEXT
);

-- ---------------------------------------------------------------------
-- 6. Sale : one sales transaction (an invoice header).
--    Linked to the Customer who bought and the Employee who served.
-- ---------------------------------------------------------------------
CREATE TABLE Sale (
    sale_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id    INTEGER NOT NULL,
    employee_id    INTEGER NOT NULL,
    sale_date      TEXT    NOT NULL,
    payment_method TEXT,
    total_amount   REAL    DEFAULT 0,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
    FOREIGN KEY (employee_id) REFERENCES Employee(employee_id)
);

-- ---------------------------------------------------------------------
-- 7. Sale_Item : the line items of a sale (an invoice detail row).
--    Resolves the many-to-many relationship between Sale and Medicine:
--    one sale can contain many medicines, and one medicine can appear
--    on many sales.
-- ---------------------------------------------------------------------
CREATE TABLE Sale_Item (
    sale_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sale_id      INTEGER NOT NULL,
    medicine_id  INTEGER NOT NULL,
    quantity     INTEGER NOT NULL CHECK (quantity > 0),
    unit_price   REAL    NOT NULL CHECK (unit_price >= 0),
    subtotal     REAL,
    FOREIGN KEY (sale_id)     REFERENCES Sale(sale_id) ON DELETE CASCADE,
    FOREIGN KEY (medicine_id) REFERENCES Medicine(medicine_id)
);
