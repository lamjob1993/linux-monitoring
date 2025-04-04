import psycopg2
from faker import Faker
from random import randint, choice, uniform
from datetime import datetime, timedelta

# Настройки подключения к PostgreSQL
conn = psycopg2.connect(
    dbname="fintech_credit_conveyor",
    user="postgres",
    password="your_password",
    host="localhost"
)
cursor = conn.cursor()

# Инициализация Faker с русской локализацией
fake = Faker('ru_RU')

# Генерация клиентов
def generate_clients(num_clients):
    clients = []
    for _ in range(num_clients):
        full_name = fake.name()
        birth_date = fake.date_of_birth(minimum_age=18, maximum_age=70)
        passport = f"{randint(1000, 9999)} {randint(100000, 999999)}"  # Формат: 1234 567890
        credit_score = randint(300, 850)
        clients.append((full_name, birth_date, passport, credit_score))
    return clients

# Генерация кредитных продуктов
def generate_credit_products(num_products):
    products = []
    product_types = ["Потребительский кредит", "Ипотека", "Автокредит", "Кредит для бизнеса"]
    for _ in range(num_products):
        product_name = choice(product_types)
        interest_rate = round(uniform(5.0, 20.0), 2)
        max_amount = randint(100000, 10000000)
        min_term = randint(6, 12)
        max_term = randint(24, 60)
        products.append((product_name, interest_rate, max_amount, min_term, max_term))
    return products

# Генерация заявок на кредит
def generate_applications(clients, products):
    applications = []
    statuses = ['submitted', 'approved', 'rejected', 'closed']
    for client in clients:
        product = choice(products)
        amount = randint(100000, product[2])  # Не превышает max_amount продукта
        term = randint(product[3], product[4])  # В рамках min_term и max_term
        status = choice(statuses)
        applications.append((
            client[0],  # client_id (будет проставлен через enumerate)
            product[0], # product_id (будет проставлен через enumerate)
            amount,
            term,
            status
        ))
    return applications

# Генерация платежей
def generate_payments(applications):
    payments = []
    for app in applications:
        if app[4] in ['approved', 'closed']:
            num_payments = app[3] // 12  # Пример: раз в месяц
            for i in range(num_payments):
                amount_due = round(app[2] / num_payments, 2)
                payment_date = datetime.now() + timedelta(days=30*i)
                status = choice(['pending', 'paid', 'overdue'])
                payments.append((
                    app[0],  # application_id (будет проставлен через enumerate)
                    amount_due,
                    payment_date.date(),
                    status
                ))
    return payments

# Генерация логов конвейера
def generate_conveyor_logs(applications):
    logs = []
    stages = ["Проверка данных", "Оценка кредитоспособности", "Утверждение", "Выдача кредита"]
    for app in applications:
        for _ in range(randint(1, 3)):
            stage = choice(stages)
            details = {
                "decision_maker": fake.name(),
                "comment": fake.sentence()
            }
            logs.append((
                app[0],  # application_id
                stage,
                details
            ))
    return logs

# Вставка данных в таблицы
def insert_data():
    # Генерация 100 клиентов
    clients = generate_clients(100)
    cursor.executemany(
        "INSERT INTO clients (full_name, birth_date, passport, credit_score) VALUES (%s, %s, %s, %s)",
        clients
    )
    client_ids = [client[0] for client in clients]

    # Генерация 5 кредитных продуктов
    products = generate_credit_products(5)
    cursor.executemany(
        "INSERT INTO credit_products (product_name, interest_rate, max_amount, min_term, max_term) VALUES (%s, %s, %s, %s, %s)",
        products
    )
    product_ids = [product[0] for product in products]

    # Генерация 200 заявок
    applications = generate_applications(client_ids, product_ids)
    cursor.executemany(
        "INSERT INTO credit_applications (client_id, product_id, amount, term, status) VALUES (%s, %s, %s, %s, %s)",
        applications
    )
    application_ids = [app[0] for app in applications]

    # Генерация платежей
    payments = generate_payments(applications)
    cursor.executemany(
        "INSERT INTO payments (application_id, amount_due, payment_date, status) VALUES (%s, %s, %s, %s)",
        payments
    )

    # Генерация логов
    logs = generate_conveyor_logs(applications)
    cursor.executemany(
        "INSERT INTO conveyor_log (application_id, stage, details) VALUES (%s, %s, %s)",
        logs
    )

    conn.commit()

if __name__ == "__main__":
    insert_data()
    cursor.close()
    conn.close()
