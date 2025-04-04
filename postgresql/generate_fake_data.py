import random
from faker import Faker
from faker.providers import date_time, internet, person, lorem
import psycopg2
from datetime import datetime, timedelta

# Инициализация Faker с поддержкой русской локализации
fake = Faker('ru_RU')
fake.add_provider(date_time)
fake.add_provider(internet)
fake.add_provider(person)
fake.add_provider(lorem)

# Подключение к базе данных
conn = psycopg2.connect(
    dbname="fintech_credit_conveyor",
    user="postgres",
    password="your_password",
    host="localhost"
)
cursor = conn.cursor()

# Генерация данных для таблицы clients
def generate_clients(n=100):
    clients = []
    for _ in range(n):
        full_name = fake.name()
        birth_date = fake.date_of_birth(minimum_age=18, maximum_age=80)
        # Генерация уникального номера паспорта (пример: 1234 567890)
        passport = f"{fake.random_number(digits=4)} {fake.random_number(digits=6)}"
        credit_score = random.randint(300, 850)
        clients.append((full_name, birth_date, passport, credit_score))
    return clients

# Генерация данных для таблицы credit_products
def generate_credit_products(n=5):
    products = []
    product_names = ["Потребительский кредит", "Автокредит", "Ипотека", "Кредит для бизнеса", "Микрозайм"]
    for i in range(n):
        product_name = product_names[i] if i < len(product_names) else fake.job()
        interest_rate = round(random.uniform(5.0, 20.0), 2)
        max_amount = round(random.uniform(10000.0, 1000000.0), 2)
        min_term = random.randint(3, 12)
        max_term = random.randint(12, 60)
        products.append((product_name, interest_rate, max_amount, min_term, max_term))
    return products

# Генерация данных для credit_applications
def generate_applications(client_ids, product_ids, n=200):
    applications = []
    statuses = ['submitted', 'approved', 'rejected', 'closed']
    for _ in range(n):
        client_id = random.choice(client_ids)
        product_id = random.choice(product_ids)
        product = next(p for p in credit_products if p[0] == product_id)
        amount = round(random.uniform(1000.0, float(product[2])), 2)
        term = random.randint(product[3], product[4])
        status = random.choices(statuses, weights=[40, 30, 20, 10])[0]
        applications.append((client_id, product_id, amount, term, status))
    return applications

# Генерация данных для payments
def generate_payments(application_ids, n=500):
    payments = []
    for app_id in application_ids:
        term = next(a for a in credit_applications if a[0] == app_id)[4]
        amount_due = round(next(a for a in credit_applications if a[0] == app_id)[3] / term, 2)
        start_date = fake.date_between(start_date='-2y', end_date='-1y')
        for month in range(term):
            payment_date = start_date + timedelta(days=30*month)
            status = random.choices(['pending', 'paid', 'overdue'], weights=[20, 70, 10])[0]
            payments.append((app_id, amount_due, payment_date, status))
    return payments

# Генерация данных для conveyor_log
def generate_logs(application_ids):
    logs = []
    stages = ['application_received', 'scoring', 'risk_assessment', 'approval', 'funding']
    for app_id in application_ids:
        for stage in stages:
            created_at = fake.date_time_between(start_date='-2y', end_date='now')
            details = {
                "stage": stage,
                "comment": fake.sentence()
            }
            logs.append((app_id, stage, details))
    return logs

# Основная функция генерации
if __name__ == "__main__":
    # Генерация клиентов
    clients = generate_clients(100)
    client_ids = [i+1 for i in range(len(clients))]
    cursor.executemany(
        "INSERT INTO clients (full_name, birth_date, passport, credit_score) VALUES (%s, %s, %s, %s)",
        clients
    )

    # Генерация кредитных продуктов
    credit_products = generate_credit_products(5)
    product_ids = [i+1 for i in range(len(credit_products))]
    cursor.executemany(
        "INSERT INTO credit_products (product_name, interest_rate, max_amount, min_term, max_term) VALUES (%s, %s, %s, %s, %s)",
        credit_products
    )

    # Генерация заявок
    credit_applications = generate_applications(client_ids, product_ids, 200)
    application_ids = [i+1 for i in range(len(credit_applications))]
    cursor.executemany(
        "INSERT INTO credit_applications (client_id, product_id, amount, term, status) VALUES (%s, %s, %s, %s, %s)",
        credit_applications
    )

    # Генерация платежей
    payments = generate_payments(application_ids, 500)
    cursor.executemany(
        "INSERT INTO payments (application_id, amount_due, payment_date, status) VALUES (%s, %s, %s, %s)",
        payments
    )

    # Генерация логов
    logs = generate_logs(application_ids)
    cursor.executemany(
        "INSERT INTO conveyor_log (application_id, stage, details) VALUES (%s, %s, %s)",
        logs
    )

    conn.commit()
    cursor.close()
    conn.close()
