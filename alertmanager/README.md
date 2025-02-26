# Alerting
**Alertmanager** — это компонент Prometheus, предназначенный для управления алертами. Он принимает алерты от Prometheus, группирует их, подавляет ненужные уведомления и доставляет их в различные системы оповещения.
## Расширенная схема: Alertmanager + Grafana

```mermaid
sequenceDiagram
    participant App as "Приложение (App)"
    participant Exporter as "Экспортер"
    participant Prometheus as "Prometheus Server"
    participant Alertmanager as "Alertmanager"
    participant Grafana as "Grafana"

    Exporter->>App: Вызов API приложения или чтение системных файлов/логов
    App-->>Exporter: Предоставление данных через API, файлы или библиотеки

    loop Каждые N секунд
        Prometheus->>Exporter: HTTP GET (Pull метрик)
        Exporter-->>Prometheus: HTTP 200 OK + Текстовые метрики
    end

    opt Если условия алерта выполнены
        Prometheus->>Alertmanager: HTTP POST (Отправка алертов)
        Alertmanager->>Grafana: Интеграция алертов в интерфейс Grafana
    end

    loop По запросу пользователя в Grafana
        Grafana->>Prometheus: HTTP GET (Запрос метрик)
        Prometheus-->>Grafana: HTTP 200 OK + Метрики в формате JSON
    end
```

**Описание:**  
- Prometheus собирает метрики и проверяет условия алертов.
- Если условия выполнены, Prometheus отправляет алерты в Alertmanager.
- Alertmanager может интегрироваться с Grafana для отображения алертов.
- Grafana запрашивает метрики у Prometheus для визуализации.

---
