import os
import uuid
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from .models import Prediction
from disease.model_loader import predict_disease

def homePage(request):
    predictions = Prediction.objects.all().order_by('-id')
    return render(request, "index.html", {
        "predictions": predictions
    })

def predict_disease_view(request):
    disease = None
    confidence = None
    solution = None
    image_url = None

    if request.method == 'POST' and request.FILES.get('leaf_image'):
        image = request.FILES['leaf_image']

        # Ensure media folder exists
        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
        
        # Upload folder path (sirf folder, file name nahi)
        upload_folder = os.path.join(settings.MEDIA_ROOT, 'uploads')
        os.makedirs(upload_folder, exist_ok=True)

        #Unique file name
        file_name = str(uuid.uuid4()) + os.path.splitext(image.name)[-1]

        # Final file path
        file_path = os.path.join(upload_folder, file_name)

        # Image save 
        with open(file_path, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)

        # ML prediction
        disease, confidence, solution = predict_disease(file_path)

        # Save in database
        prediction = Prediction.objects.create(
            image='uploads/' + file_name,
            disease=disease,
            confidence=confidence,
            solution=solution
        )

        image_url = settings.MEDIA_URL + 'uploads/' + file_name

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                "disease": disease,
                "confidence": confidence,
                "solution": solution
            })

    # Fetch updated predictions
    predictions = Prediction.objects.all().order_by('-id')

    return render(request, 'index.html', {
        'disease': disease,
        'confidence': confidence,
        'solution': solution,
        'image_url': image_url,
        'predictions': predictions
    })

        