# Расскажите о мониторинге в отделе? Как мониторилась инфраструктура и чем? Приведите примеры?

### **1. Как стек мониторинга на основе Prometheus использовался в вашей работе?**
**Пример ответа:**  
"Стек мониторинга на основе Prometheus использовался для централизованного мониторинга инфраструктуры, приложений и бизнес-метрик. Мы собирали данные с серверов (через Node Exporter), веб-серверов (Nginx Exporter), процессов (Process Exporter), баз данных (PostgreSQL Exporter) и других источников. Эти данные анализировались в Prometheus, визуализировались в Grafana, отправлялись через Alertmanager для уведомлений, а также использовались Federation и Pushgateway для специфических задач."

---

### **2. Кому вы предоставляли доступ к мониторингу и устанавливали экспортеры каким командам?**
**Пример ответа:**  
"Я предоставлял доступ к мониторингу следующим командам:
- **Команды DevOps/SRE:** для отслеживания состояния инфраструктуры и приложений.
- **Команды разработчиков:** для анализа производительности их сервисов.
- **Бизнес-аналитики:** для отслеживания ключевых бизнес-метрик (например, количество заказов или активных пользователей).
- **Менеджеры проектов:** для получения обзора состояния системы.

Экспортеры устанавливались на серверы, где работали соответствующие сервисы. Например:
- **Node Exporter** — для серверов.
- **Nginx Exporter** — для веб-серверов.
- **Process Exporter** — для мониторинга конкретных процессов.
- **Custom Exporter** — для специфических метрик.
- **PostgreSQL Exporter** — для баз данных.
- **Blackbox Exporter** — для проверки доступности сервисов.
- **Pushgateway** — для batch-задач и CI/CD пайплайнов."

---

### **3. Пример 10 кейсов использования мониторинга и их реализация**

#### **Кейс 1: Мониторинг высокой нагрузки CPU**
**Описание проблемы:**  
"Один из наших серверов начал показывать высокую нагрузку CPU, что приводило к замедлению работы приложения."

**Решение:**  
1. Настроил сбор метрик с помощью **Node Exporter**:  
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

**Результат:**  
"Мы быстро обнаружили проблему и оптимизировали код приложения, что снизило нагрузку на CPU."

---

#### **Кейс 2: Мониторинг доступности веб-сервиса**
**Описание проблемы:**  
"Один из наших веб-сервисов стал недоступен для пользователей."

**Решение:**  
1. Настроил **Blackbox Exporter** для проверки HTTP-статуса:  
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
1. Настроил **PostgreSQL Exporter** для сбора метрик репликации:  
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

#### **Кейс 4: Мониторинг Nginx**
**Описание проблемы:**  
"Нужно было отслеживать производительность Nginx (количество запросов, ошибки)."

**Решение:**  
1. Установил **Nginx Exporter** и настроил сбор метрик:  
   ```yaml
   scrape_configs:
     - job_name: 'nginx'
       static_configs:
         - targets: ['localhost:9113']
   ```
2. Создал дашборд в Grafana для анализа метрик.

**Результат:**  
"Мы смогли оперативно реагировать на падение производительности Nginx."

---

#### **Кейс 5: Мониторинг процессов**
**Описание проблемы:**  
"Нужно было отслеживать потребление ресурсов конкретными процессами."

**Решение:**  
1. Настроил **Process Exporter**:  
   ```yaml
   process_names:
     - name: "{{.Comm}}"
       cmdline:
         - "my-app"
   ```
2. Добавил алерты в Prometheus.

**Результат:**  
"Мы обнаружили утечку памяти в одном из процессов и исправили её."

---

#### **Кейс 6: Мониторинг бизнес-метрик**
**Описание проблемы:**  
"Нужно было отслеживать количество заказов в системе."

**Решение:**  
1. Написал **Custom Exporter**, который собирал метрики из базы данных.  
2. Настроил Prometheus для сбора этих метрик.

**Результат:**  
"Мы смогли анализировать тренды и прогнозировать нагрузку."

---

#### **Кейс 7: Мониторинг batch-задач**
**Описание проблемы:**  
"Batch-задачи завершались до того, как Prometheus мог их скрапить."

**Решение:**  
1. Настроил **Pushgateway** для приема метрик:  
   ```bash
   echo "batch_job_duration_seconds 42" | curl --data-binary @- http://pushgateway:9091/metrics/job/batch_job
   ```
2. Настроил Prometheus для сбора данных с Pushgateway.

**Результат:**  
"Мы смогли отслеживать продолжительность выполнения batch-задач."

---

#### **Кейс 8: Централизованный мониторинг нескольких дата-центров**
**Описание проблемы:**  
"У нас было несколько дата-центров, и нужно было объединить метрики."

**Решение:**  
1. Настроил **Prometheus Federation**:  
   ```yaml
   scrape_configs:
     - job_name: 'federate'
       honor_labels: true
       metrics_path: '/federate'
       params:
         match[]:
           - '{job="node"}'
       static_configs:
         - targets:
             - 'prometheus-dc1:9090'
             - 'prometheus-dc2:9090'
   ```

**Результат:**  
"Мы получили единый обзор метрик из всех дата-центров."

---

#### **Кейс 9: Мониторинг CI/CD пайплайнов**
**Описание проблемы:**  
"Нужно было отслеживать время выполнения CI/CD пайплайнов."

**Решение:**  
1. Добавил шаг в CI/CD пайплайн для отправки метрик в **Pushgateway**:  
   ```bash
   echo "ci_pipeline_duration_seconds $(date +%s)" | curl --data-binary @- http://pushgateway:9091/metrics/job/ci_pipeline
   ```
2. Настроил Prometheus для сбора данных с Pushgateway.

**Результат:**  
"Мы смогли анализировать время выполнения CI/CD пайплайнов."

---

#### **Кейс 10: Интеграция с Alertmanager**
**Описание проблемы:**  
"Нужно было настроить уведомления о критических событиях."

**Решение:**  
1. Настроил **Alertmanager** для отправки уведомлений в Slack:  
   ```yaml
   route:
     receiver: slack-notifications
   receivers:
     - name: slack-notifications
       slack_configs:
         - api_url: 'https://hooks.slack.com/services/...'
           channel: '#alerts'
   ```

**Результат:**  
"Команды получали уведомления о проблемах в режиме реального времени."

---

### **4. Какие каверзные вопросы могут возникнуть и как на них ответить?**

#### **Вопрос: Как решать проблемы с производительностью Prometheus?**
**Ответ:**  
"Если возникали проблемы с производительностью, я:
- Оптимизировал запросы PromQL, избегая сложных агрегаций.
- Увеличивал ресурсы сервера (CPU, RAM).
- Настроил retention period для хранения данных (например, `retention: 15d`)."

#### **Вопрос: Как обеспечивать безопасность стека мониторинга?**
**Ответ:**  
"Я ограничивал доступ через firewall, настраивал reverse proxy (Nginx) с аутентификацией и размещал все компоненты только внутри закрытой сети."
