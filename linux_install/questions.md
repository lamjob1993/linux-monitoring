### **Базовые вопросы к собеседованию**

1. **Что такое Debian?**  
   Debian — это свободный дистрибутив Linux, известный своей стабильностью и обширным репозиторием пакетов. Он часто используется как основа для других дистрибутивов (например, Ubuntu).

2. **Что такое CentOS?**  
   CentOS — это дистрибутив Linux, основанный на исходном коде Red Hat Enterprise Linux (RHEL). Он популярен в корпоративной среде благодаря своей стабильности и долгосрочной поддержке.

3. **Что такое Ubuntu?**  
   Ubuntu — это популярный дистрибутив Linux, основанный на Debian. Он ориентирован на удобство использования и регулярные обновления. Ubuntu широко используется как для рабочих станций, так и для серверов.

4. **Какая разница между Debian и Ubuntu?**  
   - Debian фокусируется на стабильности и минимализме, выпускает обновления реже.  
   - Ubuntu предлагает более частые обновления, удобный интерфейс и больше готовых решений "из коробки".

5. **Какая разница между CentOS и Ubuntu?**  
   - CentOS: стабильный, ориентированный на корпоративное использование, основан на RHEL.  
   - Ubuntu: более современный, удобный для пользователей, лучше подходит для разработчиков.

---

### **Установка и настройка**

6. **Как установить Debian?**  
   Скачайте ISO-образ с официального сайта → Запишите его на USB/CD → Загрузитесь с носителя → Следуйте инструкциям установщика.

7. **Как установить CentOS?**  
   Скачайте ISO-образ с официального сайта → Запишите его на USB/CD → Загрузитесь с носителя → Следуйте инструкциям установщика Anaconda.

8. **Как установить Ubuntu?**  
   Скачайте ISO-образ с официального сайта → Запишите его на USB/CD → Загрузитесь с носителя → Следуйте инструкциям установщика.

9. **Как проверить версию ОС в Debian?**  
   Используйте команду:  
   ```bash
   cat /etc/os-release
   ```

10. **Как проверить версию ОС в CentOS?**  
    Используйте команду:  
    ```bash
    cat /etc/redhat-release
    ```

11. **Как проверить версию ОС в Ubuntu?**  
    Используйте команду:  
    ```bash
    lsb_release -a
    ```

---

### **Пакеты и управление ими**

12. **Какой менеджер пакетов используется в Debian?**  
    В Debian используется `apt` (Advanced Package Tool) для управления пакетами.

13. **Какой менеджер пакетов используется в CentOS?**  
    В CentOS используется `yum` (или `dnf` в новых версиях) для управления пакетами.

14. **Какой менеджер пакетов используется в Ubuntu?**  
    В Ubuntu используется `apt` для управления пакетами.

15. **Как обновить систему в Debian?**  
    Используйте команды:  
    ```bash
    sudo apt update
    sudo apt upgrade
    ```

16. **Как обновить систему в CentOS?**  
    Используйте команду:  
    ```bash
    sudo yum update
    ```

17. **Как обновить систему в Ubuntu?**  
    Используйте команды:  
    ```bash
    sudo apt update
    sudo apt upgrade
    ```

18. **Как установить пакет в Debian?**  
    Используйте команду:  
    ```bash
    sudo apt install <package-name>
    ```

19. **Как установить пакет в CentOS?**  
    Используйте команду:  
    ```bash
    sudo yum install <package-name>
    ```

20. **Как установить пакет в Ubuntu?**  
    Используйте команду:  
    ```bash
    sudo apt install <package-name>
    ```

---

### **Системные настройки**

21. **Как настроить сеть в Debian?**  
    Редактируйте файл `/etc/network/interfaces`:  
    ```bash
    auto eth0
    iface eth0 inet static
        address 192.168.1.10
        netmask 255.255.255.0
        gateway 192.168.1.1
    ```

22. **Как настроить сеть в CentOS?**  
    Редактируйте файл `/etc/sysconfig/network-scripts/ifcfg-eth0`:  
    ```bash
    BOOTPROTO=static
    ONBOOT=yes
    IPADDR=192.168.1.10
    NETMASK=255.255.255.0
    GATEWAY=192.168.1.1
    ```

23. **Как настроить сеть в Ubuntu?**  
    Редактируйте файл `/etc/netplan/01-netcfg.yaml`:  
    ```yaml
    network:
      version: 2
      ethernets:
        eth0:
          dhcp4: no
          addresses:
            - 192.168.1.10/24
          gateway4: 192.168.1.1
          nameservers:
            addresses:
              - 8.8.8.8
              - 8.8.4.4
    ```

24. **Как настроить hostname в Debian?**  
    Измените файл `/etc/hostname` и выполните:  
    ```bash
    sudo hostnamectl set-hostname <new-hostname>
    ```

25. **Как настроить hostname в CentOS?**  
    Измените файл `/etc/hostname` и выполните:  
    ```bash
    sudo hostnamectl set-hostname <new-hostname>
    ```

26. **Как настроить hostname в Ubuntu?**  
    Измените файл `/etc/hostname` и выполните:  
    ```bash
    sudo hostnamectl set-hostname <new-hostname>
    ```

---

### **Продвинутые вопросы**

27. **Как настроить firewall в Debian?**  
    Используйте `ufw` (Uncomplicated Firewall):  
    ```bash
    sudo ufw enable
    sudo ufw allow ssh
    ```

28. **Как настроить firewall в CentOS?**  
    Используйте `firewalld`:  
    ```bash
    sudo systemctl start firewalld
    sudo firewall-cmd --add-service=http --permanent
    sudo firewall-cmd --reload
    ```

29. **Как настроить firewall в Ubuntu?**  
    Используйте `ufw`:  
    ```bash
    sudo ufw enable
    sudo ufw allow http
    ```

30. **Как настроить автозагрузку службы в Debian?**  
    Используйте команду:  
    ```bash
    sudo systemctl enable <service-name>
    ```

31. **Как настроить автозагрузку службы в CentOS?**  
    Используйте команду:  
    ```bash
    sudo systemctl enable <service-name>
    ```

32. **Как настроить автозагрузку службы в Ubuntu?**  
    Используйте команду:  
    ```bash
    sudo systemctl enable <service-name>
    ```

33. **Как посмотреть логи системы в Debian?**  
    Используйте команду:  
    ```bash
    journalctl
    ```

34. **Как посмотреть логи системы в CentOS?**  
    Используйте команду:  
    ```bash
    journalctl
    ```

35. **Как посмотреть логи системы в Ubuntu?**  
    Используйте команду:  
    ```bash
    journalctl
    ```
