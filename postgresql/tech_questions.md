# **Технические вопросы о PostgreSQL Exporter к собеседованию**

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

---

Эти вопросы и ответы помогут вам продемонстрировать глубокое понимание работы с **PostgreSQL Exporter** на собеседовании. Если нужна дополнительная информация по какому-то пункту, дайте знать! 😊
