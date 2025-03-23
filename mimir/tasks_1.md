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

- Тестовый режим, чтобы пощупать связку Grafana + Prometheus + Mimir
- Не использовать в ПРОД контурах

```bash
# Отключаем мультитенантность
# Мультиарендность (multi-tenancy) в системах мониторинга, таких как Grafana Mimir, предназначена для разделения данных между различными пользователями, организациями или командами
# Даже если мультиарендность отключена, Grafana может требовать указания tenant ID
# В настройках источника данных (Data Source) в Grafana добавьте HTTP-заголовок: X-Scope-OrgID: anonymous
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

# Compactor (Сжатие данных)
compactor:
  # data_dir: Указывает директорию для временных данных компактора. 
  # Здесь используется /tmp/mimir/compactor, но рекомендуется постоянное хранилище.
  data_dir: /tmp/mimir/compactor
  # sharding_ring: Определяет кольцо шардирования (Шардирование — это метод разделения данных на части (шарды) и их распределения по разным серверам или узлам для уменьшения нагрузки и повышения производительности) для распределения задач между экземплярами компактора.
  sharding_ring:
    # kvstore.store: Используется memberlist для децентрализованного управления состоянием кольца.
    kvstore:
      store: memberlist

# Distributor (Распределение данных)
distributor:
  # ring: Определяет кольцо распределителей для координации работы экземпляров.
  ring:
    # instance_addr: Адрес, который будет использоваться для регистрации экземпляра в кольце.
    # Здесь указан локальный адрес (127.0.0.1), что подходит для тестовой среды.
    instance_addr: 127.0.0.1
    # kvstore.store: Используется memberlist для управления состоянием кольца.
    kvstore:
      store: memberlist

# Ingester (Прием и хранение данных)
ingester:
  # ring: Определяет кольцо инжестеров для координации их работы.
  ring:
    # instance_addr: Адрес для регистрации экземпляра в кольце.
    # Здесь указан локальный адрес (127.0.0.1).
    instance_addr: 127.0.0.1
    # kvstore.store: Используется memberlist для управления состоянием кольца.
    kvstore:
      store: memberlist
    # replication_factor: Количество копий данных в кластере. 
    # Значение 1 означает отсутствие репликации, что подходит только для тестов.
    replication_factor: 1

# Ruler Storage (Хранилище правил для алертинга и записи)
ruler_storage:
  # backend: Выбран файловый метод хранения правил.
  backend: filesystem
  # filesystem.dir: Указывает директорию для хранения правил. 
  # Здесь используется /tmp/mimir/rules, но рекомендуется постоянное хранилище.
  filesystem:
    dir: /tmp/mimir/rules

# Store Gateway (Шлюз для доступа к долгосрочному хранилищу)
store_gateway:
  # sharding_ring: Определяет кольцо шардирования для распределения задач между экземплярами шлюза.
  sharding_ring:
    # replication_factor: Количество копий данных в кластере.
    # Значение 1 означает отсутствие репликации, что подходит только для тестов.
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
  - url: http://<MIMIR_IP>:9009/api/v1/push # имеем ввиду, что это не Data Source для Grafana, это адрес Mimir на который Prometheus пушит метрики
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
  - В настройках источника данных (Data Source) в Grafana добавьте HTTP-заголовок: `X-Scope-OrgID: anonymous`

#### 4. Grafana должна четко в разделе Explore отображать метрики проэкспонированные с Mimir
- Выбрать Explore → Выбрать Datasource → Mimir → Вбить метрику `up` в поле ввода
