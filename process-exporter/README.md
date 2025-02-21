## Process Exporter
**Process Exporter** используется для мониторинга процессов на сервере. Он собирает информацию о запущенных процессах, их состоянии и использовании ресурсов.

 - Установите `Process Exporter` в систему и натравите на него `Prometheus`
 - Проверьте экспортер на странице `/metrics`
 - Вам нужно замониторить директорию с процессами `Linux` и вывести на дашборд
 - Скачайте дашборд `Process Exporter` предназначенный для `Prometheus` с сайта `Grafana Lab`
 - Подгрузите дашборд в `Grafana`, убедитесь, что он работает и сохраните

#### Пример метрик:

  - `namedprocess_namegroup_cpu_seconds_total` — общее время использования CPU процессами.
  - `namedprocess_namegroup_memory_bytes` — использование памяти процессами.
  - `namedprocess_namegroup_open_filedesc` — количество открытых файловых дескрипторов.
  - `namedprocess_namegroup_threads` — количество потоков.
  - `namedprocess_namegroup_states` — состояние процессов (например, running, sleeping, zombie).

