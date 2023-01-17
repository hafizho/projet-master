from tkinter import Label, Entry, Button, Tk, Radiobutton, IntVar, StringVar, Toplevel, Canvas, X
from ldap_server import LdapService
from AC.client_AC import CaClient, handle_cert_local
from chat import *

import time


class LoginPage:
  #J'ai changé de sa ...
    root = Tk()
    root.geometry('500x300')
    root.title("Formulaire de connexion")

    entry_1 = Entry(root)
    entry_2 = Entry(root, show="*")
    # à sa

    def Login(self, event=None):
        print(self.entry_1)

        #if self.USERNAME.get() == "" or self.PASSWORD.get() == "":
        if self.entry_1.get() == "" or self.entry_2.get() == "":
            self.error_label.config(
                text="SVP completer les champs!", fg="#0000FF", bg="#000080") #33FF33
        else:
        #    print(self.USERNANE.get())
        #    print(self.PASSWORD.get())
           ldap_s = LdapService(admin_pwd="admin_motdepasse")
           result = ldap_s.login(username=self.entry_1.get(),
                                  password=self.entry_2.get())
           if not result:
                client = CaClient(self.USERNAME)
                client.connect()
                client.verify_cert()

                if client.cert_is_ok == "Ok":
                    self.HomeWindow()
                else:
                    self.error_label.config(
                        text="Accès refusé -- Pirate Alert --", fg="#0000FF", bg="#000080")

           else:
                self.error_label.config(
                    text=result, fg="#0000FF", bg="#000080") 

    def HomeWindow(self):
        username = self.USERNAME.get()
        self.root.withdraw()
        c = Chatroom()
        c.run(user=username)

    def navigate_to_signup(self):
        from signup import SignupPage
        self.root.withdraw()
        s = SignupPage()
        s.main()

    def main(self):
        # main frame
        #self.root = Tk()
        #self.root.geometry('600x500')
        #self.root.title("Formulaire de connection")

        # combinaison des donnes
        #self.USERNAME = StringVar(self.root)
        #self.PASSWORD = StringVar(self.root)

        # Formulaire de connection
        label_0 = Label(self.root, text="connexion", width=20, font=("bold", 20))
        label_0.place(x=90, y=30)

        # subtitle text
        sub_label = Label(self.root, text="Commencer le chat!",
                          width=45, font=("bold", 12))
        sub_label.place(x=45, y=65)

        # donnes de nom d'utilisateur
        label_1 = Label(self.root, text="Nom d'utilisateur*",
                        width=20, font=("bold", 10))
        label_1.place(x=80, y=130)
        #self.entry_1 = Entry(self.root, textvariable=self.USERNAME)
        self.entry_1.place(x=240, y=130)
             
        #mot de passe
        label_2 = Label(self.root, text="mot de passe *",
                        width=20, font=("bold", 10))
        label_2.place(x=68, y=180)
        #self.entry_2 = Entry(self.root, textvariable=self.PASSWORD, show="*")
        self.entry_2.place(x=240, y=180)

        # boutton de valdation
        btn = Button(self.root, text='valider', width=20, bg='brown',
                     fg='white', command=self.Login)
        btn.place(x=180, y=250)
        btn.bind('<Return>', self.Login)

        # Register button
        btn_2 = Button(self.root, text='S\'inscrire', width=10, command=self.navigate_to_signup, bg='#0000FF',
                       fg='#000080', borderwidth=0, font="Verdana 10 underline")
        btn_2.place(x=350, y=250)

        # erreur au niveau de saisie
        self.error_label = Label(self.root, width=60, font=("bold", 8))
        self.error_label.place(x=65, y=220)

        # theme de couleur
        self.root.config(bg="#0F0F0F")
        label_0.config(bg="#0F0F0F", fg="#0000FF")
        label_1.config(bg="#0F0F0F", fg="#0000FF")
        sub_label.config(bg="#225522", fg="#0000FF")
        label_2.config(bg="#0F0F0F", fg="#0000FF")
        self.entry_1.config(bg="#0F0F0F", fg="#0000FF", insertbackground="#0000FF")
        self.entry_2.config(bg="#0F0F0F", fg="#0000FF", insertbackground="#0000FF")
        btn.config(bg="#0F0F0F", fg="#FFFFFF",
                   activebackground="#0F0F0F", activeforeground="#FFFFFF")
        self.error_label.config(bg="#0F0F0F")

        # utiliser pour afficher le fenetre de connection
        self.root.resizable(200, 120)
        self.root.mainloop()
        print("Login à créér avec succes...")


l = LoginPage()
l.main()
