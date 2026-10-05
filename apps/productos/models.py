from django.db import models

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField("Nombre de la categoría", max_length=100, unique=True)
    descripcion = models.TextField("Descripción de la categoria", blank = True)

    class Meta:
        db_table = "categorias"
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre    