from rest_framework import serializers
from .models import User_Data

class public_serializer(serializers.ModelSerializer):
	class Meta:
		model=User_Data
		fields='__all__'
		