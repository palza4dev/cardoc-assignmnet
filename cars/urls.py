from django.urls import path

from cars.views  import TrimListView, TrimDetailView

urlpatterns = [
    path('/trim', TrimListView.as_view()),
    path('/trim/<int:trim_id>', TrimDetailView.as_view())
]