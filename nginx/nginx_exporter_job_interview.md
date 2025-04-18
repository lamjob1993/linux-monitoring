## Как вы использовали Nginx Exporter на практике, для каких команд устанавливали и какие кейсы с ним были?

---

### 1. **Как Nginx Exporter использовался в вашей работе?**

**Пример ответа:**
"Nginx Exporter использовался для мониторинга состояния веб-серверов Nginx. Мы собирали метрики, такие как количество активных подключений (`nginx_connections_active`), общее количество обработанных запросов (`nginx_requests_total`), скорость обработки запросов и статус HTTP-ответов. Эти данные интегрировались с Prometheus для анализа и с Grafana для визуализации. Это позволяло нам отслеживать производительность серверов Nginx, выявлять проблемы с нагрузкой и оперативно реагировать на инциденты."

---

### 2. **Какие команды вы использовали для работы с Nginx Exporter?**

#### Установка Nginx Exporter:
```bash
wget https://github.com/nginxinc/nginx-prometheus-exporter/releases/download/v0.12.0/nginx-prometheus-exporter_0.12.0_linux_amd64.tar.gz
tar xvfz nginx-prometheus-exporter_0.12.0_linux_amd64.tar.gz
./nginx-prometheus-exporter -nginx.scrape-uri=http://localhost/nginx_status
```
**Я устанавливал Nginx Exporter через скачивание бинарного файла с GitHub. Запускал его с флагами для настройки URL сбора метрик (например, `/nginx_status`) и указания порта для экспортера.**

#### Проверка работы Nginx Exporter:
```bash
curl http://localhost:9113/metrics
```
**Для проверки работы я использовал curl, чтобы получить метрики из `/metrics`. Это помогало убедиться, что экспортер корректно собирает данные.**

#### Настройка автозапуска через systemd:
```ini
[Unit]
Description=Nginx Exporter

[Service]
ExecStart=/usr/local/bin/nginx-prometheus-exporter -nginx.scrape-uri=http://localhost/nginx_status
Restart=always

[Install]
WantedBy=multi-user.target
```
**Для автоматического запуска я создавал unit-файл для systemd, чтобы Nginx Exporter работал как служба.**

---

### 3. **Кому вы устанавливали Nginx Exporter?**

**Пример ответа:**
"Я устанавливал Nginx Exporter на:

- **Серверы Nginx**: для мониторинга их производительности в production.
- **Команды DevOps/SRE**: для отслеживания состояния серверов и настройки алертов.
- **Команды разработчиков**: для анализа производительности их приложений, работающих за Nginx (например, время обработки запросов)."

---

### 4. **Какие каверзные вопросы могут возникнуть и как на них ответить?**

#### Вопрос: Как вы решали проблемы с производительностью Nginx Exporter?
**Ответ:**
"Если возникали проблемы с производительностью, я:

1. Оптимизировал конфигурацию Nginx, например, увеличивал лимиты на количество подключений (`worker_connections`).
2. Уменьшал частоту сбора данных через параметр `scrape_interval` в Prometheus.
3. Настроил логирование для диагностики проблем."

#### Вопрос: Как вы обеспечивали безопасность Nginx Exporter?
**Ответ:**
"Я ограничивал доступ к порту экспортера через firewall или настраивал reverse proxy (Nginx) с базовой аутентификацией. Также я ограничивал доступ к эндпоинту `/nginx_status`, разрешая только localhost."

#### Вопрос: Как вы решали проблему с большим количеством метрик?
**Ответ:**
"Если метрик было слишком много, я:

1. Отключал ненужные метрики через конфигурацию экспортера.
2. Фильтровал метрики в Prometheus, используя `relabel_configs`.
3. Использовал агрегацию данных в PromQL для уменьшения объёма информации."

#### Вопрос: Как вы настраивали мониторинг SSL/TLS в Nginx?
**Ответ:**
"Я добавлял метрики о состоянии SSL/TLS сертификатов через Blackbox Exporter. Например, я использовал запросы для отслеживания сроков действия сертификатов (`probe_ssl_earliest_cert_expiry`)."

---

### 5. **Пример успешного кейса использования Nginx Exporter**

**Пример ответа:**
"Однажды мы столкнулись с проблемой высокого времени ответа сервера Nginx. С помощью Nginx Exporter мы настроили мониторинг метрик, таких как `nginx_http_request_duration_seconds` и `nginx_connections_waiting`. Мы обнаружили, что во время пиковых нагрузок количество ожидающих подключений (`nginx_connections_waiting`) превышает допустимый порог. После оптимизации конфигурации Nginx (увеличение лимитов на подключения) время ответа значительно сократилось."

---

### 6. **Что ещё можно добавить?**

#### Интеграция с Prometheus и Grafana:
"Мы интегрировали Nginx Exporter с Prometheus для сбора метрик и с Grafana для визуализации. Это позволило нам создавать информативные дашборды с данными о производительности серверов Nginx."

#### Автоматизация установки:
"Для масштабирования я написал Ansible playbook для автоматической установки и настройки Nginx Exporter."

#### Мониторинг бизнес-метрик:
"Мы использовали Nginx Exporter для мониторинга ключевых бизнес-метрик, таких как количество HTTP-ошибок (например, `nginx_http_requests_total{status=~"5.."}`) и среднее время обработки запросов."
