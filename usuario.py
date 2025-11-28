from pessoa import Pessoa
from datetime import datetime

class Usuario(Pessoa):
    def __init__(self, nome, senha):
        super().__init__(nome, senha, 1)

    def marcar_consulta(self, data_str, conexao):
        cursor = conexao.cursor()
        data = self._parse_data_str(data_str)
        if not data:
            print("Formato de data inválido.")
            cursor.close()
            return
        medico_crm = input("Deseja escolher um médico? Informe o CRM (ou deixe vazio): ").strip() or None
        if medico_crm:
            sql_check = "SELECT id FROM consultas WHERE medico_crm = %s AND data_consulta = %s"
            cursor.execute(sql_check, (medico_crm, data))
            if cursor.fetchone():
                print("O médico está OCUPADO nesse horário. Escolha outro horário ou outro médico.")
                cursor.close()
                return
            else:
                print("O médico está DISPONÍVEL nesse horário.")
        sql = "INSERT INTO consultas (paciente, data_consulta, status, medico_crm) VALUES (%s, %s, 'Agendada', %s)"
        try:
            cursor.execute(sql, (self.nome, data, medico_crm))
            conexao.commit()
            print(f"Consulta marcada para {data}. (médico CRM: {medico_crm})")
        except Exception as e:
            print(f"Erro ao marcar consulta: {e}")
        finally:
            cursor.close()

    def ver_consultas(self, conexao):
        cursor = conexao.cursor()
        sql = "SELECT id, data_consulta, status, medico_crm FROM consultas WHERE paciente = %s ORDER BY data_consulta"
        cursor.execute(sql, (self.nome,))
        resultados = cursor.fetchall()
        print(f"\n=== Consultas de {self.nome} ===")
        if resultados:
            for idc, data, status, crm in resultados:
                print(f"ID:{idc} | Data: {data} | Status: {status} | CRM do médico: {crm}")
        else:
            print("Nenhuma consulta encontrada.")
        cursor.close()

    def listar_agenda_e_remarcar(self, conexao):
        cursor = conexao.cursor()
        sql = "SELECT id, data_consulta, medico_crm FROM consultas WHERE paciente = %s ORDER BY data_consulta"
        cursor.execute(sql, (self.nome,))
        consultas = cursor.fetchall()
        if not consultas:
            print("Você não possui consultas.")
            cursor.close()
            return
        print("\n=== Suas consultas ===")
        for idc, data, crm in consultas:
            print(f"ID:{idc} | Data:{data} | CRM:{crm}")
        escolha = input("Deseja remarcar alguma? Digite o ID ou pressione Enter: ").strip()
        if escolha:
            nova_data = input("Nova data (dd/mm/aaaa ou dd/mm/aaaa HH:MM): ").strip()
            data_nova = self._parse_data_str(nova_data)
            if not data_nova:
                print("Data inválida.")
                cursor.close()
                return
            sql_up = "UPDATE consultas SET data_consulta = %s WHERE id = %s AND paciente = %s"
            cursor.execute(sql_up, (data_nova, escolha, self.nome))
            conexao.commit()
            if cursor.rowcount > 0:
                print("Consulta remarcada com sucesso.")
            else:
                print("Falha ao remarcar.")
        cursor.close()

    def _parse_data_str(self, data_str):
        for fmt in ("%d/%m/%Y %H:%M", "%d/%m/%Y"):
            try:
                dt = datetime.strptime(data_str, fmt)
                if fmt == "%d/%m/%Y":
                    dt = dt.replace(hour=9, minute=0)
                return dt
            except:
                continue
        return None
