from celery import shared_task
import pandas as pd
from .models import DataRecord, CSVImportTask

@shared_task(bind=True)
def process_csv_file(self, file_path, import_task_id):
    import_task = CSVImportTask.objects.get(id=import_task_id)
    
    try:
        import_task.status = 'PROCESSING'
        import_task.task_id = self.request.id
        import_task.save()

        # Read CSV in chunks to handle large files efficiently
        chunk_size = 1000
        for chunk in pd.read_csv(file_path, chunksize=chunk_size):
            records = []
            for _, row in chunk.iterrows():
                record = DataRecord(
                    sepal_length=row['sepal_length'],
                    sepal_width=row['sepal_width'],
                    petal_length=row['petal_length'],
                    petal_width=row['petal_width'],
                    species=row['species']
                )
                records.append(record)
            
            # Bulk create records for better performance
            DataRecord.objects.bulk_create(records)

        import_task.status = 'COMPLETED'
        import_task.save()
        
        return {'status': 'success', 'message': 'CSV processing completed'}
        
    except Exception as e:
        import_task.status = 'FAILED'
        import_task.error_message = str(e)
        import_task.save()
        raise