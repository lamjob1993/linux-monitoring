# **Технические вопросы о Alertmanager к собеседованию**

1. **Как Alertmanager обрабатывает дублирующиеся алерты?**  
   Alertmanager автоматически удаляет дубликаты алертов, если они имеют одинаковые метки (labels).

2. **Как настроить группировку алертов в Alertmanager?**  
   Настройте параметр `group_by` в файле `alertmanager.yml`. Пример:  
   ```yaml
   group_by: ['alertname', 'cluster']
   ```

3. **Что такое `group_wait` и как он влияет на отправку уведомлений?**  
   `group_wait` определяет время ожидания перед отправкой первого уведомления для группы алертов.

4. **Как настроить интервал между отправками новых уведомлений для группы алертов?**  
   Используйте параметр `group_interval` в `alertmanager.yml`. Пример:  
   ```yaml
   group_interval: 5m
   ```

5. **Как настроить повторную отправку уведомлений для одного алерта?**  
   Используйте параметр `repeat_interval` в `alertmanager.yml`. Пример:  
   ```yaml
   repeat_interval: 1h
   ```

6. **Как маршрутизировать алерты в зависимости от их меток?**  
   Настройте маршруты в `alertmanager.yml` с использованием параметров `match` или `match_re`. Пример:  
   ```yaml
   routes:
     - match:
         severity: 'critical'
       receiver: 'critical-receiver'
   ```

7. **Как использовать регулярные выражения для маршрутизации алертов?**  
   Используйте параметр `match_re` для маршрутизации алертов по шаблонам меток. Пример:  
   ```yaml
   routes:
     - match_re:
         service: 'web|api'
       receiver: 'team-receiver'
   ```

8. **Как настроить молчание (silences) в Alertmanager?**  
   Используйте UI Alertmanager → Перейдите в раздел "Silences" → Создайте правило для игнорирования алертов.

9. **Как настроить отправку уведомлений через Webhook?**  
   Настройте файл `alertmanager.yml`:  
   ```yaml
   receivers:
     - name: 'webhook-notifications'
       webhook_configs:
         - url: 'http://example.com/webhook'
   ```

10. **Как интегрировать Alertmanager с Slack?**  
    Настройте файл `alertmanager.yml`:  
    ```yaml
    receivers:
      - name: 'slack-notifications'
        slack_configs:
          - api_url: 'https://hooks.slack.com/services/...'
            channel: '#alerts'
            send_resolved: true
    ```

11. **Как настроить отправку уведомлений на Email?**  
    Настройте файл `alertmanager.yml`:  
    ```yaml
    receivers:
      - name: 'email-notifications'
        email_configs:
          - to: 'team@example.com'
            from: 'alertmanager@example.com'
            smarthost: 'smtp.example.com:587'
            auth_username: 'user'
            auth_password: 'password'
    ```

12. **Как настроить отправку уведомлений через PagerDuty?**  
    Настройте файл `alertmanager.yml`:  
    ```yaml
    receivers:
      - name: 'pagerduty-notifications'
        pagerduty_configs:
          - routing_key: 'your-routing-key'
    ```

13. **Как настроить отправку уведомлений через OpsGenie?**  
    Настройте файл `alertmanager.yml`:  
    ```yaml
    receivers:
      - name: 'opsgenie-notifications'
        opsgenie_configs:
          - api_key: 'your-api-key'
    ```

14. **Как настроить отправку уведомлений через Telegram?**  
    Настройте файл `alertmanager.yml`:  
    ```yaml
    receivers:
      - name: 'telegram-notifications'
        telegram_configs:
          - api_url: 'https://api.telegram.org'
            bot_token: 'your-bot-token'
            chat_id: 'your-chat-id'
    ```

15. **Как настроить отправку уведомлений через VictorOps?**  
    Настройте файл `alertmanager.yml`:  
    ```yaml
    receivers:
      - name: 'victorops-notifications'
        victorops_configs:
          - api_key: 'your-api-key'
            routing_key: 'your-routing-key'
    ```

16. **Как настроить таймауты для каналов уведомлений в Alertmanager?**  
    Укажите параметр `send_timeout` для каждого канала в `alertmanager.yml`. Пример:  
    ```yaml
    webhook_configs:
      - url: 'http://example.com/webhook'
        send_timeout: 10s
    ```

17. **Как настроить высокую доступность (High Availability) для Alertmanager?**  
    Запустите несколько экземпляров Alertmanager → Настройте общее хранилище состояния (например, через меш-сеть или shared storage).

18. **Как Alertmanager решает, какой канал уведомлений использовать для алерта?**  
    Alertmanager использует маршрутизацию, определённую в файле `alertmanager.yml`, на основе меток алертов.

19. **Как настроить логирование для Alertmanager?**  
    Используйте параметр `--log.level` при запуске Alertmanager. Пример:  
    ```bash
    ./alertmanager --log.level=debug
    ```

20. **Как мониторить сам Alertmanager?**  
    Используйте встроенные метрики Alertmanager (например, `alertmanager_alerts`) → Интегрируйте их с Prometheus.

21. **Как настроить резервное копирование конфигурации Alertmanager?**  
    Регулярно сохраняйте файл `alertmanager.yml` и данные состояния (если используется shared storage).

22. **Как настроить отправку уведомлений только для разрешённых алертов?**  
    Используйте параметр `send_resolved` в конфигурации каналов уведомлений. Пример:  
    ```yaml
    slack_configs:
      - api_url: 'https://hooks.slack.com/services/...'
        send_resolved: true
    ```

23. **Как настроить переопределение меток алертов в Alertmanager?**  
    Испуйте секцию `relabel_configs` в `alertmanager.yml`. Пример:  
    ```yaml
    relabel_configs:
      - source_labels: [severity]
        target_label: priority
        replacement: 'high'
    ```

24. **Как настроить интеграцию Alertmanager с Grafana?**  
    Используйте плагин Grafana для Alertmanager → Настройте источник данных Alertmanager.

25. **Как проверить корректность конфигурации Alertmanager?**  
    Используйте команду `amtool check-config` для проверки файла `alertmanager.yml`.
