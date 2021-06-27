from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from rest_framework import exceptions

from doubt.models import DoubtsModel, DoubtQnAModel
from doubt.choices import DoubtStateChoices


class RaiseDoubtSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoubtsModel
        fields = "__all__"
        read_only_fields = ('user', 'ta')

    def create(self, validated_data):
        request = self.context['request']
        validated_data['user'] = request.user
        validated_data['ta'] = None
        return super(RaiseDoubtSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        request = self.context['request']
        if not (request.user.is_staff or request.user.is_superuser):
            raise exceptions.PermissionDenied("Not Allowed to update...")
        state = validated_data.get('state')
        if state:
            if state <= instance.state:
                raise serializers.ValidationError("Not Allowed to reduce the state...")
            if instance.state != state:
                if state == DoubtStateChoices.IN_PROCESS:
                    validated_data['ta'] = request.user
                    validated_data['picked_on'] = timezone.now()
                elif state == DoubtStateChoices.SOLVED:
                    validated_data['resolved_on'] = timezone.now()
        return super(RaiseDoubtSerializer, self).update(instance, validated_data)


class DoubtQnASerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)

    class Meta:
        model = DoubtQnAModel
        fields = "__all__"
        read_only_fields = ('user',)

    def to_representation(self, instance):
        instance.username = instance.user.username
        return super(DoubtQnASerializer, self).to_representation(instance)

    def validate(self, attrs):
        request = self.context['request']
        is_answer = attrs.get('is_answer')
        if is_answer and not (request.user.is_superuser or request.user.is_staff):
            raise exceptions.PermissionDenied("Not Permitted to submit answer")
        doubt = attrs.get("doubt")
        if not doubt.state == DoubtStateChoices.IN_PROCESS and is_answer:
            raise serializers.ValidationError("Question Already Answered or Escalated Doubt")
        return super(DoubtQnASerializer, self).validate(attrs)

    def create(self, validated_data):
        request = self.context['request']
        doubt = validated_data.get("doubt")
        is_answer = validated_data.get("is_answer")
        validated_data['user'] = request.user
        if is_answer:
            if request.user.id != doubt.ta.id:
                raise exceptions.PermissionDenied("Not Allowed To Solve Other Doubts")
        with transaction.atomic():
            instance = super(DoubtQnASerializer, self).create(validated_data)
            if is_answer:
                doubt_serializer_object = RaiseDoubtSerializer(instance=doubt, data={
                    "state": DoubtStateChoices.SOLVED
                }, partial=True, context=self.context)
                doubt_serializer_object.is_valid(raise_exception=True)
                doubt_serializer_object.save()
        return instance

    def update(self, instance, validated_data):
        # not allowing to update QnA section via serializer (Update directly in DB)
        raise exceptions.PermissionDenied("Not Allowed to update QnA section")
