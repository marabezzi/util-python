from datetime import datetime, timedelta

# Função para adicionar uma tarefa à lista
def adicionar_tarefa(lista_tarefas, nome, categoria, prioridade, prazo, horario=None):
    lista_tarefas.append({'nome': nome, 'categoria': categoria, 'prioridade': prioridade, 'prazo': prazo, 'horario': horario, 'concluida': False})

# Função para ordenar as tarefas por prioridade e prazo
def ordenar_tarefas(lista_tarefas):
    return sorted(lista_tarefas, key=lambda x: (x['prioridade'], x['prazo']))

# Função para exibir as tarefas
def exibir_tarefas(lista_tarefas):
    for idx, tarefa in enumerate(lista_tarefas, start=1):
        status = "Concluída" if tarefa['concluida'] else "Pendente"
        print(f"{idx}. {tarefa['nome']} - Categoria: {tarefa['categoria']}, Prioridade: {tarefa['prioridade']}, Prazo: {tarefa['prazo']}, Horário: {tarefa['horario']}, Status: {status}")

# Função para otimizar a semana com ciclos de trabalho e descanso
def otimizar_semana(tarefas):
    semana = {}
    for dia in range(7):
        semana[dia] = []
    for tarefa in tarefas:
        prazo = tarefa['prazo']
        if prazo >= datetime.today() and prazo <= datetime.today() + timedelta(days=6):
            dia_semana = prazo.weekday()
            semana[dia_semana].append(tarefa)
    return semana

# Função para agendar ciclos de trabalho e descanso
def agendar_ciclos_trabalho_descanso(semana):
    for dia, tarefas_dia in semana.items():
        hora_inicio = 9  # Hora de início do expediente (9:00 AM)
        tempo_disponivel = timedelta(hours=17)  # Horário de trabalho padrão (9:00 AM - 5:00 PM)
        for tarefa in tarefas_dia:
            tempo_disponivel -= timedelta(minutes=30)  # Deduzindo tempo para realizar a tarefa
            tarefa['horario'] = f"{hora_inicio}:00 AM"
            hora_inicio += 1
        numero_ciclos_trabalho = len(tarefas_dia) // 2  # Um ciclo de trabalho de 25 minutos e um intervalo de 5 minutos
        for i in range(numero_ciclos_trabalho):
            ciclo_trabalho = {'nome': f"Ciclo de Trabalho {i+1}", 'categoria': 'Trabalho', 'prioridade': 'Alta', 'prazo': semana[dia][0]['prazo'], 'horario': f"{hora_inicio}:00 AM"}
            semana[dia].append(ciclo_trabalho)
            hora_inicio += 1
            ciclo_descanso = {'nome': f"Intervalo de Descanso {i+1}", 'categoria': 'Descanso', 'prioridade': 'Baixa', 'prazo': semana[dia][0]['prazo'], 'horario': f"{hora_inicio}:00 AM"}
            semana[dia].append(ciclo_descanso)
            hora_inicio += 1

# Função principal
def main():
    # Lista para armazenar as tarefas
    tarefas = []

    # Exemplo de adição de tarefas
    adicionar_tarefa(tarefas, 'Estudar para prova de matemática', 'Estudo', 'Alta', datetime(2024, 4, 25))
    adicionar_tarefa(tarefas, 'Enviar relatório ao chefe', 'Trabalho', 'Média', datetime(2024, 4, 27))
    adicionar_tarefa(tarefas, 'Fazer compras no mercado', 'Pessoal', 'Baixa', datetime(2024, 4, 23))

    # Ordenar as tarefas
    tarefas_ordenadas = ordenar_tarefas(tarefas)

    # Exibir as tarefas ordenadas
    print("Tarefas:")
    exibir_tarefas(tarefas_ordenadas)

    # Otimizar a semana
    semana_otimizada = otimizar_semana(tarefas)

    # Agendar ciclos de trabalho e descanso
    agendar_ciclos_trabalho_descanso(semana_otimizada)

    # Exibir as tarefas otimizadas para a semana
    print("\nTarefas para a semana:")
    for dia, tarefas_dia in semana_otimizada.items():
        print(f"\nDia {dia+1}:")
        exibir_tarefas(tarefas_dia)

if __name__ == "__main__":
    main()
