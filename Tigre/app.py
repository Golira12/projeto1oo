import random
import customtkinter as ctk
from PIL import Image

# Coisas de setup do CustomTkinter - A magia acontece aqui.
# Logo, porque até jogo de aposta tem que ter marca.
# Se 'logo.jpg' sumir, a culpa não é minha!
image = ctk.CTkImage(Image.open("logo.jpg"), size=(50, 50)) 

ctk.set_appearance_mode('dark') # Modo noturno, porque aposta é coisa séria (à noite).
ctk.set_default_color_theme('dark-blue') # Azul da meia-noite, pra combinar com o saldo (às vezes).


# --- Mixin: RegrasDoJogo ---
# O policial das regras. Sem ele, é bagunça!
class RegrasDoJogo:
    """O manual de instruções que você não leu."""
    MIN_NUMERO = 1  # Limite inferior.
    MAX_NUMERO = 10 # Limite superior. Não inventa!
    MULTIPLICADOR_GANHO = 2.0 # Quanto a gente te ama (se você acertar).

    def validar_aposta(self, valor: float, saldo_disponivel: float) -> bool:
        """Checa se a aposta é válida. Dinheiro de verdade, por favor."""
        return isinstance(valor, (int, float)) and 0 < valor <= saldo_disponivel

    def validar_palpite(self, palpite: int) -> bool:
        """Checa se o palpite está no planeta certo."""
        return isinstance(palpite, int) and self.MIN_NUMERO <= palpite <= self.MAX_NUMERO

    def gerar_numero_secreto(self) -> int:
        """Gera o número mágico. Não é bruxaria, é 'random'."""
        return random.randint(self.MIN_NUMERO, self.MAX_NUMERO)


# --- Classe: Jogador ---
# O protagonista com uma carteira.
class Jogador:
    """Sua conta bancária virtual (e suas esperanças)."""
    def __init__(self, nome: str, saldo_inicial: float):
        """Nasce um apostador (ou um futuro devedor)."""
        self.nome = nome
        self.saldo = saldo_inicial

    def depositar(self, valor: float):
        """Adiciona uns trocados. Milagre."""
        if valor > 0:
            self.saldo += valor

    def sacar(self, valor: float):
        """Remove uns trocados. Tristeza."""
        if 0 < valor <= self.saldo:
            self.saldo -= valor

    def verificar_saldo(self) -> float:
        """O grande indicador de vida (ou dívida)."""
        return self.saldo


# --- Classe: Aposta ---
# O registro do seu momento de glória (ou de choro).
class Aposta:
    """O diário da sua aventura financeira."""
    def __init__(self, valor_apostado: float, palpite_jogador: int):
        """Prepara o palco para o drama."""
        self.valor_apostado = valor_apostado
        self.palpite_jogador = palpite_jogador
        self.numero_secreto = None
        self.ganhou = False
        self.valor_final = 0.0

    def processar_aposta(self, numero_secreto: int):
        """Onde a sorte é lançada. Final feliz ou... nem tanto."""
        self.numero_secreto = numero_secreto
        if self.palpite_jogador == numero_secreto:
            self.ganhou = True # Acertei, miserável!
            self.valor_final = self.valor_apostado * RegrasDoJogo.MULTIPLICADOR_GANHO
        else:
            self.ganhou = False # Perdeu, playboy!
            self.valor_final = -self.valor_apostado

    def __str__(self):
        """Transforma a aposta em fofoca para o histórico."""
        status = "GANHOU" if self.ganhou else "PERDEU"
        return f"Aposta de R${self.valor_apostado:.2f} | Palpite: {self.palpite_jogador} | Secreto: {self.numero_secreto} | Resultado: {status} | +/- R${abs(self.valor_final):.2f}"


# --- Classe Principal: App (o Mestre de Cerimônias) ---
class App(ctk.CTk, RegrasDoJogo):
    """A orquestra do jogo. Tem botões e faz contas."""
    def __init__(self):
        super().__init__()
        self.title("Jogo de Adivinhação - Por Ryan! (E uma IA engraçada)") # Título da obra.
        self.geometry("500x400") # Tamanho do palco.
        self.jogador = None # Cadê o herói?
        self.historico_apostas = [] # As cicatrizes da guerra (e as vitórias).

        # Widgets - Os artistas do palco.
        # Background: se sumir, a tela fica preta!
        self.bg_image = ctk.CTkImage(Image.open("logo.jpg"), size=(500, 400))
        self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.label_nome = ctk.CTkLabel(self, text="Nome do Herói:")
        self.entry_nome = ctk.CTkEntry(self)

        self.label_saldo = ctk.CTkLabel(self, text="Grana Inicial:")
        self.entry_saldo = ctk.CTkEntry(self)

        self.btn_iniciar = ctk.CTkButton(self, text="Iniciar Jogo (e a aventura!)", command=self.iniciar_jogo)

        # Widgets que só aparecem depois do start.
        self.label_aposta = ctk.CTkLabel(self, text="Quanto na roleta? (Corajoso(a)!)")
        self.entry_aposta = ctk.CTkEntry(self)

        self.label_palpite = ctk.CTkLabel(self, text=f"Seu Palpite ({self.MIN_NUMERO}-{self.MAX_NUMERO}):")
        self.entry_palpite = ctk.CTkEntry(self)

        self.btn_apostar = ctk.CTkButton(self, text="Mandar Ver!", command=self.jogar_rodada)
        self.btn_historico = ctk.CTkButton(self, text="Ver meu passado", command=self.mostrar_historico)

        self.resultado = ctk.CTkLabel(self, text="") # Onde a IA solta a fofoca do resultado.
        self.saldo_label = ctk.CTkLabel(self, text="") # Seu saldo, pra não se perder nas contas.

        # Layout inicial: a tela de boas-vindas.
        self.label_nome.pack(pady=5)
        self.entry_nome.pack(pady=5)
        self.label_saldo.pack(pady=5)
        self.entry_saldo.pack(pady=5)
        self.btn_iniciar.pack(pady=10)

    def iniciar_jogo(self):
        """Dá o pontapé inicial na diversão."""
        nome = self.entry_nome.get().strip()
        try:
            saldo = float(self.entry_saldo.get())
            if nome and saldo >= 0:
                self.jogador = Jogador(nome, saldo) # Nasce o jogador!
                self.resultado.configure(text=f"Bem-vindo(a), {nome}! Que a sorte esteja com você!")
                self.montar_tela_jogo() # Trocamos a tela.
            else:
                self.resultado.configure(text="Erro: Nome ou saldo inválido. Não me venha com gracinha!")
        except ValueError:
            self.resultado.configure(text="Erro: Saldo inválido. É número, colega!")

    def montar_tela_jogo(self):
        """Transforma a tela de cadastro em tela de cassino."""
        self.clear_widgets() # Some com os widgets antigos.

        self.label_aposta.pack(pady=5)
        self.entry_aposta.pack(pady=5)
        self.label_palpite.pack(pady=5)
        self.entry_palpite.pack(pady=5)
        self.btn_apostar.pack(pady=5)
        self.btn_historico.pack(pady=5)
        self.resultado.pack(pady=10)
        self.saldo_label.pack(pady=5)
        self.atualizar_saldo()

    def jogar_rodada(self):
        """Onde o destino é selado. E o saldo muda."""
        try:
            valor = float(self.entry_aposta.get())
            palpite = int(self.entry_palpite.get())

            if not self.validar_aposta(valor, self.jogador.verificar_saldo()):
                self.resultado.configure(text="Aposta inválida. Saldo insuficiente ou valor errado!")
                return
            if not self.validar_palpite(palpite):
                self.resultado.configure(text="Palpite fora do intervalo. Concentra!")
                return

            aposta = Aposta(valor, palpite) # Nova aposta, nova emoção.
            numero = self.gerar_numero_secreto() # O número que vai decidir.
            aposta.processar_aposta(numero) # Calcula o resultado: glória ou lágrimas?

            # Atualiza o saldo. A vida continua (ou não).
            if aposta.valor_final > 0:
                self.jogador.depositar(aposta.valor_final)
                self.resultado.configure(text=f"🎉 Acertou! Era {aposta.numero_secreto}. Ganhou R${aposta.valor_final:.2f}!")
            else:
                self.jogador.sacar(abs(aposta.valor_final))
                self.resultado.configure(text=f"😢 Errou. Era {aposta.numero_secreto}. Perdeu R${abs(aposta.valor_final):.2f}.")

            self.historico_apostas.append(aposta) # Adiciona à sua saga.
            self.atualizar_saldo() # Atualiza o placar.
        except ValueError:
            self.resultado.configure(text="Erro: Entrada inválida. É número, não poesia!")

    def mostrar_historico(self):
        """Reveja suas glórias (e derrotas)."""
        historico_texto = "\n".join(str(a) for a in self.historico_apostas[-5:]) or "Nada aqui. Vá apostar!"
        self.resultado.configure(text=f"📜 Histórico Recente:\n{historico_texto}")

    def atualizar_saldo(self):
        """Atualiza o saldo na tela. Seu dinheiro, sua verdade."""
        if self.jogador:
            self.saldo_label.configure(text=f"Saldo atual: R${self.jogador.verificar_saldo():.2f}")
        else:
            self.saldo_label.configure(text="Saldo: N/A")

    def clear_widgets(self):
        """Limpa a tela, tipo faxina geral."""
        for widget in self.winfo_children():
            if widget != self.bg_label: # Menos o background, ele fica!
                widget.pack_forget()

# --- Bloco Principal de Execução ---
if __name__ == "__main__":
    app = App() # O show vai começar!
    app.mainloop() # E ele não para até você fechar a janela.