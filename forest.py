import sys
import time
import random


class TemporizadorDeFoco:
    """
    Controla o tempo e se comunica com o Jardim.
    """
    def __init__(self, tempo_total_segundos: int, jardim: JardimVirtual):
        self.tempo_total = tempo_total_segundos
        self.tempo_restante = tempo_total_segundos
        self.status = "pronto"
        self.jardim = jardim # Conectando o temporizador ao jardim

    def iniciar(self):
        self.status = "rodando"
        print(f"\n🌱 Iniciando sessão de foco de {self.tempo_total} segundos...")
        print("💡 Dica: Pressione 'Ctrl + C' no terminal para simular o botão de PAUSA.")
        
        try:
            while self.tempo_restante > 0 and self.status == "rodando":
                mins, secs = divmod(self.tempo_restante, 60)
                formato_tempo = '{:02d}:{:02d}'.format(mins, secs)
                
                # O \r faz o texto reescrever na mesma linha do console
                sys.stdout.write(f'\r⏳ Tempo restante: {formato_tempo} ')
                sys.stdout.flush()
                
                time.sleep(1) # Espera 1 segundo real
                self.tempo_restante -= 1
                
            if self.tempo_restante == 0:
                self.finalizar()
                
        except KeyboardInterrupt:
            # Captura o Ctrl+C para simular a ação de Pausar [cite: 42, 44]
            self.pausar()

    def pausar(self):
        self.status = "pausado"
        print("\n\n⏸️ Temporizador pausado para ir ao banheiro/beber água. Progresso preservado! [cite: 31, 44]")
        input("Pressione ENTER para retomar o foco...")
        self.retomar()

    def retomar(self):
        self.status = "rodando"
        print("▶️ Temporizador retomado.")
        self.iniciar()

    def finalizar(self):
        self.status = "finalizado"
        self.tempo_restante = 0
        print("\n\n✅ Sessão finalizada com sucesso!")

        planta = random.randint(1,3)
        if planta==1:
            self.jardim.plantar("Carvalho")
        elif planta==2:
            self.jardim.plantar("Cerejeira")
        elif planta==3:
            self.jardim.plantar("Cacto")
        


class JardimVirtual:
    """
    Transforma o esforço abstrato (tempo) em uma recompensa visual e tangível. [cite: 46]
    """
    def __init__(self):
        self.plantas = []
        self.layout_jardim = "padrão"

    def plantar(self, tipo_planta: str):
        self.plantas.append(tipo_planta)
        # Cada sessão de foco concluída adiciona uma nova planta [cite: 51]
        print(f"\n Uma nova planta '{tipo_planta}' cresceu no seu jardim!")

    def visualizar_jardim(self):
        print("\n--- SEU JARDIM VIRTUAL ---")
        print(f"Quantidade total de plantas: {len(self.plantas)}")
        print(f"Suas plantas: {', '.join(self.plantas)}")
        print("--------------------------\n")


class repositorio:
    def __init__(self):
        self.quant = 0
        self.titulos = []
        self.conteudo = []
    
    def vizualizar_tudo(self):
        total = 0
        print("--------------")
        for i in self.titulos:
            print(f'{total}: {self.titulos[total]}')
            total +=1
        print("--------------")

    def adicionar(self, titulo: str, conteudo: str):
        self.titulos.append(titulo)
        self.conteudo.append(conteudo)
        self.quant +=1

    def ver(self, id: int):
        print(f'o conteúdo {self.titulos[id]} é:')
        print(f'{self.conteudo[id]}\n')

    def total(self):
        print(f'o total de conteúdos é {self.quant}')


class resumo(repositorio):
    
    def ver(self, id: int):
        print(f'o resumo de id {id} e título "{self.titulos[id]}" tem conteúdo:')
        print(f'{self.conteudo[id]}')


class questao(repositorio):

    def __init__(self):
        super().__init__()
        self.respostas = []

    def responder(self, id_questão: int, resposta: str):
        self.respostas[id_questão] = resposta

    def adicionar(self, titulo: str, conteudo: str):
        self.titulos.append(titulo)
        self.conteudo.append(conteudo)
        self.respostas.append('')
        self.quant +=1

    def ver(self, id_questão: int):
        print(f'a questão {self.titulos[id_questão]} é:')
        print(f'{self.conteudo[id_questão]}')
        resp = input('ver resposta? S/N').upper()

        if resp=='S':
            print(f'a resposta é: {self.respostas[id_questão]}')


class pdf(repositorio):

    def ver(self, id: int):
        print(f'o pdf de id {id} e título "{self.titulos[id]}" é:')
        print(f'{self.conteudo[id]}')


class musica(repositorio):

    def ver(self, id: int):
        print(f' a música {self.titulos[id]} é:')
        print(f'{self.conteudo[id]}')


class Meta:
    """
    Estabelece objetivos de longo prazo e progresso semanal.
    """
    def __init__(self):
        self.meta_semanal = 0 # em horas
        self.progresso_atual = 0 # em horas
        self.missoes_ativas = []

    def definir_meta(self, horas: int):
        self.meta_semanal = horas
        print(f"Meta semanal definida para {horas} horas.")

    def reivindicar_recompensa(self, missao_nome: str):
        if missao_nome in self.missoes_ativas:
            self.missoes_ativas.remove(missao_nome)
            print(f"Recompensa da missão '{missao_nome}' resgatada!")
        else:
            print("Missão não encontrada ou não concluída.")



if __name__ == "__main__":
    # 1. Criamos o jardim do usuário
    meu_jardim = JardimVirtual()
    PDFs = pdf()
    questões = questao()
    resumos = resumo()
    musicas = musica()
    while(1):
        print("sobre o que você quer ver?")
        print("1: iniciar o timer")
        print("2: vizualizar jardim")
        print("3: PDFs")
        print("4: questões")
        print("5: resumos")
        print("6: musicas")
        print("7: metas")
        print("8: encerrar programa")
        opcao=int(input())

        if opcao == 1:
            
            # 2. Criamos um temporizador de 15 segundos para teste rápido e passamos o jardim para ele
            tempo = int(input("digite seu tempo de foco: "))
            meu_timer = TemporizadorDeFoco(tempo_total_segundos=tempo, jardim=meu_jardim)
            
            # 3. Iniciamos o ciclo
            meu_timer.iniciar()

            
        elif opcao == 2:
            meu_jardim.visualizar_jardim()


        elif opcao == 3:
            print("o que sobre seus PDFs você quer ver?")
            print("1: ver meus PDFs")
            print("2: adicionar PDF")
            print("3: ler PDF\n")
            escolha = int(input())

            if escolha == 1:
                PDFs.vizualizar_tudo()

            elif escolha == 2:
                nome = input("digite o nome do pdf: ")
                conteudo = input('coloque aqui o conteúdo do pdf: ')
                PDFs.adicionar(nome, conteudo)

            elif escolha == 3:
                id = int(input("digite o id do PDF: "))
                PDFs.ver(id)

        elif opcao == 4:
            print("o que sobre suas questões você quer ver?")
            print("1: ver minhas questões")
            print("2: adicionar questão")
            print("3: ver questão")
            print("4: responder questão\n")
            escolha = int(input())

            if escolha == 1:
                questões.vizualizar_tudo()

            elif escolha == 2:
                nome = input("digite o nome da questão: ")
                conteudo = input('coloque aqui a pergunta da questão:')
                questões.adicionar(nome, conteudo)

            elif escolha == 3:
                id = int(input("digite o id da questão"))
                questões.ver(id)

            elif escolha == 4:
                id = int(input("digite o id da questão: "))
                resp = input('coloque aqui a resposta da questão:')
                questões.responder(id, resp)


        elif opcao == 5:
            print("o que sobre seus resumos você quer ver?")
            print("1: ver meus resumos")
            print("2: adicionar resumo")
            print("3: ler resumo\n")
            escolha = int(input())

            if escolha == 1:
                resumos.vizualizar_tudo()

            elif escolha == 2:
                nome = input("digite o nome do resumo: ")
                conteudo = input('coloque aqui o conteúdo do resumo: ')
                resumos.adicionar(nome, conteudo)

            elif escolha == 3:
                id = int(input("digite o id do resumo: "))
                resumos.ver(id)
    

        elif opcao == 6:
            print("o que sobre suas musicas você quer ver?")
            print("1: ver minhas musicas")
            print("2: adicionar musica")
            print("3: escutar musica\n")
            escolha = int(input())

            if escolha == 1:
                musicas.vizualizar_tudo()

            elif escolha == 2:
                nome = input("digite o nome da musica: ")
                conteudo = input('coloque aqui o link da musica:')
                musicas.adicionar(nome, conteudo)

            elif escolha == 3:
                id = int(input("digite o id da musica"))
                musicas.ver(id)

        
        elif opcao == 7:
            print("ainda em andamento\n")

    
        elif opcao == 8:
            break
