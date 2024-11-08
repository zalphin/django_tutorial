from typing import Any
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import F
from django.urls import reverse, reverse_lazy
from django.views import generic, View
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
import random

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
		return Question.objects # .filter(pub_date__lte=timezone.now())
	def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
		context = super().get_context_data(**kwargs)
		context['title'] = self.title
		return context

class ResultsView(LoginRequiredMixin, generic.DetailView):
	model = Question
	template_name = "polls/results.html"
	form_class = CreateNewPollForm
	title = "Poll results"
	def get_queryset(self):
		return Question.objects.filter(pub_date__lte=timezone.now())
	def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
		context = super().get_context_data(**kwargs)
		context['title'] = self.title
		return context

class CreateView(LoginRequiredMixin, generic.FormView):
	model = Question
	template_name = "polls/create.html"
	form_class = CreateNewPollForm
	def get_success_url(self):
		return reverse_lazy("polls:index")
	def post(self, request, **kwargs):
		form = self.form_class(request.POST)
		if (form.is_valid()):
			# Put object creation logic here
			data = form.cleaned_data
			question = Question.objects.create(question_text = data['question_text'], pub_date = data['pub_date'])
			current_user = request.user
			question.created_by = current_user.id
			question.save()
			responses = [ v for k,v in data.items() if ('response' in k and v != '') ]
			for response in responses:
				choice = Choice.objects.create(choice_text = response, question=question)
				choice.save()
			return HttpResponseRedirect(reverse("polls:index"))
		return render(request, "books/create.html")
		
	

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