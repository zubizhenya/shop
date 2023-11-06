from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError, PermissionDenied
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Bb, Rubric, Notes
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.dates import ArchiveIndexView, DateDetailView
from django.views.generic.list import ListView
from .forms import BbForm, DateFilterForm, SomeSearchForm, NotesForm
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

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
        context['form'] = NotesForm()
        context['notes'] = self.object.product.all()
        return context

    def post(self, request, *args, **kwargs):
        if 'delete_note' in request.POST:  # Проверяем, был ли отправлен запрос на удаление
            note_id = request.POST.get('note_id')  # Получаем идентификатор комментария, который нужно удалить
            note = get_object_or_404(Notes, pk=note_id)

            # Проверяем, что пользователь имеет право на удаление комментария
            if note.author == request.user or request.user.is_superuser:
                note.delete()
                return redirect('detail', pk=self.kwargs.get('pk'))
        form = NotesForm(request.POST)
        self.object = self.get_object()

        if form.is_valid():
            note = form.save(commit=False)
            note.author = self.request.user
            note.bb = get_object_or_404(Bb, id=self.kwargs.get('pk'))
            note.save()
            return redirect('detail', pk=self.kwargs.get('pk'))
        else:
            context = self.get_context_data()
            context['form'] = form
            return render(request, self.template_name, context)





class BbFirstPageView(ListView):
    template_name = 'bboard/index.html'
    context_object_name = 'bbs'
    model = Bb

    def get_queryset(self):
        # Возвращаем queryset для модели Bb
        return Bb.objects.all()

    def get(self, request, *args, **kwargs):
        form = SomeSearchForm()
        rubrics = Rubric.objects.all()
        page_num = self.request.GET.get('page', 1)
        paginator = Paginator(self.get_queryset(), 2)  # Используем get_queryset() для получения queryset
        page = paginator.get_page(page_num)
        query = request.GET.get('query', '')
        suggestions = []
        if query:
            bbs = Bb.objects.filter(title__icontains=query)
            bbr = Rubric.objects.filter(name__icontains=query)

            suggestions.extend([bb.title for bb in bbs])
            suggestions.extend([rubric.name for rubric in bbr])
        return render(request, 'bboard/index.html', {'form': form, 'rubrics': rubrics, 'page': page, 'suggestions': suggestions, })

    def post(self, request, *args, **kwargs):
        form = SomeSearchForm(request.POST)
        rubrics = Rubric.objects.all()
        bbs = Bb.objects.all()
        page_num = self.request.GET.get('page', 1)
        paginator = Paginator(self.get_queryset(), 2)
        page = paginator.get_page(page_num)

        try:
            if form.is_valid():
                some_search = form.cleaned_data['query']
                bbs = Bb.objects.filter(title__icontains=some_search).first()
                bbr = Rubric.objects.filter(name__icontains=some_search).first()

                if bbs:
                    return HttpResponseRedirect(reverse('detail', kwargs={'pk': bbs.pk}))
                if bbr:
                    return HttpResponseRedirect(reverse('by_rubric', kwargs={'rubric_id': bbr.pk}))
                if not bbs or bbr:
                    raise ValidationError('Нет совпадений', code='invalid_rubric')

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

