# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai 

@csrf_exempt
def generate_story(request):
    if request.method == 'POST':
        prompt = "Write a story about a magic backpack."
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        try:
            response = model.generate_content(prompt)
            story_text = response.text
            return JsonResponse({'story': story_text})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
