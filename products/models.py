from django.db import models


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.CharField(max_length=100, blank=False, null=False)
    price = models.FloatField(max_length=100, blank=False, null=False)
    is_available = models.IntegerField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="date created")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="last Update")

    class Meta:
        db_table = "product"
        ordering = ["id"]

    def __str__(self):
        return self.name
