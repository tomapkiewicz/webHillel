from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.db.models import F
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from .models import Page
from .cuestionario import Cuestionario, CuestionarioRespuesta
from .subscription import Subscription
from .historial import Historial
from registration.models import Profile
from .forms import PageForm
from django.http import Http404, JsonResponse
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template import loader
import threading
from datetime import datetime, timedelta
from django.http import HttpResponse
import csv
from social.models import MailContacto
import pytz
from django.template.defaultfilters import date as date_format
from datetime import date
from django.db.models import Q
from django.core.files.base import ContentFile
from django.core.mail import EmailMultiAlternatives
import qrcode
from io import BytesIO
from email.mime.image import MIMEImage

from itertools import groupby
from operator import attrgetter
import re  

@staff_member_required
def enviar_mails_confirmados(request, page_id):
    page = get_object_or_404(Page, pk=page_id)

    # Solo los que fueron confirmados
    confirmados = Subscription.objects.find_page(page).filter(pages_confirmadas=page)

    enviados = 0
    for subs in confirmados:
        user = subs.user
        nombre = user.profile.nombre or user.username
        cuerpo_default = f"Hola {nombre}! Confirmamos tu inscripción a {page.title} el día {page.fecha} a las {page.horaDesde}HS."
        cuerpo = page.cuerpo_mail if page.con_mail_personalizado else cuerpo_default
        asunto = page.asunto_mail if page.con_mail_personalizado else f"Confirmación: {page.title}"

        qr_data, qr_image = generar_qr_para_subscription(subs, page, user, request.get_host())

        enviar_mail_confirmacion(
            user=user,
            page=page,
            qr_data=qr_data,
            qr_image=qr_image,
            asunto=asunto,
            cuerpo=cuerpo
        )
        enviados += 1

    from django.contrib import messages
    messages.success(request, f"Se enviaron {enviados} mails a personas confirmadas.")
    return redirect("pages:page", pk=page.id)


def generar_qr_para_subscription(subscription, page, user, host):
    qr_data = f"/pages/validate_qr/{page.id}/{user.id}"
    if "127.0.0.1" not in host:
        qr_data = f"https://{host}{qr_data}"
    qr = qrcode.make(qr_data)
    qr_image = BytesIO()
    qr.save(qr_image, format="PNG")
    qr_image_content = ContentFile(qr_image.getvalue(), name=f"qr_{user.id}_{page.id}.png")
    subscription.qr_code.save(f"qr_{user.id}_{page.id}.png", qr_image_content)
    return qr_data, qr_image


def enviar_mail_confirmacion(user, page, qr_data, qr_image, asunto=None, cuerpo=None):
     
    html_message = loader.render_to_string("mail_body.html", {
                "texto_extra": page.textoExtraMail,
                "texto_alerta": page.alerta,
                "mail_body": cuerpo,
                "qr_url": qr_data,  # Link for QR validation
                "personalizado": page.con_mail_personalizado,
    })

    email = EmailMultiAlternatives(asunto, "", "Hillel Argentina <no_responder@domain.com>", [user.email])
    email.attach_alternative(html_message, "text/html")
    if qr_image:
        email.attach(f"qr_{user.id}_{page.id}.png", qr_image.getvalue(), "image/png")
    email.send()


@staff_member_required
def unconfirm_subscription(request, page_id, user_id):
    page = get_object_or_404(Page, pk=page_id)
    user = get_object_or_404(User, pk=user_id)
    subscription = Subscription.objects.find_or_create(user)

    if page in subscription.pages_confirmadas.all():
        subscription.pages_confirmadas.remove(page)

    return redirect('pages:page', pk=page.id)

def ConfirmSubscription(request, page_id, user_id):
    if not request.user.is_staff:
        raise Http404("No autorizado")

    page = get_object_or_404(Page, pk=page_id)
    user = get_object_or_404(User, pk=user_id)
    subscription = Subscription.objects.find_or_create(user)
    subscription.pages_confirmadas.add(page)


    return redirect(reverse("pages:page", args=[page.id]))

def CuposAgotados(request, pk):
    page = get_object_or_404(Page, pk=pk)
    usu = (
        request.user.profile.nombre + "  " + request.user.profile.apellido
        if request.user.profile.nombre is not None
        else request.user
    )

    formatted_fecha = date_format(page.fecha, r"l d \d\e F")

    asunto = "Cupos agotados - " + page.title
    html_message = loader.render_to_string(
        "mail_body.html",
        {
            "user_name": usu
            + " https://wa.me/+549"
            + str(request.user.profile.whatsapp)
            + " "
            + (
                request.user.profile.perfil_ok
                if request.user.profile.perfil_ok is not None
                else ""
            ),
            "subject": "Se quiso anotar en "
            + page.title
            + " a las "
            + str(page.horaDesde)
            + ("HS  el día " + formatted_fecha if page.fecha is not None else "")
            + " pero los cupos estaban agotados.",
        },
    )
    mailContacto = MailContacto.objects.first()
    to_mail = (mailContacto,)
    from_mail = "Hillel Argentina"
    rta = send_html_mail(asunto, html_message, to_mail, from_mail)
    response = {"is_taken": rta}
    return JsonResponse(response)


def send_html_mail(subject, html_content, recipient_list, mail_from):
    mail = send_mail(
        subject,
        html_content,
        mail_from,
        recipient_list,
        fail_silently=True,
        html_message=html_content,
    )


class StaffRequiredMixin(object):
    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(StaffRequiredMixin, self).dispatch(request, *args, **kwargs)


# Create your views here.
def Onward(request):
    return render(request, "pages/onward.html")


class PageList(ListView):
    model = Page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_anonymous:
            provincia = None
        else:
            profile = Profile.objects.get_or_create(user=self.request.user)
            if profile is None:
                provincia = None
            else:
                provincia = self.request.user.profile.provincia

        context["provincia"] = provincia
        local_tz = pytz.timezone("America/Argentina/Buenos_Aires")
        today = datetime.now(local_tz).date()

        if provincia is not None:
            active_pages = Page.objects.filter(
                Q(modalidad=True) | Q(provincia=provincia),
                activa=True,
                oculta=False,
                cowork=False,
                fecha__gte=today,
            ).order_by("fecha", "horaDesde", "-title")
        else:
            active_pages = Page.objects.filter(
                activa=True,
                oculta=False,
                cowork=False,
                fecha__gte=today,
            ).order_by("fecha", "horaDesde", "-title")

        active_pages_map = {}
        recurrent_pages_map = {}

        for page in active_pages:
            if page.recurrent_page is None:
                if page.fecha not in active_pages_map:
                    active_pages_map[page.fecha] = []
                active_pages_map[page.fecha].append(page)
            else:
                recurrent_page_id = (
                    page.recurrent_page.id
                )  # Get the id of the recurrent_page
                if recurrent_page_id not in recurrent_pages_map:
                    if page.fecha not in active_pages_map:
                        active_pages_map[page.fecha] = []
                    active_pages_map[page.fecha].append(page)
                    recurrent_pages_map[recurrent_page_id] = True

        
        #New way to group by title
        cowork_pages = Page.objects.filter(activa=True,oculta=False, cowork=True)

        for page in cowork_pages:
            match = re.split(r'\s*[-–—]\s*', page.title.strip(), maxsplit=1)

            if len(match) == 2:
                separator, activity_name = match
            else:
                separator = activity_name = page.title.strip()

            page.separator = separator.strip()
            page.activity_name = activity_name.strip()

        # 🔑 ordenamos antes de agrupar
        cowork_pages = sorted(cowork_pages, key=lambda p: p.separator)

        from itertools import groupby

        cowork_grouped = {}
        for sep, group in groupby(cowork_pages, key=lambda p: p.separator):
            cowork_grouped[sep] = list(group)

        context["cowork_grouped"] = cowork_grouped

        
        #context["cowork_grouped"] = dict(cowork_grouped)  # importante: casteamos a dict
        
        context["cowork_pages"] = cowork_pages
        context["active_pages_map"] = active_pages_map
        context["cowork_pages"] = cowork_pages

        if len(self.kwargs) > 0:
            context["cowork"] = self.kwargs["modalidad"]
        else:
            context["cowork"] = 0
        context["coworkStr"] = "calendario" if context["cowork"] == 0 else "cowork"

        return context


class PageDetail(DetailView):
    model = Page

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        local_tz = pytz.timezone("America/Argentina/Buenos_Aires")
        current_date = datetime.now(local_tz)


        if obj.fecha and obj.fecha < current_date.date():
            obj.activa = False
            obj.save()

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()

        cuestionario = Cuestionario.objects.find_or_create(page=self.object)
        if cuestionario is not None:
            context["cuestionario"] = cuestionario
            context["preguntas_range"] = range(1, 21) 
            print(context["cuestionario"])

        if self.request.user.is_anonymous:
            return context
        subscribers = Subscription.objects.find_page(self.object)
        overlaps = Subscription.objects.overlaps(self.request.user, self.object)
        # Orden alfabético sin distinguir mayúsculas/minúsculas
        subscribers_ordenados = sorted(
            subscribers,
            key=lambda sub: (
                sub.user.profile.apellido.lower() if sub.user.profile.apellido else '',
                sub.user.profile.nombre.lower() if sub.user.profile.nombre else ''
            )
        )

        context["subscribers_ordenados"] = subscribers_ordenados
        context["subscribers"] = subscribers
        context["overlaps"] = overlaps
        if subscribers is not None:
            context["usuarioAnotado"] = subscribers.filter(
                user=self.request.user
            ).exists()
        return context


class PageConfirmation(ListView):
    model = Page


@method_decorator(staff_member_required, name="dispatch")
class PageCreate(CreateView):
    model = Page
    form_class = PageForm
    # success_url = reverse_lazy('pages:pages')

    def get_success_url(self):
        return reverse_lazy("pages:pages") + "?created"


@method_decorator(staff_member_required, name="dispatch")
class PageUpdate(UpdateView):
    model = Page
    form_class = PageForm
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse_lazy("pages:update", args=[self.object.id]) + "?ok"

    def form_valid(self, form):
        self.object = form.save()

        if self.object.recurrent_page:
            recurrent_pages = self.object.recurrent_page.pages
            recurrent_pages.update(
                title=self.object.title,
                horaDesde=self.object.horaDesde,
                horaHasta=self.object.horaHasta,
                modalidad=self.object.modalidad,
                provincia=self.object.provincia,
                description=self.object.description,
                cupo=self.object.cupo,
                nuevo=self.object.nuevo,
                activa=self.object.activa,
                oculta=self.object.oculta,
                responsable=self.object.responsable,
                colaborador=self.object.colaborador,
                secreta=self.object.secreta,
                clave=self.object.clave,
                textoExtraMail=self.object.textoExtraMail,
                con_mail_personalizado=self.object.con_mail_personalizado,
                asunto_mail=self.object.asunto_mail,
                cuerpo_mail=self.object.cuerpo_mail,
            )
        return super().form_valid(form)


@method_decorator(staff_member_required, name="dispatch")
class PageDelete(DeleteView):
    model = Page
    success_url = reverse_lazy("pages:pages")


def Register(request, pk):
    if not request.user.is_authenticated:
        raise Http404("Usuario no está autenticado")

    page = get_object_or_404(Page, pk=pk)
    cuestionario = Cuestionario.objects.get(page=page)

    # Guardar respuestas
    if cuestionario:
        cuestionarioRespuesta, _ = CuestionarioRespuesta.objects.get_or_create(user=request.user, page=page)
        for i in range(1, 21):
            respuesta_key = f"respuesta{i}"
            if request.POST.get(respuesta_key):
                setattr(cuestionarioRespuesta, f"pregunta{i}", getattr(cuestionario, f"pregunta{i}"))
                setattr(cuestionarioRespuesta, f"respuesta{i}", request.POST[respuesta_key])
        cuestionarioRespuesta.save()

    if page.secreta and request.POST.get("password") != page.clave:
        return redirect(reverse_lazy("pages:page", args=[page.id]) + "?claveincorrecta")

    if page.Qanotados >= page.cupo and page.cupo != 0:
        return redirect(reverse_lazy("pages:pages") + "?agotado")

    if not request.user.profile.validado:
        return redirect(reverse_lazy("profile", args=[page.id]) + "?completar=si&pk=" + str(pk))

    subscription, _ = Subscription.objects.get_or_create(user=request.user)
    pages_to_add = page.recurrent_page.pages.all() if page.recurrent_page else [page]
    subscription.pages.add(*pages_to_add)

    con_qr = not page.con_preinscripcion
    if con_qr:
        qr_data, qr_image = generar_qr_para_subscription(subscription, page, request.user, request.get_host())
    else:
        qr_data, qr_image = None, None

    nombre = request.user.profile.nombre if request.user.profile.nombre is not None else request.user.username
    cuerpo_default = f"Hola {nombre}! \n Te anotaste en {page.title} el día {page.fecha} a las {page.horaDesde}HS. \n\n"
    cuerpo = page.cuerpo_mail if page.con_mail_personalizado else cuerpo_default
    asunto = page.asunto_mail if page.con_mail_personalizado else f"Te {'anotaste' if page.con_preinscripcion else 'esperamos'} en {page.title} {'Online' if page.modalidad else 'Presencial'}!"
    enviar_mail_confirmacion(
        cuerpo=cuerpo,
        user=request.user,
        page=page,
        qr_data=qr_data,
        qr_image=qr_image,
        asunto=asunto  
    )

    return redirect(reverse_lazy("home") + "?ok")

def validate_qr(request, page_id, user_id):
    """Validate QR Code when scanned"""
    try:
        page = Page.objects.get(id=page_id)
    except Page.DoesNotExist:
        return JsonResponse({"status": "invalid", "message": "QR Code is not valid! (page not found)"})

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"status": "invalid", "message": "QR Code is not valid! (user not found)"})

    if Subscription.objects.filter(user=user, pages=page).exists():
        return JsonResponse({"status": "valid", "message": "QR Code is valid!", "user": user.username})

    return JsonResponse({"status": "invalid", "message": "QR Code is not valid! (not subscribed)"})

def Unregister(request, pk):
    if request.user.is_authenticated:
        page = get_object_or_404(Page, pk=pk)
        subscription = Subscription.objects.find_or_create(request.user)
        
        if page.recurrent_page:
            # Si la actividad pertenece a una actividad recurrente, eliminar todas sus instancias
            related_pages = page.recurrent_page.pages.all()
            subscription.pages.remove(*related_pages)
        else:
            # Si no es recurrente, eliminar solo la actividad específica
            subscription.pages.remove(page)

    else:
        raise Http404("Usuario no está autenticado")
    return redirect(reverse_lazy("home") + "?remove")
from django.db.models import Q, F

def Asistencia(request, cowork):
    if request.user.is_authenticated:
        if request.user.groups.filter(name="BITAJON").exists() or request.user.is_staff:
            local_tz = pytz.timezone("America/Argentina/Buenos_Aires")
            today = datetime.now(local_tz).date()
            yesterday = today - timedelta(days=1)
            tomorrow = today + timedelta(days=1)

            cowork = int(cowork)

            if cowork == 1:  # COWORK
                pages = Page.objects.filter(
                    activa=True,
                    cowork=cowork
                )#.filter(
                #    Q(fecha__in=[yesterday, today, tomorrow]) | Q(fecha__isnull=True)
              #  )
            else:  # ACTIVIDADES
                pages = Page.objects.filter(
                    activa=True,
                    cowork=cowork,
                   # fecha__in=[yesterday, today, tomorrow]
                )

            unique_dates = (
                pages.filter(fecha__isnull=False)
                     .values_list("fecha", flat=True)
                     .distinct()
                     .order_by("fecha")
            )
            print("Total pages:", pages.count())
            print("Sin fecha:", pages.filter(fecha__isnull=True).count())
            for p in pages.filter(fecha__isnull=True):
                print(" -", p.title, "| cowork:", p.cowork, "| activa:", p.activa)
            return render(
                request,
                "pages/asistencia.html",
                {
                    "pages": pages,
                    "dia": today.weekday() + 1,
                    "cowork": cowork,
                    "unique_dates": unique_dates,
                },
            )

        raise Http404("Usuario no es bitajon/staff")

    raise Http404("Usuario no está autenticado")

def AsistenciaDetail(request, pk, slug):
    if request.user.is_authenticated:
        page = get_object_or_404(Page, pk=pk)
        subscribers = Subscription.objects.find_page(page)
        return render(
            request,
            "pages/asistencia_detail.html",
            {"page": page, "subscribers": subscribers},
        )
    raise Http404("Usuario no está autenticado")


def AsistenciaAdd(request, pk):
    json_response = {"created": False}
    if request.user.is_authenticated:
        username = request.GET.get("user", None)
        user = User.objects.get(username=username)
        if username:
            page = get_object_or_404(Page, pk=pk)
            local_tz = pytz.timezone("America/Argentina/Buenos_Aires")
            hoy = datetime.now(local_tz)
            historial = Historial.objects.find_or_create(page, hoy)
            historial.asistentes.add(user)

            # Se actualiza la lista de asistencias en el objeto de Historial
            subscribers = Subscription.objects.find_page(page)
            for subscripcion in subscribers:
                historial.anotados.add(subscripcion.user)

            json_response["created"] = True
            json_response["hoy"] = hoy

            return JsonResponse(json_response)
    raise Http404("Usuario no está autenticado")


def AsistenciaRemove(request, pk):
    json_response = {"created": False}
    if request.user.is_authenticated:
        username = request.GET.get("user", None)
        user = User.objects.get(username=username)
        if username:
            page = get_object_or_404(Page, pk=pk)
            local_tz = pytz.timezone("America/Argentina/Buenos_Aires")
            hoy = datetime.now(local_tz)
            historial = Historial.objects.find_or_create(page, hoy)
            historial.asistentes.remove(user)

            json_response["created"] = True
            json_response["hoy"] = hoy

            return JsonResponse(json_response)
    raise Http404("Usuario no está autenticado")


def WriteRowAsistencias(h, writer):
    if h is None:
        return Http404("Historial no encontrado")
    if h.anotados.all() is None:
        return Http404("Historial sin anotados")
    if h.asistentes.all() is None:
        return Http404("Historial sin asistentes")

    for anotado in h.anotados.all():
        asistio = "Si" if anotado in h.asistentes.all() else "No"
        asis = 1 if asistio == "Si" else 0

        Profile.objects.get_or_create(user=anotado)

        writer.writerow(
            [
                h.page.titleSTR,
                h.page.fecha,
                h.page.horaDesde,
                anotado,
                anotado.profile.nombre,
                anotado.profile.apellido,
                anotado.profile.whatsapp,
                anotado.email,
                asistio,
                asis,
            ]
        )


def DescargarAsistencias(request, pk):
    page = get_object_or_404(Page, pk=pk)

    response = HttpResponse(content="")
    local_tz = pytz.timezone("America/Argentina/Buenos_Aires")
    response["Content-Disposition"] = (
        "attachment; filename=asistencias-"
        + page.titleSTR
        + "-"
        + str(datetime.now(local_tz))
        + ".csv"
    )
    response.write("\ufeff".encode("utf8"))
    writer = csv.writer(response, dialect="excel")
    writer.writerow(
        [
            "Actividad",
            "Dia",
            "Hora Desde",
            "Fecha",
            "Usuario anotado",
            "Nombre",
            "Apellido",
            "Celular",
            "Mail",
            "Asistio?",
            "Asis",
        ]
    )

    h = Page.historialHoy(page)

    WriteRowAsistencias(h, writer)
    return response


def DescargarHistoricoAsistenciasALLDetail(request):
    local_tz = pytz.timezone("America/Argentina/Buenos_Aires")
    response = HttpResponse(content="")
    response["Content-Disposition"] = (
        "attachment; filename=asistenciasDETALLE-"
        + "historico-"
        + str(datetime.now(local_tz))
        + ".csv"
    )
    response.write("\ufeff".encode("utf8"))
    writer = csv.writer(response, dialect="excel")
    writer.writerow(
        [
            "Actividad",
            "Fecha",
            "Hora Desde",
            "Usuario anotado",
            "Nombre",
            "Apellido",
            "Celular",
            "Mail",
            "Asistio?",
            "Asis",
        ]
    )

    historiales = Historial.objects.all()
    for h in historiales:
        h.fecha = h.fecha.strftime("%d/%m/%Y")
        WriteRowAsistencias(h, writer)
    return response


def DescargarHistoricoAsistenciasALLItem(request):
    local_tz = pytz.timezone("America/Argentina/Buenos_Aires")
    # Genera un archivo por actividad-fecha y otro por actividad-fecha-asistente
    responseB = HttpResponse(content="")
    responseB["Content-Disposition"] = (
        "attachment; filename=asistenciasITEM-"
        + "historico-"
        + str(datetime.now(local_tz))
        + ".csv"
    )
    responseB.write("\ufeff".encode("utf8"))
    writerB = csv.writer(responseB, dialect="excel")
    writerB.writerow(["Actividad", "Fecha", "Hora Desde", "Qanotados", "Qasistentes"])

    historiales = Historial.objects.all()
    for h in historiales:
        writerB.writerow(
            [
                h.page.titleSTR,
                h.page.fecha,
                h.page.horaDesde,
                h.Qanotados,
                h.Qasistentes,
            ]
        )

    return responseB

# Function to export attendance history
def DescargarHistoricoAsistencias(request, pk):
    page = get_object_or_404(Page, pk=pk)
    headers = ["Actividad", "Fecha", "Hora Desde", "Usuario anotado", "Nombre", "Apellido", "Celular", "Asistio?", "Asis"]
    historial_entries = Historial.objects.find_page(page=page)
    if not historial_entries:
        raise Http404("Historial no encontrado")
    rows = []
    for h in historial_entries:
        for anotado in h.anotados.all():
            asistio = "Si" if anotado in h.asistentes.all() else "No"
            rows.append([
                h.page.titleSTR, h.page.fecha, h.page.horaDesde, anotado.username,
                anotado.profile.nombre, anotado.profile.apellido, anotado.profile.whatsapp,
                asistio, 1 if asistio == "Si" else 0
            ])
    return generate_csv_response(f"asistencias-{page.titleSTR}-all", headers, rows)

# Function to export activities
def DescargarActividades(request):
    headers = ["Titulo", "Fecha", "Hora Desde", "Hora Hasta", "Cupo", "Modalidad", "Nuevo", "Activa","Oculta", "Qanotados", "Categorias", "Responsable", "Colaborador", "Secreta", "Clave"]
    rows = [[p.titleSTR, p.fecha, p.horaDesde, p.horaHasta, p.cupo, p.modalidadSTR, p.nuevo, p.activa,p.oculta, p.Qanotados, p.categoriesSTR, p.responsable, p.colaborador, p.secreta, p.clave] for p in Page.objects.all()]
    return generate_csv_response("actividades", headers, rows)

# Function to export user profiles
def DescargarPerfiles(request):
    headers = ["Usuario", "Mail", "Nombre", "Apellido", "Fecha de nacimiento", "Edad", "Celular", "Instagram", "Onward", "Taglit", "Cómo conoció Hillel", "Estudios", "Experiencia comunitaria", "Tematicas de Interes", "Propuestas de Interes", "Observaciones", "Perfil Ok?"]
    rows = [[p.user.username, p.user.email, p.nombre, p.apellido, p.fechaNacimiento, p.edad, p.whatsapp, p.instagram, p.onward, p.taglit, p.comoConociste, p.estudios, p.experienciaComunitaria, p.tematicasInteresSTR, p.propuestasInteresSTR, p.observaciones, p.perfil_ok] for p in Profile.objects.filter(validado=True)]
    return generate_csv_response("perfiles", headers, rows)


# Helper function to generate CSV responses
def generate_csv_response(filename, headers, rows):
    local_tz = pytz.timezone("America/Argentina/Buenos_Aires")
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f"attachment; filename={filename}-{datetime.now(local_tz).strftime('%Y-%m-%d_%H-%M-%S')}.csv"
    response.write("\ufeff".encode("utf8"))
    writer = csv.writer(response, dialect="excel")
    writer.writerow(headers)
    writer.writerows(rows)
    return response

# Function to export questionaries
def DescargarCuestionarios(request):
    headers = ["Actividad"] + [f"Pregunta{i}" for i in range(1, 21)]
    rows = [[c.page.titleSTR] + [getattr(c, f"pregunta{i}", "") for i in range(1, 21)] for c in Cuestionario.objects.all()]
    return generate_csv_response("Cuestionarios", headers, rows)

# Function to export responses to questionaries
def DescargarCuestionariosRespuestas(request):
    headers = ["Actividad"] + [f"Pregunta{i}" for i in range(1, 21)] + ["Usuario"] + [f"Respuesta{i}" for i in range(1, 21)] + ["Fecha de compleción"]
    rows = [[c.page.titleSTR] + [getattr(c, f"pregunta{i}", "") for i in range(1, 21)] + [c.user.username if c.user else ""] + [getattr(c, f"respuesta{i}", "") for i in range(1, 21)] + [c.updated.strftime('%Y-%m-%d %H:%M:%S') if c.updated else ""] for c in CuestionarioRespuesta.objects.all()]
    return generate_csv_response("Cuestionarios-Respuestas", headers, rows)

# Render export page for authenticated users
def Exportar(request):
    if request.user.is_authenticated:
        return render(request, "pages/exportar.html")
    raise Http404("Usuario no está autenticado")