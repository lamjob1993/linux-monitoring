# **Технические вопросы о Debian и CentOS к собеседованию**

Вот таблица с вопросами и ответами для **Debian** и **CentOS**:

---

| **Вопрос**                                      | **Debian**                                                                 | **CentOS**                                                                 |
|-------------------------------------------------|---------------------------------------------------------------------------|---------------------------------------------------------------------------|
| **1. Как обновить систему?**                    | `sudo apt update && sudo apt upgrade`                                     | `sudo yum update` или `sudo dnf update`                                   |
| **2. Как установить пакет?**                    | `sudo apt install <package-name>`                                        | `sudo yum install <package-name>` или `sudo dnf install <package-name>`   |
| **3. Как удалить пакет?**                       | `sudo apt remove <package-name>`                                         | `sudo yum remove <package-name>` или `sudo dnf remove <package-name>`     |
| **4. Как полностью удалить пакет (с конфигами)?**| `sudo apt purge <package-name>`                                          | `sudo yum remove <package-name>` (удаляет всё, включая конфиги)           |
| **5. Как проверить статус службы?**             | `sudo systemctl status <service-name>`                                   | `sudo systemctl status <service-name>`                                   |
| **6. Как запустить службу?**                    | `sudo systemctl start <service-name>`                                    | `sudo systemctl start <service-name>`                                    |
| **7. Как добавить службу в автозапуск?**         | `sudo systemctl enable <service-name>`                                   | `sudo systemctl enable <service-name>`                                   |
| **8. Как отключить службу в автозапуске?**       | `sudo systemctl disable <service-name>`                                  | `sudo systemctl disable <service-name>`                                  |
| **9. Как посмотреть логи системы?**              | `journalctl -xe`                                                         | `journalctl -xe`                                                         |
| **10. Как создать нового пользователя?**         | `sudo adduser <username>`                                                | `sudo useradd <username>`                                                |
| **11. Как задать пароль пользователю?**          | `sudo passwd <username>`                                                 | `sudo passwd <username>`                                                 |
| **12. Как добавить пользователя в группу?**      | `sudo usermod -aG <group-name> <username>`                               | `sudo usermod -aG <group-name> <username>`                               |
| **13. Как настроить SSH-ключевую аутентификацию?**| `ssh-keygen`, затем `ssh-copy-id user@server-ip`                          | `ssh-keygen`, затем `ssh-copy-id user@server-ip`                          |
| **14. Как проверить использование дискового пространства?** | `df -h`                                                              | `df -h`                                                                  |
| **15. Как проверить использование оперативной памяти?** | `free -m` или `htop`                                                | `free -m` или `htop`                                                     |
| **16. Как настроить файрвол?**                   | `sudo ufw allow 80/tcp`, затем `sudo ufw enable`                         | `sudo firewall-cmd --add-port=80/tcp --permanent`, затем `sudo firewall-cmd --reload` |
| **17. Как изменить права доступа к файлу?**      | `chmod <permissions> <file>`                                             | `chmod <permissions> <file>`                                             |
| **18. Как изменить владельца файла?**            | `sudo chown <new-owner>:<new-group> <file>`                              | `sudo chown <new-owner>:<new-group> <file>`                              |
| **19. Как проверить открытые порты?**            | `netstat -tuln` или `ss -tuln`                                           | `netstat -tuln` или `ss -tuln`                                           |
| **20. Как настроить SELinux/AppArmor?**          | `sudo aa-status` или `sudo aa-enforce /path/to/profile`                  | `sestatus`, затем `sudo setenforce 0` или редактирование `/etc/selinux/config` |
| **21. Как посмотреть версию ОС?**                | `lsb_release -a`                                                         | `cat /etc/redhat-release`                                                |
| **22. Как перезагрузить систему?**               | `sudo reboot`                                                            | `sudo reboot`                                                            |
| **23. Как остановить службу?**                   | `sudo systemctl stop <service-name>`                                     | `sudo systemctl stop <service-name>`                                     |
| **24. Как проверить загруженные модули ядра?**   | `lsmod`                                                                  | `lsmod`                                                                  |
| **25. Как добавить репозиторий?**                | `sudo add-apt-repository <repo-url>`                                     | `sudo yum-config-manager --add-repo <repo-url>`                          |

---

### Примечания:
- **Debian** использует `apt` для управления пакетами и `ufw` для файрвола.
- **CentOS** использует `yum` или `dnf` для управления пакетами и `firewalld` для файрвола.
- Некоторые команды (например, `systemctl`, `journalctl`) работают одинаково в обоих дистрибутивах.
