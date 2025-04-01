import tkinter as tk
from tkinter import messagebox
import manipulacao_dados as dados
from validate_email_address import validate_email #necessita de instalação de pacote

tamanho_tela = "700x500"

def telaInicial(tela_anterior=None): #cria uma variavel para fechar a tela anterior
    if tela_anterior:
        tela_anterior.destroy()
    tela_opcoes = tk.Tk()  # criando tela principal
    tela_opcoes.geometry(tamanho_tela)  # tamanho da caixa em que a tela sera exibida
    tela_opcoes.resizable(width=False, height=False) # para fixar o tamanho da tela
    tela_opcoes.title("Aplicativo de Gerenciamento Financeiro Pessoal")  # definindo título da página

    tk.Label(tela_opcoes, text="Bem-Vindo(a) ao seu Gerenciador Financeiro Pessoal", font=("Arial", 20),anchor='center').grid(row=0, column=0, columnspan=2, pady=20)
    tk.Label(tela_opcoes, text="Já tem uma conta?", font=("Arial", 18), anchor='center').grid(row=1, column=0,columnspan=2, pady=20)

    tk.Button(tela_opcoes, text="Criar uma conta", command=lambda: tela_cadastro(tela_opcoes), font=("Arial", 14)).grid(row=2, column=0,padx=10, pady=10,sticky="ew")
    tk.Button(tela_opcoes, text="Fazer login", command=lambda: tela_login(tela_opcoes), font=("Arial", 14)).grid(row=3, column=0, padx=10,pady=10, sticky="ew")

    tela_opcoes.grid_columnconfigure(0, weight=1) # tornar as colunas mais largas e ajustar a disposição

    tela_opcoes.mainloop()  # loop que mantém a interface gráfica ativa


def tela_login(tela_anterior):
    def logar():
        email = entry_email.get()
        senha = entry_senha.get()
        id_user, nome = dados.login(email, senha)

        if id_user:
            tela_menu(tela_anterior, id_user, nome)
        else:
            messagebox.showerror("Erro", "Email ou senha incorretos!")

    tela_anterior.withdraw()  # Fecha a tela inicial

    login = tk.Toplevel()
    login.geometry(tamanho_tela)
    login.title("Faça Login")
    login.resizable(False, False)

    frame = tk.Frame(login, bg="#f8f9fa") # cria uma caixa e pinta com um tom de branco
    frame.place(relx=0.5, rely=0.5, anchor="center") #  posiciona o frame exatamente no centro da janela

    tk.Label(frame, text="Entre com seu Login", font=("Arial", 20, "bold"), bg="#f8f9fa").pack(pady=10)

    entry_style = {"font": ("Arial", 14), "width": 25, "bd": 2, "relief": "solid"} #padroniza o estilo do textbox

    tk.Label(frame, text="Email:", font=("Arial", 12), bg="#f8f9fa").pack(anchor="w", padx=10, pady=5)
    entry_email = tk.Entry(frame, **entry_style)
    entry_email.pack(padx=10, pady=5)

    tk.Label(frame, text="Senha:", font=("Arial", 12), bg="#f8f9fa").pack(anchor="w", padx=10, pady=5)
    entry_senha = tk.Entry(frame, show="*", **entry_style)
    entry_senha.pack(padx=10, pady=5)

    frame_buttons = tk.Frame(frame, bg="#f8f9fa")
    frame_buttons.pack(pady=20)

    button_style = {"font": ("Arial", 14), "width": 12, "bd": 2, "relief": "raised"} #padroniza o estilo do botao

    tk.Button(frame_buttons, text="Logar", command=logar, **button_style, bg="#4CAF50",fg="white").pack(side="left", padx=10)
    tk.Button(frame_buttons, text="Voltar", command=lambda: telaInicial(login), **button_style, bg="#d9534f", fg="white").pack(side="left", padx=10)

    login.mainloop()


def tela_cadastro(tela_anterior):
    def cadastra_usuario():
        nome = entry_nome.get()
        cpf = entry_cpf.get()
        dataNascimento = entry_nascimento.get()
        email = entry_email.get()
        senha = entry_senha.get()

        if nome and email and senha:
            if validate_email(email):
                id_user, nome = dados.cadastrar_usuario(nome, cpf, dataNascimento, email, senha)
                if id_user:
                    tela_menu(tela_anterior, id_user, nome)
                else:
                    messagebox.showerror("Erro", "Email já esta cadastrado no Sistema!")
            else:
                messagebox.showerror("Erro", "Email invalido, por favor verifique se inseriu @ e"
                                             " tente novamente!")
        else:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos!")

    tela_anterior.withdraw()
    cadastrar = tk.Toplevel()
    cadastrar.geometry(tamanho_tela)
    cadastrar.title("Faça Cadastro")
    cadastrar.resizable(width=False, height=False)

    frame = tk.Frame(cadastrar, bg="#f8f9fa")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(frame, text="Faça cadastro em nosso sistema!", font=("Arial", 20, "bold"), bg="#f8f9fa").pack(pady=10)

    entry_style= {"font": ("Arial", 14), "width": 25, "bd": 2, "relief": "solid"}

    tk.Label(frame, text="CPF:", font=("Arial", 12, "italic"),bg="#f8f9fa").pack(anchor="w", padx=10, pady=5)
    entry_cpf = tk.Entry(frame, **entry_style)
    entry_cpf.pack(padx=10, pady=5)

    tk.Label(frame, text="Data de nascimento:", font=("Arial", 12, "italic"), bg="#f8f9fa").pack(anchor="w", padx=10, pady=5)
    entry_nascimento = tk.Entry(frame, **entry_style)
    entry_nascimento.pack(padx=10, pady=5)

    tk.Label(frame, text="Nome:", font=("Arial", 12, "italic"), bg="#f8f9fa").pack(anchor="w", padx=10, pady=5)
    entry_nome = tk.Entry(frame, **entry_style)
    entry_nome.pack(padx=10, pady=5)

    tk.Label(frame, text="E-mail", font=("Arial", 12, "italic"), bg="#f8f9fa").pack(anchor="w", padx=10, pady=5)
    entry_email = tk.Entry(frame, **entry_style)
    entry_email.pack(padx=10, pady=5)

    tk.Label(frame, text="Senha", font=("Arial", 12, "italic"), bg="#f8f9fa").pack(anchor="w", padx=10, pady=5)
    entry_senha = tk.Entry(frame, **entry_style, show="*")
    entry_senha.pack(padx=10,pady=5)

    frame_buttons = tk.Frame(frame, bg="#f8f9fa")
    frame_buttons.pack(pady=20)

    button_style = {"font": ("Arial", 14), "width": 12, "bd": 2, "relief": "raised"}

    tk.Button(frame_buttons, text="Cadastrar", command=cadastra_usuario, **button_style, bg="#4CAF50", fg="white").pack(side="left",padx=10)
    tk.Button(frame_buttons, text="Voltar", command=lambda: telaInicial(cadastrar), **button_style, bg="#d9534f",
              fg="white").pack(side="left", padx=10)

    cadastrar.mainloop()


def tela_menu(tela_anterior, id_user, nome):
    tela_anterior.destroy()

    menu = tk.Tk()
    menu.geometry(tamanho_tela)
    menu.title("Menu")
    menu.resizable(width=False, height=False)

    titulo = tk.Frame(menu, bg="#f8f9fa")
    titulo.pack(pady=20)
    tk.Label(titulo, text=f"Bem-vindo, {nome}", font=("Arial", 20, "bold"), bg="#f8f9fa").pack(pady=10)

    frame = tk.Frame(menu, bg="#f8f9fa", bd=3, relief="solid")
    frame.place(relx=0.5, rely=0.6, anchor="center", width=500, height=300)

    button_style = {"font": ("Arial", 14), "width": 12, "bd": 2, "relief": "raised"}

    tk.Button(frame, text="Cadastrar", command=..., **button_style, bg="#4CAF50", fg="white").grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    tk.Button(frame, text="Cadastrar", command=..., **button_style, bg="#4CAF50", fg="white").grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    tk.Button(frame, text="Cadastrar", command=..., **button_style, bg="#4CAF50", fg="white").grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
    tk.Button(frame, text="Cadastrar", command=..., **button_style, bg="#4CAF50", fg="white").grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

    # configuração para as colunas e linhas crescerem de forma que fiquem quadradas
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_rowconfigure(1, weight=1)

    frame.config(height=500)  # ajuste o tamanho da altura para garantir que o frame seja grande o suficiente

    menu.mainloop()

telaInicial()  # Inicia o programa
