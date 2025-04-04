from django.db import models

class DataRecord(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class CSVImportTask(models.Model):
    file = models.FileField(upload_to='csv_uploads/')
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        app_label = 'myproject'
