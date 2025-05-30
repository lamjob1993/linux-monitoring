# Prometheus Backend

_Пользуемся официальной документацией на GitHub (в основном там прописаны Docker файлы на запуск и всегда есть конфиги)_

- Перед выполнением задания нужно пробежаться по [мини-курсу от Selectel по Bash](https://selectel.ru/blog/tutorials/linux-bash-scripting-guide/). Попробовать написать первый скрипт, запустить его, пощупать циклы и переменные и этого достаточно (можно на пару с ИИ). 

- Читаем правила [Пункт 2](https://github.com/lamjob1993/linux-monitoring/blob/main/navigation/others/%D0%9F%D1%80%D0%B5%D0%B4%D0%B8%D1%81%D0%BB%D0%BE%D0%B2%D0%B8%D0%B5%20%D0%BA%20%D0%BA%D1%83%D1%80%D1%81%D1%83.md).

## Tasks

### Запускаем голый бинарь Prometheus, пишем юнит и простую автоматизацию

1. Изначально у вас должна быть установлена первичная `виртуалка А` в виде `Debian 12.9.0` на английском языке:
   - После установки склонируйте её - это будет `виртуалка Б` и продолжайте работать на `виртуалке А`
   - В идеале сделать еще один клон с `виртуалкой С` и вообще его не трогать, чтобы она была, как резервная и `чистая ОС` на всякий случай
2. Взять директорию из корня за основную рабочую `/opt` (является частью стандартной файловой системы и предназначена для хранения дополнительного программного обеспечения):
   - Сделать себе в аккаунт **GitHub** [форк](https://github.com/lamjob1993/linux-monitoring/blob/main/.files/%D0%A4%D0%BE%D1%80%D0%BA%20%D0%B2%20GitHub.md) репозитория [linux-monitoring](https://github.com/lamjob1993/linux-monitoring), если не успели сделать до этого
   - Далее склонировать ваш форкнутый репозиторий `linux-monitoring` в свою домашнюю директорию, к примеру в `/Documents`:
      - Должна получиться домашняя клон-директория репозитория `/Documents/linux-monitoring/`:

                          /linux-monitoring      
                          ├── grafana             # Директория Grafana         
                          ├── node-exporter       # Директория Node Exporter
                          ├── prometheus          # Директория Prometheus
                          ├── e.t.c               # Остальные директории
        
3. Далее найти и скачать архив `.tar.gz` дистрибутива `Prometheus` для `Linux` самой последней второй (не третьей) версии в домашнюю директорию рядом со склонированным репозиторием `/Documents/linux-monitoring` (подсказка: GitHub, AMD64, bin)
4. Разархивировать архив и найти внутри директории бинарь `Prometheus` (директория после разархивации будет выглядеть, к примеру, вот так `/Documents/prometheus-2.53.2.linux-amd64`)
5. Проверить версию `Prometheus` (подсказка: `./prometheus --version` и запустить бинарь "на коленке" подсказка: `./bin/prometheus` или `./prometheus`)
6. Проверить запущенный на коленке `Prometheus` на веб-морде (подсказка: проверка должна быть в браузере на порту `:9090`, чтобы понять по какому ip адресу стучаться в `Prometheus`, нужно знать ip адрес интерфейса своей тачки (тачками называют машины и серверы - это синонимы))
7. Затем скопировать из директории `/Documents/prometheus-2.53.2.linux-amd64` в домашнюю директорию `/Documents/linux-monitoring/prometheus` файлы:
 
                                /prometheus      
            НЕ КОПИРОВАТЬ       ├── prometheus.yml                    # ЭТОТ ФАЙЛ НУЖНО БУДЕТ СОЗДАТЬ САМОСТОЯТЕЛЬНО ПУСТЫМ / Основной конфигурационный файл Prometheus
                                ├── prometheus                        # Бинарный файл Prometheus
                                ├── data                              # Директория, куда Prometheus пишет данные временных рядов
                                ├── consoles/                         # Директория для шаблонов консолей Prometheus
                                │   ├── index.html.example            # Пример главной страницы
                                │   ├── node-cpu.html                 # Шаблон консоли для мониторинга CPU узла
                                │   ├── node-disk.html                # Шаблон консоли для мониторинга диска узла
                                │   ├── node.html                     # Общий шаблон консоли для узла
                                │   ├── node-overview.html            # Обзорная консоль для узла
                                │   ├── prometheus.html               # Шаблон консоли для Prometheus
                                │   └── prometheus-overview.html      # Обзорная консоль для Prometheus
                                ├── console_libraries/                # Директория для библиотек шаблонов консолей
                                │   ├── menu.lib                      # Библиотека меню
                                │   └── prom.lib                      # Библиотека Prometheus
            НЕ КОПИРОВАТЬ       └── prometheus.service                # ЭТОТ ФАЙЛ НУЖНО БУДЕТ СОЗДАТЬ САМОСТОЯТЕЛЬНО ПУСТЫМ / Сервисный Unit-файл для запуска Prometheus

8. Где файл `prometheus.yml` нужно написать с нуля (это основной конфиг-файл `Prometheus`). Подсказка, как этот файл написать: `GitHub` - `prometheus/documentation/examples/prometheus.yml`
  - После написания конфиг-файла - подкидываем к запуску на коленке ваш конфиг
     - `./prometheus --config.file=prometheus.yml`
     - Тем самым мы проверяем успешный запуск Prometheus на порту `:9090` через веб-морду
     - А также проводим дебаг запуска конфиг-файла, если на этом этапе возникают ошибки, значит меняйте параметры конфиг-файла до тех пор, пока не запустите бинарь успешно
     - Пока успешно не запустили бинарь через конфиг - `unit_file` не пишем (это важно для отладки)
9. Где файл `unit_file` нужно написать с нуля (это файл отвечающий за запуск `Prometheus`)
10. Далее скопировать рекурсивно директорию `/Documents/linux-monitoring` в директорию `/opt`
11. Далее нужно создать группу пользователей `prometheus` и добавить туда пользователя `prometheus`:
    - Далее проверить эту группу пользователей, что `prometheus` добавился (одновременно идем в `ИИ` и учимся назначать владельца на директорию и на файлы)
    - При дефолтной установке пакета `Prometheus`, будь то `.rpm` или `.deb` назначение прав и назначение владельца происходит автоматически
    - Здесь мы делаем назначение вручную, чтобы понимать логику работы команд: `chown` и `chmod` (то есть пользователь `prometheus` и его группа в целях безопасности должны обслуживать одно приложение **Прометеуса** и не иметь доступ ни к чему другому - в этом смысл)
12. Затем рекурсивно назначить владельца `prometheus` и группу `prometheus` для рабочей директории `/linux-monitoring` по адресу `/opt/linux-monitoring/prometheus`:
      
                        --права-- -владелец-  -группа-           /opt/linux-monitoring      
                       drwxrwxrwx prometheus prometheus          ├── grafana             # Директория Grafana         
                       drwxrwxrwx prometheus prometheus          ├── node-exporter       # Директория Node Exporter
                       drwxrwxrwx prometheus prometheus          ├── prometheus          # Директория Prometheus
                       drwxrwxrwx prometheus prometheus          ├── e.t.c               # Остальные директории
                  
13. Далее выдать права:
   - `sudo chown -R prometheus:prometheus /opt/linux-monitoring/prometheus` # назначаем пользователя и группу пользователя
   - `sudo chmod +x /opt/linux-monitoring/prometheus/prometheus` # назначаем права на исполнение на бинарный файл
   - `sudo chmod 640 /opt/linux-monitoring/prometheus/prometheus.yaml` # выдаем права на конфиг-файл
14. Представьте себе, что вы инженер по разработке и работаете на платформе `DEV` в песочнице, у вас полностью развязаны руки, поэтому имеем это ввиду:
    - Параллельно идем в `ИИ` и учимся выставлять числовые права
    - Заодно читаем, что такое `640` и как эти числа образуются `4+2+1 (4 - чтение, 2 - запись, 1 - исполнение)`
15. Затем скопировать уже написанный вами `Unit` в директорию `/etc/systemd/system/` автозапуска `Linux`
16. Чтобы система `Linux` поняла, что файл сервиса `Unit` добавлен в директорию `/systemd`, нужно вбить команду `sudo systemctl daemon-reload`:
    - Тем самым обновляя директорию `/systemd` до актуального состояния
    - Далее ставим наш сервис на автозапуск (то есть при ребуте системы сервис `Prometheus` будет взлетать автоматом) `sudo systemctl enable`
    - Читаем подробно в `ИИ` про эту команду и заодно еще раз про повторяем про пороцессы и демоны
17. Далее запускаем сервис `Prometheus` утилитой `systemctl` (в дефолте эта утилита смотрит в автозапуск `/systemd` и будет знать о том, что там лежит наш юнит):
    - Проверяем после запуска статус `ACTIVE` командой `sudo systemctl status prometheus.service` и смотрим на работающую веб-морду
    - А если `INACTIVE` или `FAIL`, то сразу читаем логи (смотрим следующий пункт темы)
    - Подсказка: смотрим в `Unit` либо смотрим в конфиг `YAML` в `Prometheus`, скорее всего ошиблись в одном из двух, часто бывают проблемы с выдачей прав и с неверными пользователями
18. Затем выводим логи `Prometheus` в терминал, которые отбрасывает запущенный `Prometheus` с помощью утилиты `journalctl`:
    - Параллельно для справки с помощью `ИИ` читаем, что такое: `stdin`, `stdout`, `stderr` 
19. Далее парсим (фильтруем) логи утилитой `grep` в файл `prometheus.log` (находясь в корневой директории `/prometheus`) по ключевому слову `info` (сохраняем логи "под ноги" `Prometheus`):
    - То есть конечный результат лога должен содержать только строки с `info`
    - Подсказка: `journalctl | grep` - используем перенаправление вывода из `journalctl` в `grep` с помощью пайпа `|`
    - А также подумайте, как с помощью `grep`:
       - Добавить новые записи в файл с сохранением в реальном времени (то есть не через однократное сохранение лога в файл) 
       - Грепать новые логи раз в минуту, записывая в файл:
          - Поставить мини-скрипт `grep` на `Bash` - `script_logs.sh` из под рабочей директории `/opt` в планировщик `crontab` на выполнение (подсказка: `0 * * * * /путь/к/script_logs.sh`, то есть `crontab` должен будет дёргать ваш мини-скрипт на выполнение раз в минуту):
             - Советую сначала потренироваться в запуске тестового скрипта
             - К примеру для начала разобраться какие права выдать скрипту, чтобы он запустился с тестовой фразой в терминале: `Hello, World!`
20. Далее перезагружаем `Debian-виртуалку` и проверяем автозапуск через 2-3 минуты (`sudo systemctl status prometheus.service`), что юнит автоматически стартовал сервис `Prometheus` - он должен подняться на веб-морде
21. Далее копируем данные рабочего конфига `Prometheus` в домашнюю директорию `/Documents/linux-monitoring/prometheus` и далее пушим (_Внимание! В `GitHub` можно пушить только конфиг-текстовые файлы, код и любой текст - и больше ничего_) данные в свой удаленный репозиторий (подсказка: сначала сделайте `git add` потом `git commit -m "напишите какие файлы добавляете и что сделали"` и затем `git push`)
  - Пушить файлы из-под `/root` - это `bad practicies` и к тому же точно будут конфликты с правами на доступ (поэтому копируем все конфиги и скрипты сначала в домашнюю директорию, а потом пушим (при этом копируем уже в ранее склонированный репозиторий))
  - Не забываем про то, что вы написали еще и Bash скрипт, его нужно скопировать в домашнюю директорию и тоже запушить
22. Далее, так как мы подняли `Prometheus` и он работает — пробежимся по дебагу (просто представим, что приложению нужен дебаг, как будто это инцидент в банке и его нужно решать, а `Prometheus` у нас не работает):
    
    - С помощью утилиты `ss` найдите `prometheus` и посмотрите на каком порту он сидит, заодно посмотрите какой это порт: `TCP` или `UDP`
    - С помощью утилиты `telnet` проверьте доступность соединения `Prometheus` по дефолтному порту `Prometheus` (подумайте как это сделать)
    - С помощью утилиты — `curl` гетом (`GET`) скурлите (постучитесь `GET-запросом`) в `API Prometheus`, который должен вернуть `HTTP статус 2xx`, если сервису хорошо и `HTTP статус 5xx`, если плохо (заодно подтягиваем тему: методы и коды `HTTP`)
    - С помощью команды `ps` найдите `PID` процесса `Prometheus` (подсказка: `ps aux | grep ...`) и попробуйте убить его командой `kill` (сначала прочитайте, как убивать процессы, сначала во встроенном руководстве `man`, а потом в `ИИ`)
    - А также в дебаг входит `journactl` и `systemctl status`
    - Команды можно комбинировать между собой

23. В рабочую директорию `/opt/linux-monitoring/prometheus` положить второй `Bash` скрипт, который должен делать всю ручную работу выше автоматически:
    - Этот скрипт в финале должен поднять `Prometheus` с нуля за секунды и вы должны увидеть в терминале статус сервиса `ACTIVE`, а затем вы должны перейти в браузер и увидеть его на веб-морде:
       - То есть ставим всё что мы делали вручную выше на автоматизацию
    - Коммитим изменения и пушим в `GitHub` второй скрипт на установку `Prometheus` (не запускаем)
    - Далее нужно модернизировать этот скрипт на полное удаление `Prometheus` из системы, включая юнит, только осторожнее с директорией `/opt` - ее удалять не нужно
    - Коммитим изменения и пушим в `GitHub` третий скрипт на полное удаление (не запускаем)
      - Писать эти скрипты строго используя логические операторы `&&` (и) и `||` (или) - тем самым мы постепенно вникаем в тему логических операторов и учимся их комбинировать между собой:
         - То есть каждая строка скрипта должна выглядеть, как удаление директории `&&` вывод сообщения об успехе `||` вывод сообщения об ошибке:

                 rm -rf /tmp/example && echo "Директория успешно удалена" || { echo "Ошибка удаления директории"; exit 1; }

    - Далее протестировать эти два скрипта на текущей машине (с учетом того, что все ваши файлы уже запушены в `GitHub` из домашней директории и вы можете делать всё что угодно на этой машине, имеем только ввиду, что исполняемые файлы (бинарники) нельзя пушить в `GitHub`, поэтому эта тема написана таким образом, что пушить вы будете только текстовые файлы с кодом и с конфигурацией, как раз из директории локального репозитория)
24. Далее перейти в виртуальную машину `Debian Б` из `п.1` и запустить её рядом с вашей машиной `Debian А`
25. Прогнать из пункта выше готовый скрипт запуска `Prometheus` на голой машине Б:
    - Затем удалить `Prometheus` вторым скриптом (не забываем стопнуть `Prometheus` перед удалением, а после удаления сделать `daemon-reload`)
26. Далее опишу, как у нас в банке проходила миграция. Я писал скрипт на весь бэкенд мониторинга, который собирал `Prometheus` и прочее ПО в архив из текущих файлов с тачки и перекидывал архив на соседний сервер (это нормальная практика, когда тренируешься впервые на платформе `DEV` в песочнице)
    - На этом этапе мы прогонять этот скрипт **не будем**, так как уже было написано достаточно скриптов для понимания их работы
27. Далее подумать, как с помощью утилиты `SCP` перекинуть изначально скачанный архив `Prometheus` с тачки `А` на тачку `Б`:
    - Нужно иметь ввиду, что перекидывать архив нужно в директорию `/tmp` (прочитайте за что она отвечает)
    - На данном этапе `SCP` можно не прогонять, но обязательно прочитать, как это делается

## Выводы
В банке эта задача (по сборке голых бинарей всего ПО мониторинга в архив + миграция с CentOS на SberLinux) была моим первым кейсом на должности разработчика мониторинга. На задачу мне дали максимум 3 дня. На третий день уже была миграция. **Мой уровень был**: умею создавать файлы, переходить в директории, запускаю скрипты (не пишу), знаю как сохранить файл и выйти из Vim, знаю как выставлять права на файлы и распаковываю архивы, то есть уровень примерно как у вас сейчас.
