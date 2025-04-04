# PostgreSQL

_Пользуемся официальной документацией на GitHub (в основном там прописаны Docker файлы на запуск и всегда есть конфиги)_

## Tasks

### Шаг 1. Установка Postgres Exporter

- Запустите [postgres_exporter](https://github.com/prometheus-community/postgres_exporter "Prometheus exporter for PostgreSQL server metrics.") и натравите на него **Prometheus**
- ```bash
  docker run -d \
  --net=host \
  -e DATA_SOURCE_URI="localhost:5432/postgres?sslmode=disable" \
  -e DATA_SOURCE_USER=postgres \
  -e DATA_SOURCE_PASS=password \
  quay.io/prometheuscommunity/postgres-exporter
  ```

### Шаг 2. Установка Grafana и адаптация дашборда PostgreSQL

- [Скачайте дашборд](https://grafana.com/grafana/dashboards/9628-postgresql-database/) предназначенный для СУБД **PostgreSQL** и визуализируйте метрики в **Grafana**
