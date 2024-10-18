from datetime import datetime, timedelta

def obter_dias_semana(data_inicio, data_fim, dia_semana):
    # Converter strings de datas em objetos datetime, se necessário
    if isinstance(data_inicio, str):
        data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d')
    if isinstance(data_fim, str):
        data_fim = datetime.strptime(data_fim, '%Y-%m-%d')
    
    # Garantir que a data de início seja anterior ou igual à data de término
    if data_inicio > data_fim:
        raise ValueError("Data de início deve ser anterior ou igual à data de término")

    # Converter o dia da semana para número (segunda-feira é 0, domingo é 6)
    dia_semana = dia_semana.lower().strip()
    dias_semana_map = {
        'segunda': 0,
        'terça': 1,
        'quarta': 2,
        'quinta': 3,
        'sexta': 4,
        'sábado': 5,
        'domingo': 6
    }

    if dia_semana not in dias_semana_map:
        raise ValueError("Dia da semana inválido. Use nomes como 'segunda', 'terça', etc.")

    dia_semana_num = dias_semana_map[dia_semana]
    
    # Encontrar o primeiro dia da semana dentro do intervalo
    dias_encontrados = []
    delta_dias = (dia_semana_num - data_inicio.weekday()) % 7
    proximo_dia_semana = data_inicio + timedelta(days=delta_dias)

    # Adicionar todos os dias da semana encontrados entre a data de início e a data de término
    while proximo_dia_semana <= data_fim:
        dias_encontrados.append(proximo_dia_semana)
        proximo_dia_semana += timedelta(weeks=1)

    return dias_encontrados
