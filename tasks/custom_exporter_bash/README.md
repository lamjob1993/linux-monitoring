# Exporters

## Pull модель

### Custom Exporter

**Custom Exporter** — это набор Bash-скриптов, которые выполняют HTTP-запросы к сайтам (например, Google, VK, Yandex, GitHub), анализируют результаты и преобразуют их в метрики, читаемые Prometheus через Node Exporter Textfile Collector.

О **Pull** модели мы читали [здесь](https://github.com/lamjob1993/linux-monitoring/blob/main/prometheus/beginning/1.%20%D0%92%D0%B2%D0%B5%D0%B4%D0%B5%D0%BD%D0%B8%D0%B5%20(%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D1%8B%20Prometheus).md#pull-%D0%BC%D0%BE%D0%B4%D0%B5%D0%BB%D1%8C-%D0%B2-prometheus).

### Назначение Custom Exporter:

1. **Сбор специфических данных**:
   - Стандартные экспортеры (например, Node Exporter) собирают общесистемные метрики (CPU, память, диски и т.д.).
   - Если вам нужно собрать уникальные данные (например, доступность сайтов), стандартные инструменты не подойдут. Для этого создается Custom Exporter.

2. **Интеграция с Prometheus**:
   - Prometheus работает с данными в формате OpenMetrics (или текстовом формате, совместимом с этим стандартом).
   - Custom Exporter преобразует сырые данные (например, результаты `curl`) в этот формат.

3. **Гибкость**:
   - Вы можете настроить Custom Exporter под свои нужды: проверять доступность сайтов, мониторить API, собирать логи и многое другое.
