from rest_framework import serializers
from .models import Question, Answer


class QuestionSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    slug = serializers.SlugField(read_only=True)
    created_at = serializers.SerializerMethodField()
    answers_count = serializers.SerializerMethodField()
    user_answerd = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = "__all__"

    def get_created_at(self, instance):
        return instance.created_at.strftime("%B %d %Y")

    def get_answers_count(self, instance):
        return instance.answers.count()

    def get_user_answerd(self, instance):
        request = self.context.get("request")
        return instance.answers.filter(author=request.user).exists()


class AnswerSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    created_at = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    user_voted = serializers.SerializerMethodField()
    question_slug = serializers.SerializerMethodField()

    class Meta:
        model = Answer
        exclude = ["voter", "question"]
        
    def get_created_at(self, instance):
        return instance.created_at.strftime("%B %d %Y")

    def get_likes_count(self, instance):
        return instance.voter.count()

    def get_user_voted(self, instance):
        request = self.context.get("request")
        return instance.voter.filter(pk=request.user.pk).exists()

    def get_question_slug(self, instance):
        return instance.question.slug

