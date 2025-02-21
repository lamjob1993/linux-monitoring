# Grafana

## Frontend

От вас требуется поднять `Grafana` способом из раздела [Prometheus](https://github.com/lamjob1993/linux-monitoring/tree/main/grafana):
 - Можете модернизировать скрипт установщика `Prometheus`
   - Логин и пароль: **admin** и **admin** по умолчанию 
 - Далее прописываем поднятый `Prometheus`, как `Data Source` в настройках `Grafana`
 - Качаем дашборд `Prometheus` в формате `JSON - откройте его в VS Code и посмотрите на структуру` с сайта `Grafana Lab` (подсказка: дашборд должен быть только для `Prometheus`)
 - Подгружаем дашборд и сохраняем в папку Grafana, не забываем в **настройках дашборда** выбрать `Prometheus`, как `Data Source` в `Grafana`
   - Посмотрите как выглядит дашборд, полистайте виджеты, подумайте что они означают
 - Создайте новый дашборд `prometheus_dashboard` и потренируйтесь переносить виджеты на свой дашборд с дашборда `Prometheus`:
   - Скопируйте 4 виджета
   - Потренируйтесь менять размер виджетов
   - Поменяйте скопированные виджеты на кастом варианты в настройках виджетов (поиграйте, как в песочнице)
   - Подумайте, как сделать ссылку-переход с оригинального дашборда `Prometheus` на ваш дашборд
   - Перейдите на страницу `Prometheus` по адресу `/metrics` (это называется эндроинт) и дёрните оттуда 4 самые важные метрики на ваш взгляд (подсказка: ссылайтесь на [4 золотых сигнала](https://habr.com/ru/articles/747350/ "Набор метрик, которые Google рекомендует отслеживать в SRE (Site Reliability Engineering) подходе. Это Latency, Traffic, Errors и Saturation.")):
     - Попробуйте поискать на странице ключевые слова: `http`, `size`, `byte`, возможно это поможет
     - Сделайте из метрик простейшие виджеты (подсказка: про типы метрик [читаем здесь](https://habr.com/ru/companies/tochka/articles/685636/ "Типы метрик: Summary, Histogram, Gauge, Counter."))
     -  Далее возьмите в работу язык [PromQL](https://habr.com/ru/companies/tochka/articles/693834/ "PromQL - PromQL, или Prometheus Query Language, представляет собой язык запросов, который был создан специально для работы с метриками в системе Prometheus. В основе PromQL лежит концепция метрики, которая включает в себя ряд функций для обработки агрегированных и усредненных данных. Этот метод обеспечивает баланс между точностью и эффективностью, позволяя обрабатывать данные без строгого привязывания к их математическим значениям.")
       - Сделайте **агрегацию** ваших метрик с помощью **операторов** `sum` и `sum by` и посмотрите на отличия
       - Возьмите в работу **функции**: `rate` и `increase`, `sum_over_time` и `max_over_time` и посмотрите на отличия
   - Сохраните дашборд `prometheus_dashboard`


### Запросы для "четырех золотых сигналов" мониторинга в Prometheus:

Важные нюансы:
1. `[5m]` - это окно времени, которое можно изменять под свои нужды
2. Для более точных результатов можно использовать `irate` вместо `rate` при анализе коротких интервалов
3. Не забывайте про группировку данных с помощью `by` или `without` для получения детализированных метрик

1. Latency (Латентность / Время отклика)

Используя Histogram:
```promql
# 95-й процентиль латентности
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# Среднее время отклика
avg(rate(http_request_duration_seconds_sum[5m]) 
    / rate(http_request_duration_seconds_count[5m]))
```

2. Traffic (Трафик / Объем запросов)
```promql
# Общий объем запросов
rate(http_requests_total[5m])

# По HTTP методам
sum(rate(http_requests_total[5m])) by (method)

# По кодам ответов
sum(rate(http_requests_total[5m])) by (status_code)
```

3. Errors (Ошибки)
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

4. Saturation (Нагрузка / Заполненность)

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
```

Общие агрегирующие функции, которые часто используются:

- `sum()` - сумма
- `avg()` - среднее значение
- `max()` - максимальное значение
- `min()` - минимальное значение
- `stddev()` - стандартное отклонение
- `count()` - количество

Группировка результатов:
```promql
# Группировка без указанных меток
sum(...) without (instance, job)

# Группировка по указанным меткам
sum(...) by (method, status_code)
```
