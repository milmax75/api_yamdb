from django.db import models
from .validators import validate_year


class Category (models.Model):
    name = models.CharField('название категории', max_length=256)
    slug = models.SlugField(
        max_length=50,
        unique=True,
        db_index=True
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
        unique=True,
        db_index=True
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
        validators=[validate_year]
    )
    # добавить ограничение
    description = models.TextField('описание', blank=True)
    category = models.ForeignKey(        
        Category,        
        on_delete=models.SET_NULL,        
        related_name='titles',
        verbose_name='категория',
        help_text='выберете категорию',
        null = True,
        blank=True,
    )    
    genre =  models.ManyToManyField(        
        Genre,        
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='жанр',
        help_text='выберете жанр',
        null = True,
        blank=True,
    )

    class Meta:
        ordering = ('-year',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name

   



