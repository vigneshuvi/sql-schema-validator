CREATE DATABASE legacy_modernization;

-- Table 1
CREATE TABLE customer (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(150),
    created_at TIMESTAMP
);

-- Table 2
CREATE TABLE address (
    address_id SERIAL PRIMARY KEY,
    customer_id INT,
    line1 VARCHAR(200),
    city VARCHAR(100),
    state VARCHAR(50),
    zip VARCHAR(20)
);

-- Table 3
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    status VARCHAR(20)
);

-- Table 4
CREATE TABLE order_items (
    item_id SERIAL PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT
);

-- Table 5
CREATE TABLE product (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(150),
    price DECIMAL(10,2),
    stock INT
);

-- Table 6
CREATE TABLE payment (
    payment_id SERIAL PRIMARY KEY,
    order_id INT,
    amount DECIMAL(10,2),
    payment_date TIMESTAMP
);

-- Table 7
CREATE TABLE inventory (
    inv_id SERIAL PRIMARY KEY,
    product_id INT,
    warehouse VARCHAR(50),
    stock_qty INT
);

-- Table 8
CREATE TABLE supplier (
    supplier_id SERIAL PRIMARY KEY,
    name VARCHAR(150),
    contact VARCHAR(100)
);

-- Table 9
CREATE TABLE shipment (
    shipment_id SERIAL PRIMARY KEY,
    order_id INT,
    shipped_date DATE,
    carrier VARCHAR(100)
);

-- Table 10
CREATE TABLE category (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(100)
);

-- Table 11
CREATE TABLE product_category (
    product_id INT,
    category_id INT
);

-- Table 12
CREATE TABLE employee (
    emp_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    role VARCHAR(50)
);

-- Table 13
CREATE TABLE department (
    dept_id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

-- Table 14
CREATE TABLE emp_dept (
    emp_id INT,
    dept_id INT
);

-- Table 15
CREATE TABLE audit_log (
    log_id SERIAL PRIMARY KEY,
    table_name VARCHAR(100),
    action VARCHAR(50),
    created_at TIMESTAMP
);

-- Table 16
CREATE TABLE reviews (
    review_id SERIAL PRIMARY KEY,
    customer_id INT,
    product_id INT,
    rating INT,
    comments TEXT
);

-- Table 17
CREATE TABLE wallet (
    wallet_id SERIAL PRIMARY KEY,
    customer_id INT,
    balance DECIMAL(10,2)
);

-- Table 18
CREATE TABLE coupons (
    coupon_id SERIAL PRIMARY KEY,
    code VARCHAR(20),
    discount DECIMAL(5,2)
);

-- Table 19
CREATE TABLE coupon_usage (
    usage_id SERIAL PRIMARY KEY,
    coupon_id INT,
    customer_id INT
);

-- Table 20
CREATE TABLE logs_raw (
    log_id SERIAL,
    details TEXT
);

-- Table 21
CREATE TABLE notifications (
    notif_id SERIAL PRIMARY KEY,
    customer_id INT,
    message VARCHAR(255),
    sent_at TIMESTAMP
);

-- Table 22
CREATE TABLE warehouse (
    warehouse_id SERIAL PRIMARY KEY,
    location VARCHAR(200)
);

-- Table 23
CREATE TABLE warehouse_stock (
    id SERIAL PRIMARY KEY,
    warehouse_id INT,
    product_id INT,
    qty INT
);

-- Table 24
CREATE TABLE tax (
    tax_id SERIAL PRIMARY KEY,
    tax_code VARCHAR(20),
    rate DECIMAL(5,2)
);

-- Table 25
CREATE TABLE invoice (
    invoice_id SERIAL PRIMARY KEY,
    order_id INT,
    invoice_date DATE,
    total DECIMAL(10,2)
);

-- Table 26
CREATE TABLE invoice_item (
    item_id SERIAL PRIMARY KEY,
    invoice_id INT,
    product_id INT,
    price DECIMAL(10,2),
    quantity INT
);

-- Table 27
CREATE TABLE return_request (
    return_id SERIAL PRIMARY KEY,
    order_id INT,
    reason VARCHAR(255)
);

-- Table 28
CREATE TABLE return_items (
    id SERIAL PRIMARY KEY,
    return_id INT,
    product_id INT,
    qty INT
);

-- Table 29
CREATE TABLE api_keys (
    key_id SERIAL PRIMARY KEY,
    customer_id INT,
    api_key VARCHAR(255)
);

-- Table 30
CREATE TABLE feature_flags (
    flag_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    enabled BOOLEAN
);
