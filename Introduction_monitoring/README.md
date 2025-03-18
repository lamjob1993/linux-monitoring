### 1. Введение в мониторинг
Мониторинг — это процесс непрерывного сбора, анализа и визуализации метрик ИТ-инфраструктуры и приложений для обеспечения их надежности, производительности и безопасности.  
**Цели мониторинга**:  
- Обнаружение аномалий и сбоев в реальном времени.  
- Прогнозирование нагрузки и масштабирование ресурсов.  
- Аудит соответствия SLA (Service Level Agreement).  
- Оптимизация использования ресурсов (CPU, RAM, disk I/O, network).  

---

### 1.1 Сравнение Prometheus и Zabbix. Роль зонтичного мониторинга

| **Критерий**          | **Prometheus + экспортеры**                          | **Zabbix + агенты**                                  |
|------------------------|------------------------------------------------------|-----------------------------------------------------|
| **Архитектура**        | Pull-based (метрики забираются по HTTP)             | Push/pull-based (агенты отправляют данные на сервер)|
| **Сбор данных**        | Экспортеры (например, Node Exporter, Blackbox)       | Агенты (Zabbix Agent, SNMP)                         |
| **Масштабируемость**   | Горизонтальная (через federation и Thanos)           | Вертикальная (требует ресурсов на сервере)          |
| **Интеграции**         | Нативная поддержка Kubernetes, ELK (через Exporters) | Широкий спектр шаблонов для HW/SW                   |
| **Оповещения**         | Alertmanager (гибкие правила на PromQL)              | Встроенные триггеры и уведомления                   |
| **Типовые кейсы**      | Контейнеризированные среды, микросервисы             | Enterprise-инфраструктура, legacy-системы           |

**Зонтичный мониторинг** — унификация данных из Prometheus, ELK и Zabbix в единой системе (например, Grafana) для комплексного анализа.

---

### 2. Grafana: визуализация данных
**Grafana** — платформа для создания дашбордов и анализа метрик.  
**Пример**:  
- Источник данных: Prometheus (CPU usage) + Elasticsearch (логи).  
- Визуализация: График загрузки CPU с алертингом при превышении 90% + логи ошибок из Kibana.  
**Роль**:  
- Агрегация данных из Prometheus, ELK, Zabbix.  
- Настройка оповещений через Alerting Engine.  

---

### 2.1 Prometheus: сбор метрик
**Prometheus** — TSDB (Time Series Database) для мониторинга динамических сред.  
**Зачем нужен**:  
- Забирает метрики по HTTP (pull-метод).  
- Использует PromQL для сложных запросов (оптимизация через `rate()`, `avg_over_time()`).  
- Интегрируется с ELK через экспортеры (например, `prometheus-elasticsearch-exporter`).  

---

### 2.2 Экспортеры: Node Exporter
**Экспортер** — сервис, предоставляющий метрики в формате, понятном Prometheus.  
**Node Exporter**:  
- Собирает данные о CPU, RAM, дисках, сетевых интерфейсах.  
- Запускается на каждом узле и предоставляет `/metrics` по HTTP.  
- Логи Node Exporter могут экспортироваться в ELK через Filebeat.  

---

### 2.3 Mermaid Sequence Diagram (с ELK)
```mermaid
sequenceDiagram
    participant User
    participant Grafana
    participant Prometheus
    participant NodeExporter
    participant Alertmanager
    participant Elasticsearch
    participant Kibana

    Prometheus->>NodeExporter: HTTP GET /metrics (scrape)
    NodeExporter-->>Prometheus: Ответ с метриками (text/plain)
    Prometheus->>Prometheus: Хранение данных в TSDB
    NodeExporter->>Filebeat: Отправка логов (JSON)
    Filebeat->>Elasticsearch: Индексация логов (HTTP)
    Grafana->>Prometheus: HTTP GET query (PromQL)
    Grafana->>Elasticsearch: HTTP GET query (Elastic DSL)
    Prometheus-->>Grafana: Результат запроса (JSON)
    Elasticsearch-->>Grafana: Результат запроса (JSON)
    Prometheus->>Alertmanager: POST alert (при срабатывании правила)
    Alertmanager->>User: Оповещение (email/Slack/PagerDuty)
    Kibana->>Elasticsearch: Визуализация логов (Discover)
```

---

### 3. Mermaid Quadrant Chart (с ELK)
```mermaid
quadrantChart
    title Мониторинг 10 ВМ через Node Exporter и ELK
    x-axis Низкая_интеграция-->Высокая_интеграция
    y-axis Децентрализация-->Централизация
    quadrant-1 Централизованные_решения
    quadrant-2 Легковесные_агенты
    quadrant-3 Уведомления
    quadrant-4 Визуализация
    NodeExporter1: [0.2, 0.8]
    NodeExporter2: [0.3, 0.7]
    Prometheus: [0.8, 0.9]
    Grafana: [0.9, 0.9]
    Alertmanager: [0.7, 0.6]
    Elasticsearch: [0.8, 0.8]
    Kibana: [0.9, 0.8]
```

**Процессы**:  
1. **Node Exporters** публикуют метрики на порту 9100 и логи через Filebeat.  
2. **Prometheus** скребет данные по HTTP каждые 15 секунд.  
3. **Elasticsearch** индексирует логи из Filebeat.  
4. **Alertmanager** получает алерты при превышении пороговых значений.  
5. **Grafana** визуализирует метрики и логи через дашборды.  

---

### 4. Оптимизация PromQL
**Методы**:  
- Использование `rate()` для контроля скорости (например, `rate(http_requests_total[5m])`).  
- Агрегация данных: `sum by (instance) (process_cpu_seconds_total)`.  
- Подзапросы: `max_over_time(cpu_usage{env="prod"}[1h:])`.  
- Оптимизация регулярных выражений: `http_requests_total{method!~"GET|POST"}`.  

**Пример для финтеха**:  
```promql
# Обнаружение высокой latency транзакций
histogram_quantile(0.99, sum by (le) (rate(transaction_duration_seconds_bucket[5m])))
```

---

### 5. Sequence Diagram: Java-приложение в ВМ (с ELK)
```mermaid
sequenceDiagram
    participant JavaApp
    participant JMXExporter
    participant Filebeat
    participant Prometheus
    participant Alertmanager
    participant Elasticsearch
    participant Grafana

    JavaApp->>JMXExporter: Публикация JMX-метрик
    JMXExporter->>JMXExporter: HTTP endpoint /metrics
    JavaApp->>Filebeat: Логи приложения (JSON)
    Filebeat->>Elasticsearch: Индексация логов (HTTP)
    Prometheus->>JMXExporter: Scrape метрик (HTTP GET)
    Prometheus->>Alertmanager: Alert (e.g., high GC pauses)
    Alertmanager->>Admin: Slack notification
    Grafana->>Prometheus: Query JVM metrics (PromQL)
    Grafana->>Elasticsearch: Query логов ошибок (Elastic DSL)
    Grafana->>Admin: Дашборд с CPU, memory, threads + логи
```

---

### 6. Sequence Diagram: Java-приложение в Kubernetes (с ELK)
```mermaid
sequenceDiagram
    participant K8sPod
    participant PrometheusOperator
    participant Filebeat
    participant Prometheus
    participant Elasticsearch
    participant Grafana

    K8sPod->>K8sPod: Аннотация prometheus.io/scrape: true
    K8sPod->>Filebeat: Логи контейнера (stdout)
    Filebeat->>Elasticsearch: Индексация логов (HTTP)
    PrometheusOperator->>Prometheus: Создание ServiceMonitor
    Prometheus->>K8sPod: Scrape /metrics через Kubernetes API
    Prometheus->>Prometheus: Хранение метрик в TSDB
    Grafana->>Prometheus: Запрос метрик (PromQL)
    Grafana->>Elasticsearch: Запрос логов (Elastic DSL)
    Grafana->>SRE: Визуализация CPU/RAM pod-ов + логи
```

---

### 7. Завершение
**Итог**:  
- **Prometheus + Grafana + ELK** = стандарт для мониторинга и анализа логов в финтехе.  
- **Оптимизация PromQL** снижает нагрузку на TSDB и ускоряет алертинг.  
- **ELK** критичен для анализа транзакций и обнаружения фрода через логи.  
- **Рекомендация**: Используйте `rate()` и агрегации в PromQL, а для логов — Filebeat + Elasticsearch.  
