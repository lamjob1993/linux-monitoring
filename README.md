# linux-monitoring

Здесь будут задачи по Linux, мониторингу и автоматизации

**Чатом GPT это задание не прогоняем! Иначе не пройдем собеседование на Linux! **

1. Взять за рабочую директорию ../home/name_user/Documents/ и склонировать в нее учебный репозиторий по выданной (подсказка: git clone)
2. Найти и скачать архив .tar.gz дистрибутива Prometheus самой последней второй (не третьей) версии в склонированную директорию ../home/name_user/Documents/monitoring_linux/prometheus/, то есть в директорию prometheus (подсказка GitHub, AMD64, bin)
2. Разархивировать архив и найти внутри бинарь Prometheus
3. Проверить версию Prometheus (./prometheus --version) и запустить бинарь "на коленке" (подсказка ./bin/prometheus или ./prometheus)
4. Проверить запущенный Прометей (Прометеус) на веб-морде (подсказка: проверка в браузере на порту :9090, чтобы понять по какому ip адресу стучаться в Прометеус, нужно знать ip адрес интерфейса своей тачки)
5. После успешной проверки создать рядом с бинарём prometheus директорию etc и положить туда пустой файл prometheus.yml - далее наполнить этот файл дефолтным конфигом (подсказка: GitHub - prometheus/documentation/examples/prometheus.yml)
6. Далее  написать Unit, а затем положить Unit файл Prometheus в директорию systemd автозапуска Linux (подсказка: логически понять как назвать этот файл и как он должен быть написан)
7. После того как положили Unit в systemd - выдать права 777 на файл (обычно такие права не выдаются, но у нас учебный проект, имеем это ввиду (одновременно идем в ИИ GPT Qwen и учимся выставлять числовые права)), сначала создать владельца prometheus, а затем изменить владельца файла юнита на prometheus
8. Далее запускаем сервис Prometheus утилитой systemctl, проверяем статус ACTIVE, а если INACTIVE, то идем переписывать Unit либо смотрим конфиг YAML в Prometheus, скорее всего ошиблись в одном из двух (если конфиг YAML дефолтный, то дело не в нём), а также читаем логи, чтобы понять почему INACTIVE
9. Затем выводим логи в консоль (параллельно с помощью Qwen читаем что такое stdin, stdout, stderr), которые отбрасывает запущенный Prometheus утилитой journalctl и парсим их утилитой grep в файл logs.log по ключевому слову info с верхнего и нижнего регистра (то есть конечный результат лога должен содержать только info)
10. Далее написать последовательный Bash скрипт (подсказка, не забыть выдать числовые права исполнения на файл), начиная с пункта 2 раздела до пункта 7, который поднимет Prometheus с нуля (придумать в скрипте свои директории, к примеру test_prometheus и сложить Prometheus туда)
11. 
