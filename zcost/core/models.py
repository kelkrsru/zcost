from django.db import models


class CreatedModel(models.Model):
    """Абстрактная модель. Добавляет дату создания и дату обновления"""

    created = models.DateField(
        verbose_name='Дата создания',
        auto_now_add=True,
    )
    updated = models.DateField(
        verbose_name='Дата изменения',
        auto_now=True,
    )

    class Meta:
        abstract = True


class Portals(models.Model):
    """Модель портала Битрикс24"""
    member_id = models.CharField(
        verbose_name='Уникальный код портала',
        max_length=255,
        unique=True,
    )
    name = models.CharField(
        verbose_name='Имя портала',
        max_length=255,
    )
    auth_id = models.CharField(
        verbose_name='Токен аутентификации',
        max_length=255,
    )
    auth_id_create_date = models.DateTimeField(
        verbose_name='Дата получения токена аутентификации',
        auto_now=True,
    )
    refresh_id = models.CharField(
        verbose_name='Токен обновления',
        max_length=255,
    )
    client_id = models.CharField(
        verbose_name='Уникальный ID клиента',
        max_length=50,
        null=True,
        blank=True,
    )
    client_secret = models.CharField(
        verbose_name='Секретный токен клиента',
        max_length=100,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Портал'
        verbose_name_plural = 'Порталы'

    def __str__(self):
        return self.name


class Entity(CreatedModel):
    """Модель для хранения параметров сущности-объекта Б24."""
    general_number = models.CharField(
        verbose_name='Основная часть заводского номера',
        max_length=200,
        null=True,
        blank=True,
    )
    last_factory_number = models.PositiveIntegerField(
        verbose_name='Последний заводской номер',
        default=0,
    )
    portal = models.ForeignKey(
        Portals,
        verbose_name='Портал',
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class Responsible(CreatedModel):
    """Модель для хранения ответственных сотрудников из Б24."""
    id_b24 = models.PositiveIntegerField(
        verbose_name='ID в Битрикс24',
        db_index=True,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=255,
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=255,
        blank=True,
        null=True,
    )
    position = models.CharField(
        verbose_name='Должность',
        max_length=255,
        blank=True,
        null=True,
    )

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = 'Ответственный'
        verbose_name_plural = 'Ответственные'
