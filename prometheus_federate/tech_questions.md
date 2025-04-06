# **Технические вопросы по Prometheus Federation к собеседованию**

### **1. Что такое Prometheus Federation?**
**Ответ:**  
"Prometheus Federation — это механизм, который позволяет одному экземпляру Prometheus собирать метрики с других экземпляров Prometheus. Это полезно для централизации данных из разных источников (например, дата-центров или команд) и создания единого обзора всей инфраструктуры."

---

### **2. Как настроить Prometheus Federation?**
**Ответ:**  
Настройте `scrape_configs` в `prometheus.yml`:  
```yaml
scrape_configs:
  - job_name: 'federate'
    honor_labels: true
    metrics_path: '/federate'
    params:
      match[]:
        - '{job="node"}'
        - '{__name__=~"up|process_cpu_seconds_total"}'
    static_configs:
      - targets:
          - 'prometheus-dc1:9090'
          - 'prometheus-dc2:9090'
```
- `honor_labels: true` сохраняет оригинальные метки метрик.
- `match[]` фильтрует метрики, которые нужно собрать.

---

### **3. Как проверить работу Federation?**
**Ответ:**  
Используйте `curl`, чтобы получить метрики через `/federate`:  
```bash
curl http://prometheus-federation:9090/federate -G --data-urlencode 'match[]={job="node"}'
```

---

### **4. Какие метрики можно собирать через Federation?**
**Ответ:**  
Можно собирать любые метрики, доступные на целевых экземплярах Prometheus. Например:
- `up` — статус доступности экземпляров.
- `node_cpu_seconds_total` — использование CPU.
- `http_requests_total` — количество HTTP-запросов.

---

### **5. Как фильтровать метрики при использовании Federation?**
**Ответ:**  
Используйте параметр `match[]` в конфигурации:  
```yaml
params:
  match[]:
    - '{job="node"}'
    - '{__name__=~"up|process_cpu_seconds_total"}'
```
Это позволит собирать только нужные метрики, что снижает нагрузку на сеть и хранилище.

---

### **6. Как решать проблемы с производительностью при использовании Federation?**
**Ответ:**  
1. Фильтруйте только необходимые метрики через `match[]`.  
2. Уменьшайте частоту сбора данных (`scrape_interval`).  
3. Используйте агрегацию данных в PromQL для снижения объема информации.

---

### **7. Как обеспечить отказоустойчивость Federation?**
**Ответ:**  
1. Разместите центральный Prometheus на высокодоступной платформе (например, Kubernetes).  
2. Настройте несколько резервных экземпляров для перехвата данных в случае сбоя.  
3. Используйте внешнее хранилище (например, Thanos или Cortex) для долгосрочного хранения данных.

---

### **8. Как ограничить доступ к Federation?**
**Ответ:**  
Ограничьте доступ через firewall или настройте reverse proxy (Nginx) с аутентификацией:  
```nginx
server {
    listen 9090;
    location /federate {
        auth_basic "Restricted Access";
        auth_basic_user_file /etc/nginx/.htpasswd;
        proxy_pass http://localhost:9090;
    }
}
```

---

### **9. Как масштабировать мониторинг с помощью Federation?**
**Ответ:**  
1. Настройте отдельные экземпляры Prometheus для каждой команды или дата-центра.  
2. Используйте Federation для объединения данных на центральном Prometheus.  
3. Интегрируйте Grafana для создания единого дашборда.

---

### **10. Как использовать Federation для мониторинга микросервисов?**
**Ответ:**  
Настройте Federation для сбора метрик с каждого микросервиса:  
```yaml
scrape_configs:
  - job_name: 'federate'
    honor_labels: true
    metrics_path: '/federate'
    params:
      match[]:
        - '{job="service-a"}'
        - '{job="service-b"}'
    static_configs:
      - targets:
          - 'prometheus-service-a:9090'
          - 'prometheus-service-b:9090'
```

---

### **11. Как настроить долгосрочное хранение данных в Federation?**
**Ответ:**  
Используйте внешние решения, такие как:
- **Thanos:** для глобального запроса и долгосрочного хранения.  
- **Cortex:** для централизованного хранения и масштабирования.  

Пример настройки Thanos:  
```yaml
thanos:
  sidecar:
    prometheus_url: "http://localhost:9090"
```

---

### **12. Как отладить проблемы с Federation?**
**Ответ:**  
1. Проверьте логи Prometheus:  
   ```bash
   journalctl -u prometheus.service -f
   ```
2. Проверьте доступность целевых экземпляров через `/targets`.  
3. Используйте `curl` для проверки работы `/federate`.

---

### **13. Как автоматизировать настройку Federation?**
**Ответ:**  
Используйте Ansible или Terraform. Пример Ansible playbook:  
```yaml
- name: Configure Prometheus Federation
  copy:
    dest: /etc/prometheus/prometheus.yml
    content: |
      scrape_configs:
        - job_name: 'federate'
          honor_labels: true
          metrics_path: '/federate'
          params:
            match[]:
              - '{job="node"}'
          static_configs:
            - targets:
                - 'prometheus-dc1:9090'
```

---

### **14. Как использовать Federation для мониторинга бизнес-метрик?**
**Ответ:**  
Настройте Federation для сбора ключевых бизнес-метрик:  
```yaml
scrape_configs:
  - job_name: 'federate'
    honor_labels: true
    metrics_path: '/federate'
    params:
      match[]:
        - '{job="business-metrics"}'
    static_configs:
      - targets:
          - 'prometheus-team1:9090'
          - 'prometheus-team2:9090'
```

---

### **15. Какие ограничения у Prometheus Federation?**
**Ответ:**  
1. Federation не подходит для очень больших систем с огромным количеством метрик.  
2. Federation может создавать дополнительную нагрузку на сеть и хранилище.  
3. Для долгосрочного хранения лучше использовать Thanos или Cortex.
