from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from .models import CSVImportTask
from .tasks import process_csv_file
from .serializers import CSVImportTaskSerializer
import os

class CSVUploadView(APIView):
    def post(self, request):
        if 'file' not in request.FILES:
            return Response(
                {'error': 'No file provided'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        file = request.FILES['file']
        if not file.name.endswith('.csv'):
            return Response(
                {'error': 'File must be CSV'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Create import task record
        import_task = CSVImportTask.objects.create(
            file_name=file.name,
            status='PENDING'
        )
            
        # Save file temporarily
        file_path = default_storage.save(
            f'csv_uploads/{import_task.id}/{file.name}', 
            file
        )
        
        # Start Celery task
        process_csv_file.delay(file_path, import_task.id)
        
        serializer = CSVImportTaskSerializer(import_task)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

class ImportTaskStatusView(APIView):
    def get(self, request, task_id):
        try:
            import_task = CSVImportTask.objects.get(id=task_id)
            serializer = CSVImportTaskSerializer(import_task)
            return Response(serializer.data)
        except CSVImportTask.DoesNotExist:
            return Response(
                {'error': 'Import task not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )