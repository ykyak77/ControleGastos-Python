import banco_dados as banco
import bcrypt as codificacao #criptografia de senha/ exige que instale o pacote bcrypt
import sqlite3
import random #gerar numero aleatorio p criar uma conta


def gerar_conta():
    conexao, cursor = banco.conectar()

    while True:
        num_conta = random.randint(1,99999)
        cursor.execute("SELECT num_conta FROM conta WHERE num_conta = ?", (num_conta,))
        if cursor.fetchone() is None: # Se não existe, retorna o número
            return num_conta


def validarCpf(cpf):
    ...


def cadastrar_usuario(nome, cpf, dataNascimento, email, senha):
    conexao, cursor = banco.conectar()
    try:
        # Codificando a senha
        salt = codificacao.gensalt()
        senha_criptografada = codificacao.hashpw(senha.encode('utf-8'), salt)

        # cadastrando o usuario
        cursor.execute("INSERT INTO usuario(nome, cpf, data_nascimento, email, senha) VALUES(?,?,?,?,?)",
                       (nome, cpf, dataNascimento,email, senha_criptografada)) # ?, ?, ?, ? é uma técnica chamada parametrização
        conexao.commit() # cadastrar
        cursor.execute("SELECT id_user, nome FROM usuario WHERE email = ? and senha = ?", (email, senha_criptografada))
        id_usr, nome = cursor.fetchone()

        # cria uma conta automaticamente
        num_conta = gerar_conta()
        cursor.execute("INSERT INTO conta(num_conta, saldo, usuario_id) VALUES(?,?,?)",
                       (num_conta, 0.00, id_usr))
        print("Usuário cadastrado com sucesso!")
        return (id_usr, nome, num_conta) if (id_usr and nome) else None
    except sqlite3.IntegrityError:
        print("Erro: Esse login já está em uso.")
        return None
    finally:
        conexao.close()


def login(email, senha):
    conexao, cursor = banco.conectar()

    # Recupera o hash da senha armazenada no banco de dados
    cursor.execute("SELECT senha FROM usuario WHERE email = ?", (email,))
    resultado = cursor.fetchone()

    if resultado:
        senha_armazenada = resultado[0]
        #comparar as senhas
        if codificacao.checkpw(senha.encode('utf-8'), senha_armazenada):
            cursor.execute("SELECT id_user, nome FROM usuario WHERE email = ? and senha = ?", (email, senha_armazenada))
            id_usr, nome = cursor.fetchone()
            conexao.close()
            return id_usr, nome
        else:
            return None
    else:
        return None


def fazer_transasao(descricao, valor, tipo, categoria, data, usuario_id):
    conexao, cursor = banco.conectar()

    cursor.execute("INSERT INTO transacoes(descricao, valor, tipo, categoria, data, usuario_id) VALUES(?,?,?,?,?)",
                   (descricao,valor,tipo,categoria,data))

    cursor.execute("UPDATE usuarios SET saldo = saldo + ? WHERE id = ?", (valor, usuario_id))

    conexao.commit()
    conexao.close()


