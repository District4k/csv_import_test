from rest_framework import serializers
from .models import CSVImportTask, DataRecord

class CSVImportTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = CSVImportTask
        fields = ['id', 'file_name', 'uploaded_at', 'status', 'task_id', 'error_message']
        read_only_fields = fields

class DataRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataRecord
        fields = '__all__'