from django.urls import path
from . import views

urlpatterns = [
    path('show/', views.plants_list, name='plants-list'),
    path('show/<int:pk>/', views.plant_detail, name='plant-detail'),
    path('edit/<int:pk>/', views.plant_edit, name='plant-edit'),
    path('add/', views.PlantCreateView.as_view(), name='plant-create'),
    path('delete/<int:pk>/', views.plant_delete, name='plant-delete'),
    path('comment/delete/<int:pk>/', views.comment_delete, name='comment-delete'),
    path('search/', views.plant_search, name='plant-search'),
    path('search/<int:pk>/', views.plant_detail, name='plant-detail'),
    path('show/<int:ppk>/comment/<int:cpk>/comment_vote/<str:up_or_down>/', views.vote_on_comment, name='comment-vote'),
    path('show/<int:ppk>/comment/<int:cpk>/comment_report/', views.report_comment, name='report-comment'),
    path('show/<int:ppk>/comment/<int:cpk>/comment_clear_report/', views.clear_report, name='clear-report'),
]