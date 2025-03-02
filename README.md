# Monitoring

## Добро пожаловать в репозиторий Linux

### Начало

- В этом репозитории мы научимся настраивать связку мониторинга в разрезе **Linux**
- Мы поднимем бэкенд мониторинга на основе **Prometheus** и настроим фронтенд в разрезе **Grafana GUI**


### Последовательность выполнения следующая
  1. Зарегистрируйтесь и настройте доступ по `SSH` в `GitHub` [по инструкции](https://github.com/lamjob1993/linux-monitoring/blob/main/%D0%93%D0%B5%D0%BD%D0%B5%D1%80%D0%B0%D1%86%D0%B8%D1%8F%20SSH%20%D0%B4%D0%BB%D1%8F%20GitHub.md)
  2. Открываем директорию `prometheus` → `README.md` → `beginning` → `tasks.md`
  3. Открываем директорию `grafana` → `README.md` → `tasks_1.md`
  4. Открываем директорию `node-exporter` → `README.md` → `tasks.md`
  5. Открываекм директорию `prometheus-federate` → `README.md` → `tasks.md` → `После проверки закомментировать федерацию в основном конфиге`
  6. **Открываекм директорию** `pushgateway` → `README.md` → `tasks.md` 
  7. **Открываекм директорию** `custom-exporter` → `README.md` → `tasks.md`
  8. **Открываем директорию** `process-exporter` → `README.md` → `tasks.md`
  9. **Открываекм директорию** `blackbox-exporter` → `README.md` → `tasks.md`
  10. **Открываекм директорию** `nginx` → `README.md` → `tasks.md`
  11. **Открываекм директорию** `nginx-exporter` → `README.md` → `tasks.md`
  12. **Открываем директорию** `alertmanager` → `README.md` → `tasks.md`
  13. Открываем директорию `grafana` → `README.md` → `tasks_2.md`
  14. После исполнения всех пунктов полностью настройте бэкенд мониторинга и дашборды для всех экспортеров:

### О заданиях

**Задания написаны с техническим уклоном** в мониторинг и в `Linux` и таким образом, что о тех инструментах, которые в них используются спрашивают в 90% случаев на собеседованиях по части `Linux` у джунов:

- `DevOps/SRE`
- `Инженеров по сопровождению ПО`
- `Инженеров по мониторингу`
- `Администраторов Linux`
  
---

- Если грубо говоря, то этот учебный репозиторий охватывает на 90% рутину вышеперечисленных должностей в базе
- Задания носят больше лабораторный характер, и я это понимаю, но они позволят наработать нужную практику для успешного прохождения собеседования. Где-то нужно будет подумать над заданиями, а где-то я даю подсказки
- Сразу всё задание со всеми пунктами через [ChatGPT (Qwen)](https://chat.qwenlm.ai/ "Переход на оф. сайт Qwen.") не прогоняем, иначе не пройдем собеседование (пользуемся только Qwen по точечным запросам, к примеру, `как работает команда на выдачу прав`, потому что это сильно быстрее, чем поиск в Google)
- Делаем пункты строго по очереди, не перепрыгиваем!

### GIT
---
- Мы частично поработаем с `Git`, научимся делать [форк](https://github.com/lamjob1993/linux-monitoring/blob/main/%D0%A4%D0%BE%D1%80%D0%BA%20%D0%B2%20GitHub.md "Форк (Fork) — собственное ответвление (fork) какого-то проекта. Это означает, что GitHub создаст вашу собственную копию проекта, данная копия будет находиться в вашем пространстве имён, и вы сможете легко делать изменения путём отправки (push) изменений.") этого учебного репозитория к себе в `GitHub` для последующего клона локально на свой ПК:
  - Этот репозиторий специально сделан таким образом, чтобы сделать форк для вашего будущего проекта мониторинга
  - Настроим доступ по [SSH](https://github.com/lamjob1993/linux-monitoring/blob/main/%D0%93%D0%B5%D0%BD%D0%B5%D1%80%D0%B0%D1%86%D0%B8%D1%8F%20SSH%20%D0%B4%D0%BB%D1%8F%20GitHub.md "Генерация нового ключа SSH и добавление его в ssh-agent.") с вашего рабочего ПК до удаленного репозитория (который форкнули), иначе не получится [пушить](https://git-scm.com/book/ru/v2/%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D1%8B-Git-%D0%A0%D0%B0%D0%B1%D0%BE%D1%82%D0%B0-%D1%81-%D1%83%D0%B4%D0%B0%D0%BB%D1%91%D0%BD%D0%BD%D1%8B%D0%BC%D0%B8-%D1%80%D0%B5%D0%BF%D0%BE%D0%B7%D0%B8%D1%82%D0%BE%D1%80%D0%B8%D1%8F%D0%BC%D0%B8 "Когда вы хотите поделиться своими наработками, вам необходимо отправить их в удалённый репозиторий. Команда для этого действия простая: git push <remote-name> <branch-name>.") изменения на ваш удаленный сервер
  - После любых успешных изменений в ваших конфиг-файлах и в коде будем пушить их в ваш форкнутый репозиторий, то есть будем учиться сразу, как взрослые на практике
  - Такая система, как `Bitbucket` и ее аналоги `GitHub`, `GitLab` будет на любом ИТ проекте 100% и с ней надо уметь минимально работать на практике

### Автоматизация, установка и запуск сервисов
---
- По заданиям мы скачаем и вручную распакуем архивы с бинарями: `системы мониторинга Prometheus`, `Grafana GUI`, `экспортера Node Exporter` и прочих экспортеров
- Опишем их автозапуск файлами юнитов `Unit`
- Проверим запуск бэкенда мониторинга на веб-морде, параллельно проводя дебаг каждого приложения
- Далее напишем мини-автоматизацию этой рутины на `Bash`
- В будущих уроках затронем тему автоматизации с помощью `Ansible`

### Настройка окружения мониторинга

#### Backend
---
- В разрезе настройки бэкенда мониторинга: пропишем `Prometheus`, как **data source** в `Grafana` и натравим `Prometheus` на `Node Exporter` и на прочие экспортеры (когда `Prometheus` собирает данные с экспортеров - это называется скрэйпинг (scrape), помним о том, что экспортеры в сам `Prometheus` ничего не отправляют, `Prometheus` опрашивает их по протоколу `HTTP` на основе таргетов (targets) своего же конфиг-файла)
- **Напишем нагрузочное тестирование** [Pushgateway](https://github.com/prometheus/pushgateway "Pushgateway — это компонент экосистемы Prometheus, предназначенный для приема и хранения метрик, которые нельзя собирать традиционным способом через pull-модель (т.е., когда Prometheus сам запрашивает данные у целевого сервиса). Pushgateway позволяет приложениям или скриптам отправлять (push) метрики на специальный промежуточный сервер, откуда их уже может собирать Prometheus.") через проброс метрик утилитой `Curl`:
  - Метрики будем генерить скриптом `Bash` в формате [Open Metrics](https://github.com/prometheus/OpenMetrics/tree/main "OpenMetrics представляет собой эволюцию формата Prometheus для представления метрик, сохраняя при этом совместимость с уже существующими инструментами и данными.")
  - Скрипт будет подсчитывать количество метрик запушенных в `Prometheus`
  - На вход скрипту можно будет задать интересующее количество метрик
  - Скрипт будет распараллелен по потокам процессора
  - Будет задание на подумать, как мониторить максимальную нагрузку на железо во время отработки скрипта:
    - Это и будет нагрузочным тестированием, когда надо будет посчитать, к примеру: сколько уходит `RAM` на каждые миллион метрик запушенных в `Pushgateway` 
- **Научимся работать с кастомными метриками**, задействуя [Textfile Collector](https://github.com/prometheus/node_exporter "Textfile Collector — это дополнительный компонент Node Exporter , который позволяет экспортировать метрики, записанные в текстовые файлы на диске, в формате, понятном для Prometheus. Это удобный способ собирать данные, которые не могут быть получены напрямую через системные вызовы или интерфейсы, но могут быть сгенерированы скриптами или другими программами.") в `Node Exporter`

#### Frontend
---
- Скачаем и подгрузим дашборды в формате `JSON` в `Grafana`:
  - Изучим минимальные основы `PromQL` (базовый язык работы с БД TSDB в `Prometheus`)
  - [Изучим четыре золотых сигнала](https://github.com/lamjob1993/linux-monitoring/tree/main/prometheus "Как работает Prometheus и для чего он нужен") (4 Golden Signals) и научимся применять их на практике
  - Нарисуем вручную дашборды и виджеты для экспортеров:
    - Возьмем метрики с каждой инстанции мониторинга: `Prometheus`, `Grafana`, `Node Exporter` и т.д:
      - Научимся выводить их на дашборд, а также применять агрегацию и функции `PromQL`

### Вывод
---
  - Мы проработаем, как разрез настройки бэкенда `Prometheus` + `Node Exporter` + `Exporters`, так и разрез фронтенда `Grafana GUI` + `PromQL`
  - В настройку сети и `iptables` углубляться не будем, так как у вас на работе будут готовые 50-100 тачек, на которых уже развёрнут софт и сетка уже давно растроена
  - Мы идем на **джун-джун+** специалиста, где по сетям особо гонять не будут, но это не значит, что не нужно знать основы, которые я даю на курсе
  - Скорее всего вас на должности инженера будет ждать условный кейс по миграции системы мониторинга либо миграции чего угодно с серверов `CentOS` на голые `Ubuntu Server`

### Пожелания
---
Желаю удачи, вы на правильном пути!
