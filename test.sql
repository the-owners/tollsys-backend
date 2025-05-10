BEGIN;

CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> a72951a86ce4

CREATE TABLE "Permission" (
    id SERIAL, 
    name VARCHAR, 
    created_at TIMESTAMP WITHOUT TIME ZONE, 
    updated_at TIMESTAMP WITHOUT TIME ZONE, 
    PRIMARY KEY (id)
);

CREATE INDEX idx_permission_name ON "Permission" (name);

CREATE TABLE "Role" (
    id SERIAL, 
    name VARCHAR, 
    created_at TIMESTAMP WITHOUT TIME ZONE, 
    created_by INTEGER, 
    updated_at TIMESTAMP WITHOUT TIME ZONE, 
    updated_by INTEGER, 
    PRIMARY KEY (id)
);

CREATE INDEX idx_role_created_by ON "Role" (created_by);

CREATE INDEX idx_role_name ON "Role" (name);

CREATE INDEX idx_role_updated_by ON "Role" (updated_by);

CREATE TABLE "Toll" (
    id SERIAL, 
    tax_id VARCHAR, 
    legal_name VARCHAR, 
    address VARCHAR, 
    created_at TIMESTAMP WITHOUT TIME ZONE, 
    created_by INTEGER, 
    updated_at TIMESTAMP WITHOUT TIME ZONE, 
    updated_by INTEGER, 
    PRIMARY KEY (id)
);

CREATE INDEX idx_toll_created_by ON "Toll" (created_by);

CREATE INDEX idx_toll_tax_id ON "Toll" (tax_id);

CREATE INDEX idx_toll_updated_by ON "Toll" (updated_by);

CREATE TABLE "User" (
    id SERIAL, 
    name VARCHAR, 
    username VARCHAR, 
    password VARCHAR, 
    role_id INTEGER, 
    toll_id INTEGER, 
    created_at TIMESTAMP WITHOUT TIME ZONE, 
    created_by INTEGER, 
    updated_at TIMESTAMP WITHOUT TIME ZONE, 
    updated_by INTEGER, 
    PRIMARY KEY (id)
);

CREATE INDEX idx_user_created_by ON "User" (created_by);

CREATE INDEX idx_user_role_id ON "User" (role_id);

CREATE INDEX idx_user_toll_id ON "User" (toll_id);

CREATE INDEX idx_user_updated_by ON "User" (updated_by);

CREATE INDEX idx_user_username ON "User" (username);

CREATE TYPE boothstatus AS ENUM ('AVAILABLE', 'CLOSED', 'MAINTENANCE', 'OCCUPIED');

CREATE TABLE "Booth" (
    id SERIAL, 
    name VARCHAR, 
    active BOOLEAN, 
    status boothstatus, 
    toll_id INTEGER, 
    created_at TIMESTAMP WITHOUT TIME ZONE, 
    created_by INTEGER, 
    updated_at TIMESTAMP WITHOUT TIME ZONE, 
    updated_by INTEGER, 
    PRIMARY KEY (id)
);

CREATE INDEX idx_booth_created_by ON "Booth" (created_by);

CREATE INDEX idx_booth_toll_id ON "Booth" (toll_id);

CREATE INDEX idx_booth_updated_by ON "Booth" (updated_by);

CREATE TABLE "PaymentMethod" (
    id SERIAL, 
    name VARCHAR, 
    icon VARCHAR, 
    active BOOLEAN, 
    created_at TIMESTAMP WITHOUT TIME ZONE, 
    created_by INTEGER, 
    updated_at TIMESTAMP WITHOUT TIME ZONE, 
    updated_by INTEGER, 
    PRIMARY KEY (id)
);

CREATE INDEX idx_payment_method_active ON "PaymentMethod" (active);

CREATE INDEX idx_payment_method_created_by ON "PaymentMethod" (created_by);

CREATE INDEX idx_payment_method_name ON "PaymentMethod" (name);

CREATE INDEX idx_payment_method_updated_by ON "PaymentMethod" (updated_by);

CREATE TABLE "RolePermission" (
    id SERIAL, 
    role_id INTEGER, 
    permission_id INTEGER, 
    created_at TIMESTAMP WITHOUT TIME ZONE, 
    created_by INTEGER, 
    updated_at TIMESTAMP WITHOUT TIME ZONE, 
    updated_by INTEGER, 
    PRIMARY KEY (id)
);

CREATE INDEX idx_role_permission_created_by ON "RolePermission" (created_by);

CREATE INDEX idx_role_permission_permission_id ON "RolePermission" (permission_id);

CREATE INDEX idx_role_permission_role_id ON "RolePermission" (role_id);

CREATE INDEX idx_role_permission_updated_by ON "RolePermission" (updated_by);

CREATE TABLE "UserSession" (
    id SERIAL, 
    user_id INTEGER, 
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(), 
    created_by INTEGER, 
    updated_at TIMESTAMP WITHOUT TIME ZONE, 
    updated_by INTEGER, 
    closed_at TIMESTAMP WITHOUT TIME ZONE, 
    closing_reason VARCHAR, 
    closing_observations TEXT, 
    PRIMARY KEY (id)
);

CREATE INDEX idx_user_session_created_by ON "UserSession" (created_by);

CREATE INDEX idx_user_session_updated_by ON "UserSession" (updated_by);

CREATE INDEX idx_user_session_user_id ON "UserSession" (user_id);

CREATE TABLE "VehicleType" (
    id SERIAL, 
    name VARCHAR, 
    icon VARCHAR, 
    rate NUMERIC, 
    active BOOLEAN, 
    created_at TIMESTAMP WITHOUT TIME ZONE, 
    created_by INTEGER, 
    updated_at TIMESTAMP WITHOUT TIME ZONE, 
    updated_by INTEGER, 
    PRIMARY KEY (id)
);

CREATE INDEX idx_vehicle_type_active ON "VehicleType" (active);

CREATE INDEX idx_vehicle_type_created_by ON "VehicleType" (created_by);

CREATE INDEX idx_vehicle_type_name ON "VehicleType" (name);

CREATE INDEX idx_vehicle_type_updated_by ON "VehicleType" (updated_by);

CREATE TABLE "BoothCashSession" (
    id SERIAL, 
    booth_id INTEGER, 
    user_id INTEGER, 
    opened_at TIMESTAMP WITHOUT TIME ZONE, 
    initial_amount NUMERIC, 
    closing_amount NUMERIC, 
    closing_reason VARCHAR, 
    closing_observations TEXT, 
    closed_at TIMESTAMP WITHOUT TIME ZONE, 
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(), 
    created_by INTEGER, 
    updated_at TIMESTAMP WITHOUT TIME ZONE, 
    updated_by INTEGER, 
    PRIMARY KEY (id)
);

CREATE INDEX idx_booth_cash_session_booth_id ON "BoothCashSession" (booth_id);

CREATE INDEX idx_booth_cash_session_created_by ON "BoothCashSession" (created_by);

CREATE INDEX idx_booth_cash_session_updated_by ON "BoothCashSession" (updated_by);

CREATE INDEX idx_booth_cash_session_user_id ON "BoothCashSession" (user_id);

CREATE TABLE "TollPayment" (
    id SERIAL, 
    receipt_nro VARCHAR, 
    rate NUMERIC, 
    vehicle_type_id INTEGER, 
    booth_id INTEGER, 
    created_at TIMESTAMP WITHOUT TIME ZONE, 
    paymented_at TIMESTAMP WITHOUT TIME ZONE, 
    created_by INTEGER, 
    PRIMARY KEY (id), 
    UNIQUE (receipt_nro)
);

CREATE INDEX idx_toll_payment_booth_id ON "TollPayment" (booth_id);

CREATE INDEX idx_toll_payment_created_at ON "TollPayment" (created_at);

CREATE INDEX idx_toll_payment_created_by ON "TollPayment" (created_by);

CREATE INDEX idx_toll_payment_receipt_nro ON "TollPayment" (receipt_nro);

CREATE INDEX idx_toll_payment_vehicle_type_id ON "TollPayment" (vehicle_type_id);

CREATE TABLE "TollPaymentMethod" (
    id SERIAL, 
    toll_payment_id INTEGER, 
    payment_method_id INTEGER, 
    amount NUMERIC, 
    created_at TIMESTAMP WITHOUT TIME ZONE, 
    created_by INTEGER, 
    PRIMARY KEY (id)
);

CREATE INDEX idx_toll_payment_method_created_by ON "TollPaymentMethod" (created_by);

CREATE INDEX idx_toll_payment_method_payment_method_id ON "TollPaymentMethod" (payment_method_id);

CREATE INDEX idx_toll_payment_method_toll_payment_id ON "TollPaymentMethod" (toll_payment_id);

INSERT INTO alembic_version (version_num) VALUES ('a72951a86ce4') RETURNING alembic_version.version_num;

COMMIT;

