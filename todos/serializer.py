from rest_framework import serializers
from datetime import datetime
from .models import Todos

class TodosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todos
        fields = ['id', 'user', 'todo', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']

    def validate_todo(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError("Todo description cannot be empty.")
        if len(value) < 5:
            raise serializers.ValidationError("Todo description must be at least 5 characters long.")
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        if not request or not request.user:
            raise serializers.ValidationError("User information is missing.")

        validated_data['user'] = request.user
        validated_data['created_at'] = datetime.now()
        validated_data['updated_at'] = datetime.now()
        return Todos.objects.create(**validated_data)

    def update(self, instance, validated_data):
        request = self.context.get('request')
        if not request or not request.user:
            raise serializers.ValidationError("User information is missing.")
        
        if instance.user != request.user:
            raise serializers.ValidationError("You do not have permission to update this todo.")

        todo = validated_data.get('todo', instance.todo)
        instance.todo = todo
        instance.updated_at = datetime.now()
        instance.save()
        return instance

