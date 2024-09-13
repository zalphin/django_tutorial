from typing import Any
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import F
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Question, Choice

# Create your views here.
class IndexView(LoginRequiredMixin, generic.ListView):
        template_name = "polls/index.html"
        context_object_name = "latest_question_list"
        title = "Polls Index"
        def get_queryset(self):
                """ Return the last 5 published questions. """
                return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
        
        def get_context_data(self, **kwargs):
                context = super().get_context_data(**kwargs)
                context['title'] = self.title
                return context
        
class DetailView(LoginRequiredMixin, generic.DetailView):
        model = Question
        template_name = "polls/detail.html"
        title = "Poll Details"
        def get_queryset(self):
                """
                Excludes any questions that aren't published yet.
                """
                return Question.objects.filter(pub_date__lte=timezone.now())
        def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
                context = super().get_context_data(**kwargs)
                context['title'] = self.title
                return context

class ResultsView(LoginRequiredMixin, generic.DetailView):
        model = Question
        template_name = "polls/results.html"
        title = "Poll results"
        def get_queryset(self):
                return Question.objects.filter(pub_date__lte=timezone.now())
        def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
                context = super().get_context_data(**kwargs)
                context['title'] = self.title
                return context

@login_required
def test_view(request):
        title = "Test View"
        context = {'title': title}
        return render(request, "polls/test_view.html", context)

@login_required
def vote(request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        try:
                print(request.POST["choice_id"])
                selected_choice = question.choice_set.get(pk=request.POST["choice_id"])
        except (KeyError, Choice.DoesNotExist):
                # Redisplay the question voting form.
                return render(
                        request,
                        "polls/detail.html",
                        {
                                "question": question,
                                "error_message": "You didn't select a choice.",
                        },
                )
        else:
                selected_choice.votes = F("votes") + 1
                selected_choice.save()
                # Always return an HttpResponseRedirect after successfully dealing
                # with POST data. This prevents data from being posted twice if a 
                # user hits the Back button
                return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))