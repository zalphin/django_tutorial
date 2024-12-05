from django.urls import path
from . import views

app_name = "polls"
urlpatterns = [
    # path("", views.index, name="index"),
    path("", views.IndexView.as_view(), name="index"),
    path("create", views.CreateView.as_view(), name="create"),
    path("question/create", views.QuestionChoiceCreate.as_view(), name="poll_create"),
    path("<int:pk>/question/edit", views.QuestionChoiceUpdate.as_view(), name="poll_update"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote", views.vote, name="vote"),
]