# api_yamdb
api_yamdb
''' The YaMDb project was created to post user reviews on works posted on any other resources. The works themselves are not stored in YaMDb; you cannot watch a movie or listen to music here. The works are divided into categories such as "Books", "Films", "Music". For example, in the category "Books" there may be works "Winnie the Pooh and All-All-All" and "The Martian Chronicles", and in the category "Music" - the song "Yesterday" by the group "Beetles" and the second suite of Bach. The list of categories can be expanded (for example, you can add the category "Fine Arts" or "Jewellery"). A work can optionally be assigned a genre from the list of preset ones (for example, "Fairy Tale", "Rock" or "Arthouse"). Only the administrator can add works, categories and genres. Grateful or indignant users leave text reviews for the works and rate the work in the range from one to ten (an integer); from user ratings, an average rating of the work is formed - rating (integer). A user can leave only one review per work. Other users can leave comments on previously posted reviews. 
Only authenticated users can add reviews, comments and rate.

Проект YaMDb создан для размещения отзывов пользователей на произведения, размещенных на любых других ресурсах. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).
Произведению опционально может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»).
Добавлять произведения, категории и жанры может только администратор.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.
Другие пользователи могут оставлять комментарии к ранее оставленным отзывам.
Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.'''

### Команда проекта:
- milmax75 (Тимлид и разработчик 1: автор части, касающейся управления пользователями)
- Natali-cat (разработчик 2: автор части, касающейся произведений, категорий, жанров)
- D-Nevskiy (разработчик 3: автор части, касающейся отзывов, комментариев и рейтинга произведений)


### Установка.
##### Как развернуть проект на локальной машине

**Клонировать репозиторий и перейти в него в командной строке:**
Скопируйте SSH Code
> git clone * *вставьте SSH Code* *
> cd api_yamdb

Cоздать и активировать виртуальное окружение:
> python -m venv venv
> source venv/Scripts/activate

Установить зависимости из файла requirements.txt:
> python -m pip install --upgrade pip
> pip install -r requirements.txt

Выполнить миграции:
> python manage.py migrate

Запустить проект:
> python manage.py runserver

Если есть необходимость, заполнить базу тестовыми данными:
>python manage.py dataimport

### Примеры.
##### Некоторые примеры запросов к API.

**Аутенитфикация**

POST api/v1/auth/signup/
Зарегистрирует пользователя

POST api/v1/auth/token/
Выдаст токен


**Категории (типы) произведений**

GET/categories/
выведет информацию обо всех записях

POST api/v1/categories/
добавит новую запись

DELETE api/v1/categories/{slug}/
Удалит запись


**Категории жанров**

GET api/v1/genres/
выведет информацию обо всех записях

POST api/v1/genres/
добавит новую запись

DELETE api/v1/genres/{slug}/
Удалит запись


**Произведения, к которым пишут отзывы (определённый фильм, книга или песенка)**

GET api/v1/titles/
выведет информацию обо всех записях

POST api/v1/titles/
добавит новую запись

GET api/v1/titles/{titles_id}/
выведет информацию о конкретной записи

PATCH api/v1/titles/{titles_id}/
заменит информацию в записи

DELETE api/v1/titles/{titles_id}/
Удалит запись


**Отзывы**

GET api/v1/titles/{title_id}/reviews/
выведет информацию обо всех записях

POST api/v1/titles/{title_id}/reviews/
добавит новую запись

GET api/v1/titles/{title_id}/reviews/{review_id}/
выведет информацию о конкретной записи

PATCH api/v1/titles/{title_id}/reviews/{review_id}/
заменит информацию в записи

DELETE api/v1/titles/{title_id}/reviews/{review_id}/
Удалит запись


**Комментарии к отзывам**

GET api/v1/titles/{title_id}/reviews/{review_id}/comments/
выведет информацию обо всех записях

POST api/v1/titles/{title_id}/reviews/{review_id}/comments/
добавит новую запись

GET api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
выведет информацию о конкретной записи

PATCH api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
заменит информацию в записи

DELETE api/v/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
Удалит запись


**Пользователи**

GET api/v1/users/
выведет информацию обо всех записях

POST api/v1/users/
добавит новую запись

GET api/v1/users/{username}/
выведет информацию о конкретной записи

PATCH api/v1/users/{username}/
заменит информацию в записи

DELETE api/v1/users/{username}/
Удалит запись

GET api/v1/users/me/
выведет информацию об обращающемся пользователе

PATCH ai/v1/users/me/
заменит информацию об обращающемся пользователе
