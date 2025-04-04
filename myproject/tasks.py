from celery import shared_task

@shared_task
def process_csv(filename):
    print(f"Processing file: {filename}")
    return f"Processed {filename}"
