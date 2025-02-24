# Node Exporter
## Tasks

 - От вас требуется поднять `Node Exporter` способом из раздела [Prometheus](https://github.com/lamjob1993/linux-monitoring/blob/main/prometheus/Backend.md "Запускаем голый бинарь Prometheus, пишем юнит и простую автоматизацию
")
 - Можете модернизировать скрипт установщика `Prometheus`
 - Натравите на него `Prometheus`
 - Перейдите на страницу `/metrics` и удостоверьтесь, что экспортер поднялся
   - Либо используйте `curl` в терминале: `curl -k https://localhost:9100/metrics`
 - По заданию вам нужно замониторить: CPU, HDD, RAM, FS ...
 - Скачайте дашборд предназначенный для `Node Exporter` с сайта `Grafana Lab`
 - Подгрузите дашборд в `Grafana`, убедитесь, что он работает и сохраните
