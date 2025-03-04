import grpc

import jwt

from concurrent import futures

import time
import base64
from datetime import datetime, timedelta

import auth_pb2
import auth_pb2_grpc

import psycopg2
from psycopg2 import sql
from psycopg2.errors import UniqueViolation

import bcrypt
from cryptography.fernet import Fernet

cheie_statica = b'bruhbruhbruhbruhbruhbruhbruhbruh'
cheie = base64.urlsafe_b64encode(cheie_statica)
fernet = Fernet(cheie)

def conex_db():

    conn = psycopg2.connect(
        host="db_postgres",  
        database="auth_db",
        user="admin",  
        password="admin"
    )
    return conn

def creere_tb_accounts():

    create_table_query = """
    CREATE TABLE IF NOT EXISTS accounts (
        id SERIAL PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        role VARCHAR(50) NOT NULL CHECK (role IN ('student', 'profesor', 'admin'))
    );
    """
    conn = conex_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute(create_table_query)
            conn.commit()
            print("S-a creat tabela pt conturi pt ca nu exista???")

    except psycopg2.Error as eroare:
        print(f"Eroare la creerea tabelei: {eroare}")

    finally:
        conn.close()

SECRET_KEY = "bruh"
ALGORITHM = "HS512"
refresh_token_zile = 30

def creere_refresh_token(data: dict):

    expire = datetime.utcnow() + timedelta(days=refresh_token_zile)
    to_encode = {"exp": expire, **data}

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decodare_token(token: str):

    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded
    
    except jwt.ExpiredSignatureError:
        raise Exception("Token JWT expirat")
    
    except jwt.InvalidTokenError:
        raise Exception("Token JWT invalid")


class AuthService(auth_pb2_grpc.AuthServiceServicer):
    
    def decriptie_pass(self, encrypted_password: str) -> str:

        return fernet.decrypt(encrypted_password.encode()).decode()

    def CreereCont(self, cerere, context):

        email = cerere.email  
        role = cerere.role
        role_name = ["student", "profesor", "admin"][role]

        parola_criptata = cerere.password        

        conexiune_db = conex_db()

        try:
            with conexiune_db.cursor() as cursor:
                pw_hash = bcrypt.hashpw(parola_criptata.encode('utf-8'), bcrypt.gensalt())

                cursor.execute(
                    sql.SQL("INSERT INTO accounts (email, password, role) VALUES (%s, %s, %s)"),
                    [email, pw_hash.decode('utf-8'), role_name]
                )
                conexiune_db.commit()

                refresh_token = creere_refresh_token({"sub": email, "role": role_name})

                return auth_pb2.CreereContResponse(refresh_token=refresh_token)
        
        except UniqueViolation:

            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details("Exista deja un cont inregistrat cu acest email dawg.")
            return auth_pb2.CreereContResponse()
        
        except Exception as eroare:

            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Eroare: {str(eroare)}")
            return auth_pb2.CreereContResponse()
        
        finally:
            conexiune_db.close()
    
    def CreereSesiune(self, cerere, context):

        email = cerere.email

        conexiune_db = conex_db()

        try:
            with conexiune_db.cursor() as cursor:
                cursor.execute(
                    sql.SQL("SELECT password, role FROM accounts WHERE email = %s"),
                    [email]
                )
                result = cursor.fetchone()

                if result and bcrypt.checkpw(cerere.password.encode('utf-8'), result[0].encode('utf-8')):
                    role = result[1]

                    refresh_token = creere_refresh_token({"sub": email, "role": role})

                    return auth_pb2.CreereSesiuneResponse(refresh_token=refresh_token)
                
                else:
                    context.set_code(grpc.StatusCode.UNAUTHENTICATED)
                    context.set_details("Ai introdus mailul sau parola gresit dawg!")
                    return auth_pb2.CreereSesiuneResponse()
        
        finally:
            conexiune_db.close()

    def VerifSesiune(self, cerere, context):

        refresh_token = cerere.refresh_token

        try:

            decoded = decodare_token(refresh_token)

            role_map = {
            "student": auth_pb2.Role.ROLE_STUDENT,
            "profesor": auth_pb2.Role.ROLE_PROFESOR,
            "admin": auth_pb2.Role.ROLE_ADMIN,
            }       

            role_enum = role_map.get(decoded["role"].lower())
            if role_enum is None:
                raise ValueError(f"Rol invalid la nivel de token? how?: {decoded['role']}")

            return auth_pb2.VerifSesiuneResponse(
                email = decoded["sub"],
                role = role_enum
            )
        
        except Exception as error:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details(str(error))
            return auth_pb2.VerifSesiuneResponse()


def serve():
    
    creere_tb_accounts()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthService(), server)

    server.add_insecure_port('[::]:50051')
    server.start()

    try:
        while True:
            time.sleep(60 * 60 * 24)

    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
