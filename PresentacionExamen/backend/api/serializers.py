from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import (
    Asignaturas,
    Corresponde,
    Crea,
    Cursa,
    Estudiantes,
    Evalua,
    Imparte,
    Ingresa,
    Preguntas,
    Profesores,
    Programa,
    Responde,
    Respuestas,
    Salones,
    Selecciona,
    Tipospreguntas,
)


class AsignaturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asignaturas
        fields = '__all__'

class CorrespondeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Corresponde
        fields = '__all__'

class CreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crea
        fields = '__all__'

class CursaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cursa
        fields = '__all__'

class EstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudiantes
        fields = '__all__'

class EvaluaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evalua
        fields = '__all__'

class ImparteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imparte
        fields = '__all__'

class IngresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingresa
        fields = '__all__'

class PreguntasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preguntas
        fields = '__all__'

class ProfesoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profesores
        fields = '__all__'

class ProgramaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Programa
        fields = '__all__'

class RespondeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responde
        fields = '__all__'

class RespuestasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Respuestas
        fields = '__all__'

class SalonesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salones
        fields = '__all__'

class SeleccionaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selecciona
        fields = '__all__'

class TipospreguntasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipospreguntas
        fields = '__all__'

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']