from django.urls import path
from .views import PageDetail, PageList, PageCreate, PageUpdate, PageDelete, Register, Unregister, Asistencia, AsistenciaDetail, AsistenciaAdd, AsistenciaRemove, DescargarAsistencias, DescargarHistoricoAsistencias, DescargarHistoricoAsistenciasALLItem, DescargarHistoricoAsistenciasALLDetail, DescargarActividades, DescargarPerfiles, Exportar, CuposAgotados, DescargarCuestionarios, DescargarCuestionariosRespuestas

PagesPatterns = ([
    path('', PageList.as_view(), name='pages'),
    path('modalidad/<int:modalidad>', PageList.as_view(), name='pages'),
    path('<int:pk>/<slug:slug>/', PageDetail.as_view(), name='page'),
    path('<int:pk>/', PageDetail.as_view(), name='page'),
    path('create/', PageCreate.as_view(), name='create'),
    path('update/<int:pk>/', PageUpdate.as_view(), name='update'),
    path('delete/<int:pk>/', PageDelete.as_view(), name='delete'),
    path('register/<int:pk>/add', Register, name='register'),
    path('unregister/<int:pk>/remove', Unregister, name='unregister'),
    path('asistencia/<int:modalidad>', Asistencia, name='asistencia'),
    path('asistencia/<int:pk>/<slug:slug>/', AsistenciaDetail, name='asistenciaDetail'),
    path('asistenciaAdd/<int:pk>/', AsistenciaAdd, name='asistenciaAdd'),
    path('asistenciaRemove/<int:pk>/', AsistenciaRemove, name='asistenciaRemove'),
    path('descargarasistencias/<int:pk>/', DescargarAsistencias, name='descargarasistencias'),
    path('descargarhistoricoasistencias/<int:pk>/', DescargarHistoricoAsistencias, name='descargarhistoricoasistencias'),
    path('descargarhistoricoasistenciasitem/', DescargarHistoricoAsistenciasALLItem, name='descargarhistoricoasistenciasitem'),
    path('descargarhistoricoasistenciasdetail/', DescargarHistoricoAsistenciasALLDetail, name='descargarhistoricoasistenciasdetail'),
    path('descargarActividades/', DescargarActividades, name='descargarActividades'),
    path('descargarPerfiles/', DescargarPerfiles, name='descargarPerfiles'),
    path('descargarCuestionarios/', DescargarCuestionarios, name='descargarCuestionarios'),
    path('descargarCuestionariosRespuestas/', DescargarCuestionariosRespuestas, name='descargarCuestionariosRespuestas'),
    path('exportar/', Exportar, name='exportar'),
    path('cuposAgotados/<int:pk>', CuposAgotados, name='cuposAgotados'),
], 'pages')
