from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    name = models.CharField('название категории', max_length=256)
    slug = models.SlugField(
        max_length=50,
        unique=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField('название жанра', max_length=256)
    slug = models.SlugField(
        max_length=50,
        unique=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField('название', max_length=256)
    year = models.IntegerField(
        'год',
        max_length=4,
    )
    # добавить ограничение
    description = models.TextField('описание', blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='категория',
        help_text='выберете категорию',
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='жанр',
        help_text='выберете жанр',
        null=True
    )

    class Meta:
        ordering = ('-year',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField(
        verbose_name='Рейтинг',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            ),
        ]


