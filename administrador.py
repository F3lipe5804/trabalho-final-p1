from pessoa import Pessoa

class Administrador(Pessoa):
    def __init__(self, nome, senha):
        super().__init__(nome, senha, "adm")

    def cadastrar_usuario(self, conexao):
        cursor = conexao.cursor()
        print("\n=== Cadastro de Novo Usuário ===")
        nome = input("Novo cadastro: ")
        senha = input("Senha: ")
        sql = "INSERT INTO usuarios (nome, senha, tipo) VALUES (%s, %s, %s)"
        cursor.execute(sql, (nome, senha, "user"))
        conexao.commit()
        print(f"O {nome} foi cadastrado como Usuario!")
        cursor.close()

    def alterar_nivel_usuario(self, conexao):
        cursor = conexao.cursor()
        print("\n=== Alterar nível de permissão de usuário ===")
        nome = input("Nome do usuário: ")
        sql_select = "SELECT id, nome, tipo FROM usuarios WHERE nome = %s"
        cursor.execute(sql_select, (nome,))
        resultado = cursor.fetchone()

        if not resultado:
            print("Usuário não encontrado.")
            cursor.close()
            return

        id_usuario, nome_usuario, tipo_atual = resultado

        if tipo_atual == "adm":
            novo_tipo = "user"
        else:
            novo_tipo = "adm"

        sql_update = "UPDATE usuarios SET tipo = %s WHERE id = %s"
        cursor.execute(sql_update, (novo_tipo, id_usuario))
        conexao.commit()

        print(f"Nível do usuário {nome_usuario} alterado de '{tipo_atual}' para '{novo_tipo}'.")
        cursor.close()

    def agendar_consulta(self, paciente, data, conexao):
        cursor = conexao.cursor()
        sql = "INSERT INTO consultas (paciente, data_consulta, status) VALUES (%s, %s, 'Agendada')"
        cursor.execute(sql, (paciente, data))
        conexao.commit()
        print(f"Consulta para {paciente} agendada em {data}.")
        cursor.close()

    def reagendar_consulta(self, paciente, data_antiga, nova_data, conexao):
        cursor = conexao.cursor()
        sql = "UPDATE consultas SET data_consulta = %s WHERE paciente = %s AND data_consulta = %s"
        cursor.execute(sql, (nova_data, paciente, data_antiga))
        conexao.commit()
        if cursor.rowcount > 0:
            print(f"Consulta de {paciente} reagendada para {nova_data}.")
        else:
            print("Consulta não encontrada.")
        cursor.close()

    def concluir_consulta(self, paciente, data, conexao):
        cursor = conexao.cursor()
        sql = "UPDATE consultas SET status = 'Concluída' WHERE paciente = %s AND data_consulta = %s"
        cursor.execute(sql, (paciente, data))
        conexao.commit()
        if cursor.rowcount > 0:
            print("Consulta marcada como concluída.")
        else:
            print("Consulta não encontrada.")
        cursor.close()

    def ver_agenda(self, conexao):
        cursor = conexao.cursor()
        cursor.execute("SELECT paciente, data_consulta, status FROM consultas")
        resultados = cursor.fetchall()

        print(f"\n=== Agenda Médico ===")
        if resultados:
            for paciente, data, status in resultados:
                print(f"Paciente: {paciente} | Data: {data} | Status: {status}")
        else:
            print("Nenhuma consulta registrada.")
        cursor.close()
