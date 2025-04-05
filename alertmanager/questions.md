### **Базовые вопросы к собеседованию**

1. **Что такое Alertmanager? Для чего он используется?**  
   Alertmanager — это компонент Prometheus, который управляет алертами: группирует их, устраняет дублирование и отправляет уведомления в различные каналы (например, Slack, Email, PagerDuty). Он используется для централизованного управления алертингом.

2. **Какие основные функции выполняет Alertmanager?**  
   - Группировка алертов.  
   - Дедупликация (удаление дубликатов).  
   - Отправка уведомлений через различные каналы.  
   - Поддержка таймаутов и повторных уведомлений.  

3. **Как Alertmanager работает с Prometheus?**  
   Prometheus генерирует алерты на основе правил (`alerting rules`) → Передаёт алерты в Alertmanager → Alertmanager обрабатывает их и отправляет уведомления.

4. **На каком порту работает Alertmanager по умолчанию?**  
   По умолчанию Alertmanager работает на порту **9093**.

5. **Как проверить, что Alertmanager корректно работает?**  
   Откройте браузер или используйте `curl` для запроса статуса:  
   ```
   http://<alertmanager-ip>:9093
   ```

---

### **Настройка и конфигурирование**

6. **Как установить Alertmanager?**  
   Используйте Docker (`docker run prom/alertmanager`), скачайте бинарный файл с официального сайта или установите через пакетный менеджер (например, `apt` или `yum`).

7. **Как настроить Alertmanager для работы с Prometheus?**  
   Настройте файл `prometheus.yml`:  
   ```yaml
   alerting:
     alertmanagers:
       - static_configs:
           - targets:
               - <alertmanager-ip>:9093
   ```

8. **Как запустить Alertmanager в фоновом режиме?**  
   Используйте systemd для управления Alertmanager:  
   Создайте файл `/etc/systemd/system/alertmanager.service` с содержимым:  
   ```ini
   [Unit]
   Description=Alertmanager

   [Service]
   ExecStart=/usr/local/bin/alertmanager --config.file=/etc/alertmanager/alertmanager.yml

   [Install]
   WantedBy=multi-user.target
   ```
   Запустите службу:  
   ```bash
   systemctl start alertmanager
   systemctl enable alertmanager
   ```

9. **Как изменить порт Alertmanager?**  
   Запустите Alertmanager с флагом `--web.listen-address`:  
   ```bash
   ./alertmanager --web.listen-address=":9100"
   ```

10. **Как ограничить доступ к Alertmanager?**  
    Настройте firewall или reverse proxy (например, Nginx) для ограничения доступа к порту 9093.

---

### **Группировка и маршрутизация алертов**

11. **Что такое группировка алертов в Alertmanager?**  
    Группировка объединяет несколько алертов в одно уведомление. Это помогает избежать спама уведомлениями.

12. **Как настроить группировку алертов?**  
    Настройте файл `alertmanager.yml`:  
    ```yaml
    route:
      group_by: ['alertname', 'cluster']
      group_wait: 30s
      group_interval: 5m
      repeat_interval: 3h
    ```

13. **Что такое маршрутизация алертов?**  
    Маршрутизация определяет, куда отправлять алерты, на основе меток (labels). Например, алерты для разных команд могут отправляться в разные каналы.

14. **Как настроить маршрутизацию алертов?**  
    Настройте файл `alertmanager.yml`:  
    ```yaml
    route:
      receiver: 'default-receiver'
      routes:
        - match:
            team: 'frontend'
          receiver: 'frontend-receiver'
        - match:
            team: 'backend'
          receiver: 'backend-receiver'
    ```

15. **Что такое `group_wait`, `group_interval` и `repeat_interval`?**  
    - `group_wait`: Время ожидания перед отправкой первого уведомления.  
    - `group_interval`: Интервал между отправками новых уведомлений для группы.  
    - `repeat_interval`: Интервал повторной отправки уведомлений для одного алерта.

---

### **Уведомления и каналы**

16. **Какие каналы уведомлений поддерживает Alertmanager?**  
    Email, Slack, PagerDuty, OpsGenie, Webhook, Telegram, VictorOps.

17. **Как настроить отправку уведомлений в Slack?**  
    Настройте файл `alertmanager.yml`:  
    ```yaml
    receivers:
      - name: 'slack-notifications'
        slack_configs:
          - api_url: 'https://hooks.slack.com/services/...'
            channel: '#alerts'
            send_resolved: true
    ```

18. **Как настроить отправку уведомлений на Email?**  
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

19. **Как настроить повторяющиеся уведомления?**  
    Настройте параметр `repeat_interval` в `alertmanager.yml`. Например:  
    ```yaml
    repeat_interval: 1h
    ```

20. **Как настроить отправку уведомлений через Webhook?**  
    Настройте файл `alertmanager.yml`:  
    ```yaml
    receivers:
      - name: 'webhook-notifications'
        webhook_configs:
          - url: 'http://example.com/webhook'
    ```

---

### **Продвинутые вопросы**

21. **Как использовать метки (labels) для маршрутизации алертов?**  
    Настройте `match` или `match_re` в файле `alertmanager.yml`. Пример:  
    ```yaml
    routes:
      - match:
          severity: 'critical'
        receiver: 'critical-receiver'
    ```

22. **Как настроить молчание (silences) в Alertmanager?**  
    Используйте UI Alertmanager → Перейдите в раздел "Silences" → Создайте правило для игнорирования алертов.

23. **Как настроить интеграцию Alertmanager с Grafana?**  
    Используйте плагин Grafana для Alertmanager → Настройте источник данных Alertmanager.

24. **Как мониторить сам Alertmanager?**  
    Используйте встроенные метрики Alertmanager (например, `alertmanager_alerts`). Интегрируйте их с Prometheus.

25. **Как настроить высокую доступность (High Availability) для Alertmanager?**  
    Запустите несколько экземпляров Alertmanager → Настройте общее хранилище для состояния (например, через меш-сеть или shared storage).
