from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import serializers

User = get_user_model()

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        try:
            perfil = user.perfil
            token['rol'] = perfil.rol
            token['nombre_completo'] = user.get_full_name()
        except User.perfil.RelatedObjectDoesNotExist:
            token['rol'] = 'admin'
            token['nombre_completo'] = user.username

        return token

    def validate(self, attrs):
        email_o_username = attrs.get('username')
        password = attrs.get('password')

        if not email_o_username or not password:
            raise serializers.ValidationError('Email y contraseña son requeridos.')

        user = None
        try:
            user = User.objects.filter(email=email_o_username).first()
        except User.DoesNotExist:
            pass


        if not user:
            try:
                user = User.objects.get(username=email_o_username)
            except User.DoesNotExist:
                raise serializers.ValidationError('No existe un usuario con ese email o username.')

        if not user.check_password(password):
            raise serializers.ValidationError('Contraseña incorrecta.')
        
        if not user.is_active:
            raise serializers.ValidationError('Usuario inactivo.')

        attrs['username'] = user.username
        data = super().validate(attrs) 


        data['email'] = self.user.email
        

        full_name = self.user.get_full_name()
        if not full_name:
             data['nombre_completo'] = self.user.username
        else:
             data['nombre_completo'] = full_name

        try:
            data['rol'] = self.user.perfil.rol
        except AttributeError:
            data['rol'] = 'admin'
        except User.perfil.RelatedObjectDoesNotExist:
             data['rol'] = 'admin'
        
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer