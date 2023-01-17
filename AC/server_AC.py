import pika
from os import path
import datetime
from OpenSSL.crypto import verify
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes


CA_CERT_PATH = 'certificate_ca.pem'
CA_KEY_PATH = 'key_ca.pem'
cert = None
key = None


def generate_or_load():
    global cert
    global key
    if(path.isfile(CA_CERT_PATH) and path.exists(CA_CERT_PATH) and path.isfile(CA_KEY_PATH) and path.exists(CA_KEY_PATH)):
        # charger des fichiers
        print('Chargement !')
        cert = x509.load_pem_x509_certificate(
            open(CA_CERT_PATH, 'rb').read(), default_backend())
        print(cert)
        key = serialization.load_pem_private_key(
            open(CA_KEY_PATH, 'rb').read(), password=None, backend=default_backend())
    else:
        print(' Generer en cours!')
        # generate key and self signed cert
        key = rsa.generate_private_key(
            public_exponent=65536,
            key_size=2048,
            backend=default_backend()
        )   # Sauvegarder dans le disque

        with open(CA_KEY_PATH, "wb") as f:
            f.write(key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
               
                encryption_algorithm=serialization.NoEncryption()
            ))
            # Faire un certificat auto-signé
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, u"TN"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Tunis"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, u"ELGhazela"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"TEKUP"),
            x509.NameAttribute(NameOID.COMMON_NAME, u"TEKUP"),
        ])
        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            # Notre certificat CA sera valide pendant 9125 jours ~ 25 ans
            datetime.datetime.utcnow() + datetime.timedelta(days=9125)
        ).sign(key, hashes.SHA256(), default_backend())
        # Écrivez notre certificat sur le disque.
        with open(CA_CERT_PATH, "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
    return (key, cert)


def handle_cert_req(CSR_PATH):
    if(path.exists(CSR_PATH) and path.isfile(CSR_PATH)):
        # demande de certification de chargement
        print('Demande de traitement')
        csr = x509.load_pem_x509_csr(
            open(CSR_PATH, 'rb').read(), default_backend())
        cert_client = x509.CertificateBuilder().subject_name(
            csr.subject
        ).issuer_name(
            cert.subject
        ).public_key(
            csr.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            # Notre certificat CA sera valide pendant 7 jours
            datetime.datetime.utcnow() + datetime.timedelta(days=7)
        )
        for ext in csr.extensions:
            cert_client.add_extension(ext.value, ext.critical)

        cert_client = cert_client.sign(key, hashes.SHA256(), default_backend())
        with open('client_cert.pem', 'wb') as f:
            f.write(cert_client.public_bytes(serialization.Encoding.PEM))
    else:
        print('Aucune demande à traiter')


def handle_req(reqData, cert):
    csr = x509.load_pem_x509_csr(reqData, default_backend())
    cert_client = x509.CertificateBuilder().subject_name(
        csr.subject
    ).issuer_name(
        cert.subject
    ).public_key(
        csr.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        # Notre certificat CA sera valide pendant 7 jours
        datetime.datetime.utcnow() + datetime.timedelta(days=5)
    )
    for ext in csr.extensions:
        cert_client.add_extension(ext.value, ext.critical)

    cert_client = cert_client.sign(key, hashes.SHA256(), default_backend())
    return cert_client.public_bytes(serialization.Encoding.PEM).decode()


def handle_cert(data):
    if data:
        cert = x509.load_pem_x509_certificate(data, default_backend())
      
        return cert
    else:
        print('Il n\'y a pas d\'attestation')
        return None
# La première étape consiste à créer un certificat ROOT (certificat auto-signé pour l'autorité)
# générer_ou_charger()

# La deuxième consiste à gérer toute demande de certificat et à la signer à l'aide du certificat ROOT
# andle_cert_req('client_csr.pem')


class CaServer:

    def generate_authority_key(self):
        self.ca_key, self.ca_cert = generate_or_load()
        self.ca_pubkey = self.ca_key.public_key()

    def connect(self):
        self.generate_authority_key()
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.receive()

    def send(self, client_queue, action, data):

        self.channel.exchange_declare(
            exchange='cert_exchange', exchange_type='direct')
        self.channel.queue_declare(queue=client_queue, durable=True)

        message = action+'::'+data
        self.channel.basic_publish(
            exchange='cert_exchange',
            routing_key=client_queue,
            body=message
        )
        print('Server sended cert to '+str(client_queue))

    def receive(self):
        self.channel.queue_declare(queue='cert_req_queue', durable=True)

        def callback(ch, method, properties, body):
            
            client_queue, action, data = body.decode().split('::')
            if (action == 'request'):

                print('Le serveur obtient la demande de certificat de '+str(client_queue))
                data = data.encode()
                certdata = handle_req(data, self.ca_cert)
                self.send(client_queue, 'certif', certdata)
            if(action == 'verify'):
                print('Le serveur obtient la vérification de'+str(client_queue))
                certif = handle_cert(data.encode())
                print(certif)
                result = ""
                try:
                    result = self.ca_pubkey.verify(
                        certif.signature,
                        certif.tbs_certificate_bytes,
            #Dépend de l'algorithme utilisé pour créer le certificat
                        padding.PKCS1v15(),
                        certif.signature_hash_algorithm,)
                    result = "Ok"
                except Exception:
                    result = "Non vérifié"
                finally:
                    self.send(client_queue, 'vérifié', result)

            ch.basic_ack(delivery_tag=method.delivery_tag)

        self.channel.basic_consume(
            queue='cert_req_queue', on_message_callback=callback)
        print('Serveur démarré !! Écoute')
        self.channel.start_consuming()


server = CaServer()
server.connect()
