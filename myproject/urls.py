from django.urls import path
from .views import CSVUploadView, ImportTaskStatusView

urlpatterns = [
    path('upload-csv/', CSVUploadView.as_view(), name='upload-csv'),
    path('import-status/<int:task_id>/', ImportTaskStatusView.as_view(), name='import-status'),
]