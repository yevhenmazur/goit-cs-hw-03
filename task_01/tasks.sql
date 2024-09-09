
-- Отримати всі завдання певного користувача з user_id = 10
SELECT * FROM tasks WHERE user_id = 10;

-- Вибрати завдання із статусом 'new'.
SELECT tasks.*
FROM tasks
JOIN status ON tasks.status_id = status.id
WHERE status.name = 'new';

-- Оновити статус конкретного завдання з id = 1.
UPDATE tasks 
SET status_id = (SELECT id FROM status WHERE name = 'in progress')
WHERE id = 1;

-- Отримати список користувачів, які не мають жодного завдання.
SELECT name FROM users
WHERE id NOT IN (SELECT user_id
	FROM tasks
);

-- Додати нове завдання для конкретного користувача.
INSERT INTO tasks (title, description, user_id, status_id)
VALUES ('Complete homework Task 1', 'Add a new task for a specific user. Use INSERT to add a new task.', 5, 1);

-- Отримати всі завдання, які ще не завершено
SELECT tasks.title, tasks.description 
FROM tasks
JOIN status ON tasks.status_id = status.id
WHERE status.name != 'completed';

-- Видалити завдання із id = 31
DELETE FROM tasks WHERE id = 31;

-- Знайти користувачів з електронною поштою у домені example.org
SELECT * FROM users WHERE email LIKE '%example.org'

-- Оновити ім'я користувача
UPDATE users 
SET name = 'Bob'
WHERE name = 'gkelly'

-- Отримати кількість завдань для кожного статусу.
SELECT status.name, COUNT(tasks.id)
FROM tasks
JOIN status ON tasks.status_id = status.id
GROUP BY status.name;

-- Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти.
SELECT tasks.*
FROM tasks
JOIN users ON tasks.user_id = users.id
WHERE users.email LIKE '%@example.com';

-- Отримати список завдань, що не мають опису.
SELECT tasks.title 
FROM tasks
WHERE description = ''

-- Вибрати користувачів та їхні завдання, які є у статусі 'in progress'
SELECT users.name as user_name, users.email, tasks.id as task_id, tasks.title, tasks.description 
FROM users
INNER JOIN tasks ON users.id = tasks.user_id
INNER JOIN status ON tasks.status_id = status.id
WHERE status.name = 'in progress';

-- Отримати користувачів та кількість їхніх завдань.
SELECT users.id AS user_id, users.name AS user_name, COUNT(tasks.id) AS task_count
FROM users
LEFT JOIN tasks ON users.id = tasks.user_id
GROUP BY users.id, users.name;