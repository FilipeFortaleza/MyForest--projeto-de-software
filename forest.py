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


class RepositorioDeEstudos: #precisa adicionar as opções de vizualizar tudo
    """
    Centraliza o material de apoio (PDFs e questões).
    """
    def __init__(self):
        self.lista_pdfs = []
        self.conjunto_questoes = []
        self.historico_respostas = []

    def adicionar_pdf(self, nome_pdf: str):
        self.lista_pdfs.append(nome_pdf)
        print(f"\n---PDF '{nome_pdf}' adicionado com sucesso.---\n")

    def criar_resumo(self, titulo: str, conteudo: str):
        print(f"\n---Resumo '{titulo}' salvo.---\n")

    def adicionar_questao(self, questao: str):
        self.conjunto_questoes.append(questao)
        print("\n---Questão adicionada ao banco.---\n")

    def responder_questao(self, questao_id: int, resposta: str):
        self.historico_respostas.append({"id": questao_id, "resposta": resposta})
        print(f"\n---Resposta da questão {questao_id} registrada no histórico.---\n")


class Meta: #preciso refinar e decidir melhor como vão funcionar as metas
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


class Musica: #preciso ver como vai funcionar para adicionar musica, e se eu vou conseguir
    """
    Centraliza músicas no próprio site.
    """
    def __init__(self):
        self.musica_atual = None
        self.musicas_adicionadas = []
        self.playlists_feitas = {}

    def adicionar_musicas(self, nome_musica: str):
        self.musicas_adicionadas.append(nome_musica)
        print(f"Música '{nome_musica}' adicionada ao sistema.")

    def remover_musicas(self, nome_musica: str):
        if nome_musica in self.musicas_adicionadas:
            self.musicas_adicionadas.remove(nome_musica)
            print(f"Música '{nome_musica}' removida.")

    def organizar_playlists(self, nome_playlist: str, lista_musicas: list):
        self.playlists_feitas[nome_playlist] = lista_musicas
        print(f"Playlist '{nome_playlist}' criada/atualizada com sucesso.")
        
    def tocar_playlist(self, nome_playlist: str):
        if nome_playlist in self.playlists_feitas:
            self.musica_atual = self.playlists_feitas[nome_playlist][0]
            print(f"Tocando agora a playlist '{nome_playlist}'.")


# --- ÁREA DE EXECUÇÃO ---
if __name__ == "__main__":
    # 1. Criamos o jardim do usuário
    meu_jardim = JardimVirtual()
    repositorio = RepositorioDeEstudos()
    while(1):
        print("escolha uma opção abaixo:")
        print("1: iniciar o timer")
        print("2: vizualizar jardim")
        print("3: adicionar pdf")
        print("4: adicionar questão")
        print("5: adicionar resposta de questão")
        print("6: adicionar resumo")
        print("7: encerrar programa")
        opcao=int(input())

        if opcao == 1:
          
            tempo = int(input("digite seu tempo de foco: "))
            meu_timer = TemporizadorDeFoco(tempo_total_segundos=tempo, jardim=meu_jardim)
            
            meu_timer.iniciar()
            
        elif opcao == 2:
            meu_jardim.visualizar_jardim()

        elif opcao == 3:
            nome = input("digite o nome do pdf: ")
            repositorio.adicionar_pdf(nome)

        elif opcao == 4:
            questão = input("digite a questão: ")
            repositorio.adicionar_questao(questão)

        elif opcao == 5:
            resposta = input("digite a resposta da questão: ")
            id = len(repositorio.historico_respostas)
            repositorio.responder_questao(id, resposta)
        
        elif opcao == 6:
            titulo = input("digite o nome do resumo: ")
            conteúdo = input("digite o conteúdo do resumo: ")
            repositorio.criar_resumo(titulo, conteúdo)

        elif opcao == 7:
            break
