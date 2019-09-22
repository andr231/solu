from django.contrib import admin

# Register your models here.
from .models import Producto, Comentario, ImagenesProducto, CarritoCompras

@admin.register(Producto,Comentario,ImagenesProducto, CarritoCompras)
class AuthorAdmin(admin.ModelAdmin):
    pass
