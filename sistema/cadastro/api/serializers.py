from rest_framework import serializers

class TerapeutaInSerializer(serializers.Serializer):
    nome = serializers.CharField(max_length=120)
    email = serializers.EmailField()

class TerapeutaOutSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nome = serializers.CharField()
    email = serializers.EmailField()
    ativo = serializers.BooleanField()

class PacienteInSerializer(serializers.Serializer):
    nome = serializers.CharField(max_length=120)
    terapeuta_id = serializers.IntegerField(required=False, allow_null=True)

class PacienteOutSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nome = serializers.CharField()
    terapeuta_id = serializers.IntegerField(allow_null=True)
    ativo = serializers.BooleanField()

class FamiliarInSerializer(serializers.Serializer):
    nome = serializers.CharField(max_length=120)
    email = serializers.EmailField()

class FamiliarOutSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nome = serializers.CharField()
    email = serializers.EmailField()
    ativo = serializers.BooleanField()

class TransferenciaInSerializer(serializers.Serializer):
    novo_terapeuta_id = serializers.IntegerField()
