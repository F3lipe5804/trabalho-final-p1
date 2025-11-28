from pessoa import Pessoa

class Medico(Pessoa):
    def __init__(self, nome, senha, crm):
        super().__init__(nome, senha, 2)
        self.crm = crm  # atributo exclusivo do médico

    def ver_sua_agenda(self, conexao):
        cursor = conexao.cursor()
        sql = "SELECT id, paciente, data_consulta, status FROM consultas WHERE medico_crm = %s ORDER BY data_consulta"
        cursor.execute(sql, (self.crm,))
        resultados = cursor.fetchall()

        print(f"\n=== Agenda do Dr(a) {self.nome} (CRM: {self.crm}) ===")
        if resultados:
            for idc, paciente, data, status in resultados:
                print(f"ID:{idc} | Paciente: {paciente} | Data: {data} | Status: {status}")
        else:
            print("Nenhuma consulta na sua agenda.")
        cursor.close()
