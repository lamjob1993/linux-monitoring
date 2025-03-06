ЧЕРНОВИК [ НЕ ИСПОЛНЯЕМ ]

https://chat.qwen.ai/c/d05d1bc9-b4c0-4341-b270-5e4ca9e9fd56

### 1. Создание Python-приложения на банковскую тему

**Файл `app.py`:**
```python
from flask import Flask, jsonify, request
from prometheus_client import Counter, Gauge, Histogram, CollectorRegistry, push_to_gateway
import time
import threading
import random

app = Flask(__name__)

# Метрики Prometheus
REQUEST_COUNT = Counter('bank_api_requests_total', 'Total number of API requests')
TRANSFER_SUCCESS = Counter('bank_transfer_success_total', 'Successful transfers')
TRANSFER_FAILURE = Counter('bank_transfer_failure_total', 'Failed transfers')
BALANCE = Gauge('bank_account_balance', 'Current account balance', ['account_id'])
REQUEST_LATENCY = Histogram('bank_api_request_latency_seconds', 'API request latency')

# Пример данных счетов
accounts = {
    '123': 1000.0,
    '456': 500.0
}

# Фоновая задача для отправки метрик в Pushgateway
def push_metrics():
    registry = CollectorRegistry()
    # Регистрируем метрики в новом реестре (если нужно отправлять их отдельно)
    # Здесь можно добавить метрики, которые не привязаны к HTTP-запросам
    while True:
        time.sleep(10)
        try:
            push_to_gateway('localhost:9091', job='bank_app', registry=registry)
        except Exception as e:
            print(f"Error pushing metrics: {e}")

# Запуск фонового потока
threading.Thread(target=push_metrics, daemon=True).start()

@app.route('/balance/<account_id>', methods=['GET'])
@REQUEST_LATENCY.time()
def get_balance(account_id):
    REQUEST_COUNT.inc()
    balance = accounts.get(account_id, 0.0)
    BALANCE.labels(account_id=account_id).set(balance)
    return jsonify({'account_id': account_id, 'balance': balance})

@app.route('/transfer', methods=['POST'])
@REQUEST_LATENCY.time()
def transfer():
    REQUEST_COUNT.inc()
    data = request.json
    from_account = data.get('from')
    to_account = data.get('to')
    amount = data.get('amount', 0)
    
    if accounts.get(from_account, 0) >= amount:
        accounts[from_account] -= amount
        accounts[to_account] = accounts.get(to_account, 0) + amount
        TRANSFER_SUCCESS.inc()
        return jsonify({'status': 'success'})
    else:
        TRANSFER_FAILURE.inc()
        return jsonify({'status': 'failure', 'message': 'Insufficient funds'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

---

### 2. Инструкция по отправке метрик в Pushgateway

**Шаги:**
1. **Установите зависимости:**
   ```bash
   pip install flask prometheus-client
   ```

2. **Настройте Pushgateway:**
   - Запустите Pushgateway (например, в Docker):
     ```bash
     docker run -d -p 9091:9091 prom/pushgateway
     ```

3. **Отправка метрик:**
   - В приложении используется `push_to_gateway('localhost:9091', job='bank_app', registry=registry)`.
   - Метрики отправляются каждые 10 секунд (см. фоновый поток в коде).

---

### 3. Инструкция по сбору метрик через Prometheus

**Конфигурация Prometheus (`prometheus.yml`):**
```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'pushgateway'
    honor_labels: true
    static_configs:
      - targets: ['localhost:9091']
```

**Запуск Prometheus:**
```bash
docker run -d -p 9090:9090 -v /path/to/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus
```

---

### 4. Инструкция по развёртыванию на Debian

**Шаги:**

1. **Установите зависимости:**
   ```bash
   sudo apt update
   sudo apt install -y python3 python3-pip nginx
   ```

2. **Создайте виртуальное окружение:**
   ```bash
   python3 -m venv bank_app_env
   source bank_app_env/bin/activate
   pip install flask prometheus-client
   ```

3. **Настройте Nginx:**
   - Создайте файл `/etc/nginx/sites-available/bank_app`:
     ```nginx
     server {
         listen 80;
         server_name your_domain;

         location / {
             proxy_pass http://localhost:5000;
             proxy_set_header Host $host;
             proxy_set_header X-Real-IP $remote_addr;
         }
     }
     ```
   - Включите конфиг:
     ```bash
     sudo ln -s /etc/nginx/sites-available/bank_app /etc/nginx/sites-enabled/
     sudo nginx -t
     sudo systemctl restart nginx
     ```

4. **Запустите приложение как сервис systemd:**
   - Создайте файл `/etc/systemd/system/bank_app.service`:
     ```ini
     [Unit]
     Description=Bank Application
     After=network.target

     [Service]
     User=your_user
     WorkingDirectory=/path/to/app
     ExecStart=/path/to/bank_app_env/bin/python /path/to/app/app.py
     Restart=always

     [Install]
     WantedBy=multi-user.target
     ```
   - Запустите сервис:
     ```bash
     sudo systemctl daemon-reload
     sudo systemctl enable bank_app
     sudo systemctl start bank_app
     ```

5. **Проверьте работу:**
   - API доступен по `http://your_domain/balance/123`.
   - Метрики видны в Prometheus на `http://localhost:9090`.

---

### 5. Проверка работоспособности

- **Тест API:**
  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{"from": "123", "to": "456", "amount": 100}' http://localhost/transfer
  curl http://localhost/balance/123
  ```

- **Проверка метрик:**
  - В Prometheus выполните запрос `bank_api_requests_total`.
  - Метрики доступны через Pushgateway на `http://localhost:9091`.
