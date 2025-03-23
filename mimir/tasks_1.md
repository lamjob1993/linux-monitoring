# Установка Mimir в разрезе мониторинга

_Пользуемся официальной документацией на GitHub (в основном там прописаны Docker файлы на запуск и всегда есть конфиги)_

## Tasks

 - [Вспоминаем нашу схему](https://github.com/lamjob1993/linux-monitoring/blob/main/mimir/README.md#%D1%81%D1%85%D0%B5%D0%BC%D0%B0-%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D1%8B-mimir)
   - По данному `Tasks` разделу нужно выполнить только деплой:
     - `Grafana` на отдельной виртуалке
       - Если Grafana уже поднята, то отлично
     - `Mimir` на отдельной виртуалке
       - Поднимаем с нуля
     - `Prometheus` на отдельной виртуалке
       - Если Prometheus уже поднят, то отлично
 - [Далее обязательно смотрим на режимы деплоя Mimir с официального сайта](https://grafana.com/docs/mimir/latest/references/architecture/deployment-modes/)
   - А также постепенно погружаемся в схему балансировки, в следующих `Tasks` будет горизонтальное масштабирование Prometheus в разрезе трех инстансов Mimir (так называемый хэшринг из кольца Mimir, или кольцо хэшринга) завязанных на Nginx
 - [Далее обязательно смотрим этот ролик](https://grafana.com/docs/mimir/latest/get-started/)
 - [Далее обязательно смотрим на этот репозиторий с конфигами и черпаем вдохновение для деплоя Mimir](https://github.com/ktsstudio/mimir-demo/tree/main/simple)
   - Кстати, говоря на этом этапе можно поверхностно пощупать контейнеры в разрезе Docker Compose, только деплоить Compose файл лучше на отдельной виртуалке
     - Если будете ставить Docker, то строго [только по этой ссылке](https://docs.docker.com/engine/install/debian/)
 - От вас требуется поднять один инстанс `Mimir` в монолитном режиме частично способом из раздела [Prometheus](https://github.com/lamjob1993/linux-monitoring/tree/main/prometheus "Запускаем голый бинарь Prometheus, пишем юнит и простую автоматизацию.")
 - При этом упростите установку `Mimir` - после распаковки архива сделайте директорию распаковки рабочей сразу, чтобы не повторять шаги способом установки `Prometheus`
 - Настройте рабочий конфиг `Mimir` 
 - Настройте `Prometheus` на `remote-write` в `Mimir`
 - Пропишите `Data Source Mimir` в `Grafana`
 - Снимите метрики в разделе **Explore** из `Data Source Mimir` в `Grafana`
   - Достаточно вывести метрику `up`

---
