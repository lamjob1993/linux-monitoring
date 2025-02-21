# Prometheus

### Основные понятия Prometheus:

1. **Четыре золотых сигнала (Four Golden Signals)**:
   Четыре золотых сигнала — это набор метрик, предложенный Google для мониторинга производительности и здоровья распределённых систем. Они помогают быстро выявлять проблемы и обеспечивать стабильность работы приложений. Эти сигналы включают:

   1. **Latency** (Задержка / Время отклика)

        - Время, которое требуется для обработки запроса.
        - Важно измерять как успешные, так и неудачные запросы.
        - Пример: 95-й перцентиль времени ответа API.

         **Запросы**
         
         Используя Histogram:
         ```promql
         # 95-й процентиль латентности
         histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
         
         # Среднее время отклика
         avg(rate(http_request_duration_seconds_sum[5m]) 
             / rate(http_request_duration_seconds_count[5m]))
         ```
   
   2. **Traffic** (Трафик / Объем запросов)
      
       - Объём запросов, которые обрабатывает система.
       - Отражает нагрузку на систему.
       - Пример: количество HTTP-запросов в секунду.

         **Запросы**
      
         ```promql
         # Общий объем запросов
         rate(http_requests_total[5m])
         
         # По HTTP методам
         sum(rate(http_requests_total[5m])) by (method)
         
         # По кодам ответов
         sum(rate(http_requests_total[5m])) by (status_code)
         ```
   
   3. **Errors** (Ошибки)

      - Частота ошибок в системе.
      - Включает явные ошибки (например, HTTP 500) и некорректные ответы (например, неверные данные).
      - Пример: процент ошибок от общего числа запросов.
        
         **Запросы**
           
         ```promql
         # Общее количество ошибок
         sum(rate(http_requests_total{status_code=~"5.."}[5m]))
         
         # Процент ошибок (Error Budget)
         (sum(rate(http_requests_total{status_code=~"5.."}[5m]))
          /
          sum(rate(http_requests_total[5m]))) * 100
         
         # Ошибки по методам
         sum(rate(http_requests_total{status_code=~"5.."}[5m])) by (method)
         ```
   
   4. **Saturation** (Нагрузка / Заполненность)

      - Степень загруженности ресурсов системы (CPU, память, диски, сеть).
      - Показывает, насколько система близка к пределу своих возможностей.
      - Пример: использование CPU выше 80%.

         Для CPU:
         ```promql
         # Использование CPU
         100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
         
         # Средняя загрузка CPU
         avg(node_load1) by (instance)
         ```
         
         Для памяти:
         ```promql
         # Использование памяти
         (node_memory_MemTotal - node_memory_MemFree - node_memory_Buffers - node_memory_Cached)
         / node_memory_MemTotal * 100
         ```
         
         Для дискового пространства:
         ```promql
         # Занятое место на диске
         (node_filesystem_size - node_filesystem_free)
         / node_filesystem_size * 100
         ```
         
         Для сетевого трафика:
         ```promql
         # Пропускная способность сети
         sum(rate(node_network_receive_bytes_total[5m]))
         sum(rate(node_network_transmit_bytes_total[5m]))


2. **Метрика (Metric)** в Prometheus — это числовая характеристика системы, которую можно измерить (например, `http_requests_total`). Она описывает состояние или поведение компонента (CPU, память, ошибки и т.д.).

    **Типы метрик**:
    - **Counter** — монотонно возрастающее значение (например, общее число запросов).
    - **Gauge** — значение, которое может увеличиваться или уменьшаться (например, использование памяти).
    - **Histogram** — группирует данные в "корзины" (например, время ответа).
    - **Summary** — аналогичен гистограмме, но вычисляет квантили на стороне сервера.

   #### Пример метрики с лейблами:
   
    ```plaintext
    http_requests_total{method="GET", path="/status", status="200"} 1500
    ```
    - **Метрика**: `http_requests_total` (счётчик HTTP-запросов).
    - **Лейблы**: `method`, `path`, `status` (дополнительные атрибуты запроса).
    - **Значение**: 1500 (число успешных GET-запросов к `/status`).

3. **Лейбл (Label)** — это пара ключ-значение, добавляющая контекст к метрике. Например, метрика `http_requests_total` может иметь лейблы `method="POST"`, `path="/api"`, `status_code="200"`, что позволяет группировать и фильтровать данные.

   #### Как используются лейблы в PromQL?
   
   - Фильтрация:  
     `http_requests_total{status="500"}`         # Выведет только 500-ые статусы по лейблу **status**
   - Группировка:  
     `sum by (method) (http_requests_total)`     # Отсортирует сумму по лейблу **method** каждого HTTP запроса
   - Агрегация:  
     `rate(http_requests_total{job="api"}[5m])`  # Cчитает прирост значения метрики за последние 5 минут при обращении к лейблу **job**

4. **Временной ряд (Time Series)** в Prometheus — это последовательность данных, которая описывает изменение метрики во времени. Каждый временной ряд состоит из:

   1. **Имени метрики** (например, `http_requests_total`).
   2. **Набора лейблов** (например, `method="GET"`, `status="200"`, `job="api"`).
   3. **Набора значений**, где каждое значение привязано к определённому моменту времени.

   #### Пример временного ряда:
   ```plaintext
   http_requests_total{method="GET", status="200", job="api"} @timestamp1 => 100
   http_requests_total{method="GET", status="200", job="api"} @timestamp2 => 150
   http_requests_total{method="GET", status="200", job="api"} @timestamp3 => 200
   ```
   Здесь:
   - **Имя метрики**: `http_requests_total`.
   - **Лейблы**: `method="GET"`, `status="200"`, `job="api"`.
   - **Значения**: `100`, `150`, `200` (привязанные к моментам времени `timestamp1`, `timestamp2`, `timestamp3`).



     #### Как временные ряды используются в Prometheus?
      1. **Хранение данных**:  
         Prometheus хранит данные в виде временных рядов. Каждый временной ряд уникально идентифицируется комбинацией имени метрики и лейблов.
      
      2. **Запросы (PromQL)**:  
         Временные ряды используются для анализа данных. Например, вы можете запросить:  
         - Текущее значение:  
           ```promql
           http_requests_total{job="api"}
           ```
         - Скорость изменения:  
           ```promql
           rate(http_requests_total{job="api"}[5m])
           ```
      
      3. **Визуализация**:  
         Временные ряды используются в Grafana или других инструментах для построения графиков.
      
      4. **Алертинг**:  
         На основе временных рядов можно настраивать правила алертинга. Например:  
         ```promql
         rate(http_requests_total{job="api"}[5m]) > 100
         ```
      
      
      #### Как временные ряды создаются?
      1. **Экспортеры**:  
         Экспортеры (например, Node Exporter, Blackbox Exporter) собирают данные и отправляют их в Prometheus в виде временных рядов.
      
      2. **Pushgateway**:  
         Для задач с коротким сроком жизни (например, cron-задачи) данные могут быть отправлены через Pushgateway.
   
5. **Экспортер (Exporter)**  
   Это специальная программа или сервис, который собирает метрики из внешней системы (например, операционная система, база данных, аппаратное обеспечение) и предоставляет их в формате, понятном Prometheus. Экспортер действует как мост между целевой системой и Prometheus, преобразуя данные в метрики, которые Prometheus может собирать.

      1. **Сбор метрик**:
         - Экспортер собирает данные из целевой системы (например, использование CPU, память, количество запросов к базе данных).
         - Эти данные преобразуются в метрики в формате Prometheus.
      
      2. **Предоставление метрик**:
         - Экспортер предоставляет метрики через HTTP-эндпоинт, обычно в виде простого текстового формата.
         - Пример вывода:
           ```plaintext
           # HELP node_cpu_seconds_total Seconds the CPUs spent in each mode.
           # TYPE node_cpu_seconds_total counter
           node_cpu_seconds_total{cpu="0",mode="user"} 12345.67
           node_cpu_seconds_total{cpu="0",mode="system"} 6789.01
           ```
      
      3. **Сбор метрик Prometheus**:
         - Prometheus периодически запрашивает (вытягивает) метрики с экспортера по HTTP.
         - В конфигурации Prometheus указывается адрес экспортера:
           ```yaml
           scrape_configs:
             - job_name: 'node_exporter'
               static_configs:
                 - targets: ['localhost:9100']
           ```
      
      4. **Анализ и визуализация**:
         - Собранные метрики можно анализировать с помощью PromQL и визуализировать в Grafana.

6. **PromQL**  
   Язык запросов для анализа данных (например, `rate(http_requests_total[5m])`).

   Общие агрегирующие функции, которые часто используются:

   - `sum()` - сумма
   - `avg()` - среднее значение
   - `max()` - максимальное значение
   - `min()` - минимальное значение
   - `count()` - количество

    Группировка результатов:
    ```promql
    # Группировка без указанных меток (лейблам)
    sum(...) without (instance, job)
    
    # Группировка по указанным меткам (лейблам)
    sum(...) by (method, status_code)
    ```

    Важные нюансы:
    1. `[5m]` - это окно времени, которое можно изменять под свои нужды
    2. Для более точных результатов можно использовать `irate` вместо `rate` при анализе коротких интервалов
    3. Не забывайте про группировку данных с помощью `by` или `without` для получения детализированных метрик


7. **Сервис-дискавери (Service Discovery)**  
   Автоматическое обнаружение целей для сбора метрик (Kubernetes, AWS, Consul и др.).

8. **Alertmanager**  
   Компонент для управления уведомлениями на основе правил (например, отправка алерта при высокой загрузке CPU).

9. **Pushgateway**  
   Промежуточный сервис для сбора метрик от задач с коротким сроком жизни (например, cron-задач).
