# Как вы использовали PostgreSQL Exporter на практике, для каких команд устанавливали и какие кейсы с ним были?

### **1. Как PostgreSQL Exporter использовался в вашей работе?**
**Пример ответа:**  
"PostgreSQL Exporter использовался для мониторинга состояния баз данных PostgreSQL. Мы собирали метрики, такие как использование CPU, памяти, количество активных соединений, время выполнения запросов и состояние репликации. Эти данные интегрировались с Prometheus для анализа и с Grafana для визуализации. Это позволяло нам отслеживать производительность баз данных и оперативно реагировать на проблемы."

---

### **2. Какие команды вы использовали для работы с PostgreSQL Exporter?**
**Пример ответа:**

- **Установка PostgreSQL Exporter:**
  ```bash
  wget https://github.com/prometheus-community/postgres_exporter/releases/download/v0.11.1/postgres_exporter-0.11.1.linux-amd64.tar.gz
  tar xvfz postgres_exporter-0.11.1.linux-amd64.tar.gz
  ./postgres_exporter --web.listen-address=":9187" --extend.query-path=/path/to/queries.yaml
  ```
  "Я устанавливал PostgreSQL Exporter через скачивание бинарного файла с GitHub. Запускал его с флагами для настройки порта и пользовательских SQL-запросов."

- **Проверка работы PostgreSQL Exporter:**
  ```bash
  curl http://localhost:9187/metrics
  ```
  "Для проверки работы я использовал `curl`, чтобы получить метрики из `/metrics`. Это помогало убедиться, что экспортер корректно собирает данные."

- **Настройка автозапуска через systemd:**
  ```ini
  [Unit]
  Description=PostgreSQL Exporter

  [Service]
  ExecStart=/usr/local/bin/postgres_exporter --web.listen-address=":9187"

  [Install]
  WantedBy=multi-user.target
  ```
  "Для автоматического запуска я создавал unit-файл для systemd, чтобы PostgreSQL Exporter работал как служба."

---

### **3. Кому вы устанавливали PostgreSQL Exporter?**
**Пример ответа:**  
"Я устанавливал PostgreSQL Exporter на:
- **Серверы баз данных:** для мониторинга PostgreSQL в production.
- **Команды DevOps/SRE:** для отслеживания состояния баз данных и настройки алертов.
- **Команды разработчиков:** для анализа производительности их приложений, работающих с PostgreSQL."

---

### **4. Какие каверзные вопросы могут возникнуть и как на них ответить?**

#### **Вопрос: Как вы решали проблемы с производительностью PostgreSQL Exporter?**
**Ответ:**  
"Если возникали проблемы с производительностью, я:
- Оптимизировал SQL-запросы, которые использовались для сбора метрик.
- Уменьшал частоту сбора данных (например, через параметр `scrape_interval` в Prometheus).
- Настройил логирование для диагностики проблем."

#### **Вопрос: Как вы обеспечивали безопасность PostgreSQL Exporter?**
**Ответ:**  
"Я ограничивал доступ к порту экспортера через firewall или настраивал reverse proxy (Nginx) с базовой аутентификацией. Также я использовал защищённое подключение к PostgreSQL через SSL."

#### **Вопрос: Как вы решали проблему с большим количеством метрик?**
**Ответ:**  
"Если метрик было слишком много, я:
- Отключал ненужные метрики через конфигурацию экспортера.
- Фильтровал метрики в Prometheus, используя `relabel_configs`.
- Использовал агрегацию данных в PromQL для уменьшения объёма информации."

#### **Вопрос: Как вы настраивали мониторинг репликации PostgreSQL?**
**Ответ:**  
"Я добавлял пользовательские SQL-запросы в файл `queries.yaml` для сбора метрик о состоянии репликации. Например, я использовал запросы для отслеживания задержек между мастером и репликами."

---

### **5. Пример успешного кейса использования PostgreSQL Exporter**
**Пример ответа:**  
"Однажды мы столкнулись с проблемой высокого времени выполнения запросов в PostgreSQL. С помощью PostgreSQL Exporter мы настроили мониторинг метрик, таких как `pg_stat_activity` и `pg_stat_database`. Мы обнаружили, что некоторые запросы выполняются слишком долго из-за отсутствия индексов. После оптимизации базы данных время выполнения запросов значительно сократилось."

---

### **6. Что ещё можно добавить?**

- **Интеграция с Prometheus и Grafana:**  
  "Мы интегрировали PostgreSQL Exporter с Prometheus для сбора метрик и с Grafana для визуализации. Это позволило нам создавать информативные дашборды с данными о производительности баз данных."

- **Автоматизация установки:**  
  "Для масштабирования я написал Ansible playbook для автоматической установки и настройки PostgreSQL Exporter."

- **Мониторинг бизнес-метрик:**  
  "Мы использовали PostgreSQL Exporter для мониторинга ключевых бизнес-метрик, таких как количество транзакций или среднее время выполнения запросов."

---

# **Технические вопросы по PostgreSQL Exporter к собеседованию**

### **1. Как установить PostgreSQL Exporter?**
**Ответ:**  
Скачайте бинарный файл с GitHub и запустите его:  
```bash
wget https://github.com/prometheus-community/postgres_exporter/releases/download/v0.11.1/postgres_exporter-0.11.1.linux-amd64.tar.gz
tar xvfz postgres_exporter-0.11.1.linux-amd64.tar.gz
./postgres_exporter --web.listen-address=":9187"
```

---

### **2. Как проверить работу PostgreSQL Exporter?**
**Ответ:**  
Используйте `curl`, чтобы получить метрики из `/metrics`:  
```bash
curl http://localhost:9187/metrics
```

---

### **3. Как настроить автозапуск PostgreSQL Exporter через systemd?**
**Ответ:**  
Создайте unit-файл:  
```ini
[Unit]
Description=PostgreSQL Exporter

[Service]
ExecStart=/usr/local/bin/postgres_exporter --web.listen-address=":9187"

[Install]
WantedBy=multi-user.target
```
Запустите службу:  
```bash
sudo systemctl start postgres_exporter
sudo systemctl enable postgres_exporter
```

---

### **4. Как настроить подключение к PostgreSQL в PostgreSQL Exporter?**
**Ответ:**  
Укажите переменные окружения для подключения:  
```bash
export DATA_SOURCE_NAME="postgresql://username:password@localhost:5432/database?sslmode=disable"
./postgres_exporter
```

---

### **5. Как добавить пользовательские SQL-запросы для сбора метрик?**
**Ответ:**  
Создайте файл `queries.yaml` с запросами:  
```yaml
pg_stat_activity_count:
  query: "SELECT COUNT(*) AS count FROM pg_stat_activity;"
  metrics:
    - count:
        usage: "GAUGE"
        description: "Number of active connections in pg_stat_activity."
```
Запустите экспортер с флагом `--extend.query-path`:  
```bash
./postgres_exporter --extend.query-path=/path/to/queries.yaml
```

---

### **6. Какие метрики собирает PostgreSQL Exporter по умолчанию?**
**Ответ:**  
PostgreSQL Exporter собирает метрики из системных таблиц PostgreSQL, такие как:
- `pg_stat_database` — статистика баз данных.
- `pg_stat_activity` — активные соединения.
- `pg_replication` — состояние репликации.

Примеры метрик:
- `pg_exporter_scrapes_total` — количество успешных сборов данных.
- `pg_up` — доступность PostgreSQL (1 — доступен, 0 — недоступен).

---

### **7. Как интегрировать PostgreSQL Exporter с Prometheus?**
**Ответ:**  
Настройте `scrape_configs` в `prometheus.yml`:  
```yaml
scrape_configs:
  - job_name: 'postgres'
    static_configs:
      - targets: ['localhost:9187']
```

---

### **8. Как мониторить репликацию PostgreSQL с помощью PostgreSQL Exporter?**
**Ответ:**  
Добавьте SQL-запросы для мониторинга репликации в `queries.yaml`:  
```yaml
pg_replication_lag:
  query: "SELECT EXTRACT(EPOCH FROM now() - pg_last_xact_replay_timestamp()) AS lag_seconds;"
  metrics:
    - lag_seconds:
        usage: "GAUGE"
        description: "Replication lag in seconds."
```

---

### **9. Как ограничить доступ к метрикам PostgreSQL Exporter?**
**Ответ:**  
Ограничьте доступ через firewall или настройте reverse proxy (например, Nginx) с аутентификацией:  
```nginx
server {
    listen 9187;
    location /metrics {
        auth_basic "Restricted Access";
        auth_basic_user_file /etc/nginx/.htpasswd;
        proxy_pass http://localhost:9187;
    }
}
```

---

### **10. Как обеспечить безопасное подключение к PostgreSQL?**
**Ответ:**  
Используйте SSL для подключения к PostgreSQL:  
```bash
export DATA_SOURCE_NAME="postgresql://username:password@localhost:5432/database?sslmode=require"
```

---

### **11. Как отключить ненужные метрики в PostgreSQL Exporter?**
**Ответ:**  
Настройте фильтрацию метрик в Prometheus через `metric_relabel_configs`:  
```yaml
metric_relabel_configs:
  - source_labels: [__name__]
    regex: "pg_.*_unused_metric"
    action: drop
```

---

### **12. Как решить проблему высокой нагрузки на базу данных при сборе метрик?**
**Ответ:**  
Оптимизируйте SQL-запросы и уменьшите частоту сбора данных:  
- Увеличьте `scrape_interval` в Prometheus (например, до 5 минут).  
- Отключите ненужные коллекционеры через флаг `--collector.disable-defaults`.

---

### **13. Как мониторить задержки выполнения запросов в PostgreSQL?**
**Ответ:**  
Добавьте запрос для сбора времени выполнения запросов в `queries.yaml`:  
```yaml
pg_query_duration:
  query: "SELECT datname, query_start, state, query FROM pg_stat_activity WHERE state = 'active';"
  metrics:
    - query_duration_seconds:
        usage: "GAUGE"
        description: "Duration of active queries in seconds."
```

---

### **14. Как настроить логирование в PostgreSQL Exporter?**
**Ответ:**  
Используйте флаг `--log.level` для настройки уровня логирования:  
```bash
./postgres_exporter --log.level=debug
```

---

### **15. Как автоматизировать установку PostgreSQL Exporter?**
**Ответ:**  
Используйте Ansible или Docker. Пример Dockerfile:  
```dockerfile
FROM quay.io/prometheuscommunity/postgres-exporter:v0.11.1
ENV DATA_SOURCE_NAME="postgresql://username:password@localhost:5432/database?sslmode=disable"
CMD ["--web.listen-address=:9187"]
```
