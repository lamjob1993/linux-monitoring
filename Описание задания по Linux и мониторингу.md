# Linux Monitoring: Руководство по Настройке Prometheus

## 1. **Работа с файловой системой и директориями**
- **/opt** — стандартная директория в Linux, предназначенная для хранения дополнительного программного обеспечения.
- **Создание директорий**: Используется команда `mkdir`. Например:
  ```bash
  sudo mkdir -p /opt/monitoring/linux-monitoring/prometheus/{bin,etc,data,consoles,console_libraries}
  ```
  Здесь `-p` позволяет создавать вложенные директории рекурсивно.
- **Права доступа**: 
  - Команда `chmod` используется для изменения прав доступа. Например, выдача прав `777` (полный доступ) на директорию `/opt`:
    ```bash
    sudo chmod -R 777 /opt
    ```
  - Права `777` означают, что владелец, группа и остальные пользователи имеют полные права на чтение, запись и выполнение.
- **Назначение владельца**: 
  - Команда `chown` используется для изменения владельца и группы файлов/директорий. Например:
    ```bash
    sudo chown -R prometheus:prometheus /opt
    ```

---

## 2. **Работа с архивами**
- **Скачивание архива**: Используется команда `wget` или `curl` для скачивания `.tar.gz` архива Prometheus.
- **Разархивирование**: Команда `tar` используется для распаковки архивов. Например:
  ```bash
  tar -xvzf prometheus-2.53.2.linux-amd64.tar.gz
  ```
  Здесь `-x` означает извлечение, `-v` — вывод процесса, `-z` — работа с gzip, `-f` — указание файла.

---

## 3. **Управление процессами**
- **Запуск процесса**: Пример запуска Prometheus:
  ```bash
  ./prometheus --config.file=/etc/prometheus.yml
  ```
- **Проверка запущенных процессов**: Команда `ps` используется для просмотра активных процессов. Например:
  ```bash
  ps aux | grep prometheus
  ```
- **Остановка процесса**: Команда `kill` используется для завершения процесса по его PID:
  ```bash
  kill <PID>
  ```

---

## 4. **Systemd и управление сервисами**
- **Создание Unit-файла**: Файл сервиса Prometheus создается в `/etc/systemd/system/prometheus.service`:
  ```ini
  [Unit]
  Description=Prometheus Monitoring
  After=network.target

  [Service]
  User=prometheus
  Group=prometheus
  ExecStart=/opt/monitoring/linux-monitoring/prometheus/bin/prometheus --config.file=/opt/monitoring/linux-monitoring/prometheus/etc/prometheus.yml
  Restart=always

  [Install]
  WantedBy=multi-user.target
  ```
- **Обновление systemd**: После создания или изменения Unit-файла необходимо выполнить:
  ```bash
  sudo systemctl daemon-reload
  ```
- **Управление сервисом**:
  - Запуск: `sudo systemctl start prometheus`
  - Проверка статуса: `sudo systemctl status prometheus`
  - Перезапуск: `sudo systemctl restart prometheus`

---

## 5. **Networking и диагностика**
- **Проверка портов**: Команда `ss` используется для просмотра открытых портов. Например:
  ```bash
  ss -tuln | grep 9090
  ```
- **Тестирование соединений**: Команда `telnet` проверяет доступность порта:
  ```bash
  telnet localhost 9090
  ```
- **HTTP-запросы**: Команда `curl` используется для отправки HTTP-запросов. Например:
  ```bash
  curl -X GET http://localhost:9090/api/v1/status/config
  ```

---

## 6. **Логи и их анализ**
- **Просмотр логов**: Команда `journalctl` используется для просмотра логов systemd:
  ```bash
  journalctl -u prometheus
  ```
- **Фильтрация логов**: Команда `grep` используется для фильтрации строк. Например:
  ```bash
  journalctl -u prometheus | grep "info"
  ```
- **Автоматизация сбора логов**: Использование `crontab` для периодического сбора логов:
  ```bash
  0 * * * * /path/to/save_logs.sh
  ```

---

## 7. **Автоматизация через Bash-скрипты**
- **Скрипт установки Prometheus**:
  ```bash
  #!/bin/bash
  wget https://github.com/prometheus/prometheus/releases/download/v2.53.2/prometheus-2.53.2.linux-amd64.tar.gz &&
  tar -xvzf prometheus-2.53.2.linux-amd64.tar.gz &&
  sudo mv prometheus-2.53.2.linux-amd64 /opt/monitoring/linux-monitoring/prometheus &&
  sudo systemctl daemon-reload &&
  sudo systemctl start prometheus &&
  echo "Prometheus успешно установлен и запущен" || { echo "Ошибка при установке"; exit 1; }
  ```
- **Скрипт удаления Prometheus**:
  ```bash
  #!/bin/bash
  sudo systemctl stop prometheus &&
  sudo rm -rf /opt/monitoring/linux-monitoring/prometheus &&
  sudo systemctl daemon-reload &&
  echo "Prometheus успешно удален" || { echo "Ошибка при удалении"; exit 1; }
  ```

---

## 8. **Миграция между серверами**
- **Настройка SSH**: Генерация ключей и копирование публичного ключа на удаленный сервер:
  ```bash
  ssh-keygen -t rsa
  ssh-copy-id user@remote_host
  ```
- **Передача файлов**: Использование `scp` для копирования архива:
  ```bash
  scp prometheus-archive.tar.gz user@remote_host:/tmp/
  ```
- **Распаковка и установка на новом сервере**:
  ```bash
  tar -xvzf /tmp/prometheus-archive.tar.gz -C /opt/monitoring/linux-monitoring/
  sudo chown -R prometheus:prometheus /opt
  sudo systemctl start prometheus
  ```

---

## 9. **Дебаг и устранение неполадок**
- **Поиск процессов**: `ps aux | grep prometheus`
- **Проверка портов**: `ss -tuln | grep 9090`
- **Тестирование HTTP-статусов**: `curl -X GET http://localhost:9090/api/v1/status/config`
- **Анализ логов**: `journalctl -u prometheus`

---
