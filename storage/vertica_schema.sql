CREATE SCHEMA IF NOT EXISTS ecommerce;

CREATE TABLE ecommerce.fact_orders (
  order_id    BIGINT NOT NULL,
  customer_id BIGINT,
  product_id  BIGINT,
  order_date  DATE,
  amount      DECIMAL(10,2),
  status      VARCHAR(50)
) ORDER BY order_date
  SEGMENTED BY HASH(customer_id) ALL NODES;

CREATE TABLE ecommerce.dim_customers (
  customer_id BIGINT PRIMARY KEY,
  name        VARCHAR(255),
  email       VARCHAR(255),
  city        VARCHAR(100),
  signup_date DATE
);

CREATE TABLE ecommerce.dim_products (
  product_id   BIGINT PRIMARY KEY,
  product_name VARCHAR(500),
  category     VARCHAR(100),
  price        DECIMAL(10,2)
);
