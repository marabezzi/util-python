class Professor:
    def _init_(self, nome, disponibilidade):
        self.nome = nome
        self.disponibilidade = disponibilidade  # Lista de horários disponíveis

class Aula:
    def _init_(self, disciplina, professor, sala, hora):
        self.disciplina = disciplina
        self.professor = professor
        self.sala = sala
        self.hora = hora

class Horario:
    def _init_(self):
        self.dias_semana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta']
        self.horario = {dia: [] for dia in self.dias_semana}

    def adicionar_aula(self, dia, aula):
        if dia in self.dias_semana:
            self.horario[dia].append(aula)
        else:
            print("Dia da semana inválido!")

    def imprimir_horario(self):
        for dia in self.dias_semana:
            print(f"{dia}:")
            for aula in self.horario[dia]:
                print(f"\t{aula.hora}: {aula.disciplina} - {aula.professor.nome} - Sala {aula.sala}")

def verificar_disponibilidade(professor, dia, hora):
    return hora in professor.disponibilidade.get(dia, [])

# Exemplo de uso
if _name_ == "_main_":
    # Definindo professores e suas disponibilidades
    prof1 = Professor("Prof. Silva", {"Segunda": ["08:00", "09:00"], "Terça": ["10:00"]})
    prof2 = Professor("Prof. Santos", {"Segunda": ["10:00", "11:00"], "Quarta": ["08:00"]})

    horario = Horario()

    # Adicionando aulas respeitando a disponibilidade dos professores
    for dia in horario.dias_semana:
        for hora in prof1.disponibilidade.get(dia, []):
            if verificar_disponibilidade(prof1, dia, hora):
                aula = Aula('Matemática', prof1, '101', hora)
                horario.adicionar_aula(dia, aula)

        for hora in prof2.disponibilidade.get(dia, []):
            if verificar_disponibilidade(prof2, dia, hora):
                aula = Aula('História', prof2, '102', hora)
                horario.adicionar_aula(dia, aula)

    # Imprimindo horário
    horario.imprimir_horario()