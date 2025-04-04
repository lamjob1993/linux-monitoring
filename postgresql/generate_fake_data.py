import json
import random
from faker import Faker
import psycopg2
from datetime import datetime, timedelta

fake = Faker('ru_RU')

# Подключение к БД
conn = psycopg2.connect(
    dbname="fintech_credit_conveyor",
    user="postgres",
    password="your_password",
    host="localhost"
)
cursor = conn.cursor()

def generate_clients(n=100):
    clients = []
    for _ in range(n):
        clients.append((
            fake.name(),
            fake.date_of_birth(minimum_age=18, maximum_age=70),
            f"{fake.unique.random_number(digits=4)} {fake.unique.random_number(digits=6)}",
            random.randint(300, 850)
        ))
    return clients

def generate_credit_products(n=5):
    products = []
    product_types = ["Потребительский кредит", "Автокредит", "Ипотека", "Кредит для бизнеса", "Микрозайм"]
    for i in range(n):
        products.append((
            product_types[i] if i < len(product_types) else f"Специальный продукт {i+1}",
            round(random.uniform(5.0, 25.0), 2),
            round(random.uniform(50000.0, 5000000.0), 2),
            random.randint(3, 12),
            random.randint(12, 60)
        ))
    return products

def generate_applications(client_ids, product_ids, n=200):
    applications = []
    statuses = ['submitted', 'approved', 'rejected', 'closed']
    
    # Получаем параметры продуктов из БД
    cursor.execute("SELECT product_id, min_term, max_term, max_amount FROM credit_products")
    products = {row[0]: row[1:] for row in cursor.fetchall()}
    
    for _ in range(n):
        client_id = random.choice(client_ids)
        product_id = random.choice(product_ids)
        
        if product_id not in products:
            continue
        
        min_term, max_term, max_amount = products[product_id]
        term = random.randint(min_term, max_term)
        amount = round(random.uniform(1000.0, float(max_amount)), 2)
        status = random.choices(statuses, weights=[40, 30, 20, 10])[0]
        
        applications.append((client_id, product_id, amount, term, status))
    
    return applications

def generate_payments(application_ids, n=500):
    payments = []
    for app_id in application_ids:
        # Получаем параметры заявки из БД
        cursor.execute(
            "SELECT amount, term FROM credit_applications WHERE application_id = %s",
            (app_id,)
        )
        app_data = cursor.fetchone()
        
        if not app_data:
            continue
            
        amount, term = app_data
        monthly_payment = round(amount / term, 2)
        start_date = fake.date_between(start_date='-2y')
        
        for i in range(term):
            payment_date = start_date + timedelta(days=30*i)
            status = random.choices(
                ['pending', 'paid', 'overdue'],
                weights=[20, 70, 10]
            )[0]
            
            payments.append((
                app_id,
                monthly_payment,
                payment_date,
                status
            ))
    
    return payments

def generate_logs(application_ids):
    logs = []
    stages = ['application_received', 'scoring', 'risk_assessment', 'approval', 'funding']
    
    for app_id in application_ids:
        for stage in stages:
            created_at = fake.date_time_between(start_date='-2y')
            logs.append((
                app_id,
                stage,
                {
                    "status": fake.random_element(elements=('success', 'warning', 'info')),
                    "message": fake.sentence()
                }
                # Преобразование словаря в JSON-строку
                logs.append((app_id, stage, json.dumps(details)))
                
    return logs

try:
    # Генерация клиентов
    clients = generate_clients()
    cursor.executemany(
        "INSERT INTO clients (full_name, birth_date, passport, credit_score) VALUES (%s, %s, %s, %s)",
        clients
    )
    cursor.execute("SELECT client_id FROM clients")
    client_ids = [row[0] for row in cursor.fetchall()]

    # Генерация кредитных продуктов
    products = generate_credit_products()
    cursor.executemany(
        "INSERT INTO credit_products (product_name, interest_rate, max_amount, min_term, max_term) VALUES (%s, %s, %s, %s, %s)",
        products
    )
    cursor.execute("SELECT product_id FROM credit_products")
    product_ids = [row[0] for row in cursor.fetchall()]

    # Генерация заявок
    applications = generate_applications(client_ids, product_ids)
    cursor.executemany(
        "INSERT INTO credit_applications (client_id, product_id, amount, term, status) VALUES (%s, %s, %s, %s, %s)",
        applications
    )
    cursor.execute("SELECT application_id FROM credit_applications")
    application_ids = [row[0] for row in cursor.fetchall()]

    # Генерация платежей
    payments = generate_payments(application_ids)
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

except Exception as e:
    print(f"Ошибка: {str(e)}")
    conn.rollback()
else:
    conn.commit()
finally:
    cursor.close()
    conn.close()
