from typing import Any
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.db import transaction
from django.db.models import F
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views import generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import *

from .models import Question, Choice

# Create your views here.
class IndexView(LoginRequiredMixin, generic.ListView):
	template_name = "polls/index.html"
	context_object_name = "latest_question_list"
	title = "Polls Index"
	def get_queryset(self):
		""" Return the last 5 published questions. """
		return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")
	
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
	form_class = QuestionForm
	title = "Poll results"
	def get_queryset(self):
		return Question.objects.filter(pub_date__lte=timezone.now())
	def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
		context = super().get_context_data(**kwargs)
		context['title'] = self.title
		return context

class QuestionChoiceCreate(LoginRequiredMixin, CreateView):
	model = Question
	form_class = QuestionForm
	template_name = 'polls/question_form.html'
	# fields = ["question_text", "pub_date"]
	success_url = reverse_lazy("polls:index")

	def get_context_data(self, **kwargs):
		data = super(QuestionChoiceCreate, self).get_context_data(**kwargs)
		if self.request.POST:
			data['choices'] = ChoiceFormSet(self.request.POST)
		else:
			data['choices'] = ChoiceFormSet()
		return data
	
	def form_valid(self, form):
		context = self.get_context_data()
		choices = context['choices']
		with transaction.atomic():
			form.instance.created_by = self.request.user
			self.object = form.save()
			if choices.is_valid():
				choices.instance = self.object
				choices.save()
		return super(QuestionChoiceCreate, self).form_valid(form)
	
	def get_success_url(self):
		return reverse_lazy('polls:index')
	
class QuestionChoiceUpdate(LoginRequiredMixin, UpdateView):
	model = Question
	template_name = 'polls/question_form.html'
	fields = ["question_text", "pub_date"]
	success_url = reverse_lazy("polls:index")
	
	def get_context_data(self, **kwargs):
		data = super(QuestionChoiceUpdate, self).get_context_data(**kwargs)
		if self.request.POST:
			data['choices'] = ChoiceFormSet(self.request.POST, instance=self.object)
		else:
			data['choices'] = ChoiceFormSet(instance=self.object)
		return data
	def form_valid(self, form):
		context = self.get_context_data()
		choices = context['choices']
		with transaction.atomic():
			self.object = form.save()
			if choices.is_valid():
				choices.instance = self.object
				choices.save()
			messages.info(self.request, "You did it!")
		return super(QuestionChoiceUpdate, self).form_valid(form)
	def get_success_url(self) -> str:
		return reverse_lazy('polls:index')

	
class QuestionCreate(LoginRequiredMixin, CreateView):
	model = Question
	fields = ['question_text', 'pub_date']
		
@login_required
def question_delete(request, pk):
	question = get_object_or_404(Question, pk=pk)

	if request.method == 'POST':
		question.delete()
		return HttpResponseRedirect(reverse("polls:index"))
	return render(request, "polls/index.html")

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
		messages.error(request, "You didn't select a choice.")
		return render(
			request,
			"polls/detail.html",
			{
				"question": question,
				# "error_message": "You didn't select a choice.",
			},
		)
	else:
		messages.info(request, "You successfully voted for " + selected_choice.choice_text)
		selected_choice.votes = F("votes") + 1
		selected_choice.save()
		# Always return an HttpResponseRedirect after successfully dealing
		# with POST data. This prevents data from being posted twice if a 
		# user hits the Back button
		return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))