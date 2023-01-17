#application de chat messagerie

## About


## Learning objectives

When we've completed this Code Pattern, you will understand how to:

- **Objective 1**: configuration ldap server
- **Objective 2**: How to set up an authority server that accepts certification requests, creates them, then signs them in order to verify their state
- **Objective 3**: how to connect ldap with clients and generate certificate
## Flow


1- **Client side :**
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;. Register -> Enter credentials (first time)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;. Login / block authentication (redirect)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;. View all active users
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;. Select user-> chat area opened / Select room
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;. Using RSA technique  to encrypt/decrypt all messages sent between clients.
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;. See message date & time
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;. Disconnect && quit application

2- **Server side :**

- Register user : 
  <br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;. Add new user to the active directory via LDAP 
  <br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;. Create PKI -> get a x509 certificaton via authority server

- Login user :
  <br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;. Enter credentials -> verify user in the active directory via LDAP
  <br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;. Verify the signature via authority server
:


## caracteristiques:

- Save a log of the chat
- Clear the chat history
- Emoji button with various emojies to choose from and use
- Change your username
  - revert to default username
  - view your username history
  - clear your username history
- Style Customization
  - choose a custom font
  - choose from 6 different color themes
  - revert to default layout
- Select a default window size of program for everytime it opens
  - return to the default window size whenever

## Dependencies


- [pycryptodome][(https://github.com/LeminIkhalih/projet](https://github.com/LeminIkhalih/projet)): well-documented python library for encryption/decryption..
-(https://github.com/LeminIkhalih/projet)](https://github.com/LeminIkhalih/projet)): a python package that provides a high-level interface to the functions in the OpenSSL library such as X509 certs generation.
- [Tkinter](https://github.com/LeminIkhalih/projet): Standard Python interface to the Tk GUI toolkit.
- [cryptography](https://github.com/LeminIkhalih/projet): python library for X509 certs with good API
- [OpenLDAP](https://github.com/LeminIkhalih/projet): is an implementation under ubuntu for LDAP protocol
- [Pika](https://github.com/LeminIkhalih/projet): Rabbitmq python client.


## Setup

You have multiple options to setup your own instance:

- [Run it locally](#run-locally)

### 1. Open LDAP server in your machine

Clone the `LeminIkhalih/projet` repository locally. In a terminal, run:

```bash
$ git clone https://github.com//LeminIkhalih/projet.git
```



**Installation**

```bash
# install node modules for the API
$pip install pycrytodome
$pip install cryptography
$pip install python-ldap
$pip install pyopenssl
```

ce projet a fait par lemin et oumar
