from Crypto.PublicKey import RSA
from Crypto import Random 
from Crypto.Cipher import PKCS1_OAEP
import base64


def rsa_encrypt_decrypt():
    #Generation RSA
    key = RSA.generate(2048)
    #Extrac
    private_key = key.export_key('PEM')
    #Extracter le cle public
    public_key = key.publickey().exportKey('PEM')
    #recuperer le message a envoyer
    message = input('\n SVP envoyez les message  en utilisant RSA: ')
    #coder le message
    message = str.encode(message)
    #utiliser le cle public pour crypter le message
    rsa_public_key = RSA.importKey(public_key)
    #PKCS#1 OAEP c'est un asymetric cipher baser en RSA et  the OAEP padding
    rsa_public_key = PKCS1_OAEP.new(rsa_public_key)
    #cryptage finale
    encrypted_message = rsa_public_key.encrypt(message)
    
    #codeage Base64 that est utiliser pour stocker facilement en BD-serveur
    encrypted_message = base64.b64encode(encrypted_message)

    print('\nvotre message crypter est  : ', encrypted_message)

    #Decryptage en cle prive
    rsa_private_key = RSA.importKey(private_key)
    #Applique le meme magic  en utilisant  PKCS1 OAEP
    rsa_private_key = PKCS1_OAEP.new(rsa_private_key)

    #ecodage Base64 Avant  decryptage , sinon ce serait faux, it's logical right? :)


    encrypted_message = base64.b64decode(encrypted_message)
    decrypted_message = rsa_private_key.decrypt(encrypted_message)

    print('\nvotre message apres le cryptage : ', decrypted_message)

def rsa_encrypt(message, receiver_public_key):
    message = str.encode(message)
    rsa_public_key = RSA.importKey(receiver_public_key)
    rsa_public_key = PKCS1_OAEP.new(rsa_public_key)
    encrypted_message = rsa_public_key.encrypt(message)
    encrypted_message = base64.b64encode(encrypted_message)
    return encrypted_message

def rsa_decrypt(encrypted_message, receiver_private_key):
    rsa_private_key = RSA.importKey(receiver_private_key)
    rsa_private_key = PKCS1_OAEP.new(rsa_private_key)
    encrypted_message = base64.b64decode(encrypted_message)
    decrypted_message = rsa_private_key.decrypt(encrypted_message)
    return decrypted_message



#  obtenir la clé rsa du fichier
def get_rsa_key(filepath):
    with open(filepath, mode='rb') as private_file:
        priv_key_data = private_file.read()
        private_key = RSA.importKey(priv_key_data)
        
        return private_key
