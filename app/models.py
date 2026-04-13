import secrets

from django.db import models

ID_LENGTH = 8


def generate_unique_id():
    for _ in range(10):
        id = secrets.token_urlsafe(ID_LENGTH)[:ID_LENGTH]
        if not Link.objects.filter(id=id).exists():
            return id
    raise RuntimeError("Could not generate a unique link ID after 10 attempts")


class Link(models.Model):
    id = models.CharField(primary_key=True, max_length=12)
    url = models.URLField(max_length=2048)
    created_at = models.DateTimeField(auto_now_add=True)
    clicks = models.IntegerField(default=0)
    ip = models.GenericIPAddressField(null=True)

    def __str__(self):
        return self.url

    def save(self, *args, **kwargs):
        if not self.pk:
            self.id = generate_unique_id()
        super().save(*args, **kwargs)


