from rest_framework import serializers
from genres.models import Genre


class GenreSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Genre
        fields = '__all__'#QUAIS CAMPO DE RETORNO QUE ELE DEVOLVE