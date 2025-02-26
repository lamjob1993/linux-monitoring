## Targets

Это конечные точки (endpoints), с которых собираются метрики. Prometheus периодически опрашивает эти цели, чтобы получить актуальные данные. Давайте разберем, как работают targets в Prometheus.

---

### 1. **Что такое Target?**
   - Target — это URL (например, `http://localhost:9100/metrics`), который предоставляет метрики в формате Prometheus.
   - Примеры targets:
     - Node Exporter: `http://<IP>:9100/metrics`.
     - Приложение, которое экспортирует метрики: `http://<IP>:8080/metrics`.
     - Экспортеры (например, MySQL Exporter, Redis Exporter).

---

### 2. **Как Prometheus находит Targets?**
   Prometheus использует несколько механизмов для обнаружения целей (targets):

   #### a) **Статическая конфигурация**
   - Цели задаются вручную в файле конфигурации Prometheus (`prometheus.yml`).
   - Пример:
     ```yaml
     scrape_configs:
       - job_name: 'node_exporter'
         static_configs:
           - targets: ['localhost:9100', '192.168.1.2:9100']
     ```
     Здесь Prometheus будет опрашивать два targets: `localhost:9100` и `192.168.1.2:9100`.

   #### b) **Service Discovery (автоматическое обнаружение)**
   - Prometheus поддерживает интеграцию с различными системами для автоматического обнаружения целей.
   - Примеры поддерживаемых Service Discovery:
     - **Kubernetes**: Автоматически обнаруживает Pods, Services, Endpoints.
     - **Consul**: Обнаружение сервисов через Consul.
     - **AWS EC2**: Обнаружение инстансов EC2.
     - **Docker Swarm**: Обнаружение контейнеров.
     - **DNS SRV**: Обнаружение через DNS-записи.
     - **File-based Discovery**: Цели загружаются из файла (например, JSON, YAML).

   Пример конфигурации для Kubernetes:
   ```yaml
   scrape_configs:
     - job_name: 'kubernetes'
       kubernetes_sd_configs:
         - role: pod
       relabel_configs:
         - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
           action: keep
           regex: true
   ```

---

### 3. **Как Prometheus опрашивает Targets?**
   - Prometheus работает по модели **pull-based** (опрашивает таргеты).
   - Процесс:
     1. Prometheus отправляет HTTP-запрос на target (например, `http://<IP>:9100/metrics`).
     2. Target возвращает метрики в формате Prometheus (текстовый формат).
     3. Prometheus сохраняет метрики в своей базе данных (TSDB).

   - **Интервал опроса**:
     - Задается в конфигурации с помощью параметра `scrape_interval`.
     - Пример:
       ```yaml
       scrape_configs:
         - job_name: 'node_exporter'
           scrape_interval: 15s
           static_configs:
             - targets: ['localhost:9100']
       ```

---

### 4. **Лейблы (Labels) для Targets**
   - Каждый target может иметь метки (labels), которые добавляют контекст к метрикам.
   - Лейблы задаются в конфигурации или добавляются автоматически через Service Discovery.
   - Пример:
     ```yaml
     scrape_configs:
       - job_name: 'node_exporter'
         static_configs:
           - targets: ['localhost:9100']
             labels:
               region: 'us-east'
               env: 'production'
     ```
     Метки `region` и `env` будут добавлены ко всем метрикам, собранным с этого target.

---

### 5. **Relabeling (Переопределение меток)**
   - Prometheus позволяет изменять или фильтровать метки с помощью механизма **relabeling**.
   - Это полезно для:
     - Фильтрации целей.
     - Переименования меток.
     - Добавления новых меток на основе существующих.
   - Пример:
     ```yaml
     scrape_configs:
       - job_name: 'node_exporter'
         static_configs:
           - targets: ['localhost:9100']
         relabel_configs:
           - source_labels: [__address__]
             target_label: __param_target
           - source_labels: [__param_target]
             target_label: instance
           - replacement: 'node1'
             target_label: hostname
     ```

---

### 6. **Состояние Targets**
   - Prometheus отслеживает состояние каждого target:
     - **UP**: Target доступен и возвращает метрики.
     - **DOWN**: Target недоступен или возвращает ошибку.
   - Состояние можно проверить через веб-интерфейс Prometheus (http://<prometheus-server>/targets).

---

### 7. **Группировка Targets (Jobs)**
   - Targets группируются в **jobs** (задачи).
   - Каждый job имеет имя (`job_name`) и может содержать несколько targets.
   - Пример:
     ```yaml
     scrape_configs:
       - job_name: 'node_exporter'
         static_configs:
           - targets: ['localhost:9100', '192.168.1.2:9100']
       - job_name: 'app_metrics'
         static_configs:
           - targets: ['app1:8080', 'app2:8080']
     ```

---

### 8. **Пример работы с Targets**
   - Конфигурация:
     ```yaml
     scrape_configs:
       - job_name: 'node_exporter'
         scrape_interval: 15s
         static_configs:
           - targets: ['localhost:9100']
             labels:
               env: 'production'
       - job_name: 'kubernetes_pods'
         kubernetes_sd_configs:
           - role: pod
         relabel_configs:
           - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
             action: keep
             regex: true
     ```
   - Prometheus:
     1. Опрашивает `localhost:9100` каждые 15 секунд.
     2. Автоматически обнаруживает Pods в Kubernetes и собирает метрики с тех, у которых есть аннотация `prometheus.io/scrape: "true"`.

---

### Итог:
- **Targets** — это конечные точки, с которых Prometheus собирает метрики.
- Prometheus поддерживает:
  - Статическую конфигурацию targets.
  - Автоматическое обнаружение через Service Discovery.
- Targets могут иметь метки, которые добавляют контекст к метрикам.
- Состояние targets (UP/DOWN) отслеживается через веб-интерфейс Prometheus.
- Targets группируются в jobs для удобства управления.
