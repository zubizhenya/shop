from django.urls import path
from .views import index, BbByRybricView, BbCreateView, BbDetailView, BbUpdateView,BbDeleteView, BbIndexView,BbDateDetailVeiw,BbFilterView


urlpatterns = [
    path('add/', BbCreateView.as_view(), name='add'),
    path('update/<int:pk>/', BbUpdateView.as_view(), name='update'),
    path('<int:rubric_id>/', BbByRybricView.as_view(), name='by_rubric'),
    path('detail/<int:pk>/', BbDetailView.as_view(), name='detail'),
    path('delete/<int:pk>/', BbDeleteView.as_view(), name='delete'),
    path('search/', BbFilterView.as_view(), name='search'),
    path('detail/<int:year>/<int:month>/<int:day>/<int:pk>/', BbDateDetailVeiw.as_view(), name='detail'),
    path('', index, name='index'),
]