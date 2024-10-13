from django.db import models

def get_client(client_id):
    clients = {
        'claro': {
        'name': 'Claro',
        'max_delays': 5,
        'min_sequence': 5
    }}

    return clients[client_id]

def get_user(user_id):
    users = {
            'Henrique': {
            'name': 'Henrique Silveira',
            'email': 'henriquesilveira@gmail.com',
            'telefone': '48984737009',
            'empresas': ['vivo', 'claro'],
            'payment_methods': ['mastercard', 'pix'],
            'payment_history': {
                'vivo': {'pagas': 40, 'atrasadas': 2},
                'claro': {'pagas': 35, 'atrasadas': 0},
            },
            'since': '2020-01-01',
            'status': 'ativo',
            'saldo_pendente': 100.0,
            'negociacao': {
                'fatura': 'vivo',
                'valor': 92.0,
                'data': '2022-01-01'
            },
            'contratos': {
                'internet_celular': {
                    'tipo': 'mobile',
                    'info': [{
                        'ano': 2024,
                        'mes': 1,
                        'mb_usado': 450,
                        'horario_de_pico': '2024-01-01',
                        'total_contratado': 1000,

                    },{
                        'ano': 2024,
                        'mes': 2,
                        'mb_usado': 223,
                        'horario_de_pico': '2024-02-01',
                        'total_contratado': 1000,
                    }]
                }
            },
            'transactions': [
                {'expiration_date': '2024-01-01', 'delayed': False},
                {'expiration_date': '2024-02-01', 'delayed': False},
                {'expiration_date': '2024-03-01', 'delayed': True},
                {'expiration_date': '2024-04-01', 'delayed': False}
            ]
    }
    }

    return users[user_id]