# linux-monitoring

**Задание написано таким образом, что о тех инструментах, которые в нем используются, спрашивают более чем в 80% случаев на собеседовании по части Linux у джунов: DevOps, SRE, инженеров по сопровождению/мониторингу и администраторов Linux. Сразу всё задание со всеми пунктами через ChatGPT (Qwen) не прогоняем, иначе не пройдем собеседование (пользуемся только Qwen по точечным запросам, к примеру, как работает команда на выдачу прав, потому что это сильно быстрее, чем поиск в Google). Делаем пункты строго по очереди, не перепрыгиваем!**  

По заданию мы вручную распакуем архив с бинарём системы мониторинга **Prometheus**, опишем его автозапуск файлом юнита (Unit) и проверим запуск **Прометеуса** на веб-морде, параллельно проведя его дебаг. Далее напишем мини-автоматизацию этой рутины на **Bash** и сделаем тестовую миграцию на склонированную виртуальную машину **Ubuntu** (в будущих уроках затронем данную тему с помощью Ansible). В настройку сети и **iptables** углубляться не будем, так как у вас на работе будут готовые 50-100 тачек, на которых уже развёрнут софт и сетка уже давно растроена. Либо же будет условный кейс по миграции системы мониторинга и миграции чего угодно с серверов CentOS на голые Ubuntu Server или на голые SberLinux.

1. Первый пункт пока пропускаем, он в работе. Начинаем сразу с пункта 2. Взять за рабочую директорию **../home/name_user/Documents/** и склонировать в нее учебный репозиторий по выданной ссылке (подсказка: **git clone**)
2. Найти и скачать архив **.tar.gz** дистрибутива Prometheus для Linux самой последней второй (не третьей) версии в склонированную директорию **../home/name_user/Documents/monitoring_linux/prometheus/**, то есть в директорию **prometheus** (подсказка: GitHub, AMD64, bin)
3. Разархивировать архив и найти внутри директории бинарь **Prometheus**
4. Проверить версию **Prometheus** (подсказка: **./prometheus --version**) и запустить бинарь "на коленке" (подсказка: **./bin/prometheus** или **./prometheus**)
5. Проверить запущенный на коленке **Прометей** (Прометеус) на веб-морде (подсказка: проверка должна быть в браузере на порту **:9090**, чтобы понять по какому ip адресу стучаться в **Прометеус**, нужно знать ip адрес интерфейса своей тачки)
6. Создать директорию - **/bin** внутри директории - **../home/name_user/Documents/monitoring_linux/prometheus/** и скопировать в нее бинарь Prometheus (который запускали на коленке)
7. Далее создать в директории - **/prometheus** пустой файл - **prometheus.yml**, затем наполнить этот файл дефолтным конфигом Прометея (подсказка: GitHub - **prometheus/documentation/examples/prometheus.yml**, а также подумать, что означает этот конфиг на пару с Qwen GPT)
8. Далее создать пустой файл - **Unit** в директории - **/prometheus** и наполнить (на сленге - написать) его для **Prometheus** (подсказка: логически понять, как назвать Unit файл (это будет файл сервиса Прометеуса) и как он должен быть написан внутри)
9. Далее выдать права **777** на директорию **/prometheus** и на все файлы внутри (это называется рекурсивно), в которой уже должны лежать файлы: бинарь в директории **/bin**, конфиг Прометеуса и юнит Прометеуса (обычно такие права **777** не выдаются (либо выдаются в песочнице), но у нас учебный проект, поэтому имеем это ввиду (одновременно идем в ИИ GPT Qwen и учимся выставлять числовые права, заодно будем понимать, что такое 777))
10. Далее нужно создать группу пользователей **prometheus** и добавить туда пользователя **prometheus**, далее проверить эту группу пользователей, что **prometheus** добавился (одновременно идем в ИИ GPT Qwen и учимся назначать владельца на директорию и на файлы)
11. Затем рекурсивно назначить (изменить) владельца (пользователя) - **prometheus** для директории **/prometheus** и для всех файлов внутри
12. Затем скопировать Unit в директорию **/systemd** автозапуска Linux с уже выставленными правами **777** и владельцем **prometheus**
13. Чтобы система Linux поняла, что файл сервиса добавлен (Unit) в автозапуск - нужно вбить команду - **sudo systemctl daemon reload**, тем самым обновляя директорию systemd до актуального состояния (читаем подробно в Qwen про эту команду и заодно еще раз про пороцессы и демоны)
14. Далее запускаем сервис **Prometheus** утилитой **systemctl** (в дефолте эта утилита смотрит в автозапуск **systemd** и будет знать о том, что там лежит наш юнит), проверяем после запуска статус **ACTIVE** командой - **sudo systemctl status prometheus.service** и смотрим на работающую веб-морду, а если **INACTIVE**, то сразу читаем логи (смотрим следующий пункт темы), чтобы понять почему **INACTIVE** (подсказка: смотрим в **Unit** либо смотрим в конфиг **YAML** в **Prometheus**, скорее всего ошиблись в одном из двух)
15. Затем выводим логи **Prometheus** в терминал (параллельно с помощью Qwen читаем что такое **stdin**, **stdout**, **stderr**), которые отбрасывает запущенный **Prometheus** с помощью утилиты **journalctl** (смотрим в Qwen как это сделать)
16. Далее парсим (фильтруем) логи утилитой **grep** в файл **logs.log** по ключевому слову **info** с верхним и нижним регистром, то есть конечный результат лога должен содержать только строки с info (подсказка: **journalctl | grep** - используем перенаправление вывода из **journalctl** в **grep** с помощью пайпа - **|**)
17. Далее перезагружаем **Ubuntu-виртуалку** и проверяем автозапуск, что юнит автоматически стартовал сервис **Prometheus** - **sudo systemctl status prometheus.service**. После перезагрузки **Ubuntu** наш **Прометеус** должен подняться и вы увидите его интерфейс на веб-морде
18. Далее, так как мы подняли **Prometheus** и он работает - пробежимся по дебагу (просто представим, что приложению нужен дебаг, а-ля это инцидент в банке и его нужно решать, а **Прометей** у нас не работает): с помощью утилиты **ss** найдите **prometheus** и посмотрите на каком порту он сидит, заодно посмотрите какой это порт: **TCP** или **UDP**. С помощью утилиты **telnet** проверьте доступность соединения **Prometheus** по дефолтному порту Prometheus (подумайте как это сделать). С помощью утилиты - **curl** гетом (**GET**) скурлите (постучитесь GET-запросом) в **API Prometheus**, который должен вернуть **HTTP статус 2xx**, если сервису хорошо и **HTTP статус 5xx**, если плохо (заодно подтягиваем тему: методы и коды **HTTP**). А также в дебаг входит **journactl** и **systemctl status**
19. Далее написать **Bash** скрипт, начиная с пункта 2 текущей темы до старта сервиса Prometheus, включая написанный **Unit** и конфиг **Prometheus** в директории **/bin**. Этот скрипт в финале должен поднять **Prometheus** с нуля за секунды и вы должны увидеть его на веб-морде (придумать в скрипте свои директории, к примеру **test_prometheus_2** (а-ля свой проект, к примеру **Prometheus_2**) и сложить файлы **Prometheus** туда)
20. Прогнать готовый скрипт (не забыть удалить юнит из автозапуска и стопнуть поднятый Prometheus, который уже поднимали)
21. На данном этапе сохранить ваши текущие изменения и выключить виртуалку
22. Далее склонировать вашу выключенную виртуальную машину **Ubuntu**, назвать ее **Ubuntu Clone** и запустить ее рядом с вашей первой Ubuntu одновременно
23. Далее подумать, как с помощью утилиты **SCP** перекинуть рабочий и подготовленный архив **Prometheus** (подумайте, как запаковать его уже с выданными правами и конфигами, в общем Prometheus должен быть готов к запуску по вашему скрипту на новой тачке (тачками называют машины и серверы - это синонимы)) с тачки А на склонированную тачку Б
24. Финал. Прогнать готовый скрипт
25. В Сбербанке эта задача была моим первым кейсом на должности разработчика мониторинга. На задачу мне дали 2 дня. На третий день уже была миграция. **Мой уровень был**: умею создавать файлы, переходить в директории, запускаю скрипты (не пишу), знаю как сохранить файл и выйти из Vim, знаю как выставлять права на файлы и распаковываю архивы
