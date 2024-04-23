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
def otimizar_semana(tarefas, hora_inicio_agendamento, hora_fim_agendamento):
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
def agendar_ciclos_trabalho_descanso(semana, hora_inicio_agendamento, hora_fim_agendamento):
    for dia, tarefas_dia in semana.items():
        hora_inicio = hora_inicio_agendamento
        tempo_disponivel = (hora_fim_agendamento - hora_inicio_agendamento)  # Horário de trabalho padrão

        tarefas_dia = sorted(tarefas_dia, key=lambda x: x['prioridade'], reverse=True)

        for tarefa in tarefas_dia:
            if tempo_disponivel <= timedelta(minutes=0):
                break
            tempo_necessario = timedelta(minutes=30)  # Tempo necessário para realizar a tarefa
            if tempo_disponivel >= tempo_necessario:
                tarefa['horario'] = hora_inicio.strftime("%I:%M %p")
                hora_inicio += timedelta(minutes=30)  # Avança 30 minutos
                tempo_disponivel -= tempo_necessario
            else:
                break

        numero_ciclos_trabalho = len(tarefas_dia) // 2  # Um ciclo de trabalho de 25 minutos e um intervalo de 5 minutos
        for i in range(numero_ciclos_trabalho):
            ciclo_trabalho = {'nome': f"Ciclo de Trabalho {i+1}", 'categoria': 'Trabalho', 'prioridade': 'Alta', 'prazo': semana[dia][0]['prazo'], 'horario': hora_inicio.strftime("%I:%M %p")}
            semana[dia].append(ciclo_trabalho)
            hora_inicio += timedelta(minutes=25)
            ciclo_descanso = {'nome': f"Intervalo de Descanso {i+1}", 'categoria': 'Descanso', 'prioridade': 'Baixa', 'prazo': semana[dia][0]['prazo'], 'horario': hora_inicio.strftime("%I:%M %p")}
            semana[dia].append(ciclo_descanso)
            hora_inicio += timedelta(minutes=5)

# Função principal
def main():
    # Lista para armazenar as tarefas
    tarefas = []

    # Exemplo de adição de tarefas
    adicionar_tarefa(tarefas, 'Fazer a declaração do IR', 'imposto', 'Alta', datetime(2024, 4, 25))
    adicionar_tarefa(tarefas, 'CLCB do ACC', 'Trabalho', 'Média', datetime(2024, 4, 27))
    adicionar_tarefa(tarefas, 'Estudar Algebra Linear', 'Aula', 'Alta', datetime(2024, 4, 24))
    adicionar_tarefa(tarefas, 'Revisão Bibliográfica Pos-Doc', 'Estudos', 'Alta', datetime(2024, 4, 24))

    # Ordenar as tarefas
    tarefas_ordenadas = ordenar_tarefas(tarefas)

    # Função para exibir as tarefas
    def exibir_tarefas(lista_tarefas):
     for idx, tarefa in enumerate(lista_tarefas, start=1):
        status = "Concluída" if tarefa.get('concluida', False) else "Pendente"
        print(f"{idx}. {tarefa['nome']} - Categoria: {tarefa['categoria']}, Prioridade {tarefa['prioridade']}, Prazo: {tarefa['prazo']}, Horário: {tarefa['horario']}, Status: {status}")


    # Parâmetros de horário de início e término dos agendamentos
    hora_inicio_agendamento = datetime.strptime('09:00 AM', '%I:%M %p')
    hora_fim_agendamento = datetime.strptime('05:00 PM', '%I:%M %p')

    # Otimizar a semana
    semana_otimizada = otimizar_semana(tarefas, hora_inicio_agendamento, hora_fim_agendamento)

    # Agendar ciclos de trabalho e descanso
    agendar_ciclos_trabalho_descanso(semana_otimizada, hora_inicio_agendamento, hora_fim_agendamento)

    # Exibir as tarefas otimizadas para a semana
    print("\nTarefas para a semana:")
    for dia, tarefas_dia in semana_otimizada.items():
        print(f"\nDia {dia+1}:")
        exibir_tarefas(tarefas_dia)

if __name__ == "__main__":
    main()

