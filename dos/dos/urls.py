"""dos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL pythonto urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from apps.producto.views import (Indice,ListadoProducto,DetalleProducto,
                                ComentarioProducto,AniadirCarrito,EliminarCarrito,
                                ListarCarrito,ListarCarritoPendientes,ListarCarritoFinalizadas,
                                CambiarPerfil)
""" 
          
    
"""
 

urlpatterns = [
    path('', admin.site.urls),
    path('tienda/',Indice.as_view(),name='indice'),
    path('listado_productos/',ListadoProducto.as_view(),name='listado_productos'),
   # path('ingresar/',ingresar.as_view(),name='ingresar'),
    path('detalle_producto/<int:pk>/',DetalleProducto.as_view(),name='detalle_productos'),
    path('crear_comentario/',ComentarioProducto.as_view(),name='crear_comentario'),
    path('aniadir_carrito/',AniadirCarrito.as_view(),name='aniadir_carrito'),
    path('eliminar_carrito/<int:pk>/',EliminarCarrito.as_view(),name='eliminar_carrito'),
    path('listar_carrito/',ListarCarrito.as_view(),name='listar_carrito'),
    path('listar_pendientes/',ListarCarritoPendientes.as_view(),name='listar_pendientes'),
    path('listar_finalizado/',ListarCarritoFinalizadas.as_view(),name='listar_finalizado'),
    path('cambiar_perfil/',CambiarPerfil.as_view(),name='cambiar_perfil'),




]


if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)