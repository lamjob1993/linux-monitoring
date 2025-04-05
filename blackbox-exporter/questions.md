# **Специфичные вопросы о Blackbox Exporter к собеседованию**

1. **Как Blackbox Exporter выполняет проверку доступности HTTP-сервисов?**  
   Blackbox Exporter отправляет HTTP-запросы к целевому сервису и собирает метрики, такие как статус ответа, время выполнения и SSL/TLS-сертификаты.

2. **Как настроить проверку HTTPS-сервисов с валидацией SSL/TLS-сертификатов?**  
   Настройте модуль `http_2xx` с параметром `fail_if_ssl` или `fail_if_not_ssl` в файле `blackbox.yml`. Пример:  
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

3. **Как проверить задержку DNS-запросов с помощью Blackbox Exporter?**  
   Используйте модуль `dns`. Пример конфигурации:  
   ```yaml
   modules:
     dns:
       prober: dns
       timeout: 5s
       dns:
         query_name: "example.com"
   ```

4. **Как настроить ICMP-проверки (ping) в Blackbox Exporter?**  
   Используйте модуль `icmp`. Пример конфигурации:  
   ```yaml
   modules:
     icmp:
       prober: icmp
       timeout: 5s
       icmp:
         preferred_ip_protocol: "ip4"
   ```

5. **Как настроить TCP-проверки портов в Blackbox Exporter?**  
   Используйте модуль `tcp`. Пример конфигурации:  
   ```yaml
   modules:
     tcp_connect:
       prober: tcp
       timeout: 5s
       tcp:
         port: 8080
   ```

6. **Как использовать метрики `probe_success` и `probe_duration_seconds`?**  
   - `probe_success`: Показывает успешность проверки (1 — успех, 0 — неудача).  
   - `probe_duration_seconds`: Показывает время выполнения проверки.

7. **Как настроить проверку сертификатов SSL/TLS?**  
   Настройте модуль `http_2xx` с параметром `tls_config`. Пример:  
   ```yaml
   modules:
     http_2xx:
       prober: http
       timeout: 5s
       http:
         tls_config:
           insecure_skip_verify: false
   ```

8. **Как проверить, что Blackbox Exporter корректно работает с Prometheus?**  
   Откройте endpoint `/probe` в браузере или используйте `curl`:  
   ```
   http://<blackbox-exporter-ip>:9115/probe?target=<service-url>&module=http_2xx
   ```

9. **Как настроить автоматическое обнаружение сервисов для Blackbox Exporter в Prometheus?**  
   Настройте Service Discovery в `prometheus.yml`:  
   ```yaml
   scrape_configs:
     - job_name: 'blackbox'
       metrics_path: /probe
       params:
         module: [http_2xx]
       static_configs:
         - targets:
             - https://example.com
       relabel_configs:
         - source_labels: [__address__]
           target_label: __param_target
         - source_labels: [__param_target]
           target_label: instance
         - target_label: __address__
           replacement: <blackbox-exporter-ip>:9115
   ```

10. **Как настроить проверку нескольких сервисов с разными модулями?**  
    Настройте несколько job-ов в `prometheus.yml`, указав разные модули. Пример:  
    ```yaml
    scrape_configs:
      - job_name: 'http-services'
        metrics_path: /probe
        params:
          module: [http_2xx]
        static_configs:
          - targets:
              - https://example.com
      - job_name: 'tcp-services'
        metrics_path: /probe
        params:
          module: [tcp_connect]
        static_configs:
          - targets:
              - example.com:8080
    ```

11. **Как настроить проверку времени отклика HTTP-запросов?**  
    Используйте метрику `probe_duration_seconds`. Пример запроса PromQL:  
    ```
    histogram_quantile(0.95, sum(rate(probe_duration_seconds_bucket[5m])) by (le))
    ```

12. **Как настроить проверку DNS-рекурсии?**  
    Настройте модуль `dns` с параметром `query_type`. Пример:  
    ```yaml
    modules:
      dns_recursion:
        prober: dns
        timeout: 5s
        dns:
          query_name: "example.com"
          query_type: "A"
    ```

13. **Как настроить проверку IPv6-адресов в ICMP-модуле?**  
    Укажите параметр `preferred_ip_protocol` как `ip6`. Пример:  
    ```yaml
    modules:
      icmp_ipv6:
        prober: icmp
        timeout: 5s
        icmp:
          preferred_ip_protocol: "ip6"
    ```

14. **Как настроить проверку редиректов в HTTP-модуле?**  
    Настройте параметр `valid_status_codes` и `no_follow_redirects`. Пример:  
    ```yaml
    modules:
      http_redirect:
        prober: http
        timeout: 5s
        http:
          no_follow_redirects: false
          valid_status_codes: [301, 302]
    ```

15. **Как настроить логирование для Blackbox Exporter?**  
    Используйте параметр `--log.level` при запуске Blackbox Exporter. Пример:  
    ```bash
    ./blackbox_exporter --log.level=debug
    ```

16. **Как мониторить сам Blackbox Exporter?**  
    Используйте встроенные метрики Blackbox Exporter (например, `probe_success`) → Интегрируйте их с Prometheus.

17. **Как настроить проверку заголовков HTTP-ответов?**  
    Настройте параметр `headers`. Пример:  
    ```yaml
    modules:
      http_headers:
        prober: http
        timeout: 5s
        http:
          headers:
            Authorization: "Bearer token"
    ```

18. **Как настроить проверку таймаутов HTTP-запросов?**  
    Укажите параметр `timeout` в модуле `http`. Пример:  
    ```yaml
    modules:
      http_timeout:
        prober: http
        timeout: 2s
    ```

19. **Как настроить проверку больших файлов через HTTP?**  
    Настройте параметр `body_size_limit`. Пример:  
    ```yaml
    modules:
      http_large_files:
        prober: http
        timeout: 10s
        http:
          body_size_limit: 10MB
    ```

20. **Как настроить проверку HTTP-методов, отличных от GET?**  
    Настройте параметр `method`. Пример:  
    ```yaml
    modules:
      http_post:
        prober: http
        timeout: 5s
        http:
          method: POST
    ```

21. **Как настроить проверку DNS-серверов с использованием TCP?**  
    Укажите параметр `transport_protocol` как `tcp`. Пример:  
    ```yaml
    modules:
      dns_tcp:
        prober: dns
        timeout: 5s
        dns:
          transport_protocol: "tcp"
    ```

22. **Как настроить проверку нескольких DNS-записей одновременно?**  
    Настройте параметр `queries`. Пример:  
    ```yaml
    modules:
      dns_multiple:
        prober: dns
        timeout: 5s
        dns:
          queries:
            - query_name: "example.com"
              query_type: "A"
            - query_name: "example.org"
              query_type: "MX"
    ```

23. **Как настроить проверку HTTP-сервисов с аутентификацией?**  
    Настройте параметр `basic_auth`. Пример:  
    ```yaml
    modules:
      http_auth:
        prober: http
        timeout: 5s
        http:
          basic_auth:
            username: "user"
            password: "password"
    ```

24. **Как настроить проверку HTTP-сервисов с использованием прокси?**  
    Настройте параметр `proxy_url`. Пример:  
    ```yaml
    modules:
      http_proxy:
        prober: http
        timeout: 5s
        http:
          proxy_url: "http://proxy.example.com:8080"
    ```

25. **Как настроить проверку HTTP-сервисов с использованием клиентских сертификатов?**  
    Настройте параметр `tls_config` с параметрами `cert_file` и `key_file`. Пример:  
    ```yaml
    modules:
      http_client_cert:
        prober: http
        timeout: 5s
        http:
          tls_config:
            cert_file: "/path/to/client.crt"
            key_file: "/path/to/client.key"
    ```
