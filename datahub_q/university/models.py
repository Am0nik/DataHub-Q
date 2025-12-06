from django.db import models
from ckeditor.fields import RichTextField

class UniversitySection(models.Model):
    number = models.PositiveIntegerField(verbose_name="Порядковый номер", default=1)
    title = models.CharField(max_length=255, verbose_name="Название раздела")
    short_description = models.TextField(verbose_name="Краткое описание")
    description = RichTextField(verbose_name="Полное описание", blank=True, null=True)

    class Meta:
        ordering = ['number']
        verbose_name = "Раздел университета"
        verbose_name_plural = "Разделы университета"

    def __str__(self):
        return f"{self.number}. {self.title}"


class University(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название университета")
    description = RichTextField(verbose_name="Описание университета", blank=True, null=True)
    main_image = models.ImageField(upload_to='university_images/', blank=True, null=True)
    programs_link = models.URLField(verbose_name="Ссылка на программы университета", blank=True, null=True)
    admission = RichTextField(verbose_name="Информация о поступлении", blank=True, null=True)
    international_cooperation = RichTextField(verbose_name="Международное сотрудничество", blank=True, null=True)
    d_tour = models.URLField(verbose_name="Ссылка на 3D-тур по университету", blank=True, null=True)
    city = models.CharField(max_length=255, verbose_name="Город", blank=True, null=True)
    specializations = models.PositiveIntegerField(verbose_name="Количество образовательных программ", blank=True, null=True)
    stipends_bk = models.PositiveIntegerField(verbose_name="Размер стипендии баклавра", blank=True, null=True)
    stipends_mg = models.PositiveIntegerField(verbose_name="Размер стипендии магистра", blank=True, null=True)
    stipends_doc = models.PositiveIntegerField(verbose_name="Стоимость стипендии доктора", blank=True, null=True)
    
    # связь с разделами университета
    sections = models.ManyToManyField(
        UniversitySection,
        related_name='universities',
        verbose_name="Разделы университета",
        blank=True
    )

    # связь с галереей фото
    gallery_images = models.ManyToManyField(
        'UniversityImage',
        related_name='universities',
        verbose_name="Галерея изображений",
        blank=True
    )

    class Meta:
        verbose_name = "Университет"
        verbose_name_plural = "Университеты"

    def __str__(self):
        return self.title


class UniversityRanking(models.Model):
    university = models.ForeignKey(
        University, 
        on_delete=models.CASCADE,
        related_name="rankings"
    )
    system = models.CharField(
        max_length=100,
        verbose_name="Система рейтинга (QS, QS Asia, THE, ARWU...)"
    )
    year = models.PositiveIntegerField(verbose_name="Год рейтинга", blank=True, null=True)
    rank_from = models.PositiveIntegerField(verbose_name="Рейтинг от", blank=True, null=True)
    rank_to = models.PositiveIntegerField(verbose_name="Рейтинг до", blank=True, null=True)

    class Meta:
        verbose_name = "Рейтинг университета"
        verbose_name_plural = "Рейтинги университета"

    def __str__(self):
        if self.rank_to:
            return f"{self.system} {self.year}: {self.rank_from}-{self.rank_to}"
        return f"{self.system} {self.year}: {self.rank_from}"


class Program(models.Model):
    university = models.ForeignKey(University, related_name='programs', on_delete=models.CASCADE, verbose_name="Университет")
    name = models.CharField(max_length=255, verbose_name="Название программы")
    faculty = models.CharField(max_length=255, verbose_name="Факультет")
    passing_score = models.PositiveIntegerField(verbose_name="Проходной балл", blank=True, null=True)
    code = models.CharField(max_length=20, verbose_name="Код программы")
    description = RichTextField(verbose_name="Описание программы", blank=True, null=True)
    link = models.URLField(verbose_name="Ссылка на программу", blank=True, null=True)

    class Meta:
        verbose_name = "Программа обучения"
        verbose_name_plural = "Программы обучения"

    def __str__(self):
        return self.name


class UniversityImage(models.Model):
    image = models.ImageField(upload_to='universities/gallery/', verbose_name="Фото")
    caption = models.CharField(max_length=255, blank=True, null=True, verbose_name="Подпись к фото")

    class Meta:
        verbose_name = "Фото университета"
        verbose_name_plural = "Фото университета"

    def __str__(self):
        return self.caption or f"Фото {self.id}"
