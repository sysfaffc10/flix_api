from django.db.models import Avg
from rest_framework import serializers
from actors.serializers import ActorSerializer
from movies.models import Movie
from genres.models import Genre
from genres.serializers import GenreSerializer
from actors.models import Actor


class MovieSerializer(serializers.Serializer):# não estamos usando ele. Só para exemplo. aula 143
    id = serializers.IntegerField()
    title = serializers.CharField()
    genre = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(),      
    )
    release_date = serializers.DateField()
    actors = serializers.PrimaryKeyRelatedField(
        queryset = Actor.objects.all(),
        many=True,#n para n --> vários
    )
    resume = serializers.CharField()


class MovieModelSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = Movie
        fields = '__all__'#QUAIS CAMPO DE RETORNO QUE ELE DEVOLVE
              
    def validate_release_date(self, value):# essa função já tem nome definida. Sempre que validadar, deve usar a paralvra validate_
        if value.year <1900:# vou criando função para cada validação que eu queira
            raise serializers.ValidationError('A data de lançamento não pode ser inferior a 1999.')
        return value
    
    def validate_resume(self, value):
        if len(value)> 500:
            raise serializers.ValidationError('Resumo nao pode ser maior que 200 caracteres')
        return value 
    

class MovieListDetailSerializer(serializers.ModelSerializer):
    actors = ActorSerializer(many=True)# esse parâmetro é passado para indicar que é n para n
    genre = GenreSerializer()
    rate = serializers.SerializerMethodField(read_only=True)#campo calculado. quando cria calculado deve ter função com get_ na frente

    class Meta:
        model = Movie
        fields = ['id', 'title', 'genre', 'actors', 'release_date', 'rate', 'resume']

    def get_rate(self, obj): #campo calculado
        rate = obj.reviews.aggregate(Avg('stars'))['stars__avg'] # metodo simplicifado de media e agrega o compo média. Os dandar que é doi __

        if rate:
            return round (rate, 1)
        
        return None
    

class MovieStatsSerializer(serializers.Serializer):
    total_movies = serializers.IntegerField()
    movies_by_genre = serializers.ListField()
    total_reviews = serializers.IntegerField()
    average_stars = serializers.FloatField()
