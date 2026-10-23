from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.

class Comment(models.Model):
    """Comentário enviado pelo site público; lido e gerido no backend."""
    name = models.CharField(_("Nome"), max_length=50)
    email = models.EmailField(_("Email"), blank=True)
    body = models.TextField(_("Comentário"), max_length=500)
    created_at = models.DateTimeField(_("Data"), auto_now_add=True)
    is_read = models.BooleanField(_("Lido"), default=False)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["is_read", "-created_at"])]

    def __str__(self):
        return f"{self.name}: {self.body[:40]}"