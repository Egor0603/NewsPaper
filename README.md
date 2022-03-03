# skillfactory_newspaper

Репозиторий учебного проекта NewsPaper для курса "Fullstack python".

База данных: sqlite

Состоит из единственного приложения news.

Оно включает в себя модели:

Author. Авторы статей/новостей (далее - постов).

Category. Категории постов.

Post. Модель поста (новость/статья).

PostCategory. Промежуточная модель (явная) для связи "многие ко многим" Post-Category.

Comment. Комментарии к постам.



Помимо этого в корневой директории содержится файл commands.py, содержащий функцию todo(). 
В этой функции написан список команд, которые студенты курса должны писать в DjangoShell. 
На основе этого ориентировочного списка команд, ментор сможет проверять отправленные студентом команды для проверки.

По всем вопросам, которые касаются слоя моделей, можно писать на почту misha.svintsow@gmail.com или в Telegram: @mishavsv.