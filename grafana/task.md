# Grafana

## Строим визуал
## Процедура связки: Grafana (Frontend GUI) + Prometheus (Backend) + Node Exporter (Metrics)

## Разберем основные разделы перед тем как строить визуал

### 1. **Переменные в Grafana**
Переменные позволяют динамически менять параметры дашборда (например, фильтровать данные по метке `instance` или `job`).

#### Как создать переменную:
1. **Откройте настройки дашборда** → **Variables** → **Add variable**.
2. **Типы переменных**:
   - **Query**: Значения из запроса к источнику данных (например, Prometheus).
   - **Custom**: Ручной ввод значений.
   - **Label**: Значения метки из указанного источника.
   - **Ad hoc filters**: Динамические фильтры для всех метрик.

#### Пример переменной на основе метки `instance`:
- **Name**: `instance`
- **Type**: **Query**
- **Query**: `label_values(instance)`
- **Data source**: Ваш Prometheus.

Теперь в запросах к метрикам можно использовать `$instance` для подстановки выбранного значения.

---

### 2. **Лейблы (метки) в Prometheus**
Метки — это ключ-значение, добавляемые к метрикам. Они позволяют группировать и фильтровать данные.

#### Как добавить лейблы:
1. **В конфигурации Prometheus** (`prometheus.yml`):
   ```yaml
   scrape_configs:
     - job_name: 'my_job'
       static_configs:
         - targets: ['localhost:9090']
       labels:
         region: 'europe'  # Добавляет лейбл `region="europe"` ко всем метрикам этого job.
   ```
2. **Через relabel_configs** (более гибко):
   ```yaml
   relabel_configs:
     - source_labels: [__address__]
       target_label: instance
   ```

#### Пример метрики с лейблами:
Метрика `http_requests_total` с лейблами:
```
http_requests_total{method="GET", endpoint="/api", status="200"} 100
http_requests_total{method="POST", endpoint="/api", status="500"} 5
```

---

### 3. **Как лейблы отображаются в Grafana**
1. **В интерфейсе запросов**:
   - При написании PromQL-запроса, лейблы доступны для фильтрации:
     ```
     rate(http_requests_total{instance="$instance", job="my_job"}[5m])
     ```
   - В легенде графика можно использовать шаблоны лейблов: `{{method}} - {{endpoint}}`.

2. **В переменных**:
   - Используйте `label_values(<метрика>, <лейбл>)` для получения значений:
     ```
     label_values(http_requests_total, endpoint)  # Вернет ["/api", ...]
     ```

---

### 4. **Как лейблы становятся частью метрики**
- Каждая уникальная комбинация лейблов создает отдельный временной ряд.
- Например, `http_requests_total{method="GET"}` и `http_requests_total{method="POST"}` — это два разных ряда.
- **Важно**: Избегайте высокой кардинальности (уникальных комбинаций лейблов), чтобы не перегружать Prometheus.

---

### 5. **Пошаговый пример**
#### Шаг 1: Добавьте лейблы в Prometheus
```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'node_exporter'
    static_configs:
      - targets: ['host_name:9100']
    relabel_configs:
      - source_labels: [__address__]
        target_label: instance  # Добавляет лейбл `instance="host_name:9100"`
```

#### Шаг 2: Убедитесь, что метки есть в Prometheus
Перейдите в Prometheus → **Graph** → выполните запрос `up{job="node_exporter"}`. Должен отображаться лейбл `instance`.

#### Шаг 3: Создайте переменную в Grafana
- **Name**: `instance`
- **Type**: **Query**
- **Query**: `label_values(up{job="node_exporter"}, instance)`

#### Шаг 4: Используйте переменную в дашборде
Создайте график с запросом:
```
rate(node_cpu_seconds_total{instance="$instance", job="node_exporter"}[5m])
```

---

### 6. **Best Practices**
- Используйте метки для логической группировки (например, `env="prod"`, `team="backend"`).
- Не создавайте метки с уникальными значениями (например, ID пользователя).
- В Grafana используйте `$<variable_name>` для подстановки значений в запросы.
