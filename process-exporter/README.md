# Exporters

## Process Exporter

Используется для мониторинга процессов на сервере. Он собирает информацию о запущенных процессах, их состоянии и использовании ресурсов.


#### Пример метрик:

  - `namedprocess_namegroup_cpu_seconds_total` — общее время использования CPU процессами.
  - `namedprocess_namegroup_memory_bytes` — использование памяти процессами.
  - `namedprocess_namegroup_open_filedesc` — количество открытых файловых дескрипторов.
  - `namedprocess_namegroup_threads` — количество потоков.
  - `namedprocess_namegroup_states` — состояние процессов (например, running, sleeping, zombie).

#### Пример вывода:

       # HELP namedprocess_namegroup_cpu_seconds_total CPU usage in seconds
       # TYPE namedprocess_namegroup_cpu_seconds_total counter
       namedprocess_namegroup_cpu_seconds_total{groupname="nginx"} 123.45
       
       # HELP namedprocess_namegroup_memory_bytes Memory usage in bytes
       # TYPE namedprocess_namegroup_memory_bytes gauge
       namedprocess_namegroup_memory_bytes{groupname="nginx"} 1048576
       
       # HELP namedprocess_namegroup_threads Number of threads
       # TYPE namedprocess_namegroup_threads gauge
       namedprocess_namegroup_threads{groupname="nginx"} 10
