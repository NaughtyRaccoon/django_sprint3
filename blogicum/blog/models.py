from django.db import models
from django.contrib.auth.models import User


TITLESIZE = 256


class PublishedModel(models.Model):
    """
    Абстрактная модель.
    Добавляет к модели дату создания и флаг опубликовано.
    """

    is_published = models.BooleanField(
        default=True,
        blank=False,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено'
    )

    class Meta:
        abstract = True


class Post(PublishedModel):
    title = models.CharField(
        max_length=TITLESIZE,
        blank=False,
        null=False,
        verbose_name='Заголовок'
    )
    text = models.TextField(blank=False, null=False, verbose_name='Текст')
    pub_date = models.DateTimeField(
        blank=False,
        null=False,
        verbose_name='Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем — можно делать '
            'отложенные публикации.'
        )
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        'Location',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title


class Category(PublishedModel):
    title = models.CharField(
        max_length=TITLESIZE,
        blank=False,
        null=False,
        verbose_name='Заголовок'
    )
    description = models.TextField(
        blank=False,
        null=False,
        verbose_name='Описание'
    )
    slug = models.SlugField(
        max_length=64,
        unique=True,
        blank=False,
        null=False,
        verbose_name='Идентификатор',
        help_text=(
            'Идентификатор страницы для URL;'
            ' разрешены символы латиницы, цифры, дефис и подчёркивание.'
        )
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(PublishedModel):
    name = models.CharField(
        max_length=TITLESIZE,
        blank=False,
        null=False,
        verbose_name='Название места'
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name
