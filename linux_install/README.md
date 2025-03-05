# VirtualBox

## Tasks

### Установка Linux

- Для установки берем чистый образ [Debian Netinst 12.9.0 amd64](https://www.debian.org/CD/netinst/) и ставим без Desktop Environment (DE)
- Почему мы выбрали Debian:
  - Мы выбрали образ Debian, потому что у него пакетный менеджер такой же как в Ubuntu, а это значит: большое сообщество в интернете и можно найти ответ почти на любой вопрос, я уже молчу про Qwen и ChatGPT
  - Системные требования очень низкие, после запуска RAM не превышает 270Мб
- Для **VirtualBox** выбираем следующие параметры:
  - **RAM**: 1536Mb
  - **HDD**: 10Gb
  - **CPU**: 2
- Далее при установке выбираем установка через GUI
- В дальнейшем нужно будет снять все галочки и поставить, как на скрине ниже:
  - <img [https://github.com/lamjob1993/linux-monitoring/blob/main/.files/.bucket/Debian%20Install.jpg]()>
