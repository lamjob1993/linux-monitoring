# Навигация

Этот документ является центральным навигатором по всем разделам курса (разделы выполняются последовательно). Теория и вопросы к собеседованию с полными ответами находятся в папках соответствующих инструментов.

---

## Содержание

0. **Теория и фундаментальные основы**
    * [Изучить перед прохождением курса на GitHub (можно изучить только теорию)](https://teletype.in/@lamjob/wjNvt64l77l)

1.  **Введение в мониторинг и общие концепции**
    * [Введение в мониторинг](https://github.com/lamjob1993/linux-monitoring/tree/main/navigation/introduction_monitoring)
       * **Учим сразу** базовую концепцию и закрепляем по мере прохождения курса
    * [Легенда инженера по сопровождению](https://github.com/lamjob1993/linux-monitoring/blob/main/navigation/%D0%9B%D0%B5%D0%B3%D0%B5%D0%BD%D0%B4%D0%B0%20%D0%B8%D0%BD%D0%B6%D0%B5%D0%BD%D0%B5%D1%80%D0%B0.md)
       * **Учим легенду сразу** и закрепляем по мере прохождения курса
    * [Вопросы на собеседовании к легенде инженера](https://github.com/lamjob1993/linux-monitoring/blob/main/navigation/%D0%92%D0%BE%D0%BF%D1%80%D0%BE%D1%81%D1%8B%20%D0%BA%20%D0%BB%D0%B5%D0%B3%D0%B5%D0%BD%D0%B4%D0%B5.md)
       * **Учим сразу** и закрепляем по мере прохождения курса
    * [Вопросы по стеку сопровождения и мониторинга](https://teletype.in/@lamjob/sPRL_XpiLkV)
       * Технические вопросы к собеседованию без ответов
       * **Учим сразу** базовые вопросы только по: Linux и сетям: протоколам и тд, а также стараемся по основам Docker
       * **Учим позже** и углубляемся в вопросы по мере прохождения курса: Ansible, Terraform, CI/CD, K8s
    * [Пишем публичный репозиторий (pet-проект)](https://github.com/lamjob1993/linux-monitoring/blob/main/tasks/public_repository/README.md)
       * Наброски по pet-проекту должны быть готовы после прохождения раздела **"Мониторинг"**
       * Проект должен на 100% функционировать по ссылке на [GitHub](https://github.com/) после прохождения темы **"Docker Compose"**
    * [Подготовка к собеседованию по аналитике резюме](https://github.com/lamjob1993/linux-monitoring/blob/main/tasks/cv_final/README.md)
       * Приступаем к этому разделу после того, как я [утвердил ваше резюме на финал](https://t.me/c/2168307578/253/257)

2. **Установка ОС и первая практика**
    * [Установка Linux](https://github.com/lamjob1993/linux-monitoring/tree/main/tasks/linux_install)
    * [Технические вопросы к собеседованию: Debian и CentOS](https://github.com/lamjob1993/linux-monitoring/blob/main/tasks/linux_install/tech_questions.md)
    * [Настройка доступа по SSH в GitHub](https://github.com/lamjob1993/linux-monitoring/blob/main/.files/%D0%93%D0%B5%D0%BD%D0%B5%D1%80%D0%B0%D1%86%D0%B8%D1%8F%20SSH%20%D0%B4%D0%BB%D1%8F%20GitHub.md)
    * [Делаем форк этого репозитория к себе в аккаунт GitHub](https://github.com/lamjob1993/linux-monitoring/blob/main/.files/%D0%A4%D0%BE%D1%80%D0%BA%20%D0%B2%20GitHub.md)
3.  **Мониторинг в базовом исполнении**
    * [Путь Прометея](https://github.com/lamjob1993/linux-monitoring/tree/main/tasks/prometheus/README.md)
       * [Введение в Prometheus](https://github.com/lamjob1993/linux-monitoring/tree/main/tasks/prometheus/beginning)
       * [Prometheus Tasks](https://github.com/lamjob1993/linux-monitoring/tree/main/tasks/prometheus)
       * [Вопросы к интервью](https://github.com/lamjob1993/linux-monitoring/blob/main/tasks/prometheus/job_interview.md)
    * [Grafana - Визуализация и дашборды. Часть 1](https://github.com/lamjob1993/linux-monitoring/blob/main/tasks/grafana/README.md)
       * [Grafana Task 1](https://github.com/lamjob1993/linux-monitoring/tree/main/tasks/grafana)
       * Вопросы к интервью
    * Экспортеры Prometheus:
       * [Node Exporter](https://github.com/lamjob1993/linux-monitoring/blob/main/tasks/node-exporter/README.md)
          * [Node Exporter Tasks](https://github.com/lamjob1993/linux-monitoring/tree/main/tasks/node-exporter)
          * Вопросы к интервью
       * [Process Exporter](https://github.com/lamjob1993/linux-monitoring/tree/main/tasks/process-exporter/README.md)
          * [Process Exporter Tasks](https://github.com/lamjob1993/linux-monitoring/blob/main/tasks/process-exporter)
          * Вопросы к интервью
       * [Custom Exporter](https://github.com/lamjob1993/linux-monitoring/blob/main/tasks/custom_exporter_bash/README.md)
          * [Custom Exporter Tasks](https://github.com/lamjob1993/linux-monitoring/tree/main/tasks/custom_exporter_bash)
          * Вопросы к интервью
       * [Blackbox Exporter и Nginx](https://github.com/lamjob1993/linux-monitoring/blob/main/tasks/blackbox-exporter/README.md)
          * [Blackbox Exporter и Nginx Tasks](https://github.com/lamjob1993/linux-monitoring/tree/main/tasks/blackbox-exporter)
          * [Вопросы к интервью Blackbox](https://github.com/lamjob1993/linux-monitoring/blob/main/tasks/blackbox-exporter/blackbox_interview.md)
          * [Вопросы к интервью Nginx](https://github.com/lamjob1993/linux-monitoring/blob/main/tasks/blackbox-exporter/nginx_interview.md)
       * Postgres Exporter и PostgreSQL
          * [PostgreSQL](https://github.com/lamjob1993/linux-monitoring/blob/main/tasks/postgresql/README.md)
          * [Postgres Exporter](https://github.com/lamjob1993/linux-monitoring/blob/main/tasks/postgresql/README.md#%D1%87%D1%82%D0%BE-%D1%82%D0%B0%D0%BA%D0%BE%D0%B5-postgres-exporter-%D0%B8-%D0%B7%D0%B0%D1%87%D0%B5%D0%BC-%D0%BD%D1%83%D0%B6%D0%B5%D0%BD)
          * [PostgreSQL Tasks](https://github.com/lamjob1993/linux-monitoring/tree/main/tasks/postgresql)
          * [Вопросы к интервью](https://github.com/lamjob1993/linux-monitoring/blob/main/tasks/postgresql/job_interview.md)
    * [Pushgateway](https://github.com/lamjob1993/linux-monitoring/tree/main/tasks/pushgateway)
       * Вопросы к интервью
    * [Prometheus Federation](https://github.com/lamjob1993/linux-monitoring/tree/main/tasks/prometheus_federate)
       * Вопросы к интервью
    * [Alertmanager и алерты](https://github.com/lamjob1993/linux-monitoring/tree/main/tasks/alertmanager)
       * Вопросы к интервью
    * [Grafana - Визуализация и дашборды. Часть 2](https://github.com/lamjob1993/linux-monitoring/blob/main/tasks/grafana/README.md)
       * [Grafana Task 2](https://github.com/lamjob1993/linux-monitoring/tree/main/tasks/grafana)
       * Вопросы к интервью

4.  **Docker. Контейнеризация**
    * [Docker - Основы, образы, контейнеры](https://github.com/lamjob1993/docker-monitoring)
    * Вопросы к интервью

5.  **Terraform. Развертывание и управление инфраструктурой как кодом (IaC).**
    * [Terraform - Основы и провайдеры](https://github.com/lamjob1993/terraform-monitoring) / В работе
    * Вопросы к интервью

6.  **Ansible. Развертывание и управление конфигурацией и приложениями как кодом (IaC).**
    * [Ansible - Основы, инвентарь, модули](https://github.com/lamjob1993/ansible-monitoring/tree/main)
    * Вопросы к интервью

7.  **CI/CD**
    * [CI/CD - Общие принципы](../CI-CD/general_principles.md) / В работе
    * [Teamcity - Конфигурация и пайплайны](../CI-CD/Teamcity/interview_questions.md) / В работе
    * [BitBucket - Pipelines](../CI-CD/Bitbucket/interview_questions.md) / В работе
    * Вопросы к интервью 
    * ...
8.  **Kubernetes. Оркестрация контейнеров**
    * [Kubernetes - Введение](https://github.com/lamjob1993/kubernetes-monitoring)
    * [Kubernetes - Архитектура и компоненты](../Kubernetes/interview-questions/kubernetes_architecture.md) / В работе
    * [Kubernetes - Поды, Deployments, Services](../Kubernetes/interview-questions/kubernetes_objects1.md) / В работе
    * Вопросы к интервью
    * ...
9. **Финальная часть**
    * Диплом и выпускной pet-проект
    * Самопрезентация на собеседовании (презентация вашего pet-проекта собеседующему)
       * Изначально я веду собеседование и вы мне презентуете свой pet-проект
       * На реальном собеседовании стараемся выбить время в процессе, когда они у вас спросят, есть еще какие-то вопросы?
       * Демонстрация схемы проекта строго обязательна (давайте попробуем выбрать Figma, как основную площадку для рисовки)

