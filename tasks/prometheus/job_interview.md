# Как вы использовали Prometheus на практике, для каких команд устанавливали и какие кейсы с ним были?

### **1. Как Prometheus использовался в вашей работе?**
**Пример ответа:**  
"Prometheus использовался для мониторинга инфраструктуры и приложений. Мы собирали метрики с серверов (через Node Exporter), баз данных (PostgreSQL Exporter), контейнеров (cAdvisor) и пользовательских сервисов (Custom Exporter). Это позволяло нам отслеживать производительность системы, настраивать алерты через Alertmanager и анализировать тренды."

---

### **2. Какие команды вы использовали для работы с Prometheus?**
**Пример ответа:**

- **Установка Prometheus:**
  ```bash
  wget https://github.com/prometheus/prometheus/releases/download/v2.45.0/prometheus-2.45.0.linux-amd64.tar.gz
  tar xvfz prometheus-2.45.0.linux-amd64.tar.gz
  ./prometheus --config.file=/etc/prometheus/prometheus.yml
  ```
  "Я устанавливал Prometheus через скачивание бинарного файла с GitHub. Запускал его с флагом `--config.file`, чтобы указать путь к конфигурационному файлу."

- **Проверка работы Prometheus:**
  ```bash
  curl http://localhost:9090/api/v1/status/config
  ```
  "Для проверки работы я использовал API Prometheus, чтобы убедиться, что конфигурация загружена корректно."

- **Настройка автозапуска через systemd:**
  ```ini
  [Unit]
  Description=Prometheus

  [Service]
  ExecStart=/usr/local/bin/prometheus --config.file=/etc/prometheus/prometheus.yml

  [Install]
  WantedBy=multi-user.target
  ```
  "Для автоматического запуска я создавал unit-файл для systemd, чтобы Prometheus работал как служба."

---

### **3. Кому вы устанавливали Prometheus?**
**Пример ответа:**  
"Я устанавливал Prometheus для:
- **Команд DevOps/SRE:** для мониторинга инфраструктуры и приложений.
- **Команд разработчиков:** для анализа производительности их сервисов.
- **Бизнес-аналитиков:** для отслеживания ключевых бизнес-метрик (например, количество заказов или пользователей)."

---

### **4. Пример трех кейсов использования Prometheus и их реализация**

#### **Кейс 1: Мониторинг высокой нагрузки CPU**
**Описание проблемы:**  
"Один из наших серверов начал показывать высокую нагрузку CPU, что приводило к замедлению работы приложения."

**Решение:**  
1. Настроил сбор метрик с помощью Node Exporter:  
   ```yaml
   scrape_configs:
     - job_name: 'node'
       static_configs:
         - targets: ['localhost:9100']
   ```
2. Создал алерт в Prometheus:  
   ```yaml
   groups:
     - name: cpu_alerts
       rules:
         - alert: HighCpuUsage
           expr: 100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 85
           for: 5m
           labels:
             severity: critical
           annotations:
             summary: "High CPU usage on {{ $labels.instance }}"
             description: "CPU usage is above 85% for more than 5 minutes."
   ```
3. Интегрировал Alertmanager для отправки уведомлений в Slack.

**Результат:**  
"Мы быстро обнаружили проблему и оптимизировали код приложения, что снизило нагрузку на CPU."

---

#### **Кейс 2: Мониторинг доступности веб-сервиса**
**Описание проблемы:**  
"Один из наших веб-сервисов стал недоступен для пользователей."

**Решение:**  
1. Настроил Blackbox Exporter для проверки HTTP-статуса:  
   ```yaml
   scrape_configs:
     - job_name: 'blackbox'
       metrics_path: /probe
       params:
         module: [http_2xx]
       static_configs:
         - targets:
             - http://example.com
       relabel_configs:
         - source_labels: [__address__]
           target_label: __param_target
         - source_labels: [__param_target]
           target_label: instance
         - target_label: __address__
           replacement: localhost:9115
   ```
2. Создал алерт в Prometheus:  
   ```yaml
   groups:
     - name: service_availability
       rules:
         - alert: ServiceDown
           expr: probe_success == 0
           for: 2m
           labels:
             severity: critical
           annotations:
             summary: "Service {{ $labels.instance }} is down"
             description: "The service has been unavailable for more than 2 minutes."
   ```

**Результат:**  
"Мы получили уведомление о проблеме и восстановили работу сервиса за несколько минут."

---

#### **Кейс 3: Мониторинг репликации PostgreSQL**
**Описание проблемы:**  
"Мы заметили задержки в репликации PostgreSQL, что могло привести к потере данных."

**Решение:**  
1. Настроил PostgreSQL Exporter для сбора метрик репликации:  
   ```yaml
   scrape_configs:
     - job_name: 'postgres'
       static_configs:
         - targets: ['localhost:9187']
   ```
2. Создал алерт в Prometheus:  
   ```yaml
   groups:
     - name: replication_lag
       rules:
         - alert: ReplicationLag
           expr: pg_replication_lag_seconds > 30
           for: 5m
           labels:
             severity: warning
           annotations:
             summary: "Replication lag detected on {{ $labels.instance }}"
             description: "Replication lag is above 30 seconds for more than 5 minutes."
   ```

**Результат:**  
"Мы обнаружили проблему с сетевым подключением между мастером и репликой и устранили её до того, как она повлияла на пользователей."

---

### **5. Какие каверзные вопросы могут возникнуть и как на них ответить?**

#### **Вопрос: Как вы решали проблемы с производительностью Prometheus?**
**Ответ:**  
"Если возникали проблемы с производительностью, я:
- Оптимизировал запросы PromQL, избегая сложных агрегаций.
- Увеличивал ресурсы сервера (CPU, RAM).
- Настроил retention period для хранения данных (например, `retention: 15d`)."

#### **Вопрос: Как вы обеспечивали безопасность Prometheus?**
**Ответ:**  
"Я ограничивал доступ к порту Prometheus через firewall или настраивал reverse proxy (Nginx) с базовой аутентификацией. Также размещал Prometheus только внутри закрытой сети."

#### **Вопрос: Как вы решали проблему с большим количеством метрик?**
**Ответ:**  
"Если метрик было слишком много, я:
- Отключал ненужные экспортеры или метрики через `relabel_configs`.
- Фильтровал метрики в Prometheus, используя `metric_relabel_configs`.
- Использовал агрегацию данных в PromQL для уменьшения объёма информации."

---

### **6. Что ещё можно добавить?**

- **Интеграция с Grafana:**  
  "Мы интегрировали Prometheus с Grafana для создания информативных дашбордов с данными о производительности системы."

- **Автоматизация установки:**  
  "Для масштабирования я написал Ansible playbook для автоматической установки и настройки Prometheus."

- **Мониторинг бизнес-метрик:**  
  "Мы использовали Prometheus для мониторинга ключевых бизнес-метрик, таких как количество активных пользователей или среднее время обработки запроса."

--- 

# **Технические вопросы по Prometheus к собеседованию**

### **1. Как установить Prometheus?**
**Ответ:**  
Скачайте бинарный файл с GitHub и запустите его:  
```bash
wget https://github.com/prometheus/prometheus/releases/download/v2.45.0/prometheus-2.45.0.linux-amd64.tar.gz
tar xvfz prometheus-2.45.0.linux-amd64.tar.gz
./prometheus --config.file=/etc/prometheus/prometheus.yml
```

---

### **2. Как проверить работу Prometheus?**
**Ответ:**  
Используйте API или веб-интерфейс:  
```bash
curl http://localhost:9090/api/v1/status/config
```
или откройте в браузере:  
`http://localhost:9090`.

---

### **3. Как настроить автозапуск Prometheus через systemd?**
**Ответ:**  
Создайте unit-файл:  
```ini
[Unit]
Description=Prometheus

[Service]
ExecStart=/usr/local/bin/prometheus --config.file=/etc/prometheus/prometheus.yml

[Install]
WantedBy=multi-user.target
```
Запустите службу:  
```bash
sudo systemctl start prometheus
sudo systemctl enable prometheus
```

---

### **4. Как настроить сбор метрик в Prometheus?**
**Ответ:**  
Настройте `scrape_configs` в `prometheus.yml`:  
```yaml
scrape_configs:
  - job_name: 'node'
    static_configs:
      - targets: ['localhost:9100']
```

---

### **5. Как создать алерт в Prometheus?**
**Ответ:**  
Добавьте правило в файл алертов (например, `alerts.yml`):  
```yaml
groups:
  - name: example_alerts
    rules:
      - alert: HighCpuUsage
        expr: 100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 85
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High CPU usage on {{ $labels.instance }}"
          description: "CPU usage is above 85% for more than 5 minutes."
```

---

### **6. Как интегрировать Prometheus с Alertmanager?**
**Ответ:**  
Настройте конфигурацию в `prometheus.yml`:  
```yaml
alerting:
  alertmanagers:
    - static_configs:
        - targets: ['localhost:9093']
```

---

### **7. Как фильтровать метрики в Prometheus?**
**Ответ:**  
Используйте `relabel_configs` в `prometheus.yml`:  
```yaml
scrape_configs:
  - job_name: 'filter_metrics'
    static_configs:
      - targets: ['localhost:9100']
    metric_relabel_configs:
      - source_labels: [__name__]
        regex: "cpu_usage.*"
        action: keep
```

---

### **8. Как использовать PromQL для анализа данных?**
**Ответ:**  
Примеры запросов:
- Среднее значение CPU за последние 5 минут:  
  ```promql
  avg(rate(node_cpu_seconds_total[5m]))
  ```
- Количество HTTP-запросов с кодом 5xx:  
  ```promql
  sum(rate(http_requests_total{status=~"5.."}[5m]))
  ```

---

### **9. Как настроить retention period в Prometheus?**
**Ответ:**  
Укажите параметр `retention` в командной строке:  
```bash
./prometheus --storage.tsdb.retention.time=15d
```
или добавьте в `prometheus.yml`:  
```yaml
storage:
  tsdb:
    retention: 15d
```

---

### **10. Как ограничить доступ к Prometheus?**
**Ответ:**  
Ограничьте доступ через firewall или настройте reverse proxy (Nginx) с аутентификацией:  
```nginx
server {
    listen 9090;
    location / {
        auth_basic "Restricted Access";
        auth_basic_user_file /etc/nginx/.htpasswd;
        proxy_pass http://localhost:9090;
    }
}
```

---

### **11. Как мониторить контейнеры с помощью Prometheus?**
**Ответ:**  
Используйте cAdvisor или kube-state-metrics:  
```yaml
scrape_configs:
  - job_name: 'cadvisor'
    static_configs:
      - targets: ['localhost:8080']
```

---

### **12. Как решить проблему с большим количеством метрик?**
**Ответ:**  
1. Отключите ненужные метрики через `metric_relabel_configs`.  
2. Уменьшите частоту сбора данных (`scrape_interval`).  
3. Используйте агрегацию в PromQL.

---

### **12.1 Как оптимизировать производительность запросов?**
**Ответ:**  
1. Вместо того чтобы каждый раз писать длинный и сложный PromQL-запрос, вы можете использовать предварительно вычисленные метрики (Recording Rules).  
2. Вы можете агрегировать данные на уровне Prometheus (например, суммировать метрики по всем серверам или сервисам) и сохранять агрегированные результаты для дальнейшего использования (Recording Rules).

#### Recording Rules определяются в конфигурационном файле Prometheus (`prometheus.yml`) или в отдельном файле правил (например, `rules.yml`). Каждое правило состоит из:
- **Имени новой метрики** (которая будет создана).
- **PromQL-выражения**, которое вычисляет значение этой метрики.
- **Интервала выполнения правила** (обычно совпадает с интервалом сбора данных).

Пример записи правила:

```yaml
groups:
  - name: example_rules
    rules:
      - record: job:http_requests_total:sum_rate5m
        expr: sum(rate(http_requests_total[5m])) by (job)
```

Здесь:
- `record` — имя новой метрики, которая будет создана.
- `expr` — PromQL-выражение, которое вычисляет значение этой метрики.


#### Пример использования Recording Rules

#### Ситуация:
Вы хотите отслеживать количество HTTP-запросов в секунду для каждого сервиса (по метке `job`) на всех ваших серверах.

#### Без Recording Rules:
Вы пишете PromQL-запрос в Grafana:
```promql
sum(rate(http_requests_total[5m])) by (job)
```
Этот запрос выполняется каждый раз, когда Grafana обновляет дашборд, что может быть ресурсоемко.

#### С Recording Rules:
Вы добавляете правило в конфигурацию Prometheus:
```yaml
groups:
  - name: http_rules
    rules:
      - record: job:http_requests_total:sum_rate5m
        expr: sum(rate(http_requests_total[5m])) by (job)
```

Теперь Prometheus будет периодически вычислять этот запрос и сохранять результат в новой метрике `job:http_requests_total:sum_rate5m`. В Grafana вы можете просто использовать эту метрику:
```promql
job:http_requests_total:sum_rate5m
```

---

### **13. Как автоматизировать установку Prometheus?**
**Ответ:**  
Используйте Ansible или Docker. Пример Dockerfile:  
```dockerfile
FROM prom/prometheus:v2.45.0
COPY prometheus.yml /etc/prometheus/prometheus.yml
CMD ["--config.file=/etc/prometheus/prometheus.yml"]
```

---

### **14. Как мониторить бизнес-метрики с помощью Prometheus?**
**Ответ:**  
Используйте Custom Exporter для сбора бизнес-метрик (например, количество заказов):  
```yaml
scrape_configs:
  - job_name: 'business_metrics'
    static_configs:
      - targets: ['localhost:9101']
```

---

### **15. Как отладить проблемы с Prometheus?**
**Ответ:**  
1. Проверьте логи Prometheus:  
   ```bash
   journalctl -u prometheus.service -f
   ```
2. Проверьте конфигурацию:  
   ```bash
   ./promtool check config /etc/prometheus/prometheus.yml
   ```
3. Проверьте метрики через `/metrics` или API.
