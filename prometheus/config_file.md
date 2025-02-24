# Prometheus

## Разберём конфигурацию

Разбор конфига для связки: **Node Exporter**, **Process Exporter**, **Blackbox Exporter**, **Alertmanager**, **remote read/write** и **relabel config**.

---

### **Пример конфигурации Prometheus (`prometheus.yml`)**

```yaml
global:
  scrape_interval: 15s  # Как часто Prometheus будет собирать метрики (по умолчанию 15 секунд).
  evaluation_interval: 15s  # Как часто Prometheus будет оценивать правила алертинга.

# Настройки Alertmanager.
alerting:
  alertmanagers:
    - static_configs:
        - targets:
            - 'localhost:9093'  # Адрес Alertmanager.

# Правила алертинга.
rule_files:
  - 'alert_rules.yml'  # Файл с правилами алертинга.

# Настройки remote read/write.
remote_write:
  - url: 'http://remote-storage:8086/write'  # Куда отправлять метрики (например, в Thanos или Cortex).
    queue_config:
      capacity: 10000  # Максимальное количество метрик в очереди.
remote_read:
  - url: 'http://remote-storage:8086/read'  # Откуда читать метрики (например, из Thanos или Cortex).

# Конфигурация сбора метрик (scrape_configs).
scrape_configs:
  # Конфигурация для Node Exporter.
  - job_name: 'node_exporter'
    static_configs:
      - targets: ['localhost:9100']  # Адрес Node Exporter.
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - source_labels: [__param_target]
        target_label: instance
      - target_label: __address__
        replacement: 'localhost:9100'  # Адрес Node Exporter.

  # Конфигурация для Process Exporter.
  - job_name: 'process_exporter'
    static_configs:
      - targets: ['localhost:9256']  # Адрес Process Exporter.
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - source_labels: [__param_target]
        target_label: instance
      - target_label: __address__
        replacement: 'localhost:9256'  # Адрес Process Exporter.

  # Конфигурация для Blackbox Exporter.
  - job_name: 'blackbox_exporter'
    metrics_path: /probe  # Путь к метрикам Blackbox Exporter.
    params:
      module: [http_2xx]  # Модуль для проверки HTTP-запросов.
    static_configs:
      - targets:
          - 'http://example.com'  # Цель для проверки (например, веб-сайт).
          - 'http://another-example.com'
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - source_labels: [__param_target]
        target_label: instance
      - target_label: __address__
        replacement: 'localhost:9115'  # Адрес Blackbox Exporter.
```

---

### **Разберём ключевые части конфигурации:**

#### **1. `global`**
- **`scrape_interval`**: Как часто Prometheus будет собирать метрики с целевых узлов.
- **`evaluation_interval`**: Как часто Prometheus будет проверять правила алертинга.

#### **2. `alerting`**
- **`alertmanagers`**: Настройки Alertmanager, куда Prometheus будет отправлять алерты.
  - **`targets`**: Адрес Alertmanager (по умолчанию `localhost:9093`).

#### **3. `rule_files`**
- **`alert_rules.yml`**: Файл с правилами алертинга. Пример содержимого:
  ```yaml
  groups:
    - name: example
      rules:
        - alert: HighCpuUsage
          expr: 100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100 > 80
          for: 5m
          labels:
            severity: critical
          annotations:
            summary: "High CPU usage detected on {{ $labels.instance }}"
  ```

#### **4. `remote_write` и `remote_read`**
- **`remote_write`**: Куда отправлять метрики (например, в Mimir, Thanos, Cortex или другой удалённый storage).
- **`remote_read`**: Откуда читать метрики (например, из удалённого хранилища).

#### **5. `scrape_configs`**
- **`job_name`**: Имя задачи для сбора метрик.
- **`static_configs`**: Список целевых узлов (targets), с которых собираются метрики.
- **`relabel_configs`**: Правила для переименования лейблов или изменения значений метрик.

---

### **Что такое `relabel_configs`?**
`relabel_configs` — это механизм для изменения метаданных (лейблов) перед тем, как метрики будут сохранены в Prometheus. Он используется для:
- Переименования лейблов.
- Фильтрации метрик.
- Добавления или удаления лейблов.

#### Пример `relabel_configs`:
```yaml
relabel_configs:
  - source_labels: [__address__]  # Исходный лейбл (адрес целевого узла).
    target_label: __param_target  # Новый лейбл (параметр для запроса).
  - source_labels: [__param_target]
    target_label: instance  # Новый лейбл (имя инстанса).
  - target_label: __address__
    replacement: 'localhost:9100'  # Замена адреса целевого узла.
```

---

### **Итог:**
- **Node Exporter**: Собирает метрики ОС (CPU, память, диски).
- **Process Exporter**: Собирает метрики по процессам.
- **Blackbox Exporter**: Проверяет доступность сервисов (HTTP, TCP, ICMP).
- **Alertmanager**: Управляет алертами.
- **Remote Read/Write**: Интеграция с удалёнными хранилищами (например, Thanos).
- **Relabel Configs**: Переименование и фильтрация лейблов.
