from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError, PermissionDenied
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Bb, Rubric
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.dates import ArchiveIndexView, DateDetailView
from django.views.generic.list import ListView
from .forms import BbForm, DateFilterForm, RubricSearchForm
from django.urls import reverse_lazy

class BbByRybricView(TemplateView):
    template_name = 'bboard/by_rubric.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bbs'] = Bb.objects.filter(rubric=context['rubric_id'])
        context['rubrics'] = Bb.objects.all()
        context['current_rubric'] = Rubric.objects.get(pk=context['rubric_id'])
        return context

class BbDetailView(DetailView):
    model = Bb
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class BbFirstPageView(ListView):
    template_name = 'bboard/index.html'
    context_object_name = 'bbs'
    model = Bb

    def get_queryset(self):
        # Возвращаем queryset для модели Bb
        return Bb.objects.all()

    def get(self, request, *args, **kwargs):
        form = RubricSearchForm()
        rubrics = Rubric.objects.all()
        page_num = self.request.GET.get('page', 1)
        paginator = Paginator(self.get_queryset(), 2)  # Используем get_queryset() для получения queryset
        page = paginator.get_page(page_num)
        return render(request, 'bboard/index.html', {'form': form, 'rubrics': rubrics, 'page': page})

    def post(self, request, *args, **kwargs):
        form = RubricSearchForm(request.POST)
        rubrics = Rubric.objects.all()
        page_num = self.request.GET.get('page', 1)
        paginator = Paginator(self.get_queryset(), 2)
        page = paginator.get_page(page_num)

        try:
            if form.is_valid():
                rubric_search = form.cleaned_data['rubric']
                bbr = Rubric.objects.filter(name__icontains=rubric_search).first()

                if bbr:
                    return HttpResponseRedirect(reverse('by_rubric', kwargs={'rubric_id': bbr.pk}))

                if not bbr:
                    raise ValidationError('Неверно введена рубрика', code='invalid_rubric')
        except ValidationError as e:
                    # Обработка ошибки ValidationError
            error_message = e.messages[0]  # Получаем текст ошибки из сообщения ValidationError
            return render(request, 'bboard/index.html',
                                  {'form': form, 'rubrics': rubrics, 'page': page, 'error_message': error_message})

class PermissionErrorView(TemplateView):
    template_name = 'bboard/permissionerror.html'
class BbCreateView(LoginRequiredMixin, CreateView):
    login_url = 'permissionerror'
    template_name = 'bboard/create.html'
    form_class = BbForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class BbUpdateView(UpdateView):
    model = Bb
    form_class = BbForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

class BbDeleteView(DeleteView):
    model = Bb
    success_url = reverse_lazy('index')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

class BbIndexView(ArchiveIndexView):
    model = Bb
    date_field = 'published'
    date_list_period = 'year'
    template_name = 'bboard/index.html'
    context_object_name = 'bbs'
    allow_empty = True

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        context['date_list'] = Bb.objects.dates('published', 'year')
        return context

class BbDateDetailVeiw(DateDetailView):
    model = Bb
    date_field = 'published'
    month_format = '%m'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class BbFilterView(ListView):
    template_name = 'bboard/search.html'

    def get(self, request, *args, **kwargs):
        form = DateFilterForm()
        bbs = []
        return render(request, 'bboard/search.html', {'form': form, 'bbs': bbs})


    def post(self, request, *args, **kwargs):
        form = DateFilterForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            bbs = Bb.objects.filter(published__range=(start_date, end_date))
        else:
            bbs = []

        return render(request, 'bboard/search.html', {'form': form, 'bbs': bbs})

# Create your views here.
