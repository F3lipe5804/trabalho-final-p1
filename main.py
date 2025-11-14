from mysql.connector import Error
from mysql.connector.constants import ClientFlag
import mysql.connector
from pessoa import Pessoa
from administrador import Administrador
from usuario import Usuario
from sistemaconsultas import SistemaConsultas

if __name__ == "__main__":
    app = SistemaConsultas()
    app.iniciar()