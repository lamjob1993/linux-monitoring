# Установка Mimir в разрезе мониторинга

_Пользуемся официальной документацией на GitHub (в основном там прописаны Docker файлы на запуск и всегда есть конфиги)_

## Tasks

 - [Вспоминаем нашу схему](https://github.com/lamjob1993/linux-monitoring/blob/main/mimir/README.md#%D1%81%D1%85%D0%B5%D0%BC%D0%B0-%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D1%8B-mimir)
 - [Далее этот ролик обязателен к просмотру](https://grafana.com/docs/mimir/latest/get-started/)
 - [Далее обязательно смотрим на этот репозиторий с конфигами для деплоя Mimir](https://github.com/ktsstudio/mimir-demo/tree/main/simple)
 - От вас требуется поднять один инстанс `Mimir` в монолитном режиме частично способом из раздела [Prometheus](https://github.com/lamjob1993/linux-monitoring/tree/main/prometheus "Запускаем голый бинарь Prometheus, пишем юнит и простую автоматизацию.")
 - При этом упростите установку `Mimir` - после распаковки архива сделайте директорию распаковки рабочей сразу, чтобы не повторять шаги способом установки `Prometheus`
 - Настройте `Prometheus` на `remote-write` в `Mimir`
 - Пропишите `Data Source` в `Grafana`
 - Снимите метрики `Prometheus` из `Mimir` в `Grafana`

---
