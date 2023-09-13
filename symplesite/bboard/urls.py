from django.urls import path
from . import views
from .views import (BbByRybricView, BbCreateView, BbDetailView, BbUpdateView,BbDeleteView, BbIndexView,
                    BbDateDetailVeiw,BbFilterView, BbFirstPageView)


urlpatterns = [
    path('add/', BbCreateView.as_view(), name='add'),
    path('update/<int:pk>/', BbUpdateView.as_view(), name='update'),
    path('<int:rubric_id>/', BbByRybricView.as_view(), name='by_rubric'),
    path('detail/<int:pk>/', BbDetailView.as_view(), name='detail'),
    path('delete/<int:pk>/', BbDeleteView.as_view(), name='delete'),
    path('search/', BbFilterView.as_view(), name='search'),
    path('detail/<int:year>/<int:month>/<int:day>/<int:pk>/', BbDateDetailVeiw.as_view(), name='detail'),
    path('', BbFirstPageView.as_view(), name='index'),
]
