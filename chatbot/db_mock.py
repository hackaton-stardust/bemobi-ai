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
        'negociacao': {
            'fatura':'vivo',
            'valor': 92.0,
            'data': '2022-01-01
        }
    },
    {
        'id': 2,
        'nome': 'Ana',
        'sobrenome': 'Pereira',
        'email': 'ana.pereira@example.com',
        'telefone': '5548912345678',
        'empresas': ['estacio'],
        'payment_methods': ['pix'],
        'payment_history': {
            'vivo': {'pagas': 40, 'atrasadas': 2},
            'claro': {'pagas': 35, 'atrasadas': 0},
        },
        'since': '2020-01-01',
        'status': 'ativo',
        'saldo_pendente': 100.0,
        'negociacao': {
            'fatura':'vivo',
            'valor': 92.0,
            'data': '2022-01-01
        }
    }
]

mocked_payment_history = {
    1: {  # User ID 1
        'vivo': {'pagas': 40, 'atrasadas': 2},
        'claro': {'pagas': 35, 'atrasadas': 0},
    },
    2: {  # User ID 2
        'estacio': {'pagas': 10, 'atrasadas': 1},
    }
}

mocked_payment_methods = {
    'pix': {
        'name': 'Pix',
        'description': 'Transferência instantânea',
    },
    'mastercard': {
        'name': 'Mastercard',
        'description': 'Cartão de crédito',
    }
}
