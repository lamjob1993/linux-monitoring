# Установка Mimir в разрезе мониторинга

_Пользуемся официальной документацией на GitHub (в основном там прописаны Docker файлы на запуск и всегда есть конфиги)_

## Tasks

 - [Вспоминаем схему](https://github.com/lamjob1993/linux-monitoring/blob/main/mimir/README.md#%D1%81%D1%85%D0%B5%D0%BC%D0%B0-%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D1%8B-mimir)
 - От вас требуется поднять `Mimir` в монолитном режиме частично способом из раздела [Prometheus](https://github.com/lamjob1993/linux-monitoring/tree/main/prometheus "Запускаем голый бинарь Prometheus, пишем юнит и простую автоматизацию.")
 - При этом упростите установку `Mimir` - после распаковки архива сделайте директорию распаковки рабочей сразу, чтобы не повторять шаги способом установки `Prometheus`
 - Настройте `Prometheus` на `remote-write` в `Mimir`
 - Пропишите `Data Source` в `Grafana`
 - Снимите метрики `Prometheus` из `Mimir` в `Grafana`

---

#### 1. Рабочий конфиг `Mimir` для запуска в монолитном режиме

```bash
# Отключаем мультитенантность
# Мультиарендность (multi-tenancy) в системах мониторинга, таких как Grafana Mimir, предназначена для разделения данных между различными пользователями, организациями или командами
# Даже если мультиарендность отключена, Grafana может требовать указания tenant ID
# В настройках источника данных в Grafana добавьте HTTP-заголовок: X-Scope-OrgID: anonymous
multitenancy_enabled: false 

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

compactor:
  data_dir: /tmp/mimir/compactor
  sharding_ring:
    kvstore:
      store: memberlist

distributor:
  ring:
    instance_addr: 127.0.0.1
    kvstore:
      store: memberlist

ingester:
  ring:
    instance_addr: 127.0.0.1
    kvstore:
      store: memberlist
    replication_factor: 1

ruler_storage:
  backend: filesystem
  filesystem:
    dir: /tmp/mimir/rules

store_gateway:
  sharding_ring:
    replication_factor: 1

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
  - url: http://<MIMIR_IP>:9009/api/v1/push     # имеем ввиду, что это не Data Source для Grafana
    # Если используется аутентификация (например, Basic Auth):
    #basic_auth:
    #  username: "user"
    #  password: "password"
    # Или для токена:
    # bearer_token: "your_token"

```

#### 3. Добавление Data Source Mimir в Grafana
- Prometheus server URL: http://ip-address-mimir:9009/prometheus
  - **prometheus** указываем явно после `ip address Mimir` и порта

#### 4. Grafana должна четко в разделе Explore отображать метрики проэкспонированные с Mimir
- Выбрать Explore → Выбрать Datasource → Mimir → Вбить метрику `up` в поле ввода
