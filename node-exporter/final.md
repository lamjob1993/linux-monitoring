### **Базовые вопросы к собеседованию**

1. **Что такое Node Exporter? Для чего он используется?**  
   Node Exporter — это экспортер метрик для Prometheus, предназначенный для сбора системных метрик серверов (CPU, память, диск, сеть и т.д.). Он используется для мониторинга состояния серверов.

2. **Какие типы метрик собирает Node Exporter?**  
   - **Процессор**: `node_cpu_seconds_total`, загрузка CPU.  
   - **Память**: `node_memory_MemTotal_bytes`, `node_memory_MemFree_bytes`.  
   - **Диски**: `node_disk_io_time_seconds_total`, использование дисков.  
   - **Сеть**: `node_network_receive_bytes_total`, трафик сети.  
   - **Файловая система**: `node_filesystem_size_bytes`, использование файловых систем.

3. **Как установить Node Exporter?**  
   Используйте Docker (`docker run prom/node-exporter`), скачайте бинарный файл с официального сайта или установите через пакетный менеджер (например, `apt` или `yum`).

4. **Как настроить Node Exporter для работы с Prometheus?**  
   Установите Node Exporter → Настройте его endpoint в `prometheus.yml`:  
   ```yaml
   scrape_configs:
     - job_name: 'node'
       static_configs:
         - targets: ['<server-ip>:9100']
   ```

5. **На каком порту работает Node Exporter по умолчанию?**  
   По умолчанию Node Exporter работает на порту **9100**.

6. **Как проверить, что Node Exporter корректно собирает метрики?**  
   Откройте браузер или используйте `curl` для запроса метрик:  
   ```
   http://<server-ip>:9100/metrics
   ```
   Если метрики отображаются, всё настроено правильно.

---

### **Настройка и конфигурирование**

7. **Как запустить Node Exporter в фоновом режиме?**  
   Используйте systemd для управления Node Exporter:  
   Создайте файл `/etc/systemd/system/node_exporter.service` с содержимым:  
   ```ini
   [Unit]
   Description=Node Exporter

   [Service]
   ExecStart=/usr/local/bin/node_exporter

   [Install]
   WantedBy=multi-user.target
   ```
   Запустите службу:  
   ```bash
   systemctl start node_exporter
   systemctl enable node_exporter
   ```

8. **Как изменить порт Node Exporter?**  
   Запустите Node Exporter с флагом `--web.listen-address`:  
   ```bash
   ./node_exporter --web.listen-address=":9200"
   ```

9. **Как ограничить доступ к метрикам Node Exporter?**  
   Настройте firewall или reverse proxy (например, Nginx) для ограничения доступа к порту 9100.

10. **Как добавить пользовательскую метрику в Node Exporter?**  
    Node Exporter поддерживает текстовые файлы с метриками. Используйте флаг `--collector.textfile.directory` для указания директории с файлами метрик в формате Prometheus.

---

### **Метрики и их анализ**

11. **Как использовать метрики CPU из Node Exporter?**  
    Метрика `node_cpu_seconds_total` показывает время, затраченное CPU на различные задачи (user, system, idle). Пример запроса PromQL:  
    ```
    rate(node_cpu_seconds_total{mode="idle"}[5m])
    ```

12. **Как отслеживать использование памяти с помощью Node Exporter?**  
    Используйте метрики:  
    - `node_memory_MemTotal_bytes` — общий объём памяти.  
    - `node_memory_MemFree_bytes` — свободная память.  
    Пример запроса PromQL:  
    ```
    (node_memory_MemTotal_bytes - node_memory_MemFree_bytes) / node_memory_MemTotal_bytes * 100
    ```

13. **Как мониторить использование дискового пространства?**  
    Используйте метрики:  
    - `node_filesystem_size_bytes` — общий размер файловой системы.  
    - `node_filesystem_free_bytes` — свободное место.  
    Пример запроса PromQL:  
    ```
    (node_filesystem_size_bytes - node_filesystem_free_bytes) / node_filesystem_size_bytes * 100
    ```

14. **Как отслеживать сетевой трафик с помощью Node Exporter?**  
    Используйте метрики:  
    - `node_network_receive_bytes_total` — полученные байты.  
    - `node_network_transmit_bytes_total` — отправленные байты.  
    Пример запроса PromQL:  
    ```
    rate(node_network_receive_bytes_total[5m])
    ```

15. **Как мониторить нагрузку на процессор (load average)?**  
    Используйте метрику `node_load1`, `node_load5`, `node_load15`. Пример запроса PromQL:  
    ```
    node_load1
    ```

---

### **Интеграция с Prometheus**

16. **Как настроить автоматическое обнаружение серверов в Prometheus?**  
    Настройте Service Discovery в `prometheus.yml`:  
    ```yaml
    scrape_configs:
      - job_name: 'node'
        static_configs:
          - targets: ['server1:9100', 'server2:9100']
    ```

17. **Как использовать Node Exporter в Kubernetes?**  
    Разверните Node Exporter как DaemonSet в Kubernetes → Настройте Service Discovery в Prometheus.

18. **Как интегрировать Node Exporter с Grafana?**  
    Добавьте Prometheus как источник данных в Grafana → Используйте метрики Node Exporter для создания дашбордов.

19. **Какие готовые дашборды для Node Exporter доступны в Grafana?**  
    В Grafana есть популярные дашборды, например:  
    - "Node Exporter Full" (ID: 1860).  
    - "Node Exporter Server Metrics" (ID: 405).

20. **Как настроить алерты для метрик Node Exporter?**  
    Создайте правила алертов в Prometheus. Пример:  
    ```yaml
    groups:
      - name: node_alerts
        rules:
          - alert: HighCPUUsage
            expr: 100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
            for: 5m
            labels:
              severity: critical
            annotations:
              summary: "High CPU usage on {{ $labels.instance }}"
    ```

---

### **Продвинутые вопросы**

21. **Как расширить функциональность Node Exporter?**  
    Используйте сторонние коллекции метрик (например, `textfile` collector) или создайте собственные скрипты для генерации метрик.

22. **Как мониторить температуру сервера с помощью Node Exporter?**  
    Убедитесь, что `textfile` collector включен → Напишите скрипт для сбора данных о температуре → Поместите данные в файл метрик.

23. **Как мониторить RAID-массивы с помощью Node Exporter?**  
    Используйте сторонние инструменты (например, `megacli`) для сбора данных о RAID → Интегрируйте их с `textfile` collector.

24. **Как использовать Node Exporter для мониторинга виртуальных машин?**  
    Установите Node Exporter на каждую виртуальную машину → Настройте Prometheus для сбора метрик.

25. **Как настроить централизованное логирование для Node Exporter?**  
    Настройте интеграцию с Loki для анализа логов → Используйте метрики Node Exporter для корреляции с логами.
