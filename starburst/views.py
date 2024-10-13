# views.py

import openai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings
from django.shortcuts import render

openai.api_key = settings.OPENAI_API_KEY

@csrf_exempt
def chatbot_view(request):
    if request.method == 'POST':
        # Capturar a mensagem do corpo do request
        data = json.loads(request.body)
        user_message = data.get('message', '')

        # Fazer a chamada à API da OpenAI com o novo modelo
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Usando o modelo gpt-3.5-turbo
            messages=[
                {"role": "user", "content": user_message}
            ],
            max_tokens=150,
            temperature=0.7,
        )

        chatbot_reply = response['choices'][0]['message']['content'].strip()

        # Retornar a resposta para o frontend
        return JsonResponse({'reply': chatbot_reply})

    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

def chatbot_page(request):
    return render(request, 'chatbot.html')