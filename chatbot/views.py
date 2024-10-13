from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai 
import json

# Dados mockados
mocked_users = [
    {
        'id': 1,
        'nome': 'Henrique',
        'sobrenome': 'Silveira',
        'email': 'henrique.silveira@example.com',
        'telefone': '5548991743762',
        'empresas': ['vivo', 'claro'],
        'payment_methods': ['mastercard', 'pix'],
        'payment_history': {
            'vivo': {'pagas': 40, 'atrasadas': 2},
            'claro': {'pagas': 35, 'atrasadas': 0},
        },
        'since': '2020-01-01',
        'status': 'ativo',
        'saldo_pendente': 100.0,
        'uso_planos_contratados': [
            {
                'empresa': 'vivo',
                'plano': 'pós-pago',
                'data_contratacao': '2020-01-01',
                'valor': 92.0,
                'data_vencimento': '2022-01-01',
                'tamanho_plano': '10GB',  # Tamanho do plano
                'consumo_medio': 3.0  # Consumo médio em GB
            },
            {
                'empresa': 'claro',
                'plano': 'pré-pago',
                'data_contratacao': '2021-01-01',
                'valor': 50.0,
                'data_vencimento': '2022-01-01',
                'tamanho_plano': '5GB',  # Tamanho do plano
                'consumo_medio': 3.5  # Consumo médio em GB
            }
        ],
        'negociacao': {
            'fatura': 'vivo',
            'valor': 92.0,
            'data': '2022-01-01'
        }
    },
]

@csrf_exempt
def chatbot_view(request):
    if request.method == 'POST':
        try:
            # Capturando a mensagem do usuário do corpo da requisição
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()

            # Definindo um ID de usuário (por exemplo, 1)
            user_id = 1  # Isso deve vir de uma autenticação ou contexto real

            # Buscando o usuário pelo ID
            user_info = next((user for user in mocked_users if user['id'] == user_id), None)

            if user_info:
                # Criando o prompt com informações do usuário
                user_details = (
                    f"Nome: {user_info['nome']}, "
                    f"Saldo Pendente: R${user_info['saldo_pendente']:.2f}, "
                    f"Planos Contratados: {', '.join([plano['plano'] + ' (' + plano['tamanho_plano'] + ')' for plano in user_info['uso_planos_contratados']])}, "
                    f"Consumo Médio: {', '.join([plano['plano'] + ': ' + str(plano['consumo_medio']) + 'GB' for plano in user_info['uso_planos_contratados']])}.\n"
                    f"Histórico de Pagamentos: {', '.join([f'{empresa.capitalize()}: Pagas: {dados['pagas']}, Atrasadas: {dados['atrasadas']}' for empresa, dados in user_info['payment_history'].items()])}.\n"
                )

                # Combinando os detalhes do usuário com a mensagem do usuário
                prompt = f"{user_details}User: {user_message}\nChatbot:"
                model = genai.GenerativeModel("gemini-1.5-flash")

                # Gerando uma resposta usando o modelo Gemini
                response = model.generate_content(prompt)
                chatbot_reply = response.text.strip()
            else:
                chatbot_reply = "Desculpe, não consegui encontrar suas informações."

            # Retornando a resposta em json
            return JsonResponse({'reply': chatbot_reply})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
