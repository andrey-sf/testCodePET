Admin Panel
Access the admin panel at:

URL: http://localhost:8000/admin
Login: admin@admin.ru
Password: admin


команда для запуска генерации файковых данных:
python manage.py create_mock_data



инструкция регистрации:
создания пользователя
http://localhost:8000/schema/swagger-ui/#/users/users_create

создания JWT токена 
http://localhost:8000/schema/swagger-ui/#/jwt/jwt_create_create

авторизация в верхнем правом углу по access токену(не забудьте добавть JWT к токену)
