# Grafana

## Frontend

**От вас требуется поднять** `Grafana` способом из раздела [Prometheus](https://github.com/lamjob1993/linux-monitoring/blob/main/prometheus/Backend.md):
 - Можете модернизировать скрипт установщика `Prometheus`
 - Логин и пароль `Grafana`: **admin** и **admin** по умолчанию 
 - Далее прописываем поднятый `Prometheus`, как `Data Source` в настройках `Grafana`
 - Качаем дашборд `Prometheus` в формате `JSON - откройте его в VS Code и посмотрите на структуру` с сайта `Grafana Lab` (подсказка: дашборд должен быть только для `Prometheus`)
 - Подгружаем дашборд и сохраняем в папку `Grafana`
 - Посмотрите как выглядит дашборд, полистайте виджеты, подумайте что они означают

**Создайте новый дашборд** `prometheus_dashboard` и потренируйтесь переносить виджеты на свой дашборд с дашборда `Prometheus`:
   - Скопируйте 4 виджета
   - Потренируйтесь менять размер виджетов
   - Поменяйте скопированные виджеты на кастом варианты в настройках виджетов (поиграйте, как в песочнице)
   - Сделайте ссылку-переход с оригинального дашборда `Prometheus` на ваш дашборд
  
**На основе** [изученного материала](https://github.com/lamjob1993/linux-monitoring/blob/main/prometheus/README.md "Основные понятия Prometheus.") сделайте задания ниже:
     
   - Перейдите на страницу `Prometheus` по адресу `/metrics` (это называется эндроинт)
     - Найдите 4 золотых сигнала в списке метрик
   - Сделайте из метрик виджеты
   - Сделайте **агрегацию** ваших метрик и возьмите в работу **функции** на основе изученного материала
   - Сохраните дашборд `prometheus_dashboard`




















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

### 2. **Метки (Labels) в Prometheus**
Метки — это ключ-значение, добавляемые к метрикам. Они позволяют группировать и фильтровать данные.

#### Как добавить метки:
1. **В конфигурации Prometheus** (`prometheus.yml`):
   ```yaml
   scrape_configs:
     - job_name: 'my_job'
       static_configs:
         - targets: ['localhost:9090']
       labels:
         region: 'europe'  # Добавляет метку `region="europe"` ко всем метрикам этого job.
   ```
2. **Через relabel_configs** (более гибко):
   ```yaml
   relabel_configs:
     - source_labels: [__address__]
       target_label: instance
   ```

#### Пример метрики с метками:
Метрика `http_requests_total` с метками:
```
http_requests_total{method="GET", endpoint="/api", status="200"} 100
http_requests_total{method="POST", endpoint="/api", status="500"} 5
```

---

### 3. **Как метки отображаются в Grafana**
1. **В интерфейсе запросов**:
   - При написании PromQL-запроса, метки доступны для фильтрации:
     ```
     rate(http_requests_total{instance="$instance", job="my_job"}[5m])
     ```
   - В легенде графика можно использовать шаблоны меток: `{{method}} - {{endpoint}}`.

2. **В переменных**:
   - Используйте `label_values(<метрика>, <метка>)` для получения значений:
     ```
     label_values(http_requests_total, endpoint)  # Вернет ["/api", ...]
     ```

---

### 4. **Как метки становятся частью метрики**
- Каждая уникальная комбинация меток создает отдельный временной ряд.
- Например, `http_requests_total{method="GET"}` и `http_requests_total{method="POST"}` — это два разных ряда.
- **Важно**: Избегайте высокой кардинальности (уникальных комбинаций меток), чтобы не перегружать Prometheus.

---

### 5. **Пошаговый пример**
#### Шаг 1: Добавьте метки в Prometheus
```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'node_exporter'
    static_configs:
      - targets: ['node1:9100']
    relabel_configs:
      - source_labels: [__address__]
        target_label: instance  # Добавляет метку `instance="node1:9100"`
```

#### Шаг 2: Убедитесь, что метки есть в Prometheus
Перейдите в Prometheus → **Graph** → выполните запрос `up{job="node_exporter"}`. Должна отображаться метка `instance`.

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
