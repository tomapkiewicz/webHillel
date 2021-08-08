from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from .models import Page, Subscription, Day, Historial, Cuestionario, CuestionarioRespuesta
from registration.models import Profile
from .forms import PageForm 
from django.http import Http404, JsonResponse
from django.contrib.auth.models import AnonymousUser, User
from django.core.mail import send_mail
from django.template import loader
import threading
from datetime import datetime
from django.http import HttpResponse
import csv
from location.models import Provincia

def CuposAgotados(request,pk):
    page = get_object_or_404(Page, pk=pk)

    usu =  request.user.profile.nombre +' '+ request.user.profile.apellido if request.user.profile.nombre  is not None else request.user

    asunto = "Cupos agotados - " +   page.title 
    html_message = loader.render_to_string(
                'mail_body.html',
                {
                    'user_name': usu + ' quedó afuera!',
                    'subject':  'Se quiso anotar en ' + page.title + ' a las '
                    + str(page.horaDesde) + 'HS  '
                    + ' pero los cupos estaban agotados.' ,
                    'description': ' Comunicate con él haciendo click acá: https://wa.me/+54' + str(request.user.profile.whatsapp) ,                      
                }
            ) 
    to_mail = ('tomapkiewicz@gmail.com',)
    from_mail = 'Hillel Argentina <no_responder@domain.com>'

    rta = send_html_mail(asunto, html_message, to_mail, from_mail)
    
    response = {
        'is_taken': rta
    }
    return JsonResponse(response)


class EmailThread(threading.Thread):
    def __init__(self, subject, html_content, recipient_list, mail_from):
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        self.mail_from = mail_from
        threading.Thread.__init__(self)

    def run(self):
        send_mail(self.subject, self.html_content, self.mail_from, self.recipient_list,
        fail_silently=True, html_message=self.html_content)


def send_html_mail(subject, html_content, recipient_list, mail_from):
    EmailThread(subject, html_content, recipient_list, mail_from).start()


class StaffRequiredMixin(object):
    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(StaffRequiredMixin,
                     self).dispatch(request, *args, **kwargs)


# Create your views here.
class PageList(ListView):
    model = Page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['days'] = Day.objects.all()
        
        if self.request.user.is_anonymous:
            provincia = Provincia.objects.get(title="CABA")
        else:
            if self.request.user.profile is None:
                provincia = Provincia.objects.get(title="CABA")
            else:
                provincia = self.request.user.profile.provincia

        context['provincia'] = provincia
        

        for day in context['days']:
            if provincia is None:
                day.mostrar = day.HayActividadPresencial
            else:
                day.mostrar = Day.HayActividadPresencial_provincia(day,provincia)

        if len(self.kwargs) > 0:
            context['modalidad'] = self.kwargs['modalidad']
        else:
            context['modalidad'] = 0
        context['modalidadStr'] ='presencial' if context['modalidad'] == 0 else 'online'
        return context


class PageDetail(DetailView):
    model = Page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        
        cuestionario = Cuestionario.objects.find_or_create(page=self.object)
        if cuestionario is not None:
            context['cuestionario'] = cuestionario
            print(context['cuestionario'])


        if self.request.user.is_anonymous:
            return context
        subscribers = Subscription.objects.find_page(self.object)
        overlaps = Subscription.objects.overlaps(self.request.user, self.object)

        context['subscribers'] = subscribers
        context['overlaps'] = overlaps
        if subscribers is not None:
            context['usuarioAnotado'] = subscribers.filter(user=self.request.user).exists()
        return context


class PageConfirmation(ListView):
    model = Page


@method_decorator(staff_member_required, name="dispatch")
class PageCreate(CreateView):
    model = Page
    form_class = PageForm
    #success_url = reverse_lazy('pages:pages')

    def get_success_url(self):
        return reverse_lazy('pages:pages')+'?created'


@method_decorator(staff_member_required, name="dispatch")
class PageUpdate(UpdateView):
    model = Page
    form_class = PageForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse_lazy('pages:update', args=[self.object.id])+'?ok'


@method_decorator(staff_member_required, name="dispatch")
class PageDelete(DeleteView):
    model = Page
    success_url = reverse_lazy('pages:pages')


def Register(request, pk):
    if request.user.is_authenticated:
        page = get_object_or_404(Page, pk=pk)
        cuestionario = Cuestionario.objects.get(page=page)
        if cuestionario is not None:

            cuestionarioRespuesta = CuestionarioRespuesta.objects.find_or_create(user=request.user, page=page)

            if request.POST.get('respuesta1',None) is not None:
                cuestionarioRespuesta.pregunta1 = cuestionario.pregunta1
                cuestionarioRespuesta.respuesta1 = request.POST['respuesta1']

            if request.POST.get('respuesta2',None) is not None:
                cuestionarioRespuesta.pregunta2 = cuestionario.pregunta2
                cuestionarioRespuesta.respuesta2 = request.POST['respuesta2']   
   
            if request.POST.get('respuesta3',None) is not None:
                cuestionarioRespuesta.pregunta3 = cuestionario.pregunta3
                cuestionarioRespuesta.respuesta3 = request.POST['respuesta3']   

            if request.POST.get('respuesta4',None) is not None:
                cuestionarioRespuesta.pregunta4 = cuestionario.pregunta4
                cuestionarioRespuesta.respuesta4 = request.POST['respuesta4']   

            if request.POST.get('respuesta5',None) is not None:
                cuestionarioRespuesta.pregunta5 = cuestionario.pregunta5
                cuestionarioRespuesta.respuesta5 = request.POST['respuesta5']   
            
            cuestionarioRespuesta.save()       

        #Si la page es secreta validar la clave
        if page.secreta:
            if request.POST['password'] != page.clave:
                return redirect(reverse_lazy('pages:page', args=[page.id,])+ '?claveincorrecta')

        # Chequear que haya cupos disponibles (No debería llegar acá)
        if page.Qanotados >= page.cupo and page.cupo != 0:
            return redirect(reverse_lazy('pages:pages') + '?agotado')

        # chequear que el perfil esté completo
        if request.user.profile.validado is not True:
            return redirect(reverse_lazy('profile', args=[page.id,]) + '?completar=si&pk='+str(pk))

        subscription = Subscription.objects.find_or_create(request.user)
        subscription.pages.add(page)
    else:
        raise Http404("Usuario no está autenticado")

    # Mail automático
    asunto = "Te esperamos en " + page.title + "!"
    to_mail = [request.user.email]
    from_mail = 'Hillel Argentina <no_responder@domain.com>'
    host = request.get_host()
    textoExtraMail = page.textoExtraMail if page.textoExtraMail is not None else page.description 
    html_message = loader.render_to_string(
                'mail_body.html',
                {
                    'user_name': 'Hola ' + request.user.username + '!',
                    'subject':  'Te anotaste en ' + page.title + ' a las '
                    + str(page.horaDesde) + 'HS.'
                    + ' Podés darte de baja acá: '+host+'/pages/'+str(page.id),
                    'description':  textoExtraMail,
                }
            )

    send_html_mail(asunto, html_message, to_mail, from_mail)
    return redirect(reverse_lazy('home') + '?ok')


def Unregister(request, pk):
    if request.user.is_authenticated:
        page = get_object_or_404(Page, pk=pk)
        subscription = Subscription.objects.find_or_create(request.user)
        subscription.pages.remove(page)
    else:
        raise Http404("Usuario no está autenticado")
    return redirect(reverse_lazy('home')+'?remove')


def Asistencia(request, modalidad):
    if request.user.is_authenticated:
        dia = datetime.now().weekday()+1
        dias = Day.objects.all()
        pages = Page.objects.all()

        for day in dias:
            day.mostrar = Day.HayActividadPresencial_provincia(day, request.user.profile.provincia)


        return render(request, 'pages/asistencia.html',
        {'page_list': pages, 'dia': dia, 'days': dias, 'modalidad': modalidad})
    raise Http404("Usuario no está autenticado")


def AsistenciaDetail(request, pk, slug):
    if request.user.is_authenticated:
        page = get_object_or_404(Page, pk=pk)
        subscribers = Subscription.objects.find_page(page)
        return render(request, 'pages/asistencia_detail.html',
        {'page': page, 'subscribers': subscribers})
    raise Http404("Usuario no está autenticado")


def AsistenciaAdd(request, pk):
    json_response = {'created': False}
    if request.user.is_authenticated:
        username = request.GET.get('user', None)
        user = User.objects.get(username=username)
        if username:
            page = get_object_or_404(Page, pk=pk)

            hoy = datetime.now()
            historial = Historial.objects.find_or_create(page, hoy)
            historial.asistentes.add(user)

            #Se actualiza la lista de asistencias en el objeto de Historial 
            subscribers = Subscription.objects.find_page(page)
            for subscripcion in subscribers:
                historial.anotados.add(subscripcion.user)

            json_response['created'] = True
            json_response['hoy'] = hoy

            return JsonResponse(json_response)
    raise Http404("Usuario no está autenticado")


def AsistenciaRemove(request, pk):
    json_response = {'created': False}
    if request.user.is_authenticated:
        username = request.GET.get('user', None)
        user = User.objects.get(username=username)
        if username:
            page = get_object_or_404(Page, pk=pk)

            hoy = datetime.now()
            historial = Historial.objects.find_or_create(page, hoy)
            historial.asistentes.remove(user)

            json_response['created'] = True
            json_response['hoy'] = hoy

            return JsonResponse(json_response)
    raise Http404("Usuario no está autenticado")


def WriteRowAsistencias(h,writer):
    if h is None:
        return Http404("Historial no encontrado")
    if h.anotados.all() is None:
        return Http404("Historial sin anotados")
    if h.asistentes.all() is None:
        return Http404("Historial sin asistentes")

    for anotado in h.anotados.all():
        asistio = "Si"if anotado in h.asistentes.all() else "No"
        asis = 1 if asistio =="Si" else 0

        Profile.objects.get_or_create(user=anotado)

        writer.writerow([h.page.title, h.page.dia, h.page.horaDesde, 
        h.fecha, anotado,asistio,asis])


def DescargarAsistencias(request, pk):
    page = get_object_or_404(Page, pk=pk)

    response = HttpResponse(content='')
    response['Content-Disposition'] = 'attachment; filename=asistencias-' + \
        page.title + '-' + str(datetime.now()) + '.csv'
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response, dialect= 'excel')
    writer.writerow(['Actividad', 'Dia', 'Hora Desde', 'Fecha', 'Usuario anotado', 'Nombre', 'Apellido', 'Celular', 'Asistio?','Asis'])

    h = Page.historialHoy(page)

    WriteRowAsistencias(h,writer)
    return response



def DescargarHistoricoAsistenciasALLDetail(request):

    response = HttpResponse(content='')
    response['Content-Disposition'] = 'attachment; filename=asistenciasDETALLE-' + \
         'historico-' + str(datetime.now()) + '.csv'
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response, dialect= 'excel')
    writer.writerow(['Actividad','Dia','Hora Desde','Fecha', 'Usuario anotado','Asistio?','Asis'])

    historiales = Historial.objects.all()
    for h in historiales:
        h.fecha = h.fecha.strftime("%d/%m/%Y")
        WriteRowAsistencias(h,writer)  
    return response 
 

def DescargarHistoricoAsistenciasALLItem(request):

    #Genera un archivo por actividad-fecha y otro por actividad-fecha-asistente
    responseB = HttpResponse(content='')
    responseB['Content-Disposition'] = 'attachment; filename=asistenciasITEM-' + \
        'historico-' + str(datetime.now()) + '.csv'
    responseB.write(u'\ufeff'.encode('utf8'))
    writerB = csv.writer(responseB, dialect='excel')
    writerB.writerow(['Actividad','Dia','Hora Desde','Fecha', 'Qanotados','Qasistentes'])

    historiales = Historial.objects.all()
    for h in historiales:
        h.fecha = h.fecha.strftime("%d/%m/%Y")
        writerB.writerow([h.page.title, h.page.dia, h.page.horaDesde, h.fecha, h.Qanotados, h.Qasistentes])

    return responseB


def DescargarHistoricoAsistencias(request, pk):
    page = get_object_or_404(Page, pk=pk)

    response = HttpResponse(content='')
    response['Content-Disposition'] = 'attachment; filename=asistencias-' + \
        page.title + '-all-' + str(datetime.now()) + '.csv'
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response, dialect= 'excel')
    writer.writerow(['Actividad', 'Dia', 'Hora Desde', 'Fecha', 'Usuario anotado', 'Nombre', 'Apellido', 'Celular', 'Asistio?','Asis'])

    hs = Historial.objects.find_page(page=page)
    if hs is None:
        return Http404("Historial no encontrado")
    for h in hs:
        WriteRowAsistencias(h,writer)


    return response


def DescargarActividades(request):
    response = HttpResponse(content='')
    response['Content-Disposition'] = 'attachment; filename=actividades-' + \
        str(datetime.now()) + '.csv'
    
    response.write(u'\ufeff'.encode('utf8'))
    
    writer = csv.writer(response, dialect= 'excel')

    writer.writerow(['Titulo','Dia','Hora Desde','Hora Hasta',
                    'Cupo', 'Modalidad', 'Nuevo', 'Activa', 'Qanotados',  
                    'Categorias','responsable','colaborador','secreta','clave',])

    pages = Page.objects.all()

    for p in pages:
        if p is None:
            return Http404("Actividad no encontrada")
  
        writer.writerow([p.title,p.dia,p.horaDesde,p.horaHasta,p.cupo,
                p.modalidadSTR,p.nuevo,p.activa,p.Qanotados,p.categoriesSTR,
                p.responsable,p.colaborador,p.secreta,p.clave,])

    return response


def DescargarPerfiles(request):
    response = HttpResponse(content='')
    response['Content-Disposition'] = 'attachment; filename=perfiles-' + \
        str(datetime.now()) + '.csv'
    writer = csv.writer(response, dialect= 'excel')
    response.write(u'\ufeff'.encode('utf8'))
    writer.writerow(['Usuario', 'Nombre', 'Apellido','Fecha de nacimiento','Edad', 'Celular', 'Instagram',
     'Onward', 'Taglit', 'Cómo conoció Hillel', 'Estudios', 'Experiencia comunitaria', 'Intereses', ])
    
    profiles = Profile.objects.all()

    for p in profiles:
        if p is None:
            return Http404("Perfil no encontrado")
        if p.validado:
            writer.writerow([p, p.nombre, p.apellido, p.fechaNacimiento, p.edad, p.whatsapp, p.instagram,
            p.onward, p.taglit, p.comoConociste, p.estudios, p.experienciaComunitaria, p.interesesSTR])
    return response


def DescargarCuestionarios(request):
    response = HttpResponse(content='')
    response['Content-Disposition'] = 'attachment; filename=Cuestionarios-' + \
        str(datetime.now()) + '.csv'
    writer = csv.writer(response, dialect= 'excel')
    response.write(u'\ufeff'.encode('utf8'))
    writer.writerow(['Actividad', 'Pregunta1', 'Pregunta2','Pregunta3','Pregunta4','Pregunta5',])
    
    cuestionarios = Cuestionario.objects.all()

    for c in cuestionarios:
        if c is None:
            return Http404("Cuestionario no encontrado")
        writer.writerow([c.page.title,c.pregunta1,c.pregunta2,c.pregunta3,c.pregunta4,c.pregunta5,])
        return response


def DescargarCuestionariosRespuestas(request):
    response = HttpResponse(content='')
    response['Content-Disposition'] = 'attachment; filename=Cuestionarios-Respuestas-' + \
        str(datetime.now()) + '.csv'
    writer = csv.writer(response, dialect= 'excel')
    response.write(u'\ufeff'.encode('utf8'))
    writer.writerow(['Actividad', 'Pregunta1', 'Pregunta2','Pregunta3','Pregunta4','Pregunta5',
                    'Usuario', 'Respuesta1', 'Respuesta2','Respuesta3','Respuesta4','Respuesta5',])
    
    cuestionariosRespuesta = CuestionarioRespuesta.objects.all()

    for c in cuestionariosRespuesta:
        print(c.user)
        if c is None:
            return Http404("Cuestionario no encontrado")
        writer.writerow([c.page.title,c.pregunta1,c.pregunta2,c.pregunta3,c.pregunta4,c.pregunta5,
                        c.user.username,c.respuesta1,c.respuesta2,c.respuesta3,c.respuesta4,c.respuesta5])
    return response

def Exportar(request):
    if request.user.is_authenticated:
        return render(request, 'pages/exportar.html')
    raise Http404("Usuario no está autenticado")