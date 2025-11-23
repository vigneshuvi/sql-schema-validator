-- ===========================================================
-- SAMPLE SQL FILE WITH 100 TABLES + MULTIPLE ANOMALIES
-- ===========================================================

-- Database
CREATE DATABASE mf_modernization_demo;


------------------------------
-- 1–20: Missing Primary Keys
------------------------------

CREATE TABLE customer_data_01 (
    cust_id INT,
    name VARCHAR(50),
    email VARCHAR(100),
    created_on TIMESTAMP
);

CREATE TABLE customer_data_02 (
    id INT,
    full_name VARCHAR(100),
    PH_NO VARCHAR(20),
    address VARCHAR(200)
);

CREATE TABLE cust_data_singlecol_03 (
    value VARCHAR(200)
);

CREATE TABLE cust_data_singlecol_04 (
    onlycol INT
);

CREATE TABLE account_table_05 (
    acc_id INT,
    balance DECIMAL(10,2),
    FKY_customer INT,
    last_txn TIMESTAMP
);

CREATE TABLE account_table_06 (
    accno INT,
    status VARCHAR(20),
    created TIMESTAMP
);

CREATE TABLE long_table_name_customer_transaction_history_details_07 (
    id INT,
    amount DECIMAL(12,2),
    description VARCHAR(250),
    created TIMESTAMP
);

CREATE TABLE long_table_name_customer_subscription_metadata_reference_list_08 (
    id INT,
    info TEXT,
    updated TIMESTAMP
);

CREATE TABLE txn_master_09 (
    txn_id INT,
    cust_id INT,
    amount DECIMAL(10,2),
    txn_date TIMESTAMP
);

CREATE TABLE txn_master_10 (
    id INT,
    value VARCHAR(100)
);

CREATE TABLE product_data_11 (
    product_id INT,
    name VARCHAR(50),
    category VARCHAR(50),
    price DECIMAL(10,2)
);

CREATE TABLE product_data_12 (
    pid INT,
    p_name VARCHAR(50),
    FKY_cat INT
);

CREATE TABLE product_metadata_13 (
    meta_id INT,
    key VARCHAR(50),
    val VARCHAR(200)
);

CREATE TABLE warehouse_data_14 (
    wr_id INT,
    code VARCHAR(20),
    state VARCHAR(20)
);

CREATE TABLE warehouse_location_15 (
    loc_id INT,
    wr_id INT,
    FKY_region INT
);

CREATE TABLE user_login_16 (
    login_id INT,
    user_name VARCHAR(50),
    passwd VARCHAR(50),
    last_login TIMESTAMP
);

CREATE TABLE user_login_17 (
    id INT,
    login VARCHAR(50)
);

CREATE TABLE order_table_18 (
    order_id INT,
    cust_id INT,
    total DECIMAL(12,2),
    created TIMESTAMP
);

CREATE TABLE order_table_19 (
    id INT,
    description VARCHAR(200)
);

CREATE TABLE category_table_20 (
    cat_id INT,
    cat_name VARCHAR(50)
);


------------------------------
-- 21–40: Nullable Columns + No Indexes
------------------------------

CREATE TABLE employee_master_21 (
    emp_id INT,
    emp_name VARCHAR(100) NULL,
    manager_id INT NULL
);

CREATE TABLE employee_master_22 (
    id INT,
    name VARCHAR(50) NULL
);

CREATE TABLE employee_profile_23 (
    profile_id INT,
    emp_id INT,
    bio TEXT NULL
);

CREATE TABLE emp_salary_24 (
    sid INT,
    emp_id INT,
    amount DECIMAL(10,2) NULL
);

CREATE TABLE salary_revision_25 (
    rev_id INT,
    emp_id INT,
    old_amt DECIMAL(10,2) NULL,
    new_amt DECIMAL(10,2) NULL
);

CREATE TABLE bonus_table_26 (
    id INT,
    emp_id INT,
    bonus DECIMAL(10,2) NULL
);

CREATE TABLE dept_table_27 (
    dept_id INT,
    dept_name VARCHAR(100) NULL
);

CREATE TABLE dept_mapping_28 (
    id INT,
    dept_id INT,
    emp_id INT
);

CREATE TABLE dept_meta_29 (
    meta_id INT,
    key VARCHAR(50),
    val VARCHAR(200) NULL
);

CREATE TABLE skill_table_30 (
    skill_id INT,
    skill_name VARCHAR(100) NULL
);

CREATE TABLE emp_skill_map_31 (
    id INT,
    emp_id INT,
    skill_id INT
);

CREATE TABLE region_table_32 (
    region_id INT,
    region_name VARCHAR(100) NULL
);

CREATE TABLE country_table_33 (
    country_id INT,
    name VARCHAR(100) NULL
);

CREATE TABLE state_table_34 (
    state_id INT,
    country_id INT,
    state_name VARCHAR(100) NULL
);

CREATE TABLE city_table_35 (
    city_id INT,
    state_id INT,
    city_name VARCHAR(100) NULL
);

CREATE TABLE address_table_36 (
    addr_id INT,
    cust_id INT,
    city_id INT NULL,
    pin VARCHAR(10) NULL
);

CREATE TABLE audit_log_37 (
    log_id INT,
    event VARCHAR(200) NULL,
    created TIMESTAMP NULL
);

CREATE TABLE audit_meta_38 (
    meta_id INT,
    log_id INT,
    info TEXT NULL
);

CREATE TABLE meta_table_39 (
    id INT,
    key VARCHAR(200) NULL
);

CREATE TABLE shipping_table_40 (
    ship_id INT,
    order_id INT,
    mode VARCHAR(20) NULL
);


------------------------------
-- 41–60: FK-like names but no FK constraints
------------------------------

CREATE TABLE shipment_detail_41 (
    id INT,
    FKY_ship_id INT,
    FKY_order INT
);

CREATE TABLE shipment_detail_42 (
    id INT,
    FKY_ship_id INT
);

CREATE TABLE wallet_table_43 (
    wid INT,
    cust_id INT,
    FKY_topup_id INT
);

CREATE TABLE wallet_txn_44 (
    txn_id INT,
    wid INT,
    amount DECIMAL(10,2)
);

CREATE TABLE invoice_table_45 (
    invoice_id INT,
    order_id INT,
    FKY_cust INT
);

CREATE TABLE invoice_meta_46 (
    id INT,
    invoice_id INT,
    key VARCHAR(100)
);

CREATE TABLE reconciliation_47 (
    recon_id INT,
    order_id INT,
    amount DECIMAL(10,2)
);

CREATE TABLE recon_meta_48 (
    id INT,
    recon_id INT,
    detail TEXT
);

CREATE TABLE sync_table_49 (
    sync_id INT,
    ref_id INT,
    status VARCHAR(20)
);

CREATE TABLE sync_error_50 (
    id INT,
    sync_id INT,
    err TEXT
);

CREATE TABLE batch_tab_
