from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai 
import json

# Lista de palavras-chave relacionadas ao suporte a clientes
support_keywords = [
    'plano', 'saldo', 'pagamento', 'fatura', 'dado', 'assinatura', 'empresa', 
    'recorrente', 'atraso', 'pago', 'contratar', 'renovar', 'cancelar', 'negociar', 'uso',
    'olá', 'oi', 'bom dia', 'boa tarde', 'boa noite', 'ajuda', 'suporte', 'informa' 'consumo', 'pagar'
    'vivo', 'claro', 'tim', 'oi', 'mastercard', 'visa', 'pix', 'boleto', 'cartão', 'crédito', 'débito',
    'pendente', 'atrasado', 'pago', 'negociar', 'renegociar', 'fatura', 'plano', 'contrato', 'consumo',
    'vencimento', 'contratação', 'cancelamento', 'renovação', 'informação', 'detalhe', 'quem'
]

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
                # Verificando se a pergunta está relacionada ao suporte a clientes
                if any(keyword in user_message.lower() for keyword in support_keywords):
                    # Criando o prompt com informações do usuário
                    user_details = (
                        f"Nome: {user_info['nome']}, "
                        f"Saldo Pendente: R${user_info['saldo_pendente']:.2f}, "
                        f"Planos Contratados: {', '.join([plano['plano'] + ' (' + plano['tamanho_plano'] + ')' for plano in user_info['uso_planos_contratados']])}, "
                        f"Consumo Médio: {', '.join([plano['plano'] + ': ' + str(plano['consumo_medio']) + 'GB' for plano in user_info['uso_planos_contratados']])}.\n"
                        f"Histórico de Pagamentos: {', '.join([f'{empresa.capitalize()}: Pagas: {dados['pagas']}, Atrasadas: {dados['atrasadas']}' for empresa, dados in user_info['payment_history'].items()])}.\n"
                    )

                    # Combinando os detalhes do usuário com a mensagem do usuário
                    prompt = f"{user_details}User: {user_message}\nChatbot: Você é um assistente de suporte chamado Bemobi AI, responsável por oferecer um atendimento excepcional focado nos serviços de assinatura da Bemobi, como os planos Omni Pay e Omni Engage. Seu papel é esclarecer dúvidas do usuário sobre o uso dos planos contratados, histórico de pagamentos e métodos de pagamento disponíveis. Não forneça informações ou responda perguntas que não estejam relacionadas ao suporte ao cliente, como eventos, shows, política, ou notícias gerais. Caso o usuário tenha faturas em atraso, ofereça imediatamente opções de pagamento adequadas ao perfil do cliente para resolver a situação o mais rápido possível, você possui os dados do cliente então ele não ira te fornecer nada no chat."
                    model = genai.GenerativeModel("gemini-1.5-flash")

                    # Gerando uma resposta usando o modelo Gemini
                    response = model.generate_content(prompt)
                    chatbot_reply = response.text.strip()
                else:
                    # Mensagem fora do escopo de suporte a clientes
                    chatbot_reply = "Desculpe, essa questão não parece estar relacionada ao suporte de serviços de assinatura. Por favor, pergunte algo sobre seus planos, saldo ou pagamentos."
            else:
                chatbot_reply = "Desculpe, não consegui encontrar suas informações."

            # Retornando a resposta em json
            return JsonResponse({'reply': chatbot_reply})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
