### 1. Обновленные схемы в формате `flowchart TD` с детальным описанием этапов  
#### 2.3 Flowchart: Взаимодействие Java-приложения, Prometheus, Grafana и ELK  
```mermaid  
flowchart TD  
    A[Банковское Java-приложение] -->|1. JMX-метрики\n(Port 12345)| B(JMX Exporter)  
    A -->|2. Логи транзакций\n(JSON/TCP)| C(Logstash)  
    B -->|3. HTTP GET /metrics\n(Port 9404)| D(Prometheus)  
    C -->|4. Индексация логов\n(HTTP/9200)| E(Elasticsearch)  
    D -->|5. Сохранение в TSDB| D  
    D -->|6. PromQL-запросы\n(HTTP)| F(Grafana)  
    E -->|7. Поиск логов\n(Lucene)| F  
    D -->|8. Алерты\n(HTTP POST)| G(Alertmanager)  
    G -->|9. Webhook| H[Slack/Email]  
    F -->|10. Дашборд\n(JVM, API, Логи)| I[Команда DevOps]  
```  

**Пояснение этапов**:  
1. **JMX-метрики**: Приложение экспортирует метрики JVM (heap, GC, потоки) через JMX-порт.  
2. **Логи транзакций**: Логи в формате JSON отправляются в Logstash для обработки.  
3. **Сбор метрик**: Prometheus опрашивает JMX Exporter каждые 15 сек по HTTP.  
4. **Индексация**: Logstash парсит логи и сохраняет их в Elasticsearch.  
5. **TSDB**: Prometheus сохраняет метрики во внутренней БД временных рядов.  
6. **PromQL-запросы**: Grafana запрашивает данные через API Prometheus.  
7. **Поиск логов**: Grafana интегрируется с Elasticsearch для отображения логов.  
8. **Алерты**: При нарушении правил Prometheus отправляет алерт в Alertmanager.  
9. **Уведомления**: Alertmanager перенаправляет алерты в каналы связи.  
10. **Дашборд**: Инженеры анализируют SLA, метрики и логи в едином интерфейсе.  

---

#### 3. Flowchart: Инфраструктура из 10 ВМ с Java-приложением  
```mermaid  
flowchart TD  
    subgraph Infra[Инфраструктура]  
        A1[ВМ 1\nJava-приложение] -->|JMX Exporter| B1(Prometheus)  
        A2[ВМ 2\nJava-приложение] -->|JMX Exporter| B1  
        A3[ВМ 3\nNode Exporter] -->|Метрики ОС| B1  
        A4[ВМ 4-10\nNode Exporter] -->|Метрики ОС| B1  
    end  
    B1 -->|PromQL| C[Grafana]  
    B1 -->|Алерты| D[Alertmanager]  
    A1 & A2 -->|Логи| E(Logstash)  
    E -->|Индексация| F(Elasticsearch)  
    C -->|Дашборды| G[Мониторинг]  
    C -->|Kibana| F  
    D -->|Webhook| H[Уведомления]  
```  

**Пояснение этапов**:  
1. **ВМ 1-2**: Банковские Java-приложения с JMX Exporter для сбора JVM-метрик.  
2. **ВМ 3-10**: Серверы с Node Exporter для мониторинга CPU, RAM, сети.  
3. **Prometheus**: Центральный сервер опрашивает все ВМ по HTTP.  
4. **Logstash**: Принимает логи от Java-приложений, парсит и фильтрует.  
5. **Elasticsearch**: Хранит логи, позволяет выполнять поиск через Kibana.  
6. **Grafana**: Визуализирует метрики (Prometheus) и логи (Elasticsearch).  
7. **Alertmanager**: Отправляет алерты при превышении порогов (напр., CPU > 90%).  

---

#### 5. Flowchart: Java-приложение в ВМ с ELK  
```mermaid  
flowchart TD  
    A[Java-приложение] -->|1. JMX-метрики\n(Port 12345)| B(JMX Exporter)  
    A -->|2. Логи транзакций\n(JSON)| C(Logstash)  
    B -->|3. HTTP /metrics\n(Port 9404)| D(Prometheus)  
    C -->|4. Парсинг логов| E(Elasticsearch)  
    D -->|5. PromQL-анализ| F{Grafana}  
    E -->|6. Поиск логов| F  
    D -->|7. Алерт: High GC| G[Alertmanager]  
    G -->|8. Webhook| H[Slack]  
    F -->|9. Отчет по SLA| I[Бизнес-аналитика]  
```  

**Пояснение этапов**:  
1. **JMX-метрики**: Приложение предоставляет метрики через JMX-порт.  
2. **Логи транзакций**: Логи в формате JSON отправляются в Logstash.  
3. **Сбор метрик**: Prometheus парсит `/metrics` эндпоинт JMX Exporter.  
4. **Парсинг логов**: Logstash извлекает поля (напр., `transaction_id`, `status`).  
5. **PromQL-анализ**: Запросы вида `rate(jvm_gc_pause_seconds[5m])`.  
6. **Поиск логов**: Grafana выполняет запросы типа `status:500 AND service:payment`.  
7. **Алерты**: При превышении GC pause > 1 сек срабатывает алерт.  
8. **Уведомления**: Инженеры получают сообщение в Slack.  
9. **Отчеты**: Дашборды Grafana показывают выполнение SLA (напр., 99.95%).  

---

#### 6. Flowchart: Java-приложение в Kubernetes с ELK  
```mermaid  
flowchart TD  
    subgraph K8s[Kubernetes]  
        A[Pod\nJava-приложение] -->|1. /actuator/prometheus| B(Prometheus)  
        A -->|2. Логи| C(Filebeat)  
        C -->|3. Отправка логов| D(Logstash)  
    end  
    D -->|4. Индексация| E(Elasticsearch)  
    B -->|5. Service Discovery| F[Kubernetes API]  
    B -->|6. PromQL| G{Grafana}  
    E -->|7. Поиск логов| G  
    B -->|8. Алерты| H[Alertmanager]  
    H -->|9. Webhook| I[PagerDuty]  
    G -->|10. Дашборд\nK8s + JVM| J[DevOps]  
```  

**Пояснение этапов**:  
1. **Метрики приложения**: Spring Boot Actuator предоставляет эндпоинт `/actuator/prometheus`.  
2. **Логи в Pod**: Filebeat собирает логи из контейнера и буферизует их.  
3. **Отправка логов**: Filebeat пересылает логи в Logstash для обработки.  
4. **Индексация**: Logstash сохраняет логи в Elasticsearch с тегами (напр., `namespace=banking`).  
5. **Service Discovery**: Prometheus автоматически находит Pods через Kubernetes API.  
6. **PromQL-запросы**: Пример: `sum by (pod) (rate(http_requests_total[2m]))`.  
7. **Поиск логов**: Grafana использует синтаксис Kibana: `kubernetes.labels.app: banking`.  
8. **Алерты**: Правила в Prometheus отслеживают падение readiness-проверок.  
9. **PagerDuty**: Критические алерты запускают инцидент-менеджмент.  
10. **Дашборд**: Отображение метрик Pod (CPU, memory) и JVM (heap usage).  

---

### 7. Итоговый Flowchart: Полный стек мониторинга  
```mermaid  
flowchart TD  
    subgraph Apps[Приложения]  
        A[Java-приложение] -->|JMX| B(JMX Exporter)  
        A -->|Логи| C(Logstash)  
        D[Серверы] -->|Node Exporter| E(Prometheus)  
    end  
    subgraph Monitoring[Мониторинг]  
        B -->|HTTP| E  
        E -->|TSDB| E  
        E -->|PromQL| F{Grafana}  
        C -->|Elasticsearch| G[(Elasticsearch)]  
        G -->|Kibana| F  
        E -->|Alerts| H[Alertmanager]  
        H -->|Webhook| I[Slack]  
    end  
    F -->|Дашборды| J[Команда]  
    J -->|Оптимизация| Apps  
```  

**Пояснение этапов**:  
1. **Сбор данных**:  
   - Java-приложение → JMX Exporter → метрики JVM.  
   - Серверы → Node Exporter → метрики ОС.  
   - Логи → Logstash → Elasticsearch.  
2. **Хранение**:  
   - Prometheus TSDB → метрики.  
   - Elasticsearch → логи.  
3. **Анализ**:  
   - Grafana → PromQL для метрик + Lucene для логов.  
4. **Алертинг**:  
   - Alertmanager → уведомления о нарушениях SLA.  
5. **Оптимизация**:  
   - Команда анализирует дашборды, настраивает autoscaling, исправляет утечки памяти.  

---

### Итоговые изменения в тексте  
1. **Во все разделы добавлены блок-схемы** в формате `flowchart TD` с детализацией этапов.  
2. **Интеграция Java-приложения**:  
   - JMX Exporter для сбора JVM-метрик.  
   - Логи транзакций → ELK.  
3. **Добавлен стек ELK**:  
   - Logstash для парсинга, Elasticsearch для хранения, Kibana для визуализации.  
4. **Kubernetes**:  
   - Service Discovery для автоматического обнаружения Pods.  
   - Filebeat для сбора логов в K8s.  
5. **Детализация этапов**:  
   - Для каждой схемы добавлено пошаговое описание процессов (протоколы, порты, примеры запросов).  

**Финальный вывод**:  
Предложенная архитектура обеспечивает полную наблюдаемость банковского Java-приложения — от метрик JVM до бизнес-логики. Комбинация Prometheus (метрики), ELK (логи) и Grafana (визуализация) позволяет быстро выявлять и устранять инциденты, а оптимизация PromQL снижает нагрузку на систему.
