from django.urls import path
from .views import index, BbByRybricView, BbCreateView, BbDetailView

urlpatterns = [
    path('add/', BbCreateView.as_view(), name='add'),
    path('<int:rubric_id>/', BbByRybricView.as_view(), name='by_rubric'),
    path('detail/<int:pk>/', BbDetailView.as_view(), name='detail'),
    path('', index, name='index'),
]