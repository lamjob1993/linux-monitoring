# Ansible
## Inventory

**Inventory** в Ansible — это **список хостов (серверов) и групп хостов**, на которые применяются задачи из playbook. Это основной источник информации о целевых системах, их настройках и группах. Inventory позволяет организовать хосты в группы, задавать переменные и управлять ими централизованно.

---

### **Структура inventory**
Inventory можно хранить в файлах формата **ini** или **YAML**. Пример файла `inventory.ini`:

```ini
# inventory.ini
[webservers]  # Группа "webservers"
web1 ansible_host=192.168.1.10
web2 ansible_host=192.168.1.11

[dbservers]   # Группа "dbservers"
db1 ansible_host=192.168.1.20
db2 ansible_host=192.168.1.21

[all:vars]    # Переменные для всех хостов
common_var=value_for_all

[webservers:vars]  # Переменные для группы "webservers"
web_port=8080
```

---

### **Основные элементы inventory**
1. **Хосты**  
   Указываются в секциях групп или напрямую:
   ```ini
   server1 ansible_host=192.168.1.5 ansible_user=root
   ```

2. **Группы**  
   Группы объединяют хосты для совместного управления:
   ```ini
   [dbservers]
   db1 ansible_host=192.168.1.20
   db2 ansible_host=192.168.1.21
   ```

3. **Переменные**  
   Можно задавать переменные для хостов, групп или всех:
   ```ini
   [webservers:vars]
   web_root=/var/www
   ```

4. **Дочерние группы**  
   Группы могут включать другие группы:
   ```ini
   [production]
   web_servers ansible_children=webservers
   db_servers ansible_children=dbservers
   ```

---

### **Как использовать inventory**
#### 1. **Запуск playbook**
   Укажите inventory-файл через параметр `-i`:
   ```bash
   ansible-playbook -i inventory.ini deploy.yml
   ```

#### 2. **Выбор группы или хоста**
   Используйте параметр `--limit` для ограничения хостов:
   ```bash
   # Запустить только для группы "webservers"
   ansible-playbook -i inventory.ini deploy.yml --limit webservers

   # Запустить только для хоста "db1"
   ansible-playbook -i inventory.ini deploy.yml --limit db1
   ```

#### 3. **Переменные в inventory**
   Переменные из inventory доступны в playbook:
   ```yaml
   # В playbook:
   tasks:
     - name: Создать директорию
       file:
         path: "{{ web_root }}"
         state: directory
   ```

#### 4. **Динамический inventory**
   Для больших инфраструктур можно использовать скрипты или API (например, для AWS, Docker):
   ```bash
   # Пример использования скрипта для AWS EC2
   ansible-playbook -i ec2.py deploy.yml
   ```

---

### **Примеры inventory**
#### **Пример 1: Простой inventory**
```ini
# inventory.ini
[web]
web1 ansible_host=192.168.1.10
web2 ansible_host=192.168.1.11

[db]
db1 ansible_host=192.168.1.20
```

#### **Пример 2: Группы и переменные**
```ini
# inventory.ini
[app_servers]
app1 ansible_host=192.168.1.5
app2 ansible_host=192.168.1.6

[app_servers:vars]
app_env=production
app_port=8080

[db_servers]
db1 ansible_host=192.168.1.20
```

#### **Пример 3: YAML-формат**
```yaml
# inventory.yml
all:
  hosts:
    web1:
      ansible_host: 192.168.1.10
      ansible_user: root
    web2:
      ansible_host: 192.168.1.11
      ansible_user: ubuntu
  children:
    webservers:
      hosts:
        web1: ~
        web2: ~
    dbservers:
      hosts:
        db1:
          ansible_host: 192.168.1.20
```

---

### **Ключевые возможности inventory**
1. **Переменные для хостов и групп**  
   Можно задавать переменные, которые будут доступны в playbook:
   ```ini
   [webservers]
   web1 ansible_host=192.168.1.10
   web1_http_port=80
   ```

2. **Динамический inventory**  
   Используйте скрипты или плагины для генерации списка хостов (например, для облачных сервисов):
   ```bash
   # Пример скрипта для Docker
   ansible-playbook -i docker.py deploy.yml
   ```

3. **Комбинирование файлов**  
   Можно организовать inventory через несколько файлов:
   ```ini
   # inventory/group_vars/webservers.yml
   app_port: 8080

   # inventory/host_vars/web1.yml
   custom_setting: true
   ```

4. **Переопределение переменных**  
   Через командную строку или файлы переменных:
   ```bash
   ansible-playbook -i inventory.ini deploy.yml -e "app_env=staging"
   ```

---

### **Как проверить inventory**
Используйте команду `ansible-inventory` для просмотра структуры:
```bash
ansible-inventory -i inventory.ini --graph
```

Пример вывода:
```
@all:
  |--@webservers:
  |  |--web1
  |  |--web2
  |--@dbservers:
  |  |--db1
  |  |--db2
  |--@ungrouped:
```

---

### **Советы по работе с inventory**
1. **Разделение на группы**  
   Группируйте хосты по их роли (например, `webservers`, `dbservers`, `loadbalancers`).

2. **Переменные в отдельных файлах**  
   Храните переменные в `group_vars/` и `host_vars/` для лучшей организации:
   ```plaintext
   inventory/
   ├── group_vars/
   │   └── webservers.yml
   └── host_vars/
       └── web1.yml
   ```

3. **Динамический инвентори**  
   Для облачных или контейнерных сред используйте плагины или скрипты.

4. **Тестирование**  
   Проверяйте доступность хостов через `ansible <host> -m ping`:
   ```bash
   ansible web1 -i inventory.ini -m ping
   ```

---

### **Итог**
Inventory в Ansible — это **центральный каталог** ваших серверов и групп. Он позволяет:
- Централизованно управлять списком хостов.
- Группировать хосты и задавать переменные.
- Упростить масштабирование и поддержку инфраструктуры.
- Интегрировать динамические источники хостов (например, облачные сервисы).

С помощью inventory вы можете легко применять playbook к любым группам или хостам, минимизируя рутину при управлении инфраструктурой.
