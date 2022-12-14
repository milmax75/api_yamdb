from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
from .validators import validate_year, validate_username
from core.models import CreatedModel, GenreCategoryModel


class UserCustomized(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    )

    username = models.CharField(max_length=150,
                                unique=True,
                                validators=(validate_username,))
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.TextField(max_length=150, blank=True)
    last_name = models.TextField(max_length=150, blank=True)
    bio = models.CharField(max_length=500, blank=True)
    role = models.CharField(max_length=10,
                            choices=ROLE_CHOICES,
                            default='user')

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser


class Category(GenreCategoryModel):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(GenreCategoryModel):
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField('название', max_length=256)
    year = models.IntegerField(
        verbose_name='год',
        validators=(validate_year,)
    )
    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True
    )
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
        related_name='titles',
        verbose_name='жанр',
        help_text='выберете жанр',
        null=True
    )
    rating = models.IntegerField(
        verbose_name='рейтинг',
        null=True,
        default=None
    )

    class Meta:
        ordering = ('-year',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(CreatedModel):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    author = models.ForeignKey(
        UserCustomized,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField(
        verbose_name='Рейтинг',
        validators=(
            MinValueValidator(1),
            MaxValueValidator(10),
        )
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('pub_date',)
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='unique_review'
            ),
        )


class Comment(CreatedModel):
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        UserCustomized,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='comments'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('pub_date',)
