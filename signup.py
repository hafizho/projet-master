from tkinter import Label, Entry, Button, Tk, Radiobutton, IntVar, StringVar, Toplevel, Canvas
from ldap_server import LdapService
from AC.client_AC import CaClient, handle_cert_local
from chat import *
import time


class SignupPage:

    def Register(self, event=None):
        if self.USERNAME.get() == "" or self.PASSWORD.get() == "" or self.EMAIL.get() == "" or self.UID.get() == "":
            self.error_label.config(
                text="merci de remplir le champ obligatoire!", fg="#0F0F0F", bg="#33FF33")

        else:
            #user_obj = {
            utilisateur = {
                'username': self.USERNAME.get(),
                'password': self.PASSWORD.get(),
                'email': self.EMAIL.get(),
                'gender': self.GENDER.get(),
                'group_id': 500,  
                'uid': self.UID.get()
            }
            print(utilisateur)
          
            ldap_s = LdapService(admin_pwd="admin_motdepasse")
            result = ldap_s.register(utilisateur)

            if not result:
              

                self.error_label.config(
                    text="Sucess", fg="#33FF33", bg="#336633")

                time.sleep(1)

                client = CaClient(self.USERNAME)
                client.connect()
                client.request_cert()
                result = handle_cert_local('AC/client_cert.pem')
                if result:
                    self.HomeWindow()
                else:
                    self.error_label.config(
                        text="Une erreur s'est produite lors de l'obtention du certificat SSL", fg="#0F0F0F", bg="#33FF33")

            else:
                self.error_label.config(
                    text=result, fg="#0F0F0F", bg="#33FF33")

    def HomeWindow(self):
        username = self.USERNAME.get()
        self.root.withdraw()
        c = Chatroom()
        c.run(user=username)

    def navigate_to_login(self):
        self.root.withdraw()
        from login import LoginPage
        l = LoginPage()
        l.main()

    def main(self):
        # main frame
        self.root = Tk()
        self.root.geometry('700x640')
        self.root.title("Formulaire d'inscription")

        # data binding
        self.USERNAME = StringVar(self.root)
        self.EMAIL = StringVar(self.root)
        self.PASSWORD = StringVar(self.root)
        self.GENDER = StringVar(self.root)
        self.UID = StringVar(self.root)

        # Formulaire d'inscription
        label_0 = Label(self.root, text="Formulaire d'inscription",
                        width=20, font=("bold", 20))
        label_0.place(x=90, y=53)

        label_1 = Label(self.root, text="nom d'utilisateur *",
                        width=20, font=("bold", 10))
        label_1.place(x=80, y=130)
        entry_1 = Entry(self.root, textvariable=self.USERNAME)
        entry_1.place(x=240, y=130)

        label_2 = Label(self.root, text="Email *",
                        width=20, font=("bold", 10))
        label_2.place(x=68, y=180)
        entry_2 = Entry(self.root, textvariable=self.EMAIL)
        entry_2.place(x=240, y=180)

        label_2_ = Label(self.root, text="mot de passe *",
                         width=20, font=("bold", 10))
        label_2_.place(x=68, y=230)
        entry_2_ = Entry(self.root, textvariable=self.PASSWORD, show="*")
        entry_2_.place(x=240, y=230)

        # self.GENDER label & box radio
        label_3 = Label(self.root, text="Sexe",
                        width=20, font=("bold", 10))
        label_3.place(x=70, y=280)

        optionMale = Radiobutton(self.root, text="Male", padx=5, variable=self.GENDER,
                                 value=1)
        optionMale.place(x=235, y=280)
        optionFemale = Radiobutton(self.root, text="Femelle", padx=20,
                                   variable=self.GENDER, value=2)
        optionFemale.place(x=290, y=280)

        # Age de lable entree
        label_4 = Label(self.root, text="id_etudiant *",
                        width=20, font=("bold", 10))
        label_4.place(x=70, y=330)
        entry_3 = Entry(self.root, textvariable=self.UID)
        entry_3.place(x=240, y=330)

        # Erreur label
        self.error_label = Label(self.root, width=60, font=("bold", 8))
        self.error_label.place(x=65, y=370)

        # valider le boutton
        btn = Button(self.root, text='Valider', width=20, command=self.Register, bg='brown',
                     fg='white')
        btn.place(x=180, y=400)

        #Boutton de login
        btn_2 = Button(self.root, text='connexion', width=10, command=self.navigate_to_login, bg='#0000FF',#0F0F0F
                       fg='#000080', borderwidth=0, font="Verdana 10 underline")
        btn_2.place(x=350, y=400)

        #couleur
        self.root.config(bg="#0F0F0F") 
        label_0.config(bg="#0F0F0F", fg="#0000FF")
        label_1.config(bg="#0F0F0F", fg="#0000FF")
        label_2.config(bg="#0F0F0F", fg="#0000FF")
        label_2_.config(bg="#0F0F0F", fg="#0000FF")
        label_3.config(bg="#0F0F0F", fg="#0000FF")
        label_4.config(bg="#0F0F0F", fg="#0000FF")
        entry_1.config(bg="#0F0F0F", fg="#0000FF", insertbackground="#0000FF")
        entry_3.config(bg="#0F0F0F", fg="#0000FF", insertbackground="#0000FF")
        entry_2.config(bg="#0F0F0F", fg="#0000FF", insertbackground="#0000FF")
        entry_2_.config(bg="#0F0F0F", fg="#0000FF", insertbackground="#0000FF")
        optionFemale.config(bg="#0F0F0F", fg="#0000FF")
        optionMale.config(bg="#0F0F0F", fg="#0000FF")
        btn.config(bg="#0F0F0F", fg="#FFFFFF",
                   activebackground="#0F0F0F", activeforeground="#FFFFFF")
        self.error_label.config(bg="#0F0F0F")

        self.root.mainloop()
        print("formulaire d'inscription créé avec Succes...")


 #s = SignupPage()
 #s.main()
