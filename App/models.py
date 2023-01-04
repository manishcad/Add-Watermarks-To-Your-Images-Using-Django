from django.db import models
import uuid
# Create your models here.


class Watermark(models.Model):
    udi = models.UUIDField(
        default=uuid.uuid4, primary_key=True, editable=False)
    image = models.ImageField(upload_to="watermark_images")
    text = models.CharField(max_length=50)

    def __str__(self) -> str:
        return str(self.text)
