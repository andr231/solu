from django.contrib import admin

# Register your models here.
#from .models import Producto,Comentario,ImagenesProducto,CarritoCompras

#admin.site.register(Producto)
#admin.site.register(Comentario)
#admin.site.register(ImagenesProducto)
#admin.site.register(CarritoCompras)
from .models import Producto, Comentario, ImagenesProducto, CarritoCompras

@admin.register(Producto,Comentario,ImagenesProducto, CarritoCompras)
class AuthorAdmin(admin.ModelAdmin):
    pass
