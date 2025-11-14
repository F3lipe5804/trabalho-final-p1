from pessoa import Pessoa

class Usuario(Pessoa):
    def __init__(self, nome, senha):
        super().__init__(nome, senha, "user")

    def marcar_consulta(self, data, conexao):
        cursor = conexao.cursor()
        sql = "INSERT INTO consultas (paciente, data_consulta, status) VALUES (%s, %s, 'Agendada')"
        cursor.execute(sql, (self.nome, data))
        conexao.commit()
        print(f"Consulta marcada para {data}.")
        cursor.close()

    def ver_consultas(self, conexao):
        cursor = conexao.cursor()
        sql = "SELECT data_consulta, status FROM consultas WHERE paciente = %s"
        cursor.execute(sql, (self.nome,))
        resultados = cursor.fetchall()

        print(f"\n=== Consultas de {self.nome} ===")
        if resultados:
            for data, status in resultados:
                print(f"- {data} | {status}")
        else:
            print("Nenhuma consulta encontrada.")
        cursor.close()