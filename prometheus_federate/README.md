# Prometheus федерация

Схема, демонстрирующая работу федерации **Prometheus** на трех экземплярах: `prometheus-central`, `prometheus-dc1` и `prometheus-dc2`. Эта схема показывает, как локальные экземпляры **Prometheus** собирают метрики из своих дата-центров, а центральный экземпляр **Prometheus** агрегирует ключевые метрики через механизм федерации.

```mermaid
sequenceDiagram
    participant ExporterDC1 as "Экспортер в DC1"
    participant PrometheusDC1 as "Prometheus (DC1)"
    participant ExporterDC2 as "Экспортер в DC2"
    participant PrometheusDC2 as "Prometheus (DC2)"
    participant PrometheusCentral as "Prometheus Central"

    loop Каждые N секунд в DC1
        PrometheusDC1->>ExporterDC1: HTTP GET (Pull метрик)
        ExporterDC1-->>PrometheusDC1: HTTP 200 OK + Текстовые метрики
    end

    loop Каждые N секунд в DC2
        PrometheusDC2->>ExporterDC2: HTTP GET (Pull метрик)
        ExporterDC2-->>PrometheusDC2: HTTP 200 OK + Текстовые метрики
    end

    note over PrometheusCentral: Prometheus Central использует<br>федерацию для сбора метрик<br>с PrometheusDC1 и PrometheusDC2

    loop Каждые M секунд
        PrometheusCentral->>PrometheusDC1: HTTP GET (/federate)
        PrometheusDC1-->>PrometheusCentral: HTTP 200 OK + Агрегированные метрики
    end

    loop Каждые M секунд
        PrometheusCentral->>PrometheusDC2: HTTP GET (/federate)
        PrometheusDC2-->>PrometheusCentral: HTTP 200 OK + Агрегированные метрики
    end

    note over PrometheusCentral: Prometheus Central предоставляет<br>общий обзор всей инфраструктуры
```

### Объяснение схемы:

1. **Локальные экземпляры Prometheus (`PrometheusDC1` и `PrometheusDC2`)**:
   - Эти экземпляры собирают метрики из своих дата-центров (`DC1` и `DC2`) с помощью экспортеров (`ExporterDC1` и `ExporterDC2`).
   - Метрики собираются через стандартный pull-механизм Prometheus.

2. **Федерация**:
   - Центральный экземпляр Prometheus (`PrometheusCentral`) использует endpoint `/federate` для получения ключевых метрик от локальных экземпляров.
   - `PrometheusCentral` делает запросы к `PrometheusDC1` и `PrometheusDC2` с параметром `match[]`, чтобы выбрать нужные метрики.

3. **Агрегирование данных**:
   - `PrometheusCentral` агрегирует данные со всех дата-центров и предоставляет общий обзор всей инфраструктуры.

4. **Периодичность**:
   - Локальные экземпляры собирают метрики каждые `N` секунд.
   - Центральный экземпляр запрашивает метрики у локальных экземпляров каждые `M` секунд.

### Преимущества такой архитектуры:
- **Изолированность**: Каждый дата-центр имеет свой собственный экземпляр Prometheus, что снижает нагрузку и обеспечивает независимость.
- **Масштабируемость**: Можно легко добавить новые дата-центры и соответствующие экземпляры Prometheus.
- **Общий обзор**: Центральный экземпляр позволяет получать общую картину работы всей инфраструктуры. 
