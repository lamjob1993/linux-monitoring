# Blackbox Exporter
_Пользуемся официальной документацией на GitHub (в основном там прописаны Docker файлы на запуск и всегда есть конфиги)_

## Tasks 2

### Мониторинг сертификатов

Для генерации SSL-сертификатов, которые могут использоваться для проверки через **Blackbox Exporter**, необходимо создать самоподписанный сертификат или использовать сертификат, выданный доверенным центром сертификации (CA). **Blackbox Exporter** используется для мониторинга доступности и работоспособности сервисов, включая проверку SSL/TLS-соединений.

---

### 1. **Генерация самоподписанного SSL-сертификата**
Самоподписанный сертификат можно создать с помощью утилиты `openssl`.

#### a) Создание закрытого ключа
```bash
openssl genpkey -algorithm RSA -out server.key
```
Это создаст файл `server.key`, содержащий закрытый ключ.

#### b) Создание CSR (Certificate Signing Request)
CSR содержит информацию о вашем домене и открытый ключ.
```bash
openssl req -new -key server.key -out server.csr
```
В процессе выполнения команды вас попросят ввести данные, такие как страна, организация, доменное имя и т.д. Убедитесь, что поле **Common Name (CN)** соответствует доменному имени вашего сервера.

#### c) Создание самоподписанного сертификата
```bash
openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt
```
Это создаст файл `server.crt`, который является самоподписанным сертификатом, действительным в течение 365 дней.

#### d) Объединение ключа и сертификата (опционально)
Если ваш сервер требует объединенный файл, вы можете выполнить:
```bash
cat server.key server.crt > server.pem
```

Теперь у вас есть:
- `server.key` — закрытый ключ.
- `server.crt` — самоподписанный сертификат.
- (Опционально) `server.pem` — объединенный файл.

---

### 2. **Настройка Blackbox Exporter**
Blackbox Exporter позволяет выполнять различные типы проверок, включая проверку SSL/TLS. Для этого нужно настроить конфигурационный файл `blackbox.yml`.

#### Пример конфигурации для проверки SSL:
```yaml
modules:
  http_2xx_ssl:
    prober: http
    http:
      valid_http_versions: ["HTTP/1.1", "HTTP/2"]
      fail_if_ssl: false
      fail_if_not_ssl: true
      tls_config:
        insecure_skip_verify: true  # Игнорировать проверку цепочки сертификатов (например, для самоподписанных сертификатов)
```

#### Пояснения к параметрам:
- `prober: http` — указывает, что используется HTTP-пробер.
- `fail_if_ssl: false` — разрешает SSL-соединения.
- `fail_if_not_ssl: true` — требует, чтобы соединение было защищено SSL/TLS.
- `tls_config.insecure_skip_verify: true` — игнорирует проверку цепочки сертификатов (полезно для тестирования самоподписанных сертификатов).

---

### 3. **Запуск Blackbox Exporter**
Убедитесь, что Blackbox Exporter запущен с указанием конфигурационного файла:
```bash
./blackbox_exporter --config.file=blackbox.yml
```

---

### 4. **Настройка Prometheus**
Чтобы Prometheus использовал Blackbox Exporter для проверки SSL, добавьте job в конфигурацию Prometheus (`prometheus.yml`):

```yaml
scrape_configs:
  - job_name: 'ssl_check'
    metrics_path: /probe
    params:
      module: [http_2xx_ssl]  # Модуль, определенный в blackbox.yml
    static_configs:
      - targets:
          - https://your-domain.com  # URL для проверки SSL
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - target_label: __address__
        replacement: localhost:9115  # Адрес Blackbox Exporter
```

---

### 5. **Проверка локальных сертификатов**
_Перед выполнением этого пункта для начала изучите [эту тему](https://github.com/lamjob1993/linux-monitoring/tree/main/nginx) и возвращайтесь сюда на практику._


Если вы хотите протестировать локально сгенерированные сертификаты через Blackbox Exporter, выполните следующие шаги:

#### **Настройте локальный HTTPS-сервер**
Используйте Nginx для раздачи HTTPS-контента с использованием ваших сертификатов. Nginx ставим через `apt` менеджер.

Пример конфигурации для Nginx:
```nginx
server {
    listen 443 ssl;
    server_name localhost;

    ssl_certificate /path/to/server.crt;  # Путь к вашему сертификату
    ssl_certificate_key /path/to/server.key;  # Путь к вашему закрытому ключу

    location / {
        return 200 "Hello, SSL!";
    }
}
```

После настройки запустите Nginx:
```bash
sudo nginx -s reload
```

Теперь ваш локальный сервер доступен по адресу `https://localhost`.

---

### 6. **Проверка работы**
После настройки Prometheus начнет собирать метрики через Blackbox Exporter. Вы можете проверить их в интерфейсе Prometheus или Grafana.

Пример запроса для проверки статуса SSL:
```promql
probe_ssl_earliest_cert_expiry
```
Эта метрика показывает время истечения срока действия SSL-сертификата.

---

### 6. **Дополнительные рекомендации**
- Если вы используете самоподписанный сертификат, убедитесь, что параметр `insecure_skip_verify` установлен в `true`.
- Для продакшена рекомендуется использовать сертификаты, выданные доверенным центром сертификации (например, Let's Encrypt).
- Если вы хотите проверять несколько доменов, добавьте их в секцию `targets` в конфигурации Prometheus.

### 7. **Nginx Exporter**
- Вернитесь в раздел Nginx и выполните [второе упражнение](https://github.com/lamjob1993/linux-monitoring/blob/main/nginx/task_2.md)
