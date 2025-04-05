# **Технические вопросы о Prometheus к собеседованию**

### **1. Как установить Prometheus?**
**Ответ:**  
Скачайте бинарный файл с GitHub и запустите его:  
```bash
wget https://github.com/prometheus/prometheus/releases/download/v2.45.0/prometheus-2.45.0.linux-amd64.tar.gz
tar xvfz prometheus-2.45.0.linux-amd64.tar.gz
./prometheus --config.file=/etc/prometheus/prometheus.yml
```

---

### **2. Как проверить работу Prometheus?**
**Ответ:**  
Используйте API или веб-интерфейс:  
```bash
curl http://localhost:9090/api/v1/status/config
```
или откройте в браузере:  
`http://localhost:9090`.

---

### **3. Как настроить автозапуск Prometheus через systemd?**
**Ответ:**  
Создайте unit-файл:  
```ini
[Unit]
Description=Prometheus

[Service]
ExecStart=/usr/local/bin/prometheus --config.file=/etc/prometheus/prometheus.yml

[Install]
WantedBy=multi-user.target
```
Запустите службу:  
```bash
sudo systemctl start prometheus
sudo systemctl enable prometheus
```

---

### **4. Как настроить сбор метрик в Prometheus?**
**Ответ:**  
Настройте `scrape_configs` в `prometheus.yml`:  
```yaml
scrape_configs:
  - job_name: 'node'
    static_configs:
      - targets: ['localhost:9100']
```

---

### **5. Как создать алерт в Prometheus?**
**Ответ:**  
Добавьте правило в файл алертов (например, `alerts.yml`):  
```yaml
groups:
  - name: example_alerts
    rules:
      - alert: HighCpuUsage
        expr: 100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 85
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High CPU usage on {{ $labels.instance }}"
          description: "CPU usage is above 85% for more than 5 minutes."
```

---

### **6. Как интегрировать Prometheus с Alertmanager?**
**Ответ:**  
Настройте конфигурацию в `prometheus.yml`:  
```yaml
alerting:
  alertmanagers:
    - static_configs:
        - targets: ['localhost:9093']
```

---

### **7. Как фильтровать метрики в Prometheus?**
**Ответ:**  
Используйте `relabel_configs` в `prometheus.yml`:  
```yaml
scrape_configs:
  - job_name: 'filter_metrics'
    static_configs:
      - targets: ['localhost:9100']
    metric_relabel_configs:
      - source_labels: [__name__]
        regex: "cpu_usage.*"
        action: keep
```

---

### **8. Как использовать PromQL для анализа данных?**
**Ответ:**  
Примеры запросов:
- Среднее значение CPU за последние 5 минут:  
  ```promql
  avg(rate(node_cpu_seconds_total[5m]))
  ```
- Количество HTTP-запросов с кодом 5xx:  
  ```promql
  sum(rate(http_requests_total{status=~"5.."}[5m]))
  ```

---

### **9. Как настроить retention period в Prometheus?**
**Ответ:**  
Укажите параметр `retention` в командной строке:  
```bash
./prometheus --storage.tsdb.retention.time=15d
```
или добавьте в `prometheus.yml`:  
```yaml
storage:
  tsdb:
    retention: 15d
```

---

### **10. Как ограничить доступ к Prometheus?**
**Ответ:**  
Ограничьте доступ через firewall или настройте reverse proxy (Nginx) с аутентификацией:  
```nginx
server {
    listen 9090;
    location / {
        auth_basic "Restricted Access";
        auth_basic_user_file /etc/nginx/.htpasswd;
        proxy_pass http://localhost:9090;
    }
}
```

---

### **11. Как мониторить контейнеры с помощью Prometheus?**
**Ответ:**  
Используйте cAdvisor или kube-state-metrics:  
```yaml
scrape_configs:
  - job_name: 'cadvisor'
    static_configs:
      - targets: ['localhost:8080']
```

---

### **12. Как решить проблему с большим количеством метрик?**
**Ответ:**  
1. Отключите ненужные метрики через `metric_relabel_configs`.  
2. Уменьшите частоту сбора данных (`scrape_interval`).  
3. Используйте агрегацию в PromQL.

---

### **13. Как автоматизировать установку Prometheus?**
**Ответ:**  
Используйте Ansible или Docker. Пример Dockerfile:  
```dockerfile
FROM prom/prometheus:v2.45.0
COPY prometheus.yml /etc/prometheus/prometheus.yml
CMD ["--config.file=/etc/prometheus/prometheus.yml"]
```

---

### **14. Как мониторить бизнес-метрики с помощью Prometheus?**
**Ответ:**  
Используйте Custom Exporter для сбора бизнес-метрик (например, количество заказов):  
```yaml
scrape_configs:
  - job_name: 'business_metrics'
    static_configs:
      - targets: ['localhost:9101']
```

---

### **15. Как отладить проблемы с Prometheus?**
**Ответ:**  
1. Проверьте логи Prometheus:  
   ```bash
   journalctl -u prometheus.service -f
   ```
2. Проверьте конфигурацию:  
   ```bash
   ./promtool check config /etc/prometheus/prometheus.yml
   ```
3. Проверьте метрики через `/metrics` или API.
