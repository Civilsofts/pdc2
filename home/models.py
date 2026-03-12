from django.db import models
from ckeditor.fields import RichTextField


class Subscriber(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email ünvanı")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Abunə tarixi")

    class Meta:
        verbose_name = "Abunəçi"
        verbose_name_plural = "Abunəçilər"
        ordering = ['-created_at']

    def __str__(self):
        return self.email


class ServiceCategory(models.Model):
    name = models.CharField(max_length=256, verbose_name="Kateqoriya adı")
    slug = models.SlugField(max_length=256, unique=True, verbose_name="Slug (URL)")
    icon_class = models.CharField(
        max_length=128, blank=True, default="",
        verbose_name="İkon (CSS class)",
        help_text="Font Awesome class, məs: fas fa-home"
    )
    short_description = models.TextField(
        blank=True, default="",
        verbose_name="Qısa təsvir",
        help_text="Xidmətlər səhifəsində kartda görünəcək"
    )
    description = RichTextField(
        blank=True, default="",
        verbose_name="Ətraflı təsvir",
        help_text="Detal səhifəsində görünəcək"
    )
    image = models.ImageField(
        upload_to='services/', blank=True, null=True,
        verbose_name="Əsas şəkil"
    )
    banner_image = models.ImageField(
        upload_to='services/banners/', blank=True, null=True,
        verbose_name="Banner şəkli",
        help_text="Detal səhifəsinin başlıq hissəsi üçün"
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Sıra")
    is_active = models.BooleanField(default=True, verbose_name="Aktivdir")
    coming_soon = models.BooleanField(
        default=False, verbose_name="Tezliklə",
        help_text="Aktiv edildikdə alt xidmətlər əvəzinə 'Tezliklə' yazısı göstərilir"
    )

    class Meta:
        verbose_name = "Xidmət Kateqoriyası"
        verbose_name_plural = "Xidmət Kateqoriyaları"
        ordering = ['order']

    def __str__(self):
        return self.name


class ServiceItem(models.Model):
    category = models.ForeignKey(
        ServiceCategory, on_delete=models.CASCADE,
        related_name='items', verbose_name="Kateqoriya"
    )
    name = models.CharField(max_length=256, verbose_name="Xidmət adı")
    short_description = models.CharField(
        max_length=512, blank=True, default="",
        verbose_name="Qısa təsvir"
    )
    icon_class = models.CharField(
        max_length=128, blank=True, default="",
        verbose_name="İkon (CSS class)",
        help_text="Font Awesome class, məs: fas fa-wrench"
    )
    url = models.CharField(
        max_length=512, blank=True, default="",
        verbose_name="Link (URL)",
        help_text="Boş buraxsanız kateqoriya detal səhifəsinə yönləndirilir"
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Sıra")
    is_active = models.BooleanField(default=True, verbose_name="Aktivdir")

    class Meta:
        verbose_name = "Xidmət"
        verbose_name_plural = "Xidmətlər"
        ordering = ['order']

    def __str__(self):
        return f"{self.category.name} \u2192 {self.name}"
