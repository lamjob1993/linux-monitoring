## **Технические вопросы по Nginx Exporter**

1. **Что такое Nginx Exporter и для чего он используется?**
   - Ответ: Nginx Exporter — это инструмент, который собирает метрики из веб-сервера Nginx и предоставляет их в формате, совместимом с Prometheus. Он используется для мониторинга производительности и состояния сервера Nginx.

2. **Какие метрики предоставляет Nginx Exporter?**
   - Ответ: Основные метрики включают:
     - `nginx_connections_active` — текущее количество активных подключений.
     - `nginx_requests_total` — общее количество обработанных запросов.
     - `nginx_connections_handled` — количество обработанных подключений.
     - `nginx_http_requests_total` — количество HTTP-запросов по статусам.

3. **Как настроить Nginx для работы с Nginx Exporter?**
   - Ответ: Необходимо включить модуль `stub_status` в конфигурации Nginx:
     ```nginx
     location /nginx_status {
         stub_status on;
         allow 127.0.0.1;
         deny all;
     }
     ```

4. **Как установить Nginx Exporter?**
   - Ответ: Установка через скачивание бинарного файла или Docker:
     ```bash
     docker run -d --name nginx-exporter -p 9113:9113 nginx/nginx-prometheus-exporter:latest -nginx.scrape-uri=http://localhost/nginx_status
     ```

5. **Как проверить работу Nginx Exporter?**
   - Ответ: Используйте команду:
     ```bash
     curl http://localhost:9113/metrics
     ```
     Она вернет метрики в формате Prometheus.

6. **Как интегрировать Nginx Exporter с Prometheus?**
   - Ответ: Добавьте таргет в конфигурацию Prometheus (`prometheus.yml`):
     ```yaml
     scrape_configs:
       - job_name: 'nginx'
         static_configs:
           - targets: ['localhost:9113']
     ```

7. **Как обеспечить безопасность Nginx Exporter?**
   - Ответ: Ограничьте доступ к порту экспортера через firewall или настройте reverse proxy (например, Nginx) с базовой аутентификацией.

8. **Как уменьшить нагрузку на сервер от Nginx Exporter?**
   - Ответ: Уменьшите частоту сбора данных через параметр `scrape_interval` в Prometheus или отключите ненужные метрики.

9. **Можно ли использовать Nginx Exporter для мониторинга SSL/TLS?**
   - Ответ: Нет, для этого используется Blackbox Exporter. Однако можно комбинировать оба инструмента.

10. **Как настроить автозапуск Nginx Exporter?**
    - Ответ: Создайте unit-файл для systemd:
      ```ini
      [Unit]
      Description=Nginx Exporter

      [Service]
      ExecStart=/usr/local/bin/nginx-prometheus-exporter -nginx.scrape-uri=http://localhost/nginx_status
      Restart=always

      [Install]
      WantedBy=multi-user.target
      ```

---

### **Технические вопросы по Nginx**

11. **Что такое Nginx и для чего он используется?**
    - Ответ: Nginx — это высокопроизводительный веб-сервер, который также может работать как обратный прокси, балансировщик нагрузки и HTTP-кэш.

12. **Как работает асинхронная архитектура Nginx?**
    - Ответ: Nginx использует event-driven архитектуру, где один процесс может обрабатывать множество соединений одновременно, что делает его эффективным для высоких нагрузок.

13. **Как настроить балансировку нагрузки в Nginx?**
    - Ответ: Используйте блок `upstream`:
      ```nginx
      upstream backend {
          server 192.168.1.101;
          server 192.168.1.102;
      }

      server {
          location / {
              proxy_pass http://backend;
          }
      }
      ```

14. **Какие алгоритмы балансировки поддерживает Nginx?**
    - Ответ: Round Robin (по умолчанию), `least_conn`, `ip_hash`, `hash`.

15. **Как настроить HTTPS в Nginx?**
    - Ответ: Настройте SSL-сертификаты:
      ```nginx
      server {
          listen 443 ssl;
          server_name example.com;

          ssl_certificate /path/to/cert.pem;
          ssl_certificate_key /path/to/key.pem;
      }
      ```

16. **Как защитить Nginx от DDoS-атак?**
    - Ответ: Используйте модули `limit_req` и `limit_conn`:
      ```nginx
      limit_req_zone $binary_remote_addr zone=one:10m rate=1r/s;

      server {
          location / {
              limit_req zone=one burst=5 nodelay;
          }
      }
      ```

17. **Как включить gzip-сжатие в Nginx?**
    - Ответ: Добавьте следующие строки в конфигурацию:
      ```nginx
      gzip on;
      gzip_types text/plain text/css application/json application/javascript;
      ```

18. **Как настроить кэширование в Nginx?**
    - Ответ: Используйте директивы `proxy_cache`:
      ```nginx
      proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m max_size=1g;
      server {
          location / {
              proxy_cache my_cache;
              proxy_pass http://backend;
          }
      }
      ```

19. **Как проверить корректность конфигурации Nginx?**
    - Ответ: Используйте команду:
      ```bash
      sudo nginx -t
      ```

20. **Как настроить логирование в Nginx?**
    - Ответ: Настройте формат логов и пути:
      ```nginx
      log_format custom '$remote_addr - $remote_user [$time_local] "$request" '
                        '$status $body_bytes_sent "$http_referer" '
                        '"$http_user_agent" "$http_x_forwarded_for"';
      access_log /var/log/nginx/access.log custom;
      error_log /var/log/nginx/error.log warn;
      ```

---

### **Дополнительные вопросы для продвинутого уровня**

#### **Nginx Exporter**
- Как вы решали проблемы с большим количеством метрик?
- Как интегрировать Nginx Exporter с Grafana?

#### **Nginx**
- Как настроить редирект с HTTP на HTTPS?
  - Ответ: Используйте правило:
    ```nginx
    server {
        listen 80;
        server_name example.com;
        return 301 https://$host$request_uri;
    }
    ```

- Как использовать Nginx для обслуживания статического контента?
  - Ответ: Настройте директорию для статики:
    ```nginx
    server {
        root /var/www/static;
        index index.html;

        location / {
            try_files $uri $uri/ =404;
        }
    }
    ```

- Как настроить health check для бэкенд-серверов?
  - Ответ: Используйте параметры `max_fails` и `fail_timeout`:
    ```nginx
    upstream backend {
        server 192.168.1.101 max_fails=3 fail_timeout=30s;
        server 192.168.1.102 max_fails=3 fail_timeout=30s;
    }
    ```

- Как ограничить доступ к определенным IP-адресам?
  - Ответ: Используйте директивы `allow` и `deny`:
    ```nginx
    location /admin {
        allow 192.168.1.0/24;
        deny all;
    }
    ```

