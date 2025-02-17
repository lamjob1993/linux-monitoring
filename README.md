# linux-monitoring

_Задание написано таким образом, чтобы понять 80% базы Linux, которой точно хватит для прохождения собеседования в части Linux!_

По заданию мы вручную распакуем бинарь системы мониторинга Prometheus, опишем его автозапуск файлом юнита и проверим запуск Прометеуса на веб-морде. Далее напишем мини-автоматизацию этой рутины и сделаем тестовую миграцию на склонированную виртуальную машину Ubuntu. 

**Полностью через ChatGPT это задание не прогоняем, иначе не пройдем собеседование по части Linux! Делаем пункты по очереди, не перепрыгиваем!** 

1. Взять за рабочую директорию **../home/name_user/Documents/** и склонировать в нее учебный репозиторий по выданной ссылке (подсказка: **git clone**)
2. Найти и скачать архив **.tar.gz** дистрибутива Prometheus для Linux самой последней второй (не третьей) версии в склонированную директорию **../home/name_user/Documents/monitoring_linux/prometheus/**, то есть в директорию prometheus (подсказка: GitHub, AMD64, bin)
3. Разархивировать архив и найти внутри директории бинарь Prometheus
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
16. Далее парсим (фильтруем) логи утилитой **grep** в файл **logs.log** по ключевому слову **info** с верхним и нижним регистром, то есть конечный результат лога должен содержать только строки с info (подсказка: **journalctl | grep** - используем перенаправление вывода из **journalctl** в **grep** с помощью пайпа - |)
17. Далее перезагружаем **Ubuntu-виртуалку** и проверяем автозапуск, что юнит автоматически стартовал сервис **Prometheus** - **sudo systemctl status prometheus.service**. После перезагрузки **Ubuntu** - **Прометеус** должен подняться и вы увидите его интерфейс в 
18. Далее написать **Bash** скрипт, начиная с пункта 2 текущей темы до старта сервиса Prometheus, включая написанный **Unit** и конфиг **Prometheus** в директории **/bin**. Этот скрипт в финале должен поднять **Prometheus** с нуля и вы должны увидеть его на веб-морде (придумать в скрипте свои директории, к примеру test_prometheus (а-ля свой проект, к примеру Prometheus_2) и сложить файлы **Prometheus** туда)
19. На данном этапе сохранить ваши текущие изменения и выключить виртуалку, далее склонировать вашу выключенную виртуальную машину (Ubuntu), назвать ее Ubuntu Clone и запустить ее рядом с вашей первой Ubuntu одновременно
20. Далее подумать, как с помощью утилиты **SCP** перекинуть файлы с тачки А на склонированную тачку Б
21. Далее написать **Bash** скрипт, начиная с пункта 2 текущей темы до старта сервиса Prometheus. Этот скрипт в финале должен поднять Prometheus с нуля (придумать в скрипте свои директории, к примеру test_prometheus (а-ля свой проект) и сложить Prometheus туда)
22. Прогнать готовый скрипт (не забыть удалить юнит из автозапуска и стопнуть поднятый Prometheus, который уже поднимали)
