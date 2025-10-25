from django.urls import path
from .views import stats, charts_data, recent_activity

urlpatterns = [
    path('stats/', stats, name='dashboard_stats'),
    path('charts/', charts_data, name='dashboard_charts'),
    path('activity/', recent_activity, name='dashboard_activity'),
]


