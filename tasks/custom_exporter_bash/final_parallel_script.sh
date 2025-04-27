#!/bin/bash

# Файл для сохранения метрик
METRICS_FILE="final_metrics"

# Очистка файла перед записью новых данных
> "$METRICS_FILE"

# Массив сайтов для проверки
SITES=("https://x.com" "https://vk.com" "https://yandex.ru" "https://github.com")

# Функция для обработки одного сайта
process_site() {
    site=$1
    DOMAIN=$(echo "$site" | awk -F[/:] '{print $4}')
    RESULT=$(curl -o /dev/null -s -w "%{http_code} %{time_total}" "$site")
    
    HTTP_CODE=$(echo "$RESULT" | awk '{print $1}')
    RESPONSE_TIME=$(echo "$RESULT" | awk '{print $2}')
    
    # Формируем метрики
    # Перед нами формат Open Metrics для Prometheus, который Exporter отдает на страницу /metrics
    echo "# HELP http_status_code HTTP status code for $DOMAIN" >> "$METRICS_FILE"
    echo "# TYPE http_status_code gauge" >> "$METRICS_FILE"
    echo "http_status_code{domain=\"$DOMAIN\"} $HTTP_CODE" >> "$METRICS_FILE"
    
    echo "# HELP response_time Response time for $DOMAIN" >> "$METRICS_FILE"
    echo "# TYPE response_time gauge" >> "$METRICS_FILE"
    echo "response_time{domain=\"$DOMAIN\"} $RESPONSE_TIME" >> "$METRICS_FILE"
}

# Запуск обработки сайтов параллельно
for site in "${SITES[@]}"; do
    process_site "$site" &
done

# Ожидание завершения всех фоновых процессов
wait
