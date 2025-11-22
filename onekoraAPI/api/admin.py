

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from . import models


admin.site.register(models.Configuracion)
admin.site.register(models.Sector)
admin.site.register(models.Dispositivo)
admin.site.register(models.TipoResiduo)
admin.site.register(models.Camion)
admin.site.register(models.EstadoRecojo)
admin.site.register(models.Notificacion)
admin.site.register(models.HistoRecol)
admin.site.register(models.Anuncio)
admin.site.register(models.CateEducativa)
admin.site.register(models.Juego)
admin.site.register(models.HistoJuego)
admin.site.register(models.HistoRespuesta)
admin.site.register(models.Canje)

class JuegoAlternativaInline(admin.StackedInline):
    model = models.JuegoAlternativa
    extra = 3 

@admin.register(models.JuegoPregunta)
class JuegoPreguntaAdmin(admin.ModelAdmin):
    list_display = ('pregunta_txt', 'juego', 'pts_otorga')
    inlines = [JuegoAlternativaInline]

@admin.register(models.Direccion)
class DireccionAdmin(admin.ModelAdmin):
    list_display = ('user', 'descrip', 'sector', 'es_principal')
    list_filter = ('sector', 'es_principal')
    search_fields = ('user__username', 'descrip')


@admin.register(models.ArtiEducativo)
class ArtiEducativoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'tipo_post', 'esta_activo')
    list_filter = ('categoria', 'esta_activo')
    search_fields = ('titulo', 'contenido')

@admin.register(models.Ruta)
class RutaAdmin(admin.ModelAdmin):
    list_display = ('nombre_ruta', 'sector', 'tipo_residuo', 'dia_sem', 'esta_activo')
    list_filter = ('sector', 'dia_sem', 'esta_activo')

@admin.register(models.Recompensa)
class RecompensaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'costo_pts', 'stock', 'esta_activo')
    search_fields = ('nombre',)
    

@admin.register(models.PersonalMunicipal)
class PersonalMunicipalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cargo', 'area_responsable', 'telefono', 'disponible')
    list_filter = ('area_responsable', 'disponible')
    search_fields = ('nombre', 'cargo')

class UsuarioPerfilInline(admin.StackedInline):
    model = models.UsuarioPerfil
    can_delete = False
    verbose_name_plural = 'Perfil de Usuario (Campos Personalizados)'

admin.site.unregister(User)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = (UsuarioPerfilInline,)










"""
============================================================================
AVISO DE PROPIEDAD INTELECTUAL
============================================================================
* PROYECTO:        Onekora (Anteriormente "Huánuco Recicla")
* DESARROLLADOR:   Dionicio Orihuela Edson Raul
* AÑO:             2025
* UBICACIÓN:       Huánuco, Perú

----------------------------------------------------------------------------
AUTORÍA
----------------------------------------------------------------------------
Este código fuente, incluyendo la lógica de negocio, arquitectura de software
(Frontend y Backend), diseño de interfaces (UI), experiencia de usuario (UX),
activos gráficos y el rebranding de la identidad visual de la marca "Onekora",
ha sido desarrollado en su totalidad por Dionicio Orihuela Edson Raul.

El autor certifica su autoría exclusiva sobre la obra completa, abarcando:
1. Desarrollo FullStack (React Native / Django).
2. Diseño Gráfico y Creativo.
3. Ingeniería de Software y Base de Datos.

----------------------------------------------------------------------------
MARCO LEGAL
----------------------------------------------------------------------------
Esta obra está protegida por las leyes de propiedad intelectual de la
República del Perú, específicamente bajo el DECRETO LEGISLATIVO Nº 822
(Ley sobre el Derecho de Autor) y sus modificatorias.

Conforme al Artículo 22 de dicha ley, el autor reivindica su DERECHO MORAL
de paternidad sobre la obra, el cual es perpetuo, inalienable e imprescriptible.

Queda terminantemente prohibida la reproducción total o parcial, distribución,
comunicación pública, transformación o ingeniería inversa de este software
sin la autorización previa y por escrito del titular de los derechos.

Cualquier uso no autorizado de este código o de los elementos visuales
asociados constituirá una violación a los derechos de propiedad intelectual
y será sujeto a las acciones civiles y penales correspondientes ante el
INDECOPI y el Poder Judicial del Perú.

============================================================================
"""