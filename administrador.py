from pessoa import Pessoa

class Administrador(Pessoa):
    def __init__(self, nome, senha):
        super().__init__(nome, senha, "adm")

    def cadastrar_usuario(self, conexao):
        cursor = conexao.cursor()
        print("\n=== Cadastro de Novo Usuário ===")
        nome = input("Novo cadastro: ")
        senha = input("Senha: ")
        sql = "INSERT INTO usuarios (nome, senha) VALUES (%s, %s)"
        cursor.execute(sql, (nome, senha))
        conexao.commit()
        print(f"O {nome} foi cadastrado como Usuario!")
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
            for paciente, data in resultados:
                print(f"Paciente: {paciente} | Data: {data}")
        else:
            print("Nenhuma consulta registrada.")
        cursor.close()