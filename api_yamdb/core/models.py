from django.db import models


class CreatedModel(models.Model):
    text = models.TextField(
        verbose_name='Текст',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        abstract = True


class GenreCategoryModel(models.Model):
    name = models.CharField(
        'название',
        max_length=256,
        unique=True
    )
    slug = models.SlugField(
        max_length=50,
        unique=True
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
