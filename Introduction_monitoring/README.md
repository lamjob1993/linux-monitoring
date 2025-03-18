### 1. Введение в мониторинг  
**Мониторинг** — процесс непрерывного сбора, анализа и визуализации метрик, логов и состояний инфраструктуры, приложений и сервисов.  
**Цели**:  
- Обнаружение аномалий (сбои, деградация производительности).  
- Прогнозирование нагрузки и планирование ресурсов.  
- Обеспечение SLA/SLO (Service Level Agreements/Objectives).  
- Ускорение RCA (Root Cause Analysis).  

---

### 1.1 Сравнение Prometheus и Zabbix  

| **Критерий**          | **Prometheus**                          | **Zabbix**                              |  
|-----------------------|-----------------------------------------|-----------------------------------------|  
| **Архитектура**        | Pull-модель (сервер запрашивает метрики)| Push/Pull (агенты отправляют/сервер запрашивает)|  
| **Протоколы**          | HTTP(S)/PromQL                          | Zabbix-протокол, SNMP, HTTP, JMX        |  
| **Хранение данных**    | Временные ряды (TSDB)                   | Реляционная БД (MySQL, PostgreSQL)      |  
| **Масштабируемость**   | Горизонтальное (Thanos, Cortex)         | Вертикальное + прокси-серверы           |  
| **Обнаружение сервисов**| Динамическое (Kubernetes, Consul)       | Статическое + Zabbix Discovery          |  
| **Экспортеры/Агенты**  | Node Exporter, Blackbox Exporter        | Zabbix Agent, SNMP-агенты               |  
| **Зонтичный мониторинг**| Интеграция с Grafana, Alertmanager      | Встроенные дашборды, триггеры           |  

**Зонтичный мониторинг** — объединение инструментов для комплексного покрытия (напр., Prometheus + ELK для логов + Jaeger для трейсов).  

---

### 2. Grafana  
**Grafana** — платформа визуализации и анализа метрик, логов и трейсов.  
**Пример**:  
- Подключение к Prometheus для отображения CPU-нагрузки серверов.  
- Создание дашбордов с графиками, heatmap-ами и алертами.  

**Роль**:  
- Агрегация данных из разнородных источников (Prometheus, Loki, Elasticsearch).  
- Интерактивное исследование метрик через GUI.  

---

### 2.1 Prometheus  
**Prometheus** — TSDB (Time-Series Database) с pull-моделью сбора данных и языком запросов PromQL.  
**Цели**:  
- Мониторинг состояния сервисов через HTTP-эндпоинты.  
- Автоматическое обнаружение целей (Kubernetes, Consul).  
- Обработка метрик для алертинга (Alertmanager).  

---

### 2.2 Экспортер  
**Экспортер** — промежуточный агент, преобразующий системные/прикладные метрики в формат, совместимый с Prometheus.  
**Пример: Node Exporter**  
- Собирает метрики ОС (CPU, RAM, диск, сеть).  
- Предоставляет их через HTTP-эндпоинт (`/metrics`) на порту 9100.  
- Prometheus парсит их по расписанию (напр., каждые 15 сек).  

---

### 2.3 Sequence Diagram: Grafana + Prometheus + Node Exporter + Alertmanager  
```mermaid  
sequenceDiagram  
    participant NodeExporter  
    participant Prometheus  
    participant Alertmanager  
    participant Grafana  

    Prometheus->>NodeExporter: HTTP GET /metrics (TCP/9100)  
    NodeExporter-->>Prometheus: 200 OK (текст/plain)  
    Prometheus->>Prometheus: Сохранение в TSDB  
    Grafana->>Prometheus: HTTP GET /api/v1/query (PromQL)  
    Prometheus-->>Grafana: JSON-ответ  
    Prometheus->>Alertmanager: HTTP POST /api/v2/alerts (JSON)  
    Alertmanager->>Slack: Отправка алерта (webhook)  
```  

---

### 3. Quadrant Chart: Инфраструктура из 10 ВМ  
```mermaid  
quadrantChart  
    title Мониторинг 10 ВМ через Node Exporter  
    x-axis Сложность реализации  
    y-axis Критичность  

    quadrant-1 Высокая критичность, низкая сложность: [Node Exporter]  
    quadrant-2 Высокая критичность, высокая сложность: [Prometheus, Alertmanager]  
    quadrant-3 Низкая критичность, низкая сложность: [Grafana Dashboards]  
    quadrant-4 Низкая критичность, высокая сложность: [Кастомные алерты]  

    "Node Exporter (10 ВМ)": [x=0.1, y=0.9]  
    "Prometheus": [x=0.7, y=0.8]  
    "Alertmanager": [x=0.6, y=0.7]  
    "Grafana": [x=0.3, y=0.4]  
```  

**Процессы**:  
1. **Сбор данных**: Node Exporter на каждой ВМ предоставляет метрики через HTTP.  
2. **Получение метрик**: Prometheus опрашивает `/metrics` всех ВМ по расписанию.  
3. **Хранение**: TSDB Prometheus сохраняет данные с временными метками.  
4. **Визуализация**: Grafana запрашивает Prometheus через PromQL.  
5. **Алертинг**: При превышении порогов Prometheus отправляет алерты в Alertmanager.  

---

### 4. Мониторинг в финтехе  
**Метрики**:  
- **Инфраструктура**: CPU, RAM, сеть (пропускная способность, задержки).  
- **Приложения**: Время обработки транзакций, ошибки JVM (Java).  
- **Бизнес-логика**: Количество операций, фрод-события.  

**Пример для финтеха**:  
- Prometheus отслеживает задержки API платежного шлюза.  
- Alertmanager отправляет SMS при падении доступности ниже 99.9%.  
- Grafana отображает SLA в реальном времени.  

---

### 5. Sequence Diagram: Java-приложение в ВМ  
```mermaid  
sequenceDiagram  
    participant JavaApp  
    participant JMXExporter  
    participant Prometheus  
    participant Grafana  

    JavaApp->>JMXExporter: JMX-метрики (TCP/12345)  
    Prometheus->>JMXExporter: HTTP GET /metrics (TCP/9404)  
    JMXExporter-->>Prometheus: Данные в формате Prometheus  
    Grafana->>Prometheus: Запросы PromQL (HTTP)  
```  

---

### 6. Sequence Diagram: Java-приложение в Kubernetes  
```mermaid  
sequenceDiagram  
    participant JavaPod  
    participant ServiceMonitor  
    participant Prometheus  
    participant Grafana  

    JavaPod->>Prometheus: Предоставляет метрики через /actuator/prometheus (HTTP)  
    Prometheus->>Kubernetes API: Обнаружение Pods (HTTP)  
    Kubernetes API-->>Prometheus: Endpoints списки  
    Prometheus->>JavaPod: Сбор метрик каждые 15 сек  
    Grafana->>Prometheus: Визуализация через PromQL  
```  

---

### 7. Итог  
**Мониторинг** — критическая компонента DevOps-цикла, обеспечивающая:  
- **Наблюдаемость** (observability) через связку Prometheus + Grafana.  
- **Раннее реагирование** на инциденты (Alertmanager).  
- **Анализ трендов** для Capacity Planning.  

**Недостающие темы**:  
- Интеграция с логами (Loki, ELK).  
- Трассировка (Jaeger, Zipkin).  
- Оптимизация запросов PromQL.  

**Финальная схема**:  
```mermaid  
graph TD  
    A[Node Exporter] -->|HTTP| B(Prometheus)  
    B -->|PromQL| C[Grafana]  
    B -->|Alerts| D[Alertmanager]  
    D -->|Webhook| E[Slack/Email]  
    C -->|Dashboard| F[Анализ SLA]  
```  

**Заключение**: Современный мониторинг — это синергия pull-модели (Prometheus), гибкой визуализации (Grafana) и автоматизированного алертинга, обеспечивающая устойчивость и прозрачность инфраструктуры, особенно в высоконагруженных средах (финтех, банкинг).
