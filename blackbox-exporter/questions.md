### **Базовые вопросы к собеседованию**

1. **Что такое Blackbox Exporter? Для чего он используется?**  
   Blackbox Exporter — это экспортер метрик для Prometheus, предназначенный для проверки доступности и работоспособности сетевых сервисов (HTTP, HTTPS, TCP, DNS, ICMP). Он используется для внешнего мониторинга и проверки состояния сервисов.

2. **Какие типы проверок поддерживает Blackbox Exporter?**  
   - **HTTP/HTTPS**: Проверка доступности веб-сайтов и API.  
   - **TCP**: Проверка открытых портов и соединений.  
   - **DNS**: Проверка разрешения доменных имён.  
   - **ICMP**: Проверка доступности хостов через ping.  

3. **Как установить Blackbox Exporter?**  
   Используйте Docker (`docker run prom/blackbox-exporter`), скачайте бинарный файл с официального сайта или установите через пакетный менеджер (например, `apt` или `yum`).

4. **Как настроить Blackbox Exporter для работы с Prometheus?**  
   Установите Blackbox Exporter → Настройте его endpoint в `prometheus.yml`:  
   ```yaml
   scrape_configs:
     - job_name: 'blackbox'
       metrics_path: /probe
       params:
         module: [http_2xx]  # Тип проверки (например, HTTP)
       static_configs:
         - targets:
             - https://example.com  # Целевой сервис
       relabel_configs:
         - source_labels: [__address__]
           target_label: __param_target
         - source_labels: [__param_target]
           target_label: instance
         - target_label: __address__
           replacement: <blackbox-exporter-ip>:9115  # Адрес Blackbox Exporter
   ```

5. **На каком порту работает Blackbox Exporter по умолчанию?**  
   По умолчанию Blackbox Exporter работает на порту **9115**.

6. **Как проверить, что Blackbox Exporter корректно собирает метрики?**  
   Откройте браузер или используйте `curl` для запроса метрик:  
   ```
   http://<blackbox-exporter-ip>:9115/probe?target=<service-url>&module=http_2xx
   ```
   Если метрики отображаются, всё настроено правильно.

---

### **Настройка и конфигурирование**

7. **Как запустить Blackbox Exporter в фоновом режиме?**  
   Используйте systemd для управления Blackbox Exporter:  
   Создайте файл `/etc/systemd/system/blackbox_exporter.service` с содержимым:  
   ```ini
   [Unit]
   Description=Blackbox Exporter

   [Service]
   ExecStart=/usr/local/bin/blackbox_exporter --config.file=/etc/blackbox_exporter/blackbox.yml

   [Install]
   WantedBy=multi-user.target
   ```
   Запустите службу:  
   ```bash
   systemctl start blackbox_exporter
   systemctl enable blackbox_exporter
   ```

8. **Как изменить порт Blackbox Exporter?**  
   Запустите Blackbox Exporter с флагом `--web.listen-address`:  
   ```bash
   ./blackbox_exporter --web.listen-address=":9200"
   ```

9. **Как настроить модули в Blackbox Exporter?**  
   Настройте файл `blackbox.yml` с описанием модулей. Пример:  
   ```yaml
   modules:
     http_2xx:
       prober: http
       timeout: 5s
       http:
         valid_http_versions: ["HTTP/1.1", "HTTP/2"]
         valid_status_codes: []  # Пустой массив означает успешные коды (2xx)
         fail_if_ssl: false
         fail_if_not_ssl: false
   ```

10. **Как ограничить доступ к метрикам Blackbox Exporter?**  
    Настройте firewall или reverse proxy (например, Nginx) для ограничения доступа к порту 9115.

---

### **Метрики и их анализ**

11. **Какие метрики предоставляет Blackbox Exporter?**  
    Основные метрики:  
    - `probe_success`: 1 — проверка успешна, 0 — неудача.  
    - `probe_duration_seconds`: Время выполнения проверки.  
    - `probe_http_status_code`: HTTP-статус ответа.  
    - `probe_dns_lookup_time_seconds`: Время разрешения DNS.  

12. **Как использовать метрики HTTP из Blackbox Exporter?**  
    Метрика `probe_http_status_code` показывает HTTP-статус ответа. Пример запроса PromQL:  
    ```
    probe_success{job="blackbox", instance="https://example.com"}
    ```

13. **Как отслеживать время выполнения HTTP-запросов?**  
    Используйте метрику `probe_duration_seconds`. Пример запроса PromQL:  
    ```
    histogram_quantile(0.95, sum(rate(probe_duration_seconds_bucket[5m])) by (le))
    ```

14. **Как мониторить доступность DNS-серверов?**  
    Используйте метрики:  
    - `probe_success` — успех проверки.  
    - `probe_dns_lookup_time_seconds` — время разрешения DNS.  

15. **Как отслеживать доступность хостов через ICMP?**  
    Используйте метрики:  
    - `probe_success` — успех проверки.  
    - `probe_icmp_duration_seconds` — время ответа ICMP.  

---

### **Интеграция с Prometheus**

16. **Как настроить автоматическое обнаружение сервисов в Prometheus?**  
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

17. **Как использовать Blackbox Exporter в Kubernetes?**  
    Разверните Blackbox Exporter как Deployment в Kubernetes → Настройте Service Discovery в Prometheus.

18. **Как интегрировать Blackbox Exporter с Grafana?**  
    Добавьте Prometheus как источник данных в Grafana → Используйте метрики Blackbox Exporter для создания дашбордов.

19. **Какие готовые дашборды для Blackbox Exporter доступны в Grafana?**  
    В Grafana есть популярные дашборды, например:  
    - "Blackbox Exporter" (ID: 7587).  

20. **Как настроить алерты для метрик Blackbox Exporter?**  
    Создайте правила алертов в Prometheus. Пример:  
    ```yaml
    groups:
      - name: blackbox_alerts
        rules:
          - alert: ServiceDown
            expr: probe_success == 0
            for: 5m
            labels:
              severity: critical
            annotations:
              summary: "Service {{ $labels.instance }} is down"
    ```

---

### **Продвинутые вопросы**

21. **Как расширить функциональность Blackbox Exporter?**  
    Настройте дополнительные модули в `blackbox.yml` или используйте сторонние инструменты для генерации метрик.

22. **Как мониторить SSL/TLS-сертификаты с помощью Blackbox Exporter?**  
    Используйте модуль `http_2xx` с параметром `fail_if_ssl` → Настройте проверку срока действия сертификата.

23. **Как мониторить задержки DNS-запросов?**  
    Используйте метрику `probe_dns_lookup_time_seconds`. Пример запроса PromQL:  
    ```
    rate(probe_dns_lookup_time_seconds_sum[5m]) / rate(probe_dns_lookup_time_seconds_count[5m])
    ```

24. **Как использовать Blackbox Exporter для мониторинга виртуальных машин?**  
    Настройте ICMP-проверки для мониторинга доступности VM → Интегрируйте с Prometheus.

25. **Как настроить централизованное логирование для Blackbox Exporter?**  
    Настройте интеграцию с Loki для анализа логов → Используйте метрики Blackbox Exporter для корреляции с логами.
