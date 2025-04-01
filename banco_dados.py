import sqlite3 # biblioteca de para criar o banco de dados

def conectar():
    try:
        conexao = sqlite3.connect("bdFinancias.db") # cria/coneecta ao banco de dados
        cursor = conexao.cursor() # cria cursor para execultar comando do bd
        return conexao, cursor # retorno para manipular os dados futuramente
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None, None


def criacao_tabelas(): # criando as tabelas
    conexao,cursor = conectar()

    if conexao is None or cursor is None:
        print("Erro ao conectar e criar as tabelas")
        return

    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuario(
            id_user INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT NOT NULL UNIQUE,
            data_nascimento DATE NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS conta(
            num_conta INTEGER PRIMARY KEY,
            saldo REAL NOT NULL DEFAULT 0.00,
            usuario_id INTEGER,
            FOREIGN KEY (usuario_id) REFERENCES usuario (id_user)
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS transacoes(
            id_transacao INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT,
            valor REAL NOT NULL,
            tipo TEXT NOT NULL CHECK (tipo IN ('depósito', 'saque', 'transferência')),
            categoria TEXT,
            data TEXT NOT NULL,
            conta_origem INTEGER NOT NULL,
            conta_destino INTEGER NULL,
            FOREIGN KEY (conta_origem) REFERENCES conta(num_conta),
            FOREIGN KEY (conta_destino) REFERENCES conta(num_conta),
        )
        """)

        conexao.commit() # execulta os comando sql
        print("Tabelas usuario e trancacos criadas com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao criar as tabelas!: {e}")
    finally:
        conexao.close() # fecha o banco

def teste():
    conexao, cursor = conectar()

    cursor.execute("SELECT * FROM usuario")
    usuario = cursor.fetchone()  # pega a resposta do select

    conexao.close()

    if usuario:
        return usuario[1],usuario[2],usuario[3]  # Retorna o valor encontrado
    else:
        return 'Sem dados no banco'  # Retorna uma string caso não haja dados

