from django.contrib import admin
from django.urls import path
from RedUrgencia import views

urlpatterns = [
    path('admin/', admin.site.urls),
    #principal-------------------------------------------------------------------------------------
    path('', views.menu, name="menu"),
    path('login/', views.login, name="login"),
    path('contacto/', views.contacto, name="contacto"),
    path('ayuda/', views.ayuda, name="ayuda"),
    #admin-----------------------------------------------------------------------------------------
    path('menu_admin/', views.menu_admin, name="menu_admin"),
    #admin_usuario---------------------------------------------------------------------------------
    path('menu_admin_usuario/', views.menu_admin_usuario, name="menu_admin_usuario"),
    path('crear_usuario/', views.admin_crear_usuario, name="crear_usuario"),
    path('listar_usuario/', views.admin_listar_usuario, name='listar_usuario'),
    path('modificar_usuario/<int:id>/', views.admin_modificar_usuario, name='modificar_usuario'),
    path('eliminar_usuario/<int:id>/', views.admin_eliminar_usuario, name="eliminar_usuario"),
    #admin_paciente--------------------------------------------------------------------------------
    path('menu_admin_paciente/', views.menu_admin_paciente, name="menu_admin_paciente"),
    path('crear_admin/', views.admin_crear, name="crear_admin"),
    path('listar_admin/', views.admin_listar, name='listar_admin'),
    path('detalle_admin/<int:id>/', views.admin_detalle, name='detalle_admin'),
    path('modificar_admin/<int:id>/', views.admin_modificar, name='modificar_admin'),
    path('eliminar_admin/<int:id>/', views.admin_eliminar, name="eliminar_admin"),
    #emisor----------------------------------------------------------------------------------------
    path('menu_emisor/', views.menu_emisor, name="menu_emisor"),
    path('emisor/', views.emisor, name="emisor"),
    path('editar/<int:id>/', views.editar_emisor, name="editar_emisor"),
    path('lista_emisor/', views.lista_emisor, name="lista_emisor"),
    #receptor--------------------------------------------------------------------------------------
    path('menu_receptor/', views.menu_receptor, name="menu_receptor"),
    path('receptor/', views.receptor, name='receptor'),
    path('seguimiento/', views.seguimiento, name='seguimiento'),
    path('detalle/<int:id>/', views.detalles_paciente, name='detalle_paciente'),
    path('buscar_paciente/', views.buscar_paciente, name='buscar_paciente'),
]
