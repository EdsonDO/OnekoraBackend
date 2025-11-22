from django.db import models
from django.conf import settings

class UsuarioPerfil(models.Model):
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True, related_name='perfil')
    telf = models.CharField(max_length=15, blank=True, null=True) 
    pts_acum = models.IntegerField(default=0)
    recolecciones = models.IntegerField(default=0) 
    modo_viaje = models.BooleanField(default=False)
    rol = models.CharField(
        max_length=10,
        choices=[('ciudadano', 'Ciudadano'), ('recolector', 'Recolector'), ('admin', 'Admin')],
        default='ciudadano'
    )
    
    direccion = models.CharField(max_length=255, blank=True, null=True)
    sector = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.user.username

class Configuracion(models.Model):
    id_config = models.AutoField(primary_key=True)
    clave = models.CharField(max_length=50, unique=True)
    valor = models.CharField(max_length=255)
    descrip = models.TextField(blank=True, null=True)
    fecha_mod = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.clave

class Sector(models.Model):
    id_sector = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class Dispositivo(models.Model):
    id_disp = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    plataforma = models.CharField(max_length=10, choices=[('android', 'Android'), ('ios', 'iOS')])
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['token'], name='idx_token_pref'),
        ]

class Direccion(models.Model):
    id_dir = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sector = models.ForeignKey(Sector, on_delete=models.RESTRICT) 
    descrip = models.CharField(max_length=255)
    lat = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    lon = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    es_principal = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.descrip}"

class TipoResiduo(models.Model):
    class CodigoOficial(models.TextChoices):
        GENERAL = 'GEN', 'General (No Aprovechable)'
        ORGANICO = 'ORG', 'Orgánico'
        RECICLABLE = 'REC', 'Reciclable (Aprovechable)'
        PELIGROSO = 'PEL', 'Peligroso'

    id_tipo_res = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    icono = models.CharField(max_length=50, blank=True, null=True)
    codigo = models.CharField(
        max_length=3, 
        choices=CodigoOficial.choices, 
        default=CodigoOficial.GENERAL
    )
    color_hex = models.CharField(
        max_length=7, 
        default='#212121',
        help_text="Color hexadecimal para la App (Ej: #28A745)"
    )

    def __str__(self):
        return f"{self.nombre} ({self.get_codigo_display()})"

class Ruta(models.Model):
    DIAS_SEMANA = [
        ('lunes', 'Lunes'), ('martes', 'Martes'), ('miercoles', 'Miércoles'),
        ('jueves', 'Jueves'), ('viernes', 'Viernes'), ('sabado', 'Sábado'),
        ('domingo', 'Domingo')
    ]
    id_ruta = models.AutoField(primary_key=True)
    tipo_residuo = models.ForeignKey(TipoResiduo, on_delete=models.RESTRICT, db_column='id_tipo_res')
    sector = models.ForeignKey(Sector, on_delete=models.RESTRICT, db_column='id_sector')
    nombre_ruta = models.CharField(max_length=100)
    dia_sem = models.CharField(max_length=10, choices=DIAS_SEMANA)
    hora_ini = models.TimeField()
    hora_fin = models.TimeField()
    polyline_encoded = models.TextField(blank=True, null=True)
    esta_activo = models.BooleanField(default=True) 

    def __str__(self):
        return self.nombre_ruta

class Camion(models.Model):
    ESTADOS_CAMION = [
        ('en_ruta', 'En Ruta'),
        ('en_base', 'En Base'),
        ('mantenimiento', 'Mantenimiento')
    ]
    id_camion = models.CharField(max_length=10, primary_key=True)
    ruta_actual = models.ForeignKey(Ruta, on_delete=models.SET_NULL, null=True, blank=True, db_column='id_ruta_act')
    lat_act = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    lon_act = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    estado = models.CharField(max_length=15, choices=ESTADOS_CAMION, default='en_base')
    indice_punto = models.IntegerField(default=0)
    esta_activo = models.BooleanField(default=True)

    def __str__(self):
        return self.id_camion

class EstadoRecojo(models.Model):
    ESTADOS_RECOJO = [
        ('listo', 'Listo'),
        ('sin_residuos', 'Sin Residuos'),
        ('en_viaje', 'En Viaje')
    ]
    id_est_recojo = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha = models.DateField()
    estado = models.CharField(max_length=15, choices=ESTADOS_RECOJO, default='listo')

    class Meta:
        unique_together = ('user', 'fecha')

class Notificacion(models.Model):
    id_notif = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mensaje = models.CharField(max_length=255)
    leido = models.BooleanField(default=False)
    fecha_crea = models.DateTimeField(auto_now_add=True)

class SolicitudRecojo(models.Model):
    ESTADOS_SOLICITUD = [
        ('pendiente', 'Pendiente'), ('aprobado', 'Aprobado'),
        ('completado', 'Completado'), ('rechazado', 'Rechazado')
    ]
    id_solic = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha_solic = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=15, choices=ESTADOS_SOLICITUD, default='pendiente')
    descrip = models.TextField(blank=True, null=True)

class HistoRecol(models.Model):
    id_recol = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tipo_residuo = models.ForeignKey(TipoResiduo, on_delete=models.RESTRICT, db_column='id_tipo_res')
    fecha = models.DateTimeField(auto_now_add=True)
    puntos_otorgados = models.IntegerField(default=0)

class Anuncio(models.Model):
    id_anuncio = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=255)
    contenido = models.TextField()
    fecha_pub = models.DateTimeField(auto_now_add=True)
    esta_activo = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo

class CateEducativa(models.Model):
    id_cate_edu = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    icono = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.nombre

class ArtiEducativo(models.Model):
    id_art_edu = models.AutoField(primary_key=True)
    categoria = models.ForeignKey(CateEducativa, on_delete=models.RESTRICT, db_column='id_cate_edu')
    tipo_post = models.CharField(max_length=50, blank=True, null=True)
    titulo = models.CharField(max_length=255)
    resumen = models.TextField(blank=True, null=True)
    contenido = models.TextField()
    img_portada = models.CharField(max_length=255, blank=True, null=True) 
    esta_activo = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo

class Juego(models.Model):
    id_juego = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    desc_puntos = models.CharField(max_length=50, blank=True, null=True)
    esta_activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class JuegoPregunta(models.Model):
    id_preg = models.AutoField(primary_key=True)
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE, db_column='id_juego')
    pregunta_txt = models.TextField()
    pts_otorga = models.IntegerField(default=10)

    def __str__(self):
        return self.pregunta_txt[:50]

class JuegoAlternativa(models.Model):
    id_alt = models.AutoField(primary_key=True)
    pregunta = models.ForeignKey(JuegoPregunta, on_delete=models.CASCADE, db_column='id_preg')
    alternativa_txt = models.CharField(max_length=255)
    es_correcta = models.BooleanField(default=False)

    def __str__(self):
        return self.alternativa_txt

class HistoJuego(models.Model):
    id_hist_juego = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE, db_column='id_juego')
    pts_ganados_total = models.IntegerField()
    fecha_juego = models.DateTimeField(auto_now_add=True)

class HistoRespuesta(models.Model):
    id_hist_resp = models.AutoField(primary_key=True)
    hist_juego = models.ForeignKey(HistoJuego, on_delete=models.CASCADE, db_column='id_hist_juego')
    alt_elegida = models.ForeignKey(JuegoAlternativa, on_delete=models.CASCADE, db_column='id_alt_elegida')


class Recompensa(models.Model):
    id_recompensa = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    costo_pts = models.IntegerField()
    stock = models.IntegerField(default=0)
    imagen = models.CharField(max_length=255, blank=True, null=True) 
    esta_activo = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(stock__gte=0), name='chk_stock_no_negativo')
        ]

    def __str__(self):
        return self.nombre

class Canje(models.Model):
    id_canje = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recompensa = models.ForeignKey(Recompensa, on_delete=models.RESTRICT, db_column='id_recompensa')
    fecha_canje = models.DateTimeField(auto_now_add=True)
    costo_pts = models.IntegerField()

class PersonalMunicipal(models.Model):
    id_personal = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100) 
    area_responsable = models.CharField(max_length=50) 
    telefono = models.CharField(max_length=15, blank=True, null=True)
    contacto_msg = models.CharField(max_length=100, blank=True, null=True)
    disponible = models.BooleanField(default=True)
    esta_activo = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre
    



















































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