# Навигация

- _Этот документ является центральным навигатором по всем разделам курса (разделы выполняются последовательно)._
- _Теория и вопросы к собеседованию с полными ответами находятся в директориях соответствующих инструментов._
- _Объему содержания не пугаемся, так как оно здесь носит еще и информационно-развернутый характер._

---

## Содержание

_Roadmap / Дорожная карта_

1. [Предисловие к курсу](https://github.com/lamjob1993/linux-monitoring/blob/main/navigation/others/%D0%9F%D1%80%D0%B5%D0%B4%D0%B8%D1%81%D0%BB%D0%BE%D0%B2%D0%B8%D0%B5%20%D0%BA%20%D0%BA%D1%83%D1%80%D1%81%D1%83.md)
2.  **Теория и фундаментальные основы (в базовом виде)**
    * [Изучаем теорию](https://teletype.in/@lamjob/wjNvt64l77l)
    * [Изучаем практику по Linux](https://teletype.in/@lamjob/SsV-puwmQlR)

3.  **Введение в мониторинг и общие концепции (теория)**
    * [Введение в мониторинг](https://github.com/lamjob1993/linux-monitoring/tree/main/navigation/introduction_monitoring)
       * **Учим сразу** базовую концепцию и закрепляем по мере прохождения курса
    * [Наш технический стек](https://github.com/lamjob1993/linux-monitoring/blob/main/navigation/others/%D0%A1%D1%82%D0%B5%D0%BA%20%D0%BE%D1%82%D0%B4%D0%B5%D0%BB%D0%B0.md)
       * **Учим сразу** базовую концепцию и закрепляем по мере прохождения курса
    * [Кто такой инженер по сопровождению](https://teletype.in/@lamjob/B9uUuCqXaTu)
    * [Легенда инженера по сопровождению](https://github.com/lamjob1993/linux-monitoring/blob/main/navigation/others/%D0%9B%D0%B5%D0%B3%D0%B5%D0%BD%D0%B4%D0%B0%20%D0%B8%D0%BD%D0%B6%D0%B5%D0%BD%D0%B5%D1%80%D0%B0.md)
       * **Учим сразу** легенду и закрепляем по мере прохождения курса
    * [Пишем публичный репозиторий (pet-проект)](https://github.com/lamjob1993/linux-monitoring/blob/main/navigation/public_repository/README.md)
       * **Драфты по pet-проекту** должны быть готовы после прохождения раздела **"Prometheus. Мониторинг в базовом исполнении"**
       * **Pet-проект** должен быть готов на 100% по ссылке на [GitHub](https://github.com/) после прохождения раздела Docker: после темы **"Docker Compose"**
       * [Pet-проекты в качестве примеров (финтех тематика)](https://github.com/lamjob1993/linux-monitoring/blob/main/navigation/public_repository/example-pet.md)
    
4. **Вопросы к собеседованию (теория)**
    * [Вопросы к собеседованию по легенде инженера](https://github.com/lamjob1993/linux-monitoring/blob/main/navigation/others/%D0%92%D0%BE%D0%BF%D1%80%D0%BE%D1%81%D1%8B%20%D0%BA%20%D0%BB%D0%B5%D0%B3%D0%B5%D0%BD%D0%B4%D0%B5.md)
       * **Учим сразу** вопросы и закрепляем по мере прохождения курса
    * [Технические вопросы к собеседованию без ответов](https://github.com/lamjob1993/linux-monitoring/blob/main/navigation/others/%D0%92%D0%BE%D0%BF%D1%80%D0%BE%D1%81%D1%8B%20%D0%B1%D0%B5%D0%B7%20%D0%BE%D1%82%D0%B2%D0%B5%D1%82%D0%BE%D0%B2.md)
       * **Учим строго сразу**: Linux → Сети → Docker → это три основных кита для прохождения собеседования
       * **Учим позже после**: Linux → Сети → Docker и углубляемся в вопросы после Docker по мере прохождения курса: Terraform → Ansible → CI/CD → K8s
       * **Вопросы специально** написаны без ответов, чтобы вы сами их искали и тем самым готовились и запоминали

4. **Установка ОС и первая практика**
    * [Установка Linux](https://github.com/lamjob1993/linux-monitoring/tree/main/tasks/linux_install)
    * [Технические вопросы к собеседованию: Debian и CentOS](https://github.com/lamjob1993/linux-monitoring/blob/main/tasks/linux_install/tech_questions.md)
    * [Настройка доступа по SSH в GitHub](https://github.com/lamjob1993/linux-monitoring/blob/main/.files/%D0%93%D0%B5%D0%BD%D0%B5%D1%80%D0%B0%D1%86%D0%B8%D1%8F%20SSH%20%D0%B4%D0%BB%D1%8F%20GitHub.md)
    * Делаем [форк](https://github.com/lamjob1993/linux-monitoring/blob/main/.files/%D0%A4%D0%BE%D1%80%D0%BA%20%D0%B2%20GitHub.md) нашего репозитория [linux-monitoring](https://github.com/lamjob1993/linux-monitoring) к себе в аккаунт GitHub

5.  **Prometheus. Мониторинг в базовом исполнении**
    * [Содержание раздела: Мониторинг](https://github.com/lamjob1993/linux-monitoring/blob/main/tasks/README.md)
    * [Готовим драфт по pet-проекту](https://github.com/lamjob1993/linux-monitoring/blob/main/navigation/public_repository/README.md)
       * [Pet-проекты в качестве примеров (финтех тематика)](https://github.com/lamjob1993/linux-monitoring/blob/main/navigation/public_repository/example-pet.md)
    * На этом этапе студент самостоятельно пишет ментору и ставит собеседование (готовим глобальный мониторинг + Linux + Сети)

6.  **Docker. Контейнеризация**
    * [Docker - Основы, образы, контейнеры](https://github.com/lamjob1993/docker-monitoring)
    * Вопросы к интервью
    * [Пишем финальный pet-проект и публикуем](https://github.com/lamjob1993/linux-monitoring/blob/main/navigation/public_repository/README.md)
       * [Pet-проекты в качестве примеров (финтех тематика)](https://github.com/lamjob1993/linux-monitoring/blob/main/navigation/public_repository/example-pet.md)
    * На этом этапе студент самостоятельно пишет ментору и ставит собеседование (готовим глобальный мониторинг + Linux + Сети + Docker)

7.  **Terraform. Развертывание и управление инфраструктурой как кодом (IaC)**
    * [Terraform - Основы и провайдеры](https://github.com/lamjob1993/terraform-monitoring)
    * Вопросы к интервью
    * [Обновляем финальный pet-проект](https://github.com/lamjob1993/linux-monitoring/blob/main/navigation/public_repository/README.md)
       * [Pet-проекты в качестве примеров (финтех тематика)](https://github.com/lamjob1993/linux-monitoring/blob/main/navigation/public_repository/example-pet.md)

8.  **Ansible. Развертывание и управление конфигурацией и приложениями как кодом (IaC)**
    * [Ansible - Основы, инвентори, модули, роли](https://github.com/lamjob1993/ansible-monitoring/tree/main)
    * Вопросы к интервью
    * [Обновляем финальный pet-проект](https://github.com/lamjob1993/linux-monitoring/blob/main/navigation/public_repository/README.md)
       * [Pet-проекты в качестве примеров (финтех тематика)](https://github.com/lamjob1993/linux-monitoring/blob/main/navigation/public_repository/example-pet.md)

9.  **CI/CD**
    * [CI/CD - Общие принципы](https://github.com/lamjob1993/ci-cd-monitoring) / В работе
    * [Teamcity - Конфигурация и пайплайны](https://github.com/lamjob1993/ci-cd-monitoring) / В работе
    * [BitBucket - Pipelines](https://github.com/lamjob1993/ci-cd-monitoring) / В работе
    * Вопросы к интервью
    * [Обновляем финальный pet-проект](https://github.com/lamjob1993/linux-monitoring/blob/main/navigation/public_repository/README.md)
       * [Pet-проекты в качестве примеров (финтех тематика)](https://github.com/lamjob1993/linux-monitoring/blob/main/navigation/public_repository/example-pet.md)
    * На этом этапе студент самостоятельно пишет ментору и ставит собеседование (готовим глобальный мониторинг + Linux + Сети + Docker + Ansible + Terraform + CI/CD)
    * ...

10. **Kubernetes. Оркестрация контейнеров**
    * [Kubernetes - Введение](https://github.com/lamjob1993/kubernetes-monitoring)
    * [Обновляем финальный pet-проект](https://github.com/lamjob1993/linux-monitoring/blob/main/navigation/public_repository/README.md)
       * [Pet-проекты в качестве примеров (финтех тематика)](https://github.com/lamjob1993/linux-monitoring/blob/main/navigation/public_repository/example-pet.md)
    * Вопросы к интервью
    * На этом этапе студент самостоятельно пишет ментору и ставит собеседование (готовим глобальный мониторинг + Linux + Сети + Docker + Ansible + Terraform + CI/CD + Kubernetes)
    * ...

11. **Финальная часть**
    * [Пишем резюме](https://t.me/c/2168307578/253/257)
       * [Подготовка к собеседованию по вашему финальному резюме](https://github.com/lamjob1993/linux-monitoring/blob/main/navigation/cv_final/README.md)
    * Возвращаемся и изучаем повторно с закреплением [главы 7-10 по курсу Телеграм](https://t.me/c/2168307578/1/140) 
    * Добавить софты и как держаться на собесе (в отдельную главу и уделить этой части отдельное внимание на собеседовании, попробовать прямо на собеседовании учить навыкам этикета и открытости)
    * Дипломный (выпускной pet-проект)
    * Добавить раздел по безопасности
    * Самопрезентация на собеседовании (презентация вашего pet-проекта собеседующему):
       * Изначально я веду собеседование и вы мне презентуете свой pet-проект
       * На реальном собеседовании стараемся выбить время в процессе, когда они у вас спросят, у вас есть еще какие-то вопросы?
       * Демонстрация схемы проекта строго обязательна (давайте попробуем выбрать Figma, как основную площадку для рисовки)

