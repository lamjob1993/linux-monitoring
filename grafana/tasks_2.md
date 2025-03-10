# Grafana

_Эта директория выполняется в самом конце курса._

## Tasks

### [Примеры дашбордов](https://play.grafana.org/dashboards)

### Создайте новый дашборд
Под названием `prometheus_dashboard` в вашей папке и потренируйтесь переносить виджеты на свой дашборд с дашборда `Prometheus` (экспортеры пока не используем, `Prometheus` может мониторить сам себя и отбрасывать метрики):

**Уровень**: Низкий
   - Скопируйте 4 виджета
   - Потренируйтесь менять размер виджетов
   - Поменяйте скопированные виджеты на кастом варианты в настройках виджетов (поиграйте, как в песочнице: с цветом, типами виджетов и т.д)
   - Сделайте ссылку-переход с оригинального дашборда `Prometheus` на ваш дашборд

---

### На основе изученного материала, сделайте задания ниже:
  
**Уровень**: Низкий
   - Перейдите на страницу `Node Exporter` по адресу `/metrics`
   - Найдите в списке метрик 4 типа метрик, ссылаясь на **4 золотых сигнала**
   - Выведите метрики на дашборд и нарисуйте нужные виджеты
   - Сделайте **агрегацию** ваших метрик и возьмите в работу **функции**
   - Сохраните дашборд `node_exporter_dashboard`

---

**Уровень**: Низкий
   - Натравите `Prometheus` на все экспортеры, написав один длинный конфиг-файл, и замониторьте ваш сервер (вашу тачку) в `Grafana`
   - Сделайте один глобальный дашборд, который называется `All_Exporters` со ссылками на мониторинг ваших отдельных дашбордов для каждого экспортера и подумайте над визуалом странички этого дашборда, можно красиво вывести слева ссылку на дашборд, а справа маленький превью-виджет с сылками на:
     - `prometheus`
     - `node-exporter`
     - `process-exporter`
     - `blackbox-exporter`
     - `alertmanager`
     - `И так далее`

---

**Уровень**: Низкий
   - Подумайте логически и соберите еще один дашборд `Monitoring_Global` из всех экспортеров сразу в одном месте
   - Постройте логику таким образом, чтобы данные с дашборда хорошо читались
   - Сверху вниз и слева направо без разрывов, с симметричными виджетами и одинаковыми размерами
   - Это будет один дашборд, набитый разными виджетами и разными метриками со всех экспортеров
   - Например, можно взять логику дашборда сверху вниз:
       - `Node Exporter` выводит значения `CPU + RAM + HDD` сервера и схлопывается под шторку
       - `Process Exporter` выводит текущие процессы сервера и схлопывается под шторку
       - `BlackBox Exporter` мониторит ваши серверы и схлопывается под шторку
       - `И так далее`
