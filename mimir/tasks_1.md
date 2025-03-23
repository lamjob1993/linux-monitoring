# Установка Mimir в разрезе мониторинга

_Пользуемся официальной документацией на GitHub (в основном там прописаны Docker файлы на запуск и всегда есть конфиги)_

## Tasks

 - От вас требуется поднять `Mimir` в монолитном режиме частично способом из раздела [Prometheus](https://github.com/lamjob1993/linux-monitoring/tree/main/prometheus "Запускаем голый бинарь Prometheus, пишем юнит и простую автоматизацию.")
 - При этом упростите установку `Mimir` - после распаковки архива сделайте директорию распаковки рабочей сразу, чтобы не повторять шаги способом установки `Prometheus`
 - Настройте `Prometheus` на `remote-write` в `Mimir`
 - Пропишите `Data Source` в `Grafana`
 - Снимите метрики `Prometheus` из `Mimir` в `Grafana`

---

Минимально рабочий конфиг `Mimir` для запуска в монолитном режиме:

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
