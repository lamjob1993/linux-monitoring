# PostgreSQL

_Пользуемся официальной документацией на GitHub (в основном там прописаны Docker файлы на запуск и всегда есть конфиги)_

## Задачник по запросам к БД
Для выполнения запросов необходимо подключиться к базе с помощью **DBeaver**.

### 20 SQL-запросов для базы данных `fintech_credit_conveyor` с нарастанием сложности

---

#### **Уровень 1: Простые SELECT**
1. **Все клиенты**  
   ```sql
   SELECT * FROM clients;
   ```

2. **Логи с фильтром по статусу "warning"**  
   ```sql
   SELECT * FROM conveyor_log 
   WHERE details->>'status' = 'warning';
   ```

3. **Кредитные продукты с процентной ставкой выше 15%**  
   ```sql
   SELECT * FROM credit_products 
   WHERE interest_rate > 15.0;
   ```

4. **Заявки со статусом "approved"**  
   ```sql
   SELECT * FROM credit_applications 
   WHERE status = 'approved';
   ```

5. **Просроченные платежи**  
   ```sql
   SELECT * FROM payments 
   WHERE status = 'overdue';
   ```

---

#### **Уровень 2: JOIN и базовая агрегация**
6. **Клиенты и их кредитные заявки**  
   ```sql
   SELECT c.full_name, a.amount, a.status 
   FROM clients c 
   JOIN credit_applications a ON c.client_id = a.client_id;
   ```

7. **Средний кредитный рейтинг клиентов**  
   ```sql
   SELECT AVG(credit_score) AS avg_score FROM clients;
   ```

8. **Количество заявок по продуктам**  
   ```sql
   SELECT p.product_name, COUNT(a.application_id) AS total_apps 
   FROM credit_products p 
   LEFT JOIN credit_applications a ON p.product_id = a.product_id 
   GROUP BY p.product_name;
   ```

9. **Платежи с деталями заявки**  
   ```sql
   SELECT p.payment_id, a.amount, p.status, p.payment_date 
   FROM payments p 
   JOIN credit_applications a ON p.application_id = a.application_id;
   ```

10. **Логи с фильтром по этапу "scoring"**  
    ```sql
    SELECT * FROM conveyor_log 
    WHERE stage = 'scoring';
    ```

---

#### **Уровень 3: Сложные фильтры и сортировка**
11. **Клиенты с паспортами, начинающимися на "1234"**  
    ```sql
    SELECT * FROM clients 
    WHERE passport LIKE '1234%';
    ```

12. **Заявки на сумму больше средней**  
    ```sql
    SELECT * FROM credit_applications 
    WHERE amount > (SELECT AVG(amount) FROM credit_applications);
    ```

13. **Платежи за последние 6 месяцев**  
    ```sql
    SELECT * FROM payments 
    WHERE payment_date >= NOW() - INTERVAL '6 months';
    ```

14. **Клиенты с кредитным рейтингом ниже 600 и активными заявками**  
    ```sql
    SELECT c.* 
    FROM clients c 
    JOIN credit_applications a ON c.client_id = a.client_id 
    WHERE c.credit_score < 600 AND a.status = 'submitted';
    ```

15. **Продукты с максимальным сроком больше 36 месяцев**  
    ```sql
    SELECT * FROM credit_products 
    WHERE max_term > 36;
    ```

---

#### **Уровень 4: Оконные функции и CTE**
16. **Топ-5 клиентов по количеству заявок**  
    ```sql
    SELECT client_id, COUNT(*) AS app_count 
    FROM credit_applications 
    GROUP BY client_id 
    ORDER BY app_count DESC 
    LIMIT 5;
    ```

17. **Сумма платежей по заявкам с разбивкой по месяцам**  
    ```sql
    SELECT 
        DATE_TRUNC('month', payment_date) AS month,
        SUM(amount_due) AS total 
    FROM payments 
    GROUP BY month 
    ORDER BY month;
    ```

18. **Клиенты с их самой крупной заявкой**  
    ```sql
    WITH MaxApplications AS (
        SELECT 
            client_id, 
            MAX(amount) AS max_amount 
        FROM credit_applications 
        GROUP BY client_id
    )
    SELECT c.full_name, m.max_amount 
    FROM clients c 
    JOIN MaxApplications m ON c.client_id = m.client_id;
    ```

19. **Логи с ранжированием по времени создания**  
    ```sql
    SELECT 
        log_id, 
        application_id, 
        stage, 
        ROW_NUMBER() OVER (PARTITION BY application_id ORDER BY created_at) AS step_number 
    FROM conveyor_log;
    ```

20. **Клиенты без просроченных платежей**  
    ```sql
    SELECT c.* 
    FROM clients c 
    WHERE NOT EXISTS (
        SELECT 1 
        FROM credit_applications a 
        JOIN payments p ON a.application_id = p.application_id 
        WHERE a.client_id = c.client_id AND p.status = 'overdue'
    );
    ```

---

#### **Каверзные запросы**
21. **Клиенты, у которых все заявки были отклонены**  
    ```sql
    SELECT c.* 
    FROM clients c 
    WHERE NOT EXISTS (
        SELECT 1 
        FROM credit_applications a 
        WHERE a.client_id = c.client_id AND a.status <> 'rejected'
    );
    ```

22. **Продукты, которые никогда не использовались в заявках**  
    ```sql
    SELECT * FROM credit_products 
    WHERE product_id NOT IN (
        SELECT DISTINCT product_id FROM credit_applications
    );
    ```

23. **Платежи, сумма которых превышает среднюю по продукту**  
    ```sql
    SELECT p.* 
    FROM payments p 
    JOIN credit_applications a ON p.application_id = a.application_id 
    JOIN credit_products pr ON a.product_id = pr.product_id 
    WHERE p.amount_due > pr.max_amount / pr.max_term;
    ```

24. **Логи, где этап "approval" длился более 1 дня**  
    ```sql
    WITH ApprovalTimes AS (
        SELECT 
            application_id,
            MIN(created_at) FILTER (WHERE stage = 'approval') AS approval_start,
            MAX(created_at) FILTER (WHERE stage = 'approval') AS approval_end
        FROM conveyor_log 
        GROUP BY application_id
    )
    SELECT * 
    FROM ApprovalTimes 
    WHERE approval_end - approval_start > INTERVAL '1 day';
    ```

---

### Примечания:
- Запросы используют возможности PostgreSQL: оконные функции (`ROW_NUMBER`, `RANK`), CTE (`WITH`), JSONB-поля (`details->>'status'`), агрегаты и фильтры.
- Для работы с датами использованы функции `DATE_TRUNC`, `NOW()`, и интервалы.
- В сложных запросах применяются подзапросы и `EXISTS`/`NOT EXISTS` для корреляции данных.
