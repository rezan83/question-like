from rest_framework.exceptions import ValidationError
from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Question, Answer
from .serializers import QuestionSerializer, AnswerSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthorOrReadOnly


class QuestionView(viewsets.ModelViewSet):
    queryset = Question.objects.all().order_by("-created_at")
    serializer_class = QuestionSerializer
    lookup_field = "slug"

    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AnswerCreateView(generics.CreateAPIView):
    queryset = Answer.objects.all().order_by("-created_at")
    serializer_class = AnswerSerializer
    # lookup_field = "slug"

    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        author = self.request.user
        q_slug = self.kwargs.get("slug")
        question = generics.get_object_or_404(Question, slug=q_slug)
        if question.answers.filter(author=author).exists():
            raise ValidationError("you already answered")

        serializer.save(author=author, question=question)


class AnswerRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    lookup_field = "uuid"

    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]


class AnswerListView(generics.ListAPIView):
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    # queryset = Answer.objects.all()

    def get_queryset(self):
        q_slug = self.kwargs.get("slug")
        return Answer.objects.filter(question__slug=q_slug).order_by("-created_at")


class AnswerLikeView(APIView):
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]
    # queryset = Answer.objects.all()

    def post(self, request, uuid):
        answer = generics.get_object_or_404(Answer, uuid=uuid)
        user = request.user
        answer.voter.add(user)
        answer.save()
        context = {"request": request}
        serializer = self.serializer_class(answer, context=context)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, uuid):
        answer = generics.get_object_or_404(Answer, uuid=uuid)
        user = request.user
        answer.voter.remove(user)
        answer.save()
        context = {"request": request}
        serializer = self.serializer_class(answer, context=context)
        return Response(serializer.data, status=status.HTTP_200_OK)