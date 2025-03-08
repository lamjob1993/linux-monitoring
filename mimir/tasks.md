# Mimir
_Пользуемся официальной документацией на GitHub (в основном там прописаны Docker файлы на запуск и всегда есть конфиги)_
## Tasks

 - От вас требуется поднять `Mimir` частично способом из раздела [Prometheus](https://github.com/lamjob1993/linux-monitoring/tree/main/prometheus "Запускаем голый бинарь Prometheus, пишем юнит и простую автоматизацию
")
 - При этом упростите установку `Mimir` - после распаковки архива сделайте директорию распаковки рабочей сразу, чтобы не повторять шаги способом установки `Prometheus`
 - Настройте `Prometheus` на `remote-write` в `Mimir`
 - Пропишите Data Source в `Grafana`
 - Снимите метрики в `Grafana`

---

Минимально рабочий конфиг для запуска (в работе):

```bash
# Настройки сервера
server:
  http_listen_port: 8080  # Порт для HTTP API

# Distributor (распределитель данных)
distributor:
  ring:
    kvstore:
      store: inmemory  # Хранилище кольца распределения (inmemory для тестов)

# Ingester (компонент для приема и хранения временных метрик)
ingester:
  ring:
    kvstore:
      store: inmemory  # Хранилище кольца инжестера (inmemory для тестов)
    replication_factor: 1  # Фактор репликации (1 для тестов)

# Storage (хранилище данных)
#storage:
#  engine: tsdb  # Использование локальной файловой системы
#  tsdb:
#    dir: /opt/linux-monitoring/mimir/tsdb  # Директория для хранения данных TSDB

# Query Scheduler (для маршрутизации запросов)
# query_scheduler:
#  enabled: true

# Query Frontend (для оптимизации запросов)
#query_frontend:
#  enabled: true

# Querier (для выполнения запросов к данным)
#querier:
#  max_samples_per_query: 100000000  # Максимальное количество выборок для одного запроса

# API (настройки API для Prometheus/Grafana)
api:
  prometheus_http_prefix: /api/v1  # Префикс для PromQL API
```
