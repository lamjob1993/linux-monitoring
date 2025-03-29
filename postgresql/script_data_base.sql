-- Создание базы данных
CREATE DATABASE fintech_credit_conveyor
    WITH OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8'
    TEMPLATE = template0;

-- Подключение к базе
\c fintech_credit_conveyor;

-- Таблица клиентов
CREATE TABLE clients (
    client_id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    birth_date DATE NOT NULL,
    passport VARCHAR(20) UNIQUE NOT NULL,
    credit_score INT CHECK (credit_score BETWEEN 300 AND 850),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица кредитных продуктов
CREATE TABLE credit_products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    interest_rate NUMERIC(5,2) NOT NULL CHECK (interest_rate > 0),
    max_amount NUMERIC(15,2) NOT NULL,
    min_term INT NOT NULL,
    max_term INT NOT NULL
);

-- Таблица заявок на кредит
CREATE TABLE credit_applications (
    application_id SERIAL PRIMARY KEY,
    client_id INT REFERENCES clients(client_id) ON DELETE CASCADE,
    product_id INT REFERENCES credit_products(product_id) ON DELETE SET NULL,
    amount NUMERIC(15,2) NOT NULL,
    term INT NOT NULL,
    status VARCHAR(50) DEFAULT 'submitted' CHECK (status IN ('submitted', 'approved', 'rejected', 'closed')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица платежей
CREATE TABLE payments (
    payment_id SERIAL PRIMARY KEY,
    application_id INT REFERENCES credit_applications(application_id) ON DELETE CASCADE,
    amount_due NUMERIC(15,2) NOT NULL,
    payment_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'paid', 'overdue'))
);

-- Логирование кредитного конвейера
CREATE TABLE conveyor_log (
    log_id SERIAL PRIMARY KEY,
    application_id INT REFERENCES credit_applications(application_id),
    stage VARCHAR(50) NOT NULL,
    details JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Индексы для оптимизации
CREATE INDEX idx_client_passport ON clients(passport);
CREATE INDEX idx_application_status ON credit_applications(status);
CREATE INDEX idx_payment_status ON payments(status);
