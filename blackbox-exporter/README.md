## Blackbox Exporter

**Blackbox Exporter** используется для проверки доступности и работоспособности внешних сервисов (например, **HTTP**, **TCP**, **ICMP**, **DNS** и т.д.). На странице /metrics будут отображаться метрики, связанные с результатами этих проверок.

 - Установите `Blackbox Exporter` в систему и натравите на него `Prometheus`
 - Подумайте, как настроить конфиг экспортера (подсказка: возможно конфиг нужен не один?)
 - Перейдите на страницу `/metrics` и удостоверьтесь, что экспортер поднялся
 - По заданию вам нужно замониторить 5 серверов (сайтов), например: **Google**, **Yandex** и **VK** + 2 любых на свой выбор
 - Скачайте дашборд предназначенный для `Blackbox Exporter` с сайта `Grafana Lab`
 - Подгрузите дашборд в `Grafana`, убедитесь, что он работает и сохраните

Blackbox Exporter и Process Exporter — это инструменты для мониторинга в экосистеме Prometheus. Они предоставляют метрики на своих эндпоинтах `/metrics`, которые используются для сбора данных и анализа состояния системы. Давайте разберем, что можно ожидать на странице `/metrics` для каждого из них.

---

#### Пример метрик:
- `probe_success` — показывает, была ли проверка успешной (1 — успешно, 0 — неудача).
- `probe_duration_seconds` — время, затраченное на выполнение проверки.
- `probe_http_status_code` — HTTP-статус код, если проверялся HTTP-сервис.
- `probe_http_duration_seconds` — время выполнения HTTP-запроса.
- `probe_ssl_earliest_cert_expiry` — срок действия SSL-сертификата (если проверяется HTTPS).

#### Пример вывода:
```plaintext
# HELP probe_success Displays whether or not the probe was a success
# TYPE probe_success gauge
probe_success{instance="http://example.com", job="http_2xx"} 1

# HELP probe_duration_seconds Returns how long the probe took to complete in seconds
# TYPE probe_duration_seconds gauge
probe_duration_seconds{instance="http://example.com", job="http_2xx"} 0.123456789

# HELP probe_http_status_code Response HTTP status code
# TYPE probe_http_status_code gauge
probe_http_status_code{instance="http://example.com", job="http_2xx"} 200
```
