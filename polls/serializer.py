from django.contrib.auth.models import User
from .models import Poll
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password



class UsersSelectSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username'
        ]


class PollModelSerializer(serializers.ModelSerializer):
    answer = serializers.CharField(read_only=True, required=False)


    class Meta:
        model = Poll
        fields = [
            'id',
            'question',
            'answer'
        ]

    # def create(self, validated_data):
    #     instance = Poll.objects.create(
    #         author=self.context['request'].user,
    #         question=validated_data['question']
    #     )
    #     return instance
    #
    # def to_representation(self, instance):
    #     self.field['id']=UsersSelectSerializer()
    #     return super(PollModelSerializer, self).to_representation(instance)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']

        )


        user.set_password(validated_data["password"])
        user.save()

        return user


