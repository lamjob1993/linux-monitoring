# Monitoring

## Добро пожаловать в репозиторий по мониторингу

### Начало
- Этот репозиторий представляет собой на 75% задачник + необходимую теорию на 25%
- Глобально мы поднимем бэкенд мониторинга на основе: **Prometheus** и самописного банковского приложения
- Настроим фронтенд: **Grafana GUI** + **PromQL**
- И всё это разрезе **Linux** (Terminal Debian)

### Последовательность выполнения заданий
  1. Открываем директорию **`linux_install`** → `README.md` → `Список пакетов.md` → `Установка пакетов.md`
  2. Регистрируем и настраиваем доступ по `SSH` в `GitHub` по [инструкции](https://github.com/lamjob1993/linux-monitoring/blob/main/.files/%D0%93%D0%B5%D0%BD%D0%B5%D1%80%D0%B0%D1%86%D0%B8%D1%8F%20SSH%20%D0%B4%D0%BB%D1%8F%20GitHub.md)
  3. Открываем директорию **`prometheus`** → `README.md` → `beginning` → `tasks_1.md` → `tasks_2.md`
  4. Открываем директорию **`grafana`** → `README.md` → `tasks_1.md`
  5. Открываем директорию `node-exporter` → `README.md` → `tasks.md`
  6. Открываем директорию `pushgateway` → `README.md` → `tasks.md`
  7. Открываем директорию `prometheus-federate` → `README.md` → `tasks.md`
  8. Открываем директорию `alertmanager` → `README.md` → `tasks.md`
  9. Открываем директорию `process-exporter` → `README.md` → `tasks.md`
  10. Открываем директорию `blackbox-exporter` → `README.md` → `tasks.md`
  11. Открываем директорию `custom-exporter` → `README.md` → `tasks_1.md` → `tasks_2.md`
  12. **Открываем директорию** `postgresql` → `README.md` → `tasks.md`
  13. **Открываем директорию** `postgres_exporter` → `README.md` → `tasks.md`
  14. **Открываем директорию** `mimir` → `README.md` → `tasks.md`
  15. **Открываем директорию** `nginx` → `README.md` → `tasks.md`
  16. **Открываем директорию** `nginx-exporter` → `README.md` → `tasks.md`
  17. Открываем директорию `grafana` → `README.md` → `tasks_2.md`
  18. После исполнения всех пунктов:
      - У вас должна быть написана полная автоматизация на деплой бэкенда мониторинга
      - Должны быть построены дашборды для всех экспортеров, включая глобальный дашборд с ссылками на них
  19. Далее нужно будет создать от своего лица публичный репозиторий в **GitHub** на тему мониторинга, который будет служить для вас, как портфолио для работодателя (так называемый [Pet-проект](https://practicum.yandex.ru/blog/chto-takoe-pet-proekty-idei-dlya-novichkov/ "С помощью пет-проектов можно улучшить навыки и найти работу. Рассказываем, как их создавать, чем вдохновляться, а также какие у таких проектов есть плюсы и минусы."))

### О заданиях
**Задания написаны с техническим уклоном** в мониторинг и в `Linux` и таким образом, что о тех инструментах, которые в них используются спрашивают в 90% случаев на собеседованиях по части `Linux` у джунов:

- `DevOps/SRE`
- `Инженеров по сопровождению ПО`
- `Инженеров по мониторингу`
- `Администраторов Linux`
  
---

- Этот учебный репозиторий охватывает на 90% рутину вышеперечисленных должностей в базе
- Задания носят больше лабораторный характер, и я это понимаю, но они позволят наработать нужную практику для успешного прохождения собеседования. Где-то нужно будет подумать над заданиями, а где-то я даю подсказки
- Сразу всё задание со всеми пунктами через ChatGPT (Qwen) не прогоняем, иначе не пройдем собеседование
- Пользуемся Qwen только по точечным запросам, к примеру, `как работает команда на выдачу прав`, потому что это сильно быстрее, чем поиск в Google
- Делаем пункты строго по очереди и не перепрыгиваем

### GIT
- Мы будем работать с `Git`, научимся делать форк этого репозитория к себе в `GitHub` для последующего клона локально на ваш ПК:
  - Этот репозиторий специально сделан таким образом, чтобы сделать форк для вашего будущего проекта мониторинга
  - Настроим доступ по SSH до удаленного репозитория (который форкнули), иначе не получится пушить изменения на удаленный сервер
  - После любых успешных изменений в ваших конфиг-файлах и в коде будем пушить их в форкнутый репозиторий, то есть будем учиться сразу, как взрослые на практике, постепенно вплетая ежедневный прогресс в `GitHub`
  - Такая система контроля версий, как `GitHub` или её аналоги в виде `Bitbucket` и `GitLab` будут использоваться на любом IT-проекте, и с этой системой надо уметь работать на практике обязательно

### Окружение мониторинга

#### Backend

- Мы развернем бэкенд мониторинга в разрезе **Unit-сервисов** + поднимем балансир в виде **Nginx**
- Изучим сложные векторные схемы в разрезе мониторинга
- Поднимем **Prometheus** (познакомимся с моделями **Pull** и **Push**) + **Node Exporter** + **Alertmanager** + **All Exporters со всего репозитория** + автоматизируем процессы установки на **Bash** (а в дальнейшем научимся работать с **Ansible**)
- Напишем кастомные экспортеры (**Bash**) и разработаем свои самостоятельно (**Golang**)
- Разработаем базу данных **PostgreSQL** и развернем её, замониторив через **Postgres Exporter**
- Разберемся, как работает интерфейс **API** на практике, написав банковское приложение на **Python**, сняв с него метрики
- Горизантально смасштабируем **Prometheus** с помощью **Prometheus Federate** и **Mimir**
- Напишем (выпустим) тестовый блок сертификатов и замониторим их через **Blackbox Exporter**, а также пропингуем серверы
- Замониторим процессы с помощью **Process Exporter**
- Плавно перейдем от виртуализации и **Unit-сервисов** на контейнеризацию в разрезе **Docker** и поднимем наиболее сложный бэк с помощью **Docker Compose**
- CI/CD  # _(в работе)_
- Kubernetes/K8S  # _(в работе)_

#### Frontend

- Скачаем, подгрузим, нарисуем и разработаем дашборды в формате `JSON` для `Grafana` на основе метрик
  - Познакомимся с Data Source и с переменными в Grafana
- Изучим основы `Prometheus` и `PromQL` (базовый язык работы с БД `Prometheus`)
  - Будем применять на практике четыре золотых сигнала и изучим типы метрик
  - Выучим регулярные выражения
  - А также применим различные агрегации и функции

### Вывод

  - В настройку сети и **iptables** сильно углубляться не будем, так как у вас на работе будут готовые машины, на которых уже развёрнут софт и сетка уже давно растроена
  - Мы идем на **Juniour-Juniour+** специалиста, где по сетям особо гонять не будут, но это не значит, что не нужно знать основы, которые я даю на курсе
  - Скорее всего на должности инженера по сопровождению-мониторингу вас будет ждать условный кейс по миграции системы мониторинга, либо миграции какого угодно софта с уже настроенных серверов **CentOS** на голые **Ubuntu Server** и т.д

### Пожелания

Желаю удачи! Вы на правильном пути!
