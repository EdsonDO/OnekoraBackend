from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import serializers
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import UsuarioPerfil

User = get_user_model()

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        try:
            perfil = user.perfil
            token['rol'] = perfil.rol
            token['nombre_completo'] = user.get_full_name()
            token['telf'] = perfil.telf
            token['direccion'] = perfil.direccion
            token['sector'] = perfil.sector
        except (AttributeError, User.perfil.RelatedObjectDoesNotExist):
            token['rol'] = 'admin'
            token['nombre_completo'] = user.username
            token['telf'] = ''
            token['direccion'] = ''
            token['sector'] = ''

        return token

    def validate(self, attrs):
        email_o_username = attrs.get('username')
        password = attrs.get('password')

        if not email_o_username or not password:
            raise serializers.ValidationError('Correo y contraseña son requeridos.')

        user = None
        try:
            user = User.objects.filter(email=email_o_username).first()
        except User.DoesNotExist:
            pass 

        if not user:
            try:
                user = User.objects.get(username=email_o_username)
            except User.DoesNotExist:
                raise serializers.ValidationError('No existe un usuario con ese correo o usuario.')

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
            data['telf'] = self.user.perfil.telf
            data['direccion'] = self.user.perfil.direccion
            data['sector'] = self.user.perfil.sector
        except (AttributeError, User.perfil.RelatedObjectDoesNotExist):
            data['rol'] = 'admin'
            data['telf'] = ''
            data['direccion'] = ''
            data['sector'] = ''
        
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterSerializer(serializers.ModelSerializer):
    
    password_2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    telf = serializers.CharField(required=False, allow_blank=True)
    direccion = serializers.CharField(required=False, allow_blank=True)
    sector = serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name', 
            'password', 'password_2', 'telf', 'direccion', 'sector'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs.get('password_2'):
            raise serializers.ValidationError({"password": "Las contraseñas deben coincidir."})
        
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "Ya existe un usuario con este email."})
            
        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError({"username": "Este nombre de usuario ya existe."})

        return attrs

    def create(self, validated_data):
        
        validated_data.pop('password_2', None)
        telf = validated_data.pop('telf', '')
        direccion = validated_data.pop('direccion', '')
        sector = validated_data.pop('sector', '')
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        
        try:
            UsuarioPerfil.objects.create(
                user=user, 
                rol='ciudadano',
                telf=telf,
                direccion=direccion,
                sector=sector
            )
        except Exception as e:
            user.delete()
            raise serializers.ValidationError(f"Error al crear el perfil: {e}")

        return user

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer