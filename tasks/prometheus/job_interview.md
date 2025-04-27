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
