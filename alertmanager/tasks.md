# Настройка и запуск Alertmanager для Prometheus
_Пользуемся официальной документацией на GitHub (в основном там прописаны Docker файлы на запуск, но всегда есть конфиги)_

### 1. **Установка Alertmanager**

#### a) Скачайте и установите Alertmanager:
Вы можете скачать последнюю версию Alertmanager с официального сайта [Prometheus](https://prometheus.io/download/) (директории указаны условно - имеем это ввиду, так что распаковку производим в вашу рабочую директорию).

```bash
# Создайте директорию для Alertmanager
mkdir -p /opt/alertmanager

# Скачайте бинарник (замените версию на актуальную)
wget https://github.com/prometheus/alertmanager/releases/download/v0.26.0/alertmanager-0.26.0.linux-amd64.tar.gz

# Распакуйте архив
tar xvf alertmanager-0.26.0.linux-amd64.tar.gz -C /opt/alertmanager

# Переименуйте директорию для удобства
mv /opt/alertmanager/alertmanager-0.26.0.linux-amd64 /opt/alertmanager/bin

# Добавьте исполняемые права
chmod +x /opt/alertmanager/bin/alertmanager
```

---

### 2. **Создание конфигурационного файла Alertmanager**

   - Alertmanager использует файл конфигурации `alertmanager.yml`, где вы можете настроить способы отправки уведомлений (например, через email, Slack, webhook и т.д.).
   - Вам нужно сделать конфиг на рабочие алерты для **Telegram**, разобраться как это сделать, у вас уже должен быть рабочий Node Exporter, который будет собирать метрики CPU, задача будет нагрузить CPU и увидеть как алерт прилетает в **Telegram**

#### Пример базового конфигурационного файла:

Создайте файл `/opt/alertmanager/alertmanager.yml` со следующим содержимым:

```yaml
global:
  resolve_timeout: 5m           # Время, через которое оповещение считается "разрешенным"

route:
  group_by: ['alertname']       # Группировка оповещений по имени
  group_wait: 30s               # Время ожидания перед отправкой первой группы
  group_interval: 5m            # Интервал между отправками новых групп
  repeat_interval: 1h           # Интервал повторной отправки оповещений
  receiver: 'default-receiver'  # Получатель оповещений 

receivers:
  - name: 'default-receiver'
    telegram_configs:
      - api_url: 'https://api.telegram.org/bot<YOUR_BOT_TOKEN>/sendMessage' # URL API Telegram
        chat_id: <YOUR_CHAT_ID> # ID чата в Telegram
        send_resolved: true     # Отправлять уведомления о разрешении проблемы

inhibit_rules:
  - source_match:
      severity: 'critical'
    target_match:
      severity: 'warning'
    equal: ['alertname', 'dev', 'instance']
```

**Объяснение параметров:**
- `resolve_timeout`: Время, через которое считается, что инцидент решен.
- `route`: Описывает логику маршрутизации уведомлений.
- `receivers`: Описывает методы отправки уведомлений.
- `inhibit_rules`: Правила подавления дублирующихся или менее важных алертов.

> **Примечание:** Если вы хотите использовать другие каналы уведомлений (например, email), добавьте соответствующие секции в `receivers`.

---

### 3. **Запуск Alertmanager**

Запустите Alertmanager из командной строки:

```bash
/opt/alertmanager/bin/alertmanager --config.file=/opt/alertmanager/alertmanager.yml
```

Проверьте, что Alertmanager работает, открыв его веб-интерфейс по адресу:  
[http://localhost:9093](http://localhost:9093)

Если все настроено правильно, вы увидите интерфейс Alertmanager.

---

### 4. **Интеграция Alertmanager с Prometheus**

Чтобы Prometheus мог отправлять алерты в Alertmanager, нужно настроить его конфигурацию.

#### Настройка `prometheus.yml`:

Откройте файл конфигурации Prometheus (`prometheus.yml`) и добавьте секцию `alerting`:

```yaml
alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - localhost:9093 # Адрес вашего Alertmanager
```

> **Важно:** Убедитесь, что порт `9093` открыт и доступен для Prometheus.

#### Перезапустите Prometheus:

```bash
systemctl restart prometheus
```

---

### 5. **Создание правил алертов в Prometheus**

Чтобы создать правила алертов, добавьте их в файл конфигурации Prometheus (`prometheus.yml`) или поместите в отдельную директорию.

#### Пример правила алерта:

Создайте файл `/etc/prometheus/rules/example.rules.yml`:

```yaml
groups:
  - name: example
    rules:
      - alert: HighCPUUsage
        expr: 100 - (avg by(instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage on {{ $labels.instance }}"
          description: "CPU usage is above 80% for more than 5 minutes."
```

Добавьте ссылку на этот файл в `prometheus.yml`:

```yaml
rule_files:
  - "/etc/prometheus/rules/*.rules.yml"   # Файл с правилами оповещений
```

Перезапустите Prometheus:

```bash
systemctl restart prometheus
```

---

### 6. **Тестирование алертов**

Чтобы проверить работу алертов:
1. Загрузите метрики в Prometheus так, чтобы они триггерили правило (например, искусственно увеличьте нагрузку на CPU).
2. Проверьте статус алертов в веб-интерфейсе Alertmanager ([http://localhost:9093](http://localhost:9093)).
3. Убедитесь, что уведомление пришло на указанный канал (Slack, email и т.д.).

---

### 7. **Настройка автозапуска Alertmanager**

Для удобства можно настроить автозапуск Alertmanager с помощью systemd.

#### Создайте файл службы:

```bash
sudo nano /etc/systemd/system/alertmanager.service
```

Добавьте следующее содержимое:

```ini
[Unit]
Description=Alertmanager
Wants=network-online.target
After=network-online.target

[Service]
User=prometheus
Group=prometheus
Type=simple
ExecStart=/opt/alertmanager/bin/alertmanager --config.file=/opt/alertmanager/alertmanager.yml
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

#### Перезагрузите systemd и запустите службу:

```bash
sudo systemctl daemon-reload
sudo systemctl start alertmanager
sudo systemctl enable alertmanager
```
