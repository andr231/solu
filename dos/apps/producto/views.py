from django.shortcuts import render,HttpResponse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView, TemplateView, CreateView, DeleteView
from .models import Producto,Comentario,CarritoCompras
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q, Max, Min
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect

#from .models import Producto
#from django.views.generic import TemplateView
# Create your views here.
class Indice(TemplateView):
    template_name = 'index.html'
"""ver todos los  producto s """

class ListadoProducto(ListView):
    template_name = 'listado_productos.html' 
    model = Producto
    paginate_by = 10

    def get_queryset(self):
        query = None

        if ('nombre' in self.request.GET) and self.request.GET['nombre'] != "":
            query = Q(nombre=self.request.GET["nombre"])

        if ('maximo' in self.request.GET) and self.request.GET['maximo'] != "":
            try:
                if query == None:
                    query = Q(precio__lte=int(float(self.request.GET['maximo'])))
                else:
                    query = query & Q(precio__lte=int(float(self.request.GET['maximo'])))
            except:
                pass


        if ('minimo' in self.request.GET) and self.request.GET['minimo'] != "":
            try:
                if query == None:
                    query = Q(precio__gte=int(float(self.request.GET['minimo'])))
                else:
                    query = query & Q(precio__gte=int(float(self.request.GET['minimo'])))
            except:
                pass


        if query is not None:
            productos = Producto.objects.filter(query)
        else:
            productos = Producto.objects.all()
        return productos
"""ver los detalles del  producto comprado o antes de comprar """

class DetalleProducto(DetailView):
    template_name = 'detalle.html'
    model = Producto
"""anadir un  comentario al producto comprado """
class ComentarioProducto(CreateView):
    template_name = 'detalle.html'
    model = Comentario
    fields = ('comentario','usuario','producto',)

    def get_success_url(self):
        return "/detalle_producto/{}/".format(self.object.producto.pk)
"""anadir un producto al carrrito"""
class AniadirCarrito(CreateView):
    model = CarritoCompras
    fields = ('usuario','producto','precio',)
    success_url = reverse_lazy('indice')
    login_url = 'ingresar'

class EliminarCarrito(DeleteView):
    queryset = CarritoCompras.objects.filter(comprado=False)
    model = CarritoCompras
    success_url = reverse_lazy('indice')
    login_url = 'ingresar'

class ListarCarrito(ListView):
    template_name = 'carrito.html'
    model = CarritoCompras
    queryset = CarritoCompras.objects.filter(comprado=False,pendiente=False)
    login_url = 'ingresar'

    def get_context_data(self, **kwargs):
        context = super(ListarCarrito, self).get_context_data(**kwargs)
        context['tab'] = 'sincomprar'
        return context

class ListarCarritoPendientes(ListView):
    template_name = 'carrito.html'
    model = CarritoCompras
    queryset = CarritoCompras.objects.filter(comprado=False,pendiente=True)
    login_url = 'ingresar'

    def get_context_data(self, **kwargs):
        context = super(ListarCarritoPendientes, self).get_context_data(**kwargs)
        context['tab'] = 'pendientes'
        return context 

class ListarCarritoFinalizadas(ListView):
    template_name = 'carrito.html'
    model = CarritoCompras
    queryset = CarritoCompras.objects.filter(comprado=True,pendiente=False)
    login_url = 'ingresar'

    def get_context_data(self, **kwargs):
        context = super(ListarCarritoFinalizadas, self).get_context_data(**kwargs)
        context['tab'] = 'finalizadas'
        return context


class CambiarPerfil(UpdateView):
  #model = User 
    fields = ('telefono','last_name','first_name','email',)
    success_url = '/'
    template_name = 'perfil.html'

    def get_object(self, queryset=None):
        return self.request.user


"""login""""""
def registrar(request):
	nombre =  request.POST.get("nombre")
	apellidos = request.POST.get("apellidos")
	correo = request.POST.get("correo")
	usuario = request.POST.get("usuario")
	password = request.POST.get("password")
	terminos = request.POST.getlist("terminos")
	privacidad = request.POST.getlist("aviso")

    user = User.objects.filter(username=usuario).exists()
    if user == False:
        if terminos and privacidad:
            user = User.objects.create_user(first_name=nombre,
            last_name = apellidos,
            email = correo,
            username = usuario,
            password = password)
        user = authenticate(request, username=usuario, password=password)
        print("ESTE ES EL USUARIO QUE ACABO DE REGISTRAR", user)
        user.is_active = False
        user.save()

        current_site = get_current_site(request)
        mail_subject = 'Activacion de cuenta'
        message = render_to_string('acc_active_email.html',{
            'user':user,
            'domain':current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            'token':account_activation_token.make_token(user),
            })
        emaild = EmailMessage(mail_subject, message, to = [correo])
        emaild.send()

        usuarioCreado = 2
        data = { "usuarioCreado":usuarioCreado }

        return JsonResponse(data, safe=False)
    else:
         usuarioRep = 0
         data = { "usuarioRep":usuarioRep }
         return JsonResponse(data, safe=False)

def iniciosesion(request):
    username = request.POST.get("usuario")
    password = request.POST.get("password")

    try:
        username = authenticate(request, username=username, password=password)
        login(request,username)
        return redirect('home')
    except Exception as e:
        sweetify.error(request, 'Oops!', text='�El Usuario y/o Contrase�a es Incorrecto!', persistent=':�(')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))


def cerrarsesion(request):
    logout(request)
    return HttpResponseRedirect("/")

    
"""