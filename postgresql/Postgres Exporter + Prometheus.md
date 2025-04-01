# PostgreSQL

## Установка и настройка мониторинга

_Сначала думаем над каждым заданием в разделе `Tasks`, если не можем понять какой-то инструмент не менее 40-ка минут и только потом смотрим этот раздел по пунктам!_

## **Шаг 1: Установка и настройка postgres_exporter**
Ppostgres_exporter нужен для мониторинга PostgreSQL через Prometheus.

1. **Установите `postgres_exporter`**:
   ```bash
   sudo apt install postgresql-exporter -y
   ```

2. **Создайте пользователя для мониторинга**:
   Подключитесь к PostgreSQL:
   ```bash
   sudo -u postgres psql
   ```
   Выполните:
   ```sql
   CREATE USER exporter WITH PASSWORD 'exporter_password';
   GRANT pg_monitor TO exporter;
   \q
   ```

3. **Настройте `postgresql.conf`**:
   Откройте файл конфигурации PostgreSQL:
   ```bash
   sudo nano /etc/postgresql/<version>/main/postgresql.conf
   ```
   Найдите строку `shared_preload_libraries` и измените её:
   ```conf
   shared_preload_libraries = 'pg_stat_statements'
   ```

4. **Настройте `pg_hba.conf`**:
   Откройте файл:
   ```bash
   sudo nano /etc/postgresql/<version>/main/pg_hba.conf
   ```
   Добавьте строку для пользователя `exporter`:
   ```conf
   host    all             exporter        127.0.0.1/32            md5
   ```

5. **Перезапустите PostgreSQL**:
   ```bash
   sudo systemctl restart postgresql
   ```

6. **Запустите `postgres_exporter`**:
   Настройте переменные окружения:
   ```bash
   export DATA_SOURCE_NAME="postgresql://exporter:exporter_password@localhost:5432/fintech_credit_conveyor?sslmode=disable"
   ```
   Запустите экспортер:
   ```bash
   postgres_exporter
   ```

---

## **Шаг 2: Интеграция с Prometheus**
1. **Установите Prometheus**:
   ```bash
   sudo apt install prometheus -y
   ```

2. **Настройте `prometheus.yml`**:
   Откройте файл конфигурации:
   ```bash
   sudo nano /etc/prometheus/prometheus.yml
   ```
   Добавьте таргет для `postgres_exporter`:
   ```yaml
   scrape_configs:
     - job_name: 'postgres'
       static_configs:
         - targets: ['localhost:9187']
   ```

3. **Перезапустите Prometheus**:
   ```bash
   sudo systemctl restart prometheus
   ```

4. **Проверьте метрики**:
   Откройте браузер и перейдите на адрес Prometheus:
   ```
   http://localhost:9090
   ```
