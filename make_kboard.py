import json

def create_kboard(text): # Функция создания клавиатуры бота, в зависимости от запроса ('меню', либо 'календарь')
    if text == 'меню':
        sched = {
        'one_time': False,
        'buttons': [[{
            'action': {
                'type': 'text',
                'payload': json.dumps({'buttons': 'пнн'}),
                'label': 'Неделя',
            },
            'color': 'primary'
        },
        ],

        [{
            'action': {
                'type': 'text',
                'payload': json.dumps({'buttons': 'пнн'}),
                'label': 'Календарь',
            },
            'color': 'primary'
        }
        ],

        [{
            'action': {
                'type': 'text',
                'payload': json.dumps({'buttons': 'пнн'}),
                'label': 'Сегодня',
            },
            'color': 'primary'
        }
        ],

        [{
            'action': {
                'type': 'text',
                'payload': json.dumps({'buttons': 'пнн'}),
                'label': 'Помощь',
            },
            'color': 'negative'
        }
        ]

        ]
    }
    elif text == 'календарь':
        sched = {
            'one_time': True,
            'buttons': [
            [{
                'action': {
                    'type': 'text',
                    'payload': json.dumps({'buttons': 'пнн'}),
                    'label': 'Понедельник нижняя',
                },
                'color': 'primary'
            },
            {
                'action': {
                    'type': 'text',
                    'payload': json.dumps({'buttons': 'пнв'}),
                    'label': 'Понедельник верхняя',
                },
                'color': 'positive'
            }
            ],

            [{
                'action': {
                    'type': 'text',
                    'payload': json.dumps({'buttons': 'пнн'}),
                    'label': 'Вторник нижняя',
                },
                'color': 'primary'
            },
            {
                'action': {
                    'type': 'text',
                    'payload': json.dumps({'buttons': 'пнв'}),
                    'label': 'Вторник верхняя',
                },
                'color': 'positive'
            }
            ],

            [{
                'action': {
                    'type': 'text',
                    'payload': json.dumps({'buttons': 'пнн'}),
                    'label': 'Среда нижняя',
                },
                'color': 'primary'
            },
            {
                'action': {
                    'type': 'text',
                    'payload': json.dumps({'buttons': 'пнв'}),
                    'label': 'Среда верхняя',
                },
                'color': 'positive'
            }
            ],

            [{
                'action': {
                    'type': 'text',
                    'payload': json.dumps({'buttons': 'пнн'}),
                    'label': 'Четверг нижняя',
                },
                'color': 'primary'
            },
            {
                'action': {
                    'type': 'text',
                    'payload': json.dumps({'buttons': 'пнв'}),
                    'label': 'Четверг верхняя',
                },
                'color': 'positive'
            }
            ],

             [{
                'action': {
                    'type': 'text',
                    'payload': json.dumps({'buttons': 'пнн'}),
                    'label': 'Пятница нижняя',
                },
                'color': 'primary'
            },
            {
                'action': {
                    'type': 'text',
                    'payload': json.dumps({'buttons': 'пнв'}),
                    'label': 'Пятница верхняя',
                },
                'color': 'positive'
            }
            ],

            [{
                'action': {
                    'type': 'text',
                    'payload': json.dumps({'buttons': 'пнн'}),
                    'label': 'Суббота нижняя',
                },
                'color': 'primary'
            },
            {
                'action': {
                    'type': 'text',
                    'payload': json.dumps({'buttons': 'пнв'}),
                    'label': 'Суббота верхняя',
                },
                'color': 'positive'
            }
            ],

            [{
                'action': {
                    'type': 'text',
                    'payload': json.dumps({'buttons': 'пнв'}),
                    'label': 'Меню',
                },
                'color': 'negative'
            }
            ],

            ]
        }

    kb = json.dumps(sched, ensure_ascii=False).encode('utf-8')
    kb = str(kb.decode('utf-8'))
    return kb # Возврат строки с клавиатурой