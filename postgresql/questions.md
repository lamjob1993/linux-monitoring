### **Базовые вопросы к собеседованию**

1. **Что такое PostgreSQL Exporter? Для чего он используется?**  
   PostgreSQL Exporter — это экспортер метрик для Prometheus, предназначенный для сбора данных о состоянии и производительности базы данных PostgreSQL. Он используется для мониторинга PostgreSQL в реальном времени.

2. **Какие типы метрик собирает PostgreSQL Exporter?**  
   - **Производительность**: количество запросов, время выполнения запросов.  
   - **Состояние базы данных**: размер таблиц, индексов, состояние репликации.  
   - **Ресурсы**: использование памяти, блокировок, подключений.  
   - **Ошибки**: количество ошибок, таймаутов.  

3. **Как установить PostgreSQL Exporter?**  
   Используйте Docker (`docker run wrouesnel/postgres_exporter`), скачайте бинарный файл с официального сайта или установите через пакетный менеджер (например, `apt` или `yum`).

4. **Как настроить PostgreSQL Exporter для работы с Prometheus?**  
   Установите PostgreSQL Exporter → Настройте его endpoint в `prometheus.yml`:  
   ```yaml
   scrape_configs:
     - job_name: 'postgres'
       static_configs:
         - targets: ['<exporter-ip>:9187']
   ```

5. **На каком порту работает PostgreSQL Exporter по умолчанию?**  
   По умолчанию PostgreSQL Exporter работает на порту **9187**.

6. **Как проверить, что PostgreSQL Exporter корректно собирает метрики?**  
   Откройте браузер или используйте `curl` для запроса метрик:  
   ```
   http://<exporter-ip>:9187/metrics
   ```
   Если метрики отображаются, всё настроено правильно.

---

### **Настройка и конфигурирование**

7. **Как запустить PostgreSQL Exporter в фоновом режиме?**  
   Используйте systemd для управления PostgreSQL Exporter:  
   Создайте файл `/etc/systemd/system/postgres_exporter.service` с содержимым:  
   ```ini
   [Unit]
   Description=PostgreSQL Exporter

   [Service]
   ExecStart=/usr/local/bin/postgres_exporter --config.file=/etc/postgres_exporter/config.yml

   [Install]
   WantedBy=multi-user.target
   ```
   Запустите службу:  
   ```bash
   systemctl start postgres_exporter
   systemctl enable postgres_exporter
   ```

8. **Как изменить порт PostgreSQL Exporter?**  
   Запустите PostgreSQL Exporter с флагом `--web.listen-address`:  
   ```bash
   ./postgres_exporter --web.listen-address=":9200"
   ```

9. **Как настроить подключение к PostgreSQL в PostgreSQL Exporter?**  
   Укажите параметры подключения через переменные окружения или файл конфигурации. Пример:  
   ```bash
   export DATA_SOURCE_NAME="postgresql://username:password@localhost:5432/database?sslmode=disable"
   ```

10. **Как ограничить доступ к метрикам PostgreSQL Exporter?**  
    Настройте firewall или reverse proxy (например, Nginx) для ограничения доступа к порту 9187.

---

### **Метрики и их анализ**

11. **Какие основные метрики предоставляет PostgreSQL Exporter?**  
    Основные метрики:  
    - `pg_stat_database_*`: Статистика базы данных (например, количество запросов).  
    - `pg_stat_activity_*`: Информация о текущих подключениях.  
    - `pg_locks_*`: Количество блокировок.  
    - `pg_replication_*`: Состояние репликации.  

12. **Как использовать метрики производительности из PostgreSQL Exporter?**  
    Метрика `pg_stat_database_tup_fetched` показывает количество выбранных строк. Пример запроса PromQL:  
    ```
    rate(pg_stat_database_tup_fetched[5m])
    ```

13. **Как отслеживать количество активных подключений?**  
    Используйте метрику `pg_stat_activity_count`. Пример запроса PromQL:  
    ```
    sum(pg_stat_activity_count)
    ```

14. **Как мониторить репликацию в PostgreSQL?**  
    Используйте метрики:  
    - `pg_replication_lag`: Задержка репликации.  
    - `pg_replication_is_replica`: Статус реплики.  

15. **Как отслеживать использование дискового пространства?**  
    Используйте метрики:  
    - `pg_database_size_bytes`: Размер базы данных.  
    - `pg_table_size_bytes`: Размер таблиц.  

---

### **Интеграция с Prometheus**

16. **Как настроить автоматическое обнаружение баз данных в Prometheus?**  
    Настройте Service Discovery в `prometheus.yml`:  
    ```yaml
    scrape_configs:
      - job_name: 'postgres'
        static_configs:
          - targets:
              - <exporter-ip>:9187
    ```

17. **Как использовать PostgreSQL Exporter в Kubernetes?**  
    Разверните PostgreSQL Exporter как Deployment в Kubernetes → Настройте Service Discovery в Prometheus.

18. **Как интегрировать PostgreSQL Exporter с Grafana?**  
    Добавьте Prometheus как источник данных в Grafana → Используйте метрики PostgreSQL Exporter для создания дашбордов.

19. **Какие готовые дашборды для PostgreSQL Exporter доступны в Grafana?**  
    В Grafana есть популярные дашборды, например:  
    - "PostgreSQL Overview" (ID: 9628).  

20. **Как настроить алерты для метрик PostgreSQL Exporter?**  
    Создайте правила алертов в Prometheus. Пример:  
    ```yaml
    groups:
      - name: postgres_alerts
        rules:
          - alert: HighConnectionCount
            expr: pg_stat_activity_count > 100
            for: 5m
            labels:
              severity: warning
            annotations:
              summary: "High connection count on {{ $labels.instance }}"
    ```

---

### **Продвинутые вопросы**

21. **Как расширить функциональность PostgreSQL Exporter?**  
    Настройте пользовательские SQL-запросы для сбора дополнительных метрик → Используйте параметр `--extend.query-path`.

22. **Как мониторить блокировки в PostgreSQL?**  
    Используйте метрики `pg_locks_*`. Пример запроса PromQL:  
    ```
    sum(pg_locks_waiting)
    ```

23. **Как мониторить задержки репликации?**  
    Используйте метрику `pg_replication_lag`. Пример запроса PromQL:  
    ```
    max(pg_replication_lag)
    ```

24. **Как использовать PostgreSQL Exporter для мониторинга нескольких баз данных?**  
    Настройте несколько экземпляров PostgreSQL Exporter → Укажите разные параметры подключения для каждой базы данных.

25. **Как настроить централизованное логирование для PostgreSQL Exporter?**  
    Настройте интеграцию с Loki для анализа логов → Используйте метрики PostgreSQL Exporter для корреляции с логами.

---

Теперь у вас есть полный список вопросов и ответов по **PostgreSQL Exporter**. Это поможет вам подготовиться к собеседованию или лучше понять работу этого инструмента. Если нужно углубиться в какой-то раздел, дайте знать!
