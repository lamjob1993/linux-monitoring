# Установка Mimir в разрезе мониторинга

_Пользуемся официальной документацией на GitHub (в основном там прописаны Docker файлы на запуск и всегда есть конфиги)_

## Tasks

 - От вас требуется поднять `Mimir` в монолитном режиме частично способом из раздела [Prometheus](https://github.com/lamjob1993/linux-monitoring/tree/main/prometheus "Запускаем голый бинарь Prometheus, пишем юнит и простую автоматизацию.")
 - При этом упростите установку `Mimir` - после распаковки архива сделайте директорию распаковки рабочей сразу, чтобы не повторять шаги способом установки `Prometheus`
 - Настройте `Prometheus` на `remote-write` в `Mimir`
 - Пропишите `Data Source` в `Grafana`
 - Снимите метрики `Prometheus` из `Mimir` в `Grafana`

---

#### 1. Рабочий конфиг `Mimir` для запуска в монолитном режиме

```bash

# Режим работы: monolithic (все компоненты в одном процессе)
target: all

# Настройки хранилища (например, локальная файловая система)
blocks_storage:
  backend: filesystem
  filesystem:
    dir: /var/lib/mimir/data

# Порт для HTTP API
server:
  http_listen_port: 9009

```

#### 2. Рабочий конфиг `Prometheus` на `remote-write` в `Mimir`

```bash

global:
  scrape_interval: 15s # Интервал сбора метрик

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090'] # Сбор метрик с самого Prometheus

remote_write:
  - url: http://<MIMIR_IP>:9009/api/v1/push
    # Если используется аутентификация (например, Basic Auth):
    #basic_auth:
    #  username: "user"
    #  password: "password"
    # Или для токена:
    # bearer_token: "your_token"

```
