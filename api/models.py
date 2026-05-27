from django.db import models


class Period(models.Model):
    """
    Геологический период.
    Хранит название и временные границы в миллионах лет назад.
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Название'
    )
    start_mya = models.IntegerField(
        verbose_name='Начало (млн лет назад)'
    )
    end_mya = models.IntegerField(
        verbose_name='Конец (млн лет назад)'
    )

    class Meta:
        verbose_name = 'Геологический период'
        verbose_name_plural = 'Геологические периоды'
        ordering = ['start_mya']  # от древних к новым

    def __str__(self):
        return f"{self.name} ({self.start_mya}-{self.end_mya} млн лет назад)"


class Diet(models.Model):
    """
    Тип питания динозавра.
    Например: хищник, травоядный, всеядный.
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Название'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )

    class Meta:
        verbose_name = 'Тип питания'
        verbose_name_plural = 'Типы питания'

    def __str__(self):
        return self.name


class Dinosaur(models.Model):
    """
    Динозавр.
    Содержит название, размеры (длина в метрах, вес в тоннах),
    привязку к геологическому периоду и типу питания.
    """
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    length_m = models.FloatField(
        verbose_name='Длина (метры)'
    )
    weight_t = models.FloatField(
        verbose_name='Вес (тонны)'
    )
    period = models.ForeignKey(
        Period,
        on_delete=models.CASCADE,
        related_name='dinosaurs',
        verbose_name='Период'
    )
    diet = models.ForeignKey(
        Diet,
        on_delete=models.CASCADE,
        related_name='dinosaurs',
        verbose_name='Тип питания'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )

    class Meta:
        verbose_name = 'Динозавр'
        verbose_name_plural = 'Динозавры'
        ordering = ['name']

    def __str__(self):
        return self.name