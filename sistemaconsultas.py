from mysql.connector import Error
from mysql.connector.constants import ClientFlag
import mysql.connector
from administrador import Administrador
from usuario import Usuario
from medico import Medico
from datetime import datetime

class SistemaConsultas:
    def __init__(self):
        try:
            config = {
                'user': '' ,
                'password': '',
                'host': '',
                'port': ,
                'client_flags': ,
                'ssl_ca': r'', #Necessario trocar para rodar o codigo
                'database': ''
            }

            self.conexao = mysql.connector.connect(**config)
            print("Conexão MySQL estabelecida com sucesso!\n")

        except Error as e:
            print(f"Erro ao conectar ao banco: {e}")
            exit()

    def criar_tabelas(self):
        cursor = self.conexao.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(50) UNIQUE NOT NULL,
            senha VARCHAR(50) NOT NULL,
            tipo TINYINT NOT NULL DEFAULT 1,
            crm VARCHAR(50) DEFAULT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS consultas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            paciente VARCHAR(50) NOT NULL,
            data_consulta DATETIME NOT NULL,
            status ENUM('Agendada', 'Concluída') DEFAULT 'Agendada',
            medico_crm VARCHAR(50) DEFAULT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)

        self.conexao.commit()
        cursor.close()

    def cadastrar_usuario(self):
        print("\n=== Cadastro de Novo Usuário ===")
        nome = input("Novo cadastro: ").strip()
        senha = input("Senha: ").strip()

        cursor = self.conexao.cursor()
        try:
            sql = "INSERT INTO usuarios (nome, senha, tipo, crm) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (nome, senha, 1, None))
            self.conexao.commit()
            print(f"Usuário '{nome}' cadastrado com sucesso como USUÁRIO comum!")
        except mysql.connector.IntegrityError:
            print("Usuário já existe!")
        except Exception as e:
            print(f"Erro: {e}")
        finally:
            cursor.close()

    def autenticar_usuario(self, nome, senha):
        cursor = self.conexao.cursor(dictionary=True)
        sql = "SELECT * FROM usuarios WHERE nome = %s AND senha = %s"
        cursor.execute(sql, (nome, senha))
        usuario = cursor.fetchone()
        cursor.close()
        return usuario

    def login(self):
        print("\n=== Login ===")
        nome = input("Login: ").strip()
        senha = input("Senha: ").strip()

        usuario = self.autenticar_usuario(nome, senha)
        if usuario:
            tipo = usuario["tipo"]
            crm = usuario.get("crm")
            print(f"\nBem-vindo, {nome} (tipo {tipo})!")
            if tipo == 3:
                self.menu_adm(Administrador(nome, senha))
            elif tipo == 2:
                self.menu_med(Medico(nome, senha, crm))
            else:
                self.menu_user(Usuario(nome, senha))
        else:
            print("Login ou senha incorretos!")

    def menu_user(self, usuario):
        while True:
            print(f"\n=== Menu do Usuário ({usuario.nome}) ===")
            print("1 - Marcar consulta")
            print("2 - Ver minhas consultas")
            print("0 - Sair")
            opc = input("Escolha: ")

            if opc == "1":
                data = input("Data da consulta (dd/mm/aaaa ou dd/mm/aaaa HH:MM): ").strip()
                usuario.marcar_consulta(data, self.conexao)
            elif opc == "2":
                usuario.ver_consultas(self.conexao)
            elif opc == "0":
                break
            else:
                print("Opção inválida!")

    def menu_adm(self, adm):
        while True:
            print(f"\n=== Menu do Administrador ({adm.nome}) ===")
            print("1 - Agendar consulta")
            print("2 - Reagendar consulta")
            print("3 - Marcar consulta como concluída")
            print("4 - Ver todas as consultas")
            print("5 - Cadastrar usuário")
            print("6 - Alterar nível de usuário")
            print("0 - Sair")
            opc = input("Escolha: ")

            if opc == "1":
                paciente = input("Nome do paciente: ").strip()
                data = input("Data da consulta (dd/mm/aaaa ou dd/mm/aaaa HH:MM): ").strip()
                adm.agendar_consulta(paciente, data, self.conexao)
            elif opc == "2":
                paciente = input("Nome do paciente: ").strip()
                antiga = input("Data antiga (dd/mm/aaaa ou dd/mm/aaaa HH:MM): ").strip()
                nova = input("Nova data (dd/mm/aaaa ou dd/mm/aaaa HH:MM): ").strip()
                adm.reagendar_consulta(paciente, antiga, nova, self.conexao)
            elif opc == "3":
                paciente = input("Nome do paciente: ").strip()
                data = input("Data da consulta: ").strip()
                adm.concluir_consulta(paciente, data, self.conexao)
            elif opc == "4":
                adm.ver_agenda(self.conexao)
            elif opc == "5":
                adm.cadastrar_usuario(self.conexao)
            elif opc == "6":
                adm.alterar_nivel_usuario(self.conexao)
            elif opc == "0":
                break
            else:
                print("Opção inválida!")

    def menu_med(self, medico):
        while True:
            print(f"\n=== Menu do Médico ({medico.nome} - CRM {medico.crm}) ===")
            print("1 - Ver minha agenda")
            print("0 - Sair")
            opc = input("Escolha: ")

            if opc == "1":
                medico.ver_sua_agenda(self.conexao)
            elif opc == "0":
                break
            else:
                print("Opção inválida!")

    def ver_agenda_do_medico_com_status(self, crm, conexao):
        cursor = conexao.cursor()
        sql = "SELECT data_consulta FROM consultas WHERE medico_crm = %s ORDER BY data_consulta"
        cursor.execute(sql, (crm,))
        resultados = cursor.fetchall()
        ocupado = set()
        for (dt,) in resultados:
            ocupado.add(dt)
        cursor.close()
        return ocupado

    def iniciar(self):
        self.criar_tabelas()
        while True:
            print("\n=== SISTEMA DE CONSULTAS ===")
            print("1 - Login")
            print("2 - Cadastrar usuário")
            print("0 - Sair")
            opc = input("Escolha: ")

            if opc == "1":
                self.login()
            elif opc == "2":
                self.cadastrar_usuario()
            elif opc == "0":
                print("Encerrando o sistema...")
                self.conexao.close()
                break
            else:
                print("Opção inválida!")
