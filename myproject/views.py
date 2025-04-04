from django.shortcuts import render
from django.http import JsonResponse
from .tasks import process_csv
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def upload_csv(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        process_csv.delay(file.name)
        return JsonResponse({"message": "CSV upload started!", "task_id": "some-task-id"})
    return JsonResponse({"error": "No file provided"}, status=400)
