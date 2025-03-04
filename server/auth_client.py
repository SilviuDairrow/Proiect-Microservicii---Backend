import grpc
import auth_pb2
import auth_pb2_grpc
from cryptography.fernet import Fernet
import base64

class AuthClient:
    def __init__(self, host='auth-server', port=50051):
        
        cheie_statica = b'bruhbruhbruhbruhbruhbruhbruhbruh'
        self.key = base64.urlsafe_b64encode(cheie_statica)
        self.fernet = Fernet(self.key)
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = auth_pb2_grpc.AuthServiceStub(self.channel)

    def criptare_parola(self, password: str) -> str:
        
        return self.fernet.encrypt(password.encode()).decode()

    def creeare_cont(self, email, password, role):

        #parola_criptata = self.criptare_parola(password)
        
        cerere = auth_pb2.CreereContRequest(email=email, password=password, role=role)
        return self.stub.CreereCont(cerere)

    def verif_sesiune(self, refresh_token):

        cerere = auth_pb2.VerifSesiuneRequest(refresh_token=refresh_token)
        return self.stub.VerifSesiune(cerere)

    def login(self, email, password):

        #parola_criptata = self.criptare_parola(password)

        cerere = auth_pb2.CreereSesiuneRequest(email=email, password=password,)
        return self.stub.CreereSesiune(cerere)


    def close(self):

        self.channel.close()