## Node Exporter

Это один из самых популярных экспортеров для Prometheus, предназначенный для сбора метрик, связанных с состоянием сервера (ноды). Он предоставляет информацию о CPU, памяти, дисках, сети, файловых системах и других ресурсах системы - Установите `Blackbox Exporter` в систему и натравите на него `Prometheus`

 - От вас требуется поднять `Node Exporter` способом из раздела `Prometheus`
   - Можете модернизировать скрипт установщика `Prometheus`
 - Натравите на него `Prometheus`
 - Перейдите на страницу `/metrics` и удостоверьтесь, что экспортер поднялся
 - По заданию вам нужно замониторить свою тачку
 - Скачайте дашборд предназначенный для `Node Exporter` с сайта `Grafana Lab`
 - Подгрузите дашборд в `Grafana`, убедитесь, что он работает и сохраните

---

### Основные метрики:

#### **1. CPU и процессы**
- `node_cpu_seconds_total` — общее время, проведенное процессором в каждом режиме (user, system, idle и т.д.).
- `node_load1`, `node_load5`, `node_load15` — средняя загрузка системы за 1, 5 и 15 минут.
- `node_context_switches_total` — количество переключений контекста.
- `node_forks_total` — количество созданных процессов.

Пример:
```plaintext
# HELP node_cpu_seconds_total Seconds the CPUs spent in each mode.
# TYPE node_cpu_seconds_total counter
node_cpu_seconds_total{cpu="0",mode="user"} 12345.67
node_cpu_seconds_total{cpu="0",mode="system"} 2345.67

# HELP node_load1 1m load average.
# TYPE node_load1 gauge
node_load1 0.75
```

---

#### **2. Память**
- `node_memory_MemTotal_bytes` — общий объем оперативной памяти.
- `node_memory_MemFree_bytes` — свободная оперативная память.
- `node_memory_Buffers_bytes`, `node_memory_Cached_bytes` — память, используемая для буферов и кэша.
- `node_memory_SwapTotal_bytes`, `node_memory_SwapFree_bytes` — общий и свободный объем swap.

Пример:
```plaintext
# HELP node_memory_MemTotal_bytes Memory information field MemTotal_bytes.
# TYPE node_memory_MemTotal_bytes gauge
node_memory_MemTotal_bytes 8589934592

# HELP node_memory_MemFree_bytes Memory information field MemFree_bytes.
# TYPE node_memory_MemFree_bytes gauge
node_memory_MemFree_bytes 2147483648
```

---

#### **3. Диски и файловые системы**
- `node_filesystem_size_bytes` — общий размер файловой системы.
- `node_filesystem_free_bytes` — свободное место на файловой системе.
- `node_filesystem_avail_bytes` — доступное место для пользователей.
- `node_disk_read_bytes_total`, `node_disk_written_bytes_total` — количество прочитанных и записанных байт на диске.
- `node_disk_io_time_seconds_total` — время, затраченное на операции ввода-вывода.

Пример:
```plaintext
# HELP node_filesystem_size_bytes Filesystem size in bytes.
# TYPE node_filesystem_size_bytes gauge
node_filesystem_size_bytes{device="/dev/sda1",fstype="ext4",mountpoint="/"} 10737418240

# HELP node_disk_read_bytes_total The total number of bytes read successfully.
# TYPE node_disk_read_bytes_total counter
node_disk_read_bytes_total{device="sda"} 1234567890
```

---

#### **4. Сеть**
- `node_network_receive_bytes_total` — количество байт, полученных через сетевой интерфейс.
- `node_network_transmit_bytes_total` — количество байт, отправленных через сетевой интерфейс.
- `node_network_up` — статус сетевого интерфейса (1 — включен, 0 — выключен).

Пример:
```plaintext
# HELP node_network_receive_bytes_total Network device statistic receive_bytes.
# TYPE node_network_receive_bytes_total counter
node_network_receive_bytes_total{device="eth0"} 987654321

# HELP node_network_transmit_bytes_total Network device statistic transmit_bytes.
# TYPE node_network_transmit_bytes_total counter
node_network_transmit_bytes_total{device="eth0"} 123456789
```

---

#### **5. Системные метрики**
- `node_boot_time_seconds` — время последней загрузки системы.
- `node_time_seconds` — текущее время системы в Unix-формате.
- `node_uname_info` — информация о версии ядра и операционной системы.

Пример:
```plaintext
# HELP node_boot_time_seconds Node boot time, in unixtime.
# TYPE node_boot_time_seconds gauge
node_boot_time_seconds 1698765432

# HELP node_uname_info Labeled system information as provided by the uname system call.
# TYPE node_uname_info gauge
node_uname_info{domainname="(none)",machine="x86_64",nodename="server1",release="5.4.0-42-generic",sysname="Linux",version="#46-Ubuntu SMP Fri Jul 10 00:24:02 UTC 2020"} 1
```

---

#### **6. Температура и аппаратное состояние**
- `node_hwmon_temp_celsius` — температура компонентов (если поддерживается).
- `node_hwmon_fan_rpm` — скорость вращения вентиляторов (если поддерживается).

Пример:
```plaintext
# HELP node_hwmon_temp_celsius Hardware monitor for temperature (input)
# TYPE node_hwmon_temp_celsius gauge
node_hwmon_temp_celsius{chip="platform_coretemp_0",sensor="temp1"} 45.0
```
