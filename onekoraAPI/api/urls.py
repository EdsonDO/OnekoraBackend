from django.urls import path
from .views import MyTokenObtainPairView, RegisterView, UpdateStatsView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='user_register'),
    path('update-stats/', UpdateStatsView.as_view(), name='update_stats'),
]
















































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