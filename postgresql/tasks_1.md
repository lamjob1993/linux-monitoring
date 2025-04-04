# PostgreSQL

_Пользуемся официальной документацией на GitHub (в основном там прописаны Docker файлы на запуск и всегда есть конфиги)_

## Tasks

### Шаг 1. Установка PostgreSQL и создание первой БД

- Установите БД **PostgreSQL** стандартным способом через `apt` в систему **Debian**
- Далее нужно написать скрипт для создания базы данных
- Основные темы и таблицы для скрипта:

  1. **Клиенты** (персональные данные, кредитная история).  
  2. **Кредитные продукты** (условия, ставки, сроки).  
  3. **Заявки на кредит** (статусы, история изменений).  
  4. **Платежи** (график, просрочки, суммы).  
  5. **Кредитный конвейер** (логирование этапов обработки заявок). 

- Далее войдите через терминал в **PostgreSQL**
- Создайте новую базу данных
  - `CREATE DATABASE fintech_credit_conveyor`; 
- Подключитесь к созданной базе данных `\c fintech_credit_conveyor`
- Создайте таблицы внутри базы данных
  - Проверьте созданные таблицы `\dt`
  - [Образец схемы БД - пользуемся для создания базы](https://github.com/lamjob1993/linux-monitoring/blob/main/postgresql/%D0%A8%D0%BF%D0%B0%D1%80%D0%B3%D0%B0%D0%BB%D0%BA%D0%B0%20(%D1%81%D0%BE%D0%B7%D0%B4%D0%B0%D0%BD%D0%B8%D0%B5%20%D0%91%D0%94%20%D0%B8%20%D1%82%D0%B0%D0%B1%D0%BB%D0%B8%D1%86).md "Создание базы данных")

### Шаг 2. Генерация данных для БД

- Набейте фейковыми данными БД с помощью библиотеки **Python Faker**
  - Установите пакет для создания виртуальных окружений (если не установлен) `sudo apt install python3-venv`
  - Создайте виртуальное окружение `python3 -m venv myenv` - на этом этапе создается директория `myenv`, лучше находиться в директории **Documents**
    - ```bash

        -rw-r--r-- 1 lamjob lamjob  222 Mar 26 13:45 back_prometheus.yml
        -rw-r--r-- 1 lamjob lamjob  776 Mar 26 13:05 docker-compose.yml
        drwxr-xr-x 5 lamjob lamjob 4096 Apr  3 20:15 myenv
        -rw-r--r-- 1 lamjob lamjob  327 Mar 26 13:51 prometheus.yml

      ```
  - Активируйте его `source myenv/bin/activate`
    - ```bash

        lamjob@debian:~/Documents/monitoring$ source myenv/bin/activate
        (myenv) lamjob@debian:~/Documents/monitoring$

      ```
  - Теперь установите пакеты внутри окружения `pip install faker psycopg2-binary`
    - ```bash
  
      (myenv) lamjob@debian:~/Documents/monitoring$ pip install faker psycopg2-binary
      Collecting faker
        Downloading faker-37.1.0-py3-none-any.whl (1.9 MB)
           ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.9/1.9 MB 652.0 kB/s eta 0:00:00
      Collecting psycopg2-binary
        Downloading psycopg2_binary-2.9.10-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (3.0 MB)
           ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 3.0/3.0 MB 826.1 kB/s eta 0:00:00
      Collecting tzdata
        Downloading tzdata-2025.2-py2.py3-none-any.whl (347 kB)
           ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 347.8/347.8 kB 2.1 MB/s eta 0:00:00
      Installing collected packages: tzdata, psycopg2-binary, faker
      Successfully installed faker-37.1.0 psycopg2-binary-2.9.10 tzdata-2025.2
      (myenv) lamjob@debian:~/Documents/monitoring$
  
      ```
    - Проверка библиотек установленных в виртуальном окружении `pip list`
      - ```bash
        (myenv) lamjob@debian:~/Documents/monitoring$ pip list
        Package         Version
        --------------- -------
        Faker           37.1.0
        pip             23.0.1
        psycopg2-binary 2.9.10
        setuptools      66.1.1
        tzdata          2025.2
        ```
  - Подключение к базе данных из виртуального окружения
    - Для подключения к базе данных **PostgreSQL** используется библиотека **psycopg2**. Если она установлена в виртуальном окружении, то:
      - Подключение к базе данных будет работать только через интерпретатор **Python** из этого окружения.
      - Нет необходимости выходить из виртуального окружения для выполнения запросов к базе данных.
      - ```python
        # Настройки подключения к PostgreSQL
        conn = psycopg2.connect(
            dbname="fintech_credit_conveyor",
            user="postgres",
            password="your_password",
            host="localhost"
        ```
  - Запустите скрипт из активированного виртуального окружения `python generate_fake_data.py` (не забываем дать права на исполнение `chmod +x`)
    - В этом случае:
      - Используется интерпретатор **Python** из виртуального окружения.
      - Установленные зависимости (например, **faker** и **psycopg2-binary**) будут доступны, так как они установлены именно в это окружение.


### Шаг 3. Установка Postgres Exporter

- Установите [postgres_exporter](https://github.com/prometheus-community/postgres_exporter "Prometheus exporter for PostgreSQL server metrics.") и натравите на него **Prometheus**

### Шаг 4. Установка Grafana и адаптация дашборда PostgreSQL

- Скачайте дашборд предназначенный для СУБД **PostgreSQL** и визуализируйте метрики в **Grafana**
