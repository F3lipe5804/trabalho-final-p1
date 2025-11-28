from pessoa import Pessoa
from datetime import datetime

class Administrador(Pessoa):
    def __init__(self, nome, senha):
        super().__init__(nome, senha, 3)

    def cadastrar_usuario(self, conexao):
        cursor = conexao.cursor()
        print("\n=== Cadastro de Novo Usuário (ADM) ===")
        nome = input("Nome do novo usuário: ").strip()
        senha = input("Senha: ").strip()
        print("Tipo: 1 - usuário | 2 - médico | 3 - adm")
        try:
            tipo = int(input("Escolha o tipo (1/2/3): ").strip())
            if tipo not in (1, 2, 3):
                print("Tipo inválido. Será cadastrado como usuário (1).")
                tipo = 1
        except ValueError:
            tipo = 1
        crm = None
        if tipo == 2:
            crm = input("Informe o CRM do médico (ou deixe vazio): ").strip() or None
        sql = "INSERT INTO usuarios (nome, senha, tipo, crm) VALUES (%s, %s, %s, %s)"
        try:
            cursor.execute(sql, (nome, senha, tipo, crm))
            conexao.commit()
            print(f"Usuário '{nome}' cadastrado com sucesso com tipo {tipo}!")
        except Exception as e:
            print(f"Erro ao cadastrar usuário: {e}")
        finally:
            cursor.close()

    def alterar_nivel_usuario(self, conexao):
        cursor = conexao.cursor()
        print("\n=== Alterar nível de permissão de usuário ===")
        nome = input("Nome do usuário a alterar: ").strip()
        sql_select = "SELECT id, nome, tipo, crm FROM usuarios WHERE nome = %s"
        cursor.execute(sql_select, (nome,))
        resultado = cursor.fetchone()
        if not resultado:
            print("Usuário não encontrado.")
            cursor.close()
            return
        id_usuario, nome_usuario, tipo_atual, crm_atual = resultado
        print(f"Usuário encontrado: {nome_usuario} (tipo atual: {tipo_atual})")
        print("Escolha o novo nível: 1 - usuário | 2 - médico | 3 - adm")
        try:
            novo_tipo = int(input("Novo nível (1/2/3): ").strip())
            if novo_tipo not in (1,2,3):
                print("Nível inválido. Operação cancelada.")
                cursor.close()
                return
        except ValueError:
            print("Entrada inválida. Operação cancelada.")
            cursor.close()
            return
        novo_crm = crm_atual
        if novo_tipo == 2:
            novo_crm = input("Informe o CRM para este usuário (ou deixe vazio): ").strip() or None
        else:
            novo_crm = None
        sql_update = "UPDATE usuarios SET tipo = %s, crm = %s WHERE id = %s"
        try:
            cursor.execute(sql_update, (novo_tipo, novo_crm, id_usuario))
            conexao.commit()
            print(f"Nível do usuário {nome_usuario} alterado de '{tipo_atual}' para '{novo_tipo}'.")
        except Exception as e:
            print(f"Erro ao alterar nível: {e}")
        finally:
            cursor.close()

    def agendar_consulta(self, paciente, data_str, conexao):
        cursor = conexao.cursor()
        data = self._parse_data_str(data_str)
        if not data:
            print("Formato de data inválido.")
            cursor.close()
            return
        medico_crm = input("CRM do médico (opcional, enter para nenhum): ").strip() or None
        if medico_crm:
            sql_check = "SELECT id FROM consultas WHERE medico_crm = %s AND data_consulta = %s"
            cursor.execute(sql_check, (medico_crm, data))
            if cursor.fetchone():
                print("Atenção: o médico já está ocupado nesse horário. Mesmo assim deseja agendar? (s/N)")
                resp = input().strip().lower()
                if resp != 's':
                    print("Agendamento cancelado.")
                    cursor.close()
                    return
        sql = "INSERT INTO consultas (paciente, data_consulta, status, medico_crm) VALUES (%s, %s, 'Agendada', %s)"
        try:
            cursor.execute(sql, (paciente, data, medico_crm))
            conexao.commit()
            print(f"Consulta para {paciente} agendada em {data}. (CRM: {medico_crm})")
        except Exception as e:
            print(f"Erro ao agendar consulta: {e}")
        finally:
            cursor.close()

    def reagendar_consulta(self, paciente, data_antiga_str, nova_data_str, conexao):
        cursor = conexao.cursor()
        antiga = self._parse_data_str(data_antiga_str)
        nova = self._parse_data_str(nova_data_str)
        if not antiga or not nova:
            print("Formato de data inválido.")
            cursor.close()
            return
        sql = "UPDATE consultas SET data_consulta = %s WHERE paciente = %s AND data_consulta = %s"
        cursor.execute(sql, (nova, paciente, antiga))
        conexao.commit()
        if cursor.rowcount > 0:
            print(f"Consulta de {paciente} reagendada para {nova}.")
        else:
            print("Consulta não encontrada.")
        cursor.close()

    def concluir_consulta(self, paciente, data_str, conexao):
        cursor = conexao.cursor()
        data = self._parse_data_str(data_str)
        if not data:
            print("Formato de data inválido.")
            cursor.close()
            return
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
        sql = "SELECT id, paciente, data_consulta, status, medico_crm FROM consultas ORDER BY data_consulta"
        cursor.execute(sql)
        resultados = cursor.fetchall()
        print(f"\n=== Agenda (ADM vê todas) ===")
        if resultados:
            for idc, paciente, data, status, crm in resultados:
                print(f"ID:{idc} | Paciente: {paciente} | Data: {data} | Status: {status} | CRM: {crm}")
        else:
            print("Nenhuma consulta registrada.")
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
