import random
import customtkinter as ctk
from PIL import Image
image = ctk.CTkImage(Image.open("logo.jpg"), size=(50, 50))

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')


class RegrasDoJogo:
    MIN_NUMERO = 1
    MAX_NUMERO = 10
    MULTIPLICADOR_GANHO = 2.0

    def validar_aposta(self, valor: float, saldo_disponivel: float) -> bool:
        return isinstance(valor, (int, float)) and 0 < valor <= saldo_disponivel

    def validar_palpite(self, palpite: int) -> bool:
        return isinstance(palpite, int) and self.MIN_NUMERO <= palpite <= self.MAX_NUMERO

    def gerar_numero_secreto(self) -> int:
        return random.randint(self.MIN_NUMERO, self.MAX_NUMERO)


class Jogador:
    def __init__(self, nome: str, saldo_inicial: float):
        self.nome = nome
        self.saldo = saldo_inicial

    def depositar(self, valor: float):
        if valor > 0:
            self.saldo += valor

    def sacar(self, valor: float):
        if 0 < valor <= self.saldo:
            self.saldo -= valor

    def verificar_saldo(self) -> float:
        return self.saldo


class Aposta:
    def __init__(self, valor_apostado: float, palpite_jogador: int):
        self.valor_apostado = valor_apostado
        self.palpite_jogador = palpite_jogador
        self.numero_secreto = None
        self.ganhou = False
        self.valor_final = 0.0

    def processar_aposta(self, numero_secreto: int):
        self.numero_secreto = numero_secreto
        if self.palpite_jogador == numero_secreto:
            self.ganhou = True
            self.valor_final = self.valor_apostado * RegrasDoJogo.MULTIPLICADOR_GANHO
        else:
            self.ganhou = False
            self.valor_final = -self.valor_apostado

    def __str__(self):
        status = "GANHOU" if self.ganhou else "PERDEU"
        return f"Aposta de R${self.valor_apostado:.2f} | Palpite: {self.palpite_jogador} | Secreto: {self.numero_secreto} | Resultado: {status} | +/- R${abs(self.valor_final):.2f}"


class App(ctk.CTk, RegrasDoJogo):
    def __init__(self):
        super().__init__()
        self.title("Jogo de Adivinhação")
        self.geometry("500x400")
        self.jogador = None
        self.historico_apostas = []

        # Widgets

        self.bg_image = ctk.CTkImage(Image.open("logo.jpg"), size=(500, 400))  # ajuste ao tamanho da janela
        self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)


        self.label_nome = ctk.CTkLabel(self, text="Nome:")
        self.entry_nome = ctk.CTkEntry(self)

        self.label_saldo = ctk.CTkLabel(self, text="Saldo inicial:")
        self.entry_saldo = ctk.CTkEntry(self)

        self.btn_iniciar = ctk.CTkButton(self, text="Iniciar Jogo", command=self.iniciar_jogo)

        self.label_aposta = ctk.CTkLabel(self, text="Valor da Aposta:")
        self.entry_aposta = ctk.CTkEntry(self)

        self.label_palpite = ctk.CTkLabel(self, text="Seu Palpite (1-10):")
        self.entry_palpite = ctk.CTkEntry(self)

        self.btn_apostar = ctk.CTkButton(self, text="Fazer Aposta", command=self.jogar_rodada)
        self.btn_historico = ctk.CTkButton(self, text="Ver Histórico", command=self.mostrar_historico)

        self.resultado = ctk.CTkLabel(self, text="")
        self.saldo_label = ctk.CTkLabel(self, text="")

        # Layout inicial
        self.label_nome.pack(pady=5)
        self.entry_nome.pack(pady=5)
        self.label_saldo.pack(pady=5)
        self.entry_saldo.pack(pady=5)
        self.btn_iniciar.pack(pady=10)

    def iniciar_jogo(self):
        nome = self.entry_nome.get().strip()
        try:
            saldo = float(self.entry_saldo.get())
            if nome and saldo >= 0:
                self.jogador = Jogador(nome, saldo)
                self.resultado.configure(text=f"Bem-vindo(a), {nome}!")
                self.montar_tela_jogo()
        except ValueError:
            self.resultado.configure(text="Erro: saldo inválido.")

    def montar_tela_jogo(self):
        self.clear_widgets()

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
        try:
            valor = float(self.entry_aposta.get())
            palpite = int(self.entry_palpite.get())

            if not self.validar_aposta(valor, self.jogador.verificar_saldo()):
                self.resultado.configure(text="Aposta inválida.")
                return
            if not self.validar_palpite(palpite):
                self.resultado.configure(text="Palpite fora do intervalo.")
                return

            aposta = Aposta(valor, palpite)
            numero = self.gerar_numero_secreto()
            aposta.processar_aposta(numero)

            if aposta.valor_final > 0:
                self.jogador.depositar(aposta.valor_final)
            else:
                self.jogador.sacar(abs(aposta.valor_final))

            self.historico_apostas.append(aposta)
            self.resultado.configure(text=str(aposta))
            self.atualizar_saldo()
        except ValueError:
            self.resultado.configure(text="Erro: entrada inválida.")

    def mostrar_historico(self):
        historico_texto = "\n".join(str(a) for a in self.historico_apostas[-5:]) or "Nenhuma aposta ainda."
        self.resultado.configure(text=historico_texto)

    def atualizar_saldo(self):
        self.saldo_label.configure(text=f"Saldo atual: R${self.jogador.verificar_saldo():.2f}")

    def clear_widgets(self):
        for widget in self.winfo_children():
            widget.pack_forget()


if __name__ == "__main__":
    app = App()
    app.mainloop()
