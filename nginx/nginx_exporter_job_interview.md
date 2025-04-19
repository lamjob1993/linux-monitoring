## Практический опыт использования Nginx Exporter

На практике **Nginx Exporter** используется для мониторинга производительности и состояния веб-сервера Nginx.

---

### 1. **Кейс: Мониторинг загрузки серверов Nginx**
#### Задача:
Мониторинг количества активных подключений, общего числа запросов и обработанных соединений для анализа нагрузки на серверы Nginx.

#### Решение:
- Установка **Nginx Exporter** для сбора метрик.
- Интеграция с **Prometheus** для хранения данных.
- Визуализация данных в **Grafana**.

#### Шаги:
1. **Настройка Nginx**:
   - Добавление эндпоинта `/nginx_status` для модуля `stub_status`.
   ```nginx
   server {
       listen 80;
       server_name nginx.example.com;

       location /nginx_status {
           stub_status on;
           allow 127.0.0.1; # Разрешаем доступ только с localhost
           deny all;       # Запрещаем доступ с других IP
       }
   }
   ```

2. **Установка Nginx Exporter**:
   - Использование Docker для запуска экспортера:
   ```bash
   docker run -d \
     --name nginx-exporter \
     -p 9113:9113 \
     nginx/nginx-prometheus-exporter:latest \
     -nginx.scrape-uri=http://localhost/nginx_status
   ```

3. **Настройка Prometheus**:
   - Добавление таргета для Nginx Exporter в конфигурацию Prometheus (`prometheus.yml`):
   ```yaml
   scrape_configs:
     - job_name: 'nginx'
       static_configs:
         - targets: ['localhost:9113']
   ```

4. **Создание дашборда в Grafana**:
   - Панели для отображения:
     - `nginx_connections_active` — текущее количество активных подключений.
     - `rate(nginx_requests_total[1m])` — скорость обработки запросов за минуту.
     - `nginx_connections_handled` — общее количество обработанных подключений.

#### Результат:
- Было выявлено, что во время пиковых нагрузок количество активных подключений (`nginx_connections_active`) превышает допустимый порог, что приводило к замедлению обработки запросов. Это позволило оптимизировать конфигурацию Nginx (например, увеличить лимиты на количество подключений).

---

### 2. **Кейс: Выявление проблем с производительностью**
#### Задача:
Определить причины снижения производительности веб-сервера Nginx.

#### Решение:
- Использование метрик Nginx Exporter для анализа:
  - Количество обработанных запросов.
  - Время ответа сервера.
  - Количество ошибок (например, HTTP 5xx).

#### Шаги:
1. **Добавление метрик в Prometheus**:
   - Создание алертов для критических ситуаций:
   ```yaml
   groups:
     - name: nginx_alerts
       rules:
         - alert: HighActiveConnections
           expr: nginx_connections_active > 500
           for: 5m
           labels:
             severity: critical
           annotations:
             summary: "High number of active connections on Nginx"
             description: "Nginx has more than 500 active connections for the last 5 minutes."

         - alert: HighErrorRate
           expr: rate(nginx_http_requests_total{status=~"5.."}[5m]) > 0.1
           for: 5m
           labels:
             severity: warning
           annotations:
             summary: "High error rate on Nginx"
             description: "More than 10% of requests result in HTTP 5xx errors."
   ```

2. **Анализ данных в Grafana**:
   - Создание графиков для отслеживания:
     - Количество ошибок (`nginx_http_requests_total{status=~"5.."}`).
     - Скорость обработки запросов (`rate(nginx_requests_total[1m])`).

#### Результат:
- Было обнаружено, что во время пиковых нагрузок количество HTTP 5xx ошибок резко возрастало. Это указывало на проблемы с бэкенд-серверами, которые обрабатывали запросы. После масштабирования бэкенда проблема была решена.

---

### 3. **Кейс: Оптимизация конфигурации Nginx**
#### Задача:
Оптимизация параметров Nginx для повышения производительности.

#### Решение:
- Использование метрик Nginx Exporter для анализа:
  - Количество обработанных запросов.
  - Размер очереди ожидающих подключений.
  - Среднее время обработки запросов.

#### Шаги:
1. **Настройка метрик**:
   - Добавление графиков в Grafana для отслеживания:
     - `nginx_connections_reading`, `nginx_connections_writing`, `nginx_connections_waiting`.
     - `rate(nginx_requests_total[1m])`.

2. **Анализ данных**:
   - Было выявлено, что количество ожидающих подключений (`nginx_connections_waiting`) часто превышает допустимый порог. Это указывало на необходимость увеличения количества worker-процессов и их соединений.

3. **Изменение конфигурации Nginx**:
   ```nginx
   worker_processes auto;
   worker_connections 4096;
   multi_accept on;
   ```

#### Результат:
- После изменения конфигурации количество ожидающих подключений значительно снизилось, что улучшило общую производительность сервера.

---

### 4. **Кейс: Алертинг на основе метрик**
#### Задача:
Настроить алертинг для своевременного обнаружения проблем с сервером Nginx.

#### Решение:
- Использование Prometheus Alertmanager для отправки уведомлений о проблемах.

#### Шаги:
1. **Настройка алертов в Prometheus**:
   ```yaml
   groups:
     - name: nginx_alerts
       rules:
         - alert: NginxDown
           expr: up{job="nginx"} == 0
           for: 1m
           labels:
             severity: critical
           annotations:
             summary: "Nginx is down"
             description: "Nginx exporter is not reachable for more than 1 minute."

         - alert: HighLatency
           expr: rate(nginx_http_request_duration_seconds_sum[5m]) / rate(nginx_http_request_duration_seconds_count[5m]) > 2
           for: 5m
           labels:
             severity: warning
           annotations:
             summary: "High latency on Nginx"
             description: "Average request duration exceeds 2 seconds."
   ```

2. **Настройка Alertmanager**:
   - Настройка отправки уведомлений в Slack или email.

#### Результат:
- Алерты помогли своевременно обнаруживать проблемы с доступностью сервера Nginx и высокой задержкой обработки запросов.

---

### 5. **Кейс: Мониторинг SSL-сертификатов**
#### Задача:
Отслеживание сроков действия SSL-сертификатов для предотвращения их истечения.

#### Решение:
- Использование метрики `probe_ssl_earliest_cert_expiry` из Blackbox Exporter в сочетании с Nginx Exporter.

#### Шаги:
1. **Настройка Blackbox Exporter**:
   ```yaml
   modules:
     http_2xx:
       prober: http
       timeout: 5s
       http:
         valid_http_versions: ["HTTP/1.1", "HTTP/2"]
         fail_if_ssl: false
         fail_if_not_ssl: true
   ```

2. **Добавление алерта в Prometheus**:
   ```yaml
   groups:
     - name: ssl_alerts
       rules:
         - alert: SSLCertExpiry
           expr: probe_ssl_earliest_cert_expiry - time() < 86400 * 7
           for: 1h
           labels:
             severity: critical
           annotations:
             summary: "SSL certificate is expiring soon"
             description: "SSL certificate for {{ $labels.instance }} will expire in less than 7 days."
   ```

#### Результат:
- Алерты помогли своевременно обновлять SSL-сертификаты, предотвращая простои из-за их истечения.
