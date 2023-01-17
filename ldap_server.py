import ldap
import hashlib
import sys
from base64 import b64encode


class LdapService():

    ldap_server = "ldap.tek-up.de"  
    ldap_ou = "security"  
    ldap_group = "security-group"  

    # domaine d'admin
    LDAP_ADMIN_DN = "cn=admin,dc=tek-up,dc=de"
    LDAP_ADMIN_PWD = ""

    def __init__(self, admin_pwd):
        self.LDAP_ADMIN_PWD = admin_pwd

    def login(self, username, password):
        self.username = username
        self.password = password

        
        user_dn = "cn=" + self.username + ",cn=" + self.ldap_group + ",ou=" + \
            self.ldap_ou + ",dc=tek-up,dc=de"

        print(user_dn)


        LDAP_BASE_DN = "cn=" + self.ldap_group + \
                ",ou=" + self.ldap_ou + ",dc=tek-up,dc=de"

        # start connection
        ldap_client = ldap.initialize(self.ldap_server)
        # search for specific user
        search_filter = "cn=" + self.username

        try:
            # if authentication successful, get the full user data
            ldap_client.bind_s(user_dn, self.password)
            result = ldap_client.search_s(
                LDAP_BASE_DN, ldap.SCOPE_SUBTREE, search_filter)

            # return all user data results
            ldap_client.unbind_s()
            print(result)
            return None
        except ldap.INVALID_CREDENTIALS:
            ldap_client.unbind()
            print("Nom d'utilisateur ou mot de passe erroné..")
            return "Nom d'utilisateur ou mot de passe erroné.."
        except ldap.SERVER_DOWN:
            print("le serveur est en panne pour le moment, Veuillez réessayer!")
            return "le serveur est en panne pour le moment, Veuillez réessaye!"
        except ldap.LDAPError:
            ldap_client.unbind_s()
            print("Authentication error!")
            return "Authentication error!"

    def register(self, user):

        # domaine de base
        LDAP_BASE_DN = "cn=" + self.ldap_group + \
            ",ou=" + self.ldap_ou + ",dc=tek-up,dc=de"
        # home base
        HOME_BASE = "/home/users"

        # nouveau utilisateur rejoindre le domaine
        dn = 'cn=' + user['username'] + ',' + LDAP_BASE_DN
        home_dir = HOME_BASE + '/' + user['username']
        gid = user['group_id']

        # coder le mot de passe en utilisant hashlib
        hashed_pwd = hashlib.md5(user['password'].encode("UTF-8"))

        entry = []
        entry.extend([
            ('objectClass', [b'inetOrgPerson',
                             b'posixAccount', b'top']),
            ('uid', user['username'].encode("UTF-8")),
            ('givenname', user['username'].encode("UTF-8")),
            ('sn', user['username'].encode("UTF-8")),
            ('mail', user['email'].encode("UTF-8")),
            ('uidNumber', user['uid'].encode("UTF-8")),
            ('gidNumber', str(gid).encode("UTF-8")),
            ('loginShell', [b'/bin/sh']),
            ('homeDirectory', home_dir.encode("UTF-8")),
            ('userPassword', [b'{md5}' +
                              b64encode(hashed_pwd.digest())])

        ])

        # connect to host with admin
        ldap_conn = ldap.initialize(self.ldap_server)
        ldap_conn.simple_bind_s(self.LDAP_ADMIN_DN, self.LDAP_ADMIN_PWD)

        try:
            # add entry in the directory
            ldap_conn.add_s(dn, entry)
            print("succes")
            return None
        except Exception:
            return sys.exc_info()[0]

        finally:
            ldap_conn.unbind_s()

s = LdapService(admin_pwd="admin_motdepasse")

utilisateur = {
    'username': 'visit',
    'password': '1111',
    'email': 'gu@gmail.com',
    'gender': 'male',
}
