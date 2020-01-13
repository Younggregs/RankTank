from rest_framework import serializers
from .models import Account, Contest, Contestant

##################################
#RankTank
##################################

class AccountSerializer(serializers.ModelSerializer):

     class Meta:
        model = Account
        fields = '__all__'


class FetchAccountSerializer(serializers.ModelSerializer):

     class Meta:
        model = Account
        fields = ['email', 'firstname', 'lastname', 'is_admin', 'is_super']



class ContestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contest
        fields = '__all__'




class ContestantSerializer(serializers.ModelSerializer):

     class Meta:
        model = Contestant
        fields = '__all__'

    

class ContestantTankerSerializer(serializers.Serializer):

    id = serializers.CharField()
    contestant = serializers.CharField()


class ErrorCheckSerializer(serializers.Serializer):

    error = serializers.CharField()


class SuccessSerializer(serializers.Serializer):

    code = serializers.CharField()




