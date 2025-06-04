from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import requests
import re
import json
import hashlib
import pygame
import os
import asyncio
from functools import partial
import threading
from itertools import combinations
import time



# Stayl
# Stili per il pulsante
bottone = """
    QPushButton {
        color: #FFFFFF; 
        font: 30pt Arial Black;
        background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #F6F84B, stop:1 #F07A39);
        border-radius: 20px;
        padding: 10px 20px;
        margin-top: 30px;
    }
    
    QPushButton:hover {
        background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #D4D629, stop:1 #DE5827);
    }
    
    QPushButton:pressed {
        background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #B2B408, stop:1 #BC3605);
    }
"""
testo="""
    font: 30px Arial;
    color: white;
    padding: 5px;
"""
verde="""
    font: 30px Arial;
    color: #8EFA00;
    padding: 5px;
"""
giallo="""
    font: 30px Arial;
    color: #FFFB00;
    padding: 5px;
"""
rosso="""
    font: 30px Arial;
    color: #FF2600;
    padding: 5px;
"""
textinput="""
    font: 30pt Arial;
    color: #64B4FF; /* colore del testo */
    border: 2px solid #4298EF; /* bordo grigio con spessore 2px */
    border-radius: 5px; /* angoli arrotondati */
    background-color: #0076BA;
    padding: 5px; /* spazio interno */
    selection-color: #fff; /* colore del testo selezionato */
    selection-background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #F6F84B, stop:1 #F07A39); /* sfumatura di colore per il testo selezionato */
"""
codice="""
    font: 60pt Arial;
    color: #64B4FF; /* colore del testo */
    border: 3px solid #4298EF; /* bordo grigio con spessore 2px */
    border-radius: 20px; /* angoli arrotondati */
    background-color: #0076BA;
    width: 20px; /* spazio interno */
    height: 30px;
    selection-color: #fff; /* colore del testo selezionato */
    selection-background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #F6F84B, stop:1 #F07A39); /* sfumatura di colore per il testo selezionato */
"""
titolo = """
    font: 70px Arial Black;
    color: #64B4FF;
    padding: 5px;
"""
account_settings = """
    QPushButton {
        border: none;
        background-image: url('Gioco di Scopa/Icone/account_resized.png');
        background-position: center; /* Imposta la posizione dell'immagine al centro */
        background-repeat: no-repeat;
        background-origin: content;
        width: 100px;
        height: 100px;
    }
    
    QPushButton:hover {
        background-image: url('Gioco di Scopa/Icone/account_hover_resized.png');
    }
    
    QPushButton:pressed {
        background-image: url('Gioco di Scopa/Icone/account_press_resized.png');
    }
"""
settings = """
    QPushButton {
        border: none;
        background-image: url('Gioco di Scopa/Icone/impostazioni_resized.png');
        background-position: center; /* Imposta la posizione dell'immagine al centro */
        background-repeat: no-repeat;
        background-origin: content;
        width: 100px;
        height: 100px;
    }
    
    QPushButton:hover {
        background-image: url('Gioco di Scopa/Icone/impostazioni_hover_resized.png');
    }
    
    QPushButton:pressed {
        background-image: url('Gioco di Scopa/Icone/impostazioni_press_resized.png');
    }
"""
play = """
    QPushButton {
        border: none;
        background-image: url('Gioco di Scopa/Icone/play_resized.png');
        background-position: center; /* Imposta la posizione dell'immagine al centro */
        background-repeat: no-repeat;
        background-origin: content;
        width: 100px;
        height: 100px;
    }
    
    QPushButton:hover {
        background-image: url('Gioco di Scopa/Icone/play_hover_resized.png');
    }
    
    QPushButton:pressed {
        background-image: url('Gioco di Scopa/Icone/play_press_resized.png');
    }
"""
home = """
    QPushButton {
        border: none;
        background-image: url('Gioco di Scopa/Icone/home_resized.png');
        background-position: center; /* Imposta la posizione dell'immagine al centro */
        background-repeat: no-repeat;
        background-origin: content;
        width: 100px;
        height: 100px;
    }
    
    QPushButton:hover {
        background-image: url('Gioco di Scopa/Icone/home_hover_resized.png');
    }
    
    QPushButton:pressed {
        background-image: url('Gioco di Scopa/Icone/home_press_resized.png');
    }
"""
info = """
    QPushButton {
        border: none;
        background-image: url('Gioco di Scopa/Icone/info_resized.png');
        background-position: center; /* Imposta la posizione dell'immagine al centro */
        background-repeat: no-repeat;
        background-origin: content;
        width: 100px;
        height: 100px;
    }
    
    QPushButton:hover {
        background-image: url('Gioco di Scopa/Icone/info_hover_resized.png');
    }
    
    QPushButton:pressed {
        background-image: url('Gioco di Scopa/Icone/info_press_resized.png');
    }
"""
d = """
    QPushButton {
        border: none;
        background-image: url('Gioco di Scopa/Icone/d_resized.png');
        background-position: center; /* Imposta la posizione dell'immagine al centro */
        background-repeat: no-repeat;
        background-origin: content;
        width: 100px;
        height: 100px;
    }
    
    QPushButton:hover {
        background-image: url('Gioco di Scopa/Icone/d_hover_resized.png');
    }
    
    QPushButton:pressed {
        background-image: url('Gioco di Scopa/Icone/d_press_resized.png');
    }
"""
slider_style = """
QSlider::groove:horizontal {
    border: 5px solid #4298EF;
    border-radius: 14px;
    height: 40px;
    width: 530px;
    background: #64B4FF;
}

QSlider::handle:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #F6F84B, stop:1 #F07A39);
    width: 40px;
    height: 40px;
    border-radius: 13px;
    border: 2px solid rgba(0, 0, 0, 0);
    margin: -2px -2px;
}
"""
titoloo = """
    background-color: none;
    font: 40px Arial Black;
    color: #85E7BB;
    padding: 5px;
"""
testoo ="""
    background-color: none;
    font: 20px Arial;
    color: #85E7BB;
    padding: 5px;
"""

# suoni
class MusicManager:
    def __init__(self):
        pygame.init()
        try:
            with open('Gioco di Scopa/dati.json', 'r') as file:
                # Carica i dati dal file JSON in un dizionario
                musica = json.load(file)['musica']
        except (FileNotFoundError, KeyError):
            musica = 50
        self.background_music = pygame.mixer.Sound("Gioco di Scopa/musica/low.mp3")
        self.background_volume = musica/100  # Volume iniziale del suono di background

    def play_background_music(self):
        self.background_music.set_volume(self.background_volume)
        self.background_music.play(loops=-1)

    def set_background_volume(self, volume):
        self.background_volume = volume / 100.0
        self.background_music.set_volume(self.background_volume)

class SoundManager:
    def __init__(self):
        pygame.init()
        try:
            with open('Gioco di Scopa/dati.json', 'r') as file:
                # Carica i dati dal file JSON in un dizionario
                suono = json.load(file)['suono']
        except (FileNotFoundError, KeyError):
            suono = 50
        self.click_sound = pygame.mixer.Sound("Gioco di Scopa/musica/click.mp3")
        self.click_volume = suono/100 # Volume iniziale del suono di background

    def play_click_sound(self):
        self.click_sound.set_volume(self.click_volume)
        self.click_sound.play()

    def set_click_volume(self, volume):
        self.click_volume = volume / 100.0
        self.click_sound.set_volume(self.click_volume)



# Definizione di una classe generica per le pagine dell'applicazione
class Page(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        if not self.layout():
            self.layout = QVBoxLayout(self)


# 0 Classe per la pagina di login, eredita dalla classe Page
class LoginPage(Page):
    def __init__(self, stacked_layout, sound_manager, parent=None):
        super().__init__(parent)
        self.stacked_layout = stacked_layout
        self.sound_manager = sound_manager

        # Aggiungi un'immagine di accesso
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.pixmap = QPixmap("Gioco di Scopa/Icone/accedi.png")
        self.image_label.setPixmap(self.pixmap.scaledToHeight(60))
        self.layout.addWidget(self.image_label)



        # Aggiungi etichette e campi di inserimento per l'utente, l'email e la password
        self.user_name_label = QLabel("Inserisci l'User Name:")
        self.layout.addWidget(self.user_name_label)
        self.user_name_label.setStyleSheet(testo)
        self.user_name_entry = QLineEdit()
        self.user_name_entry.setStyleSheet(textinput)
        self.layout.addWidget(self.user_name_entry)

        self.email_label = QLabel("Inserisci l'Email:")
        self.layout.addWidget(self.email_label)
        self.email_label.setStyleSheet(testo)
        self.email_entry = QLineEdit()
        self.email_entry.setStyleSheet(textinput)
        self.layout.addWidget(self.email_entry)

        self.password_label = QLabel("Inserisci la Password:")
        self.password_label.setStyleSheet(testo)
        self.layout.addWidget(self.password_label)
        self.password_entry = QLineEdit()
        self.password_entry.setStyleSheet(textinput)
        # Imposta lo stile per nascondere i caratteri della password
        self.password_entry.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.password_entry)

        # Crea un layout orizzontale per organizzare i bottoni affiancati
        self.button_layout = QHBoxLayout()

        # Aggiungi pulsanti per accedere e registrarsi
        self.access_button = QPushButton("Accedi")
        self.access_button.setStyleSheet(bottone)
        self.access_button.clicked.connect(self.access)
        self.button_layout.addWidget(self.access_button)

        self.register_button = QPushButton("Registrati")
        self.register_button.setStyleSheet(bottone)
        self.register_button.clicked.connect(self.register)
        self.button_layout.addWidget(self.register_button)

        # Aggiungi il layout orizzontale al layout principale
        self.layout.addLayout(self.button_layout)

        # Aggiungi una label per visualizzare eventuali risultati o messaggi
        self.result_label = QLabel("")
        self.result_label.setStyleSheet(testo)
        self.layout.addWidget(self.result_label)

    # Funzione per verificare se una stringa è un'email valida
    def is_valid_email(self, email):
        if email:
            # Definisci un'espressione regolare per la validazione dell'email
            regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            # Verifica se l'email corrisponde all'espressione regolare
            return re.match(regex, email) is not None
        else:
            return True

    def access(self):
        self.sound_manager.play_click_sound()
        credenziali_corrette = False
        # Ottieni i dati inseriti dall'utente
        user_name = self.user_name_entry.text()
        email = self.email_entry.text()
        pwd = self.password_entry.text()
        password = hashlib.md5(pwd.encode()).hexdigest()

        # Verifica se l'email è valida
        if not self.is_valid_email(email):
            self.result_label.setText("Inserisci un'email valida")
            return

        # Dati da inviare al server
        data_to_send = {
            'user_name': user_name,  # Chiave corretta per l'utente
            'email': email,          # Indirizzo email
            'password': password     # Password
        }

        try:
            # Invia i dati al server tramite una richiesta POST
            response = requests.post('http://localhost:8080/access', data=data_to_send)
            # Verifica lo stato della risposta
            if response.status_code == 200:
                # Se la richiesta ha avuto successo, visualizza il messaggio di risposta dal server
                self.result_label.setText(response.json()['message'])
                credenziali_corrette = response.json()['accesso_effettuato']
                if credenziali_corrette:
                    self.stacked_layout.setCurrentIndex(1)  # Mostra la pagina di verifica
                    with open('Gioco di Scopa/dati.json', 'r') as file:
                        dati = json.load(file)

                    # Aggiorna o aggiungi il dato desiderato
                    dati['user_name'] = user_name
                    dati['email'] = email
                    dati['password'] = password

                    # Scrivi la struttura dati aggiornata nel file JSON
                    with open('Gioco di Scopa/dati.json', 'w') as file:
                        json.dump(dati, file)
            else:
                # Se c'è stato un errore nella richiesta, visualizza un messaggio di errore generico
                self.result_label.setText('Errore durante la richiesta al server')
        except requests.exceptions.ConnectionError:
            # Se non è possibile connettersi al server, visualizza un messaggio di errore
            self.result_label.setText('Errore durante la connessione al server')

    def register(self):
        self.sound_manager.play_click_sound()
        credenziali_corrette = False
        # Ottieni i dati inseriti dall'utente
        user_name = self.user_name_entry.text()
        email = self.email_entry.text()
        pwd = self.password_entry.text()
        password = hashlib.md5(pwd.encode()).hexdigest()

        # Verifica se l'email è valida
        if not self.is_valid_email(email):
            self.result_label.setText("Inserisci un'email valida")
            return

        # Dati da inviare al server
        data_to_send = {
            'user_name': user_name,  # Chiave corretta per l'utente
            'email': email,          # Indirizzo email
            'password': password     # Password
        }

        try:
            # Invia i dati al server tramite una richiesta POST
            response = requests.post('http://localhost:8080/register', data=data_to_send)
            # Verifica lo stato della risposta
            if response.status_code == 200:
                # Se la richiesta ha avuto successo, visualizza il messaggio di risposta dal server
                self.result_label.setText(response.json()['message'])
                credenziali_corrette = response.json()['accesso_effettuato']
                if credenziali_corrette:
                    self.stacked_layout.setCurrentIndex(1)  # Mostra la pagina di verifica
                    with open('Gioco di Scopa/dati.json', 'r') as file:
                        dati = json.load(file)

                    # Aggiorna o aggiungi il dato desiderato
                    dati['user_name'] = user_name
                    dati['email'] = email
                    dati['password'] = password

                    # Scrivi la struttura dati aggiornata nel file JSON
                    with open('Gioco di Scopa/dati.json', 'w') as file:
                        json.dump(dati, file)
            else:
                # Se c'è stato un errore nella richiesta, visualizza un messaggio di errore generico
                self.result_label.setText('Errore durante la richiesta al server')
        except requests.exceptions.ConnectionError:
            # Se non è possibile connettersi al server, visualizza un messaggio di errore
            self.result_label.setText('Errore durante la connessione al server')

# 1 Classe per la pagina di Verifica del codice di verifica, eredita dalla classe Page
class VerificationPage(Page):
    def __init__(self, stacked_layout, sound_manager, account_page, impostazioni_page, parent=None):
        super().__init__(parent)
        self.stacked_layout = stacked_layout
        self.sound_manager = sound_manager
        self.account_page = account_page
        self.impostazioni_page = impostazioni_page

        # Bottone per le impostazioni 
        self.d_button = QPushButton()
        self.d_button.setStyleSheet(d)
        self.d_button.setFixedSize(50, 80)
        self.d_button.clicked.connect(self.torna_al_login)

        # Aggiungi un'immagine di accesso
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.pixmap = QPixmap("Gioco di Scopa/Icone/accedi.png")
        self.image_label.setPixmap(self.pixmap.scaledToHeight(80))

        # Aggiungi spazio
        self.spazio_label = QLabel(" ")
        self.spazio_label.setStyleSheet(testo)

        # Creazione di un layout orizzontale per gli elementi
        d_button_layout = QHBoxLayout()
        d_button_layout.addWidget(self.d_button)
        d_button_layout.setAlignment(Qt.AlignLeft)

        d_button_layout_top = QHBoxLayout()
        d_button_layout_top.addLayout(d_button_layout)
        d_button_layout_top.setAlignment(Qt.AlignTop)

        # Creazione di un layout orizzontale per gli elementi
        image_label_layout = QHBoxLayout()
        image_label_layout.addWidget(self.image_label)
        image_label_layout.setAlignment(Qt.AlignCenter)

        # Creazione di un layout orizzontale per gli elementi
        top_buttons_layout = QHBoxLayout()
        top_buttons_layout.addLayout(d_button_layout_top)
        top_buttons_layout.addLayout(image_label_layout)
        top_buttons_layout.addWidget(self.spazio_label)
        top_buttons_layout.setAlignment(Qt.AlignTop)
        self.layout.addLayout(top_buttons_layout)

        # Etichetta per spiegare lo scopo della casella di input
        self.codice_label = QLabel("Inserisci il Codice di Verifica:")
        self.codice_label.setStyleSheet(testo)
        self.layout.addWidget(self.codice_label)

        # Layout orizzontale per contenere le caselle di input
        self.input_layout = QHBoxLayout()

        # Lista per memorizzare le caselle di input
        self.input_boxes = []

        self.spazio = QLabel(" ")
        self.spazio.setStyleSheet(testo)
        self.input_layout.addWidget(self.spazio)

        # Crea e aggiungi 6 QLineEdit al layout
        for i in range(6):
            input_box = QLineEdit()
            input_box.setMaxLength(1)  # Imposta la lunghezza massima a 1 carattere
            input_box.setValidator(QIntValidator())  # Accetta solo numeri interi
            input_box.setStyleSheet(codice)  # Imposta la dimensione del testo
            input_box.setAlignment(Qt.AlignCenter)  # Centra il testo nella casella di input
            input_box.setFixedWidth(80)  # Imposta la larghezza fissa della casella di input
            input_box.setFixedHeight(110)  # Imposta l'altezza fissa della casella di input
            input_box.textChanged.connect(self.on_text_changed)  # Connessione al metodo on_text_changed
            self.input_layout.addWidget(input_box)
            self.input_boxes.append(input_box)
            if i == 2:
                self.spazio = QLabel(" ")
                self.spazio.setStyleSheet(testo)
                self.input_layout.addWidget(self.spazio)

            self.spazio = QLabel(" ")
            self.spazio.setStyleSheet(testo)
            self.input_layout.addWidget(self.spazio)

        # Aggiungi il layout delle caselle di input al layout principale
        self.layout.addLayout(self.input_layout)


        # Pulsante per inviare il codice di verifica
        self.invia_button = QPushButton("Invia")
        self.invia_button.setStyleSheet(bottone)
        self.layout.addWidget(self.invia_button)
        self.invia_button.clicked.connect(self.invia_codice)

        # Etichetta per spiegare lo scopo della casella di input
        self.result_label = QLabel("")
        self.result_label.setStyleSheet(testo)
        self.layout.addWidget(self.result_label)

    # Metodo chiamato quando il testo di una casella di input cambia
    def on_text_changed(self):
        # Ottieni la casella di input corrente
        current_box = self.sender()

        # Ottieni l'indice della casella di input corrente
        index = self.input_boxes.index(current_box)

        # Se il testo nella casella di input corrente è stato inserito e la casella di input non è l'ultima
        if current_box.text() and index < len(self.input_boxes) - 1:
            # Sposta il focus alla casella di input successiva
            self.input_boxes[index + 1].setFocus()
            
    # Metodo per gestire l'invio del codice di verifica
    def invia_codice(self):
        self.sound_manager.play_click_sound()
        codice_corretto = False
        # Ottieni i dati inseriti dall'utente
        codice = ''.join(input_box.text() for input_box in self.input_boxes)

        with open('Gioco di Scopa/dati.json', 'r') as file:
            # Carica i dati dal file JSON
            dati = json.load(file)
            # Preleva il valore corrispondente all'indice specificato
            valori = list(dati.values())
            email=valori[1]

        # Dati da inviare al server
        data_to_send = {
            'codice': str(codice),  # Chiave corretta per l'utente
            'email':email
        }

        try:
            # Invia i dati al server tramite una richiesta POST
            response = requests.post('http://localhost:8080/verifica_codice', data=data_to_send)
            # Verifica lo stato della risposta
            if response.status_code == 200:
                # Se la richiesta ha avuto successo, visualizza il messaggio di risposta dal server
                self.result_label.setText(response.json()['message'])
                codice_corretto = response.json()['codice_corretto']
                if codice_corretto:
                    self.account_page.nomee()
                    self.account_page.vittoriee()
                    self.account_page.sconfittee()
                    self.account_page.percentualee()
                    self.impostazioni_page.on_musica_volume_changed(50)
                    self.impostazioni_page.on_tasti_suono_changed(50)
                    self.impostazioni_page.get_vittorie()
                    self.stacked_layout.setCurrentIndex(2)  # Mostra la pagina di verifica
                    # Elimina il veccio file
                    if os.path.exists('Gioco di Scopa/dati2.json'):
                        os.remove('Gioco di Scopa/dati2.json')
            else:
                # Se c'è stato un errore nella richiesta, visualizza un messaggio di errore generico
                self.result_label.setText('Errore durante la richiesta al server')
        except requests.exceptions.ConnectionError:
            # Se non è possibile connettersi al server, visualizza un messaggio di errore
            self.result_label.setText('Errore durante la connessione al server')

    def torna_al_login(self):
        self.sound_manager.play_click_sound()
        self.stacked_layout.setCurrentIndex(0)

# 2 Classe per la pagina della Home, eredita dalla classe Page
class HomePage(Page):
    def __init__(self, stacked_layout, sound_manager, parent=None):
        super().__init__(parent)
        self.stacked_layout = stacked_layout
        self.sound_manager = sound_manager

        # Bottone per le impostazioni dell'account
        self.account_settings_button = QPushButton()
        self.account_settings_button.setStyleSheet(account_settings)
        self.account_settings_button.setFixedSize(100, 100)
        self.account_settings_button.clicked.connect(self.open_account_settings)

        # Immagine centrale grande
        self.game_image_label = QLabel()
        self.game_image_label.setPixmap(QPixmap("Gioco di Scopa/Icone/logo.png").scaledToHeight(400))

        # Bottone per le impostazioni generali
        self.settings_button = QPushButton()
        self.settings_button.setStyleSheet(settings)
        self.settings_button.setFixedSize(100, 100)
        self.settings_button.clicked.connect(self.open_general_settings)

        # Bottone per avviare il gioco
        self.play_button = QPushButton()
        self.play_button.setStyleSheet(play)
        self.play_button.setFixedSize(120, 120)
        self.play_button.clicked.connect(self.start_game)

        # Aggiungi spazio
        self.spazio_label = QLabel(" ")
        self.spazio_label.setStyleSheet(testo)


        # Creazione di un layout orizzontale per i primi tre elementi
        account_settings_button_layout = QHBoxLayout()
        account_settings_button_layout.addWidget(self.account_settings_button)
        account_settings_button_layout.setAlignment(Qt.AlignLeft)

        account_settings_button_layout_top = QHBoxLayout()
        account_settings_button_layout_top.addLayout(account_settings_button_layout)
        account_settings_button_layout_top.setAlignment(Qt.AlignTop)


        game_image_label_layout = QHBoxLayout()
        game_image_label_layout.addWidget(self.game_image_label)
        game_image_label_layout.setAlignment(Qt.AlignCenter)


        settings_button_layout = QHBoxLayout()
        settings_button_layout.addWidget(self.settings_button)
        settings_button_layout.setAlignment(Qt.AlignRight)

        settings_button_layout_top = QHBoxLayout()
        settings_button_layout_top.addLayout(settings_button_layout)
        settings_button_layout_top.setAlignment(Qt.AlignTop)

        # Creazione di un layout orizzontale per i primi tre elementi
        top_buttons_layout = QHBoxLayout()
        top_buttons_layout.addLayout(account_settings_button_layout_top)
        top_buttons_layout.addLayout(settings_button_layout_top)
        top_buttons_layout.setAlignment(Qt.AlignTop)

        # Creazione di un layout verticale per il pulsante play
        play_button_layout = QVBoxLayout()
        play_button_layout.addWidget(self.play_button)
        play_button_layout.setAlignment(Qt.AlignCenter)

        top_buttons_layout2 = QVBoxLayout()
        top_buttons_layout2.addLayout(top_buttons_layout)
        top_buttons_layout2.addWidget(self.spazio_label)
        top_buttons_layout2.addWidget(self.spazio_label)
        top_buttons_layout2.addLayout(game_image_label_layout)
        top_buttons_layout2.addWidget(self.spazio_label)
        top_buttons_layout2.addLayout(play_button_layout)
        top_buttons_layout2.setAlignment(Qt.AlignTop)

        # Aggiunta dei layout al layout verticale principale
        self.layout.addLayout(top_buttons_layout2)
        


    def open_account_settings(self):
        self.sound_manager.play_click_sound()
        self.stacked_layout.setCurrentIndex(3)

    def open_general_settings(self):
        self.sound_manager.play_click_sound()
        self.stacked_layout.setCurrentIndex(4)

    def start_game(self):
        self.sound_manager.play_click_sound()
        self.stacked_layout.setCurrentIndex(5)

# 3 Classe per la pagina del'Account, eredita dalla classe Page
class AccountPage(Page):
    def __init__(self, stacked_layout, sound_manager, parent=None):
        super().__init__(parent)
        self.stacked_layout = stacked_layout
        self.sound_manager = sound_manager

        # Bottone per le impostazioni dell'account
        self.home_button = QPushButton()
        self.home_button.setStyleSheet(home)
        self.home_button.setFixedSize(100, 100)
        self.home_button.clicked.connect(self.torna_alla_home)

        # Aggiungi un'immagine di accesso
        self.account_image_label = QLabel()
        self.pixmap = QPixmap("Gioco di Scopa/Icone/accounto.png")
        self.account_image_label.setPixmap(self.pixmap.scaledToHeight(70))
        self.account_image_label.setAlignment(Qt.AlignCenter)

        # Aggiungi spazio
        self.spazio_label = QLabel(" ")
        self.spazio_label.setStyleSheet(testo)

        # Aggiungi Nome
        self.nome_label = QLabel(f"Ciao {self.nome()}")
        self.nome_label.setStyleSheet(titolo)
        self.nome2_label = QLabel("Ecco le tue statistiche:")
        self.nome2_label.setStyleSheet(testo)

        # Aggiungi partite vinet
        self.vittoria_label = QLabel("Partite vinte:")
        self.vittoria_label.setStyleSheet(testo)
        self.vittorie_label = QLabel(f"{self.vittorie()}")
        self.vittorie_label.setStyleSheet(verde)

        # Aggiungi partite perse
        self.sconfitta_label = QLabel("Partite perse:")
        self.sconfitta_label.setStyleSheet(testo)
        self.sconfitte_label = QLabel(f"{self.sconfitte()}")
        self.sconfitte_label.setStyleSheet(rosso)

        # Aggiungi percentuale di successo
        self.percentual_label = QLabel("Percentuale di successo:")
        self.percentual_label.setStyleSheet(testo)
        self.percentuale_label = QLabel(f"{self.percentuale()}%")
        if self.percentuale() > 60:
            self.percentuale_label.setStyleSheet(verde)
        elif self.percentuale() < 40:
            self.percentuale_label.setStyleSheet(rosso)
        else:
            self.percentuale_label.setStyleSheet(giallo)

        # Pulsante per cambiare account
        self.log_out = QPushButton("Cambia account")
        self.log_out.setStyleSheet(bottone)
        self.log_out.clicked.connect(self.cambia_account)

        # Creazione di un layout orizzontale per gli elementi
        home_button_layout = QHBoxLayout()
        home_button_layout.addWidget(self.home_button)
        home_button_layout.setAlignment(Qt.AlignLeft)

        home_button_layout_top = QHBoxLayout()
        home_button_layout_top.addLayout(home_button_layout)
        home_button_layout_top.setAlignment(Qt.AlignTop)

        # Creazione di un layout orizzontale per gli elementi
        account_image_label_layout = QHBoxLayout()
        account_image_label_layout.addWidget(self.account_image_label)
        account_image_label_layout.setAlignment(Qt.AlignCenter)

        # Creazione di un layout orizzontale per gli elementi
        top_buttons_layout = QHBoxLayout()
        top_buttons_layout.addLayout(home_button_layout_top)
        top_buttons_layout.addLayout(account_image_label_layout)
        top_buttons_layout.addWidget(self.spazio_label)
        top_buttons_layout.setAlignment(Qt.AlignTop)

        # Creazione di un layout verticale per il pulsante play
        label_layout = QVBoxLayout()
        label_layout.addWidget(self.nome_label)
        label_layout.addWidget(self.nome2_label)
        label_layout.addWidget(self.vittoria_label)
        label_layout.addWidget(self.vittorie_label)
        label_layout.addWidget(self.sconfitta_label)
        label_layout.addWidget(self.sconfitte_label)
        label_layout.addWidget(self.percentual_label)
        label_layout.addWidget(self.percentuale_label)
        label_layout.addWidget(self.log_out)
        label_layout.setAlignment(Qt.AlignTop)


        # layout base
        layout_base = QVBoxLayout()
        layout_base.addLayout(top_buttons_layout)
        layout_base.addLayout(label_layout)
        layout_base.setAlignment(Qt.AlignTop)

        # Aggiunta dei layout al layout verticale principale
        self.layout.addLayout(layout_base)


    def torna_alla_home(self):
        self.sound_manager.play_click_sound()
        self.stacked_layout.setCurrentIndex(2)

    def cambia_account(self):
        self.sound_manager.play_click_sound()
        self.stacked_layout.setCurrentIndex(13)
        with open('Gioco di Scopa/dati.json', 'r') as file:
            dati = json.load(file)

        # Scrivi la struttura dati aggiornata nel file JSON
        with open('Gioco di Scopa/dati2.json', 'w') as file:
            json.dump(dati, file)

        # Aggiorna o aggiungi il dato desiderato
        dati['user_name'] = ''
        dati['email'] = ''
        dati['password'] = ''
        dati['musica'] = 50
        dati['suono'] = 50
        dati['stato'] = 1
        dati['Giocatori'] = 2
        dati['numero'] = 1
        dati['Punti_Vittoria'] = 11
        
        # Scrivi la struttura dati aggiornata nel file JSON
        with open('Gioco di Scopa/dati.json', 'w') as file:
            json.dump(dati, file)
 
    def vittorie(self):

        with open('Gioco di Scopa/dati.json', 'r') as file:
            # Carica i dati dal file JSON
            user_name = json.load(file)['user_name']

        if user_name =="":
            # Se non è possibile connettersi al server, visualizza un messaggio di errore
            with open('Gioco di Scopa/dati.json', 'r') as file:
                # Carica i dati dal file JSON in un dizionario
                ris = json.load(file)['vittorie']
        else:
            # Dati da inviare al server
            data_to_send = {
                'user_name':user_name
            }

            try:
                # Invia i dati al server tramite una richiesta POST
                response = requests.post('http://localhost:8080/vittorie', data=data_to_send)
                # Verifica lo stato della risposta
                if response.status_code == 200:
                    ris = response.json()['val'][0]
                    # Carica i dati dal file JSON in un dizionario
                    with open('Gioco di Scopa/dati.json', 'r') as file:
                        dati = json.load(file)

                    # Aggiorna o aggiungi il dato desiderato
                    dati['vittorie'] = ris

                    # Scrivi la struttura dati aggiornata nel file JSON
                    with open('Gioco di Scopa/dati.json', 'w') as file:
                        json.dump(dati, file)
                else:
                    # Se c'è stato un errore nella richiesta, visualizza un messaggio di errore generico
                    with open('Gioco di Scopa/dati.json', 'r') as file:
                        # Carica i dati dal file JSON in un dizionario
                        ris = json.load(file)['vittorie']
            except requests.exceptions.ConnectionError:
                # Se non è possibile connettersi al server, visualizza un messaggio di errore
                with open('Gioco di Scopa/dati.json', 'r') as file:
                    # Carica i dati dal file JSON in un dizionario
                    ris = json.load(file)['vittorie']
    
        return int(ris)
    
    def vittoriee(self):
        self.vittorie_label.setText(f"{self.vittorie()}")

    def sconfitte(self):

        with open('Gioco di Scopa/dati.json', 'r') as file:
            # Carica i dati dal file JSON
            user_name = json.load(file)['user_name']

        if user_name =="":
            # Se non è possibile connettersi al server, visualizza un messaggio di errore
            with open('Gioco di Scopa/dati.json', 'r') as file:
                # Carica i dati dal file JSON in un dizionario
                ris = json.load(file)['sconfitte']
        else:
            # Dati da inviare al server
            data_to_send = {
                'user_name':user_name
            }
            try:
                # Invia i dati al server tramite una richiesta POST
                response = requests.post('http://localhost:8080/sconfitte', data=data_to_send)
                # Verifica lo stato della risposta
                if response.status_code == 200:
                    ris = response.json()['val'][0]
                    # Carica i dati dal file JSON in un dizionario
                    with open('Gioco di Scopa/dati.json', 'r') as file:
                        dati = json.load(file)

                    # Aggiorna o aggiungi il dato desiderato
                    dati['sconfitte'] = ris

                    # Scrivi la struttura dati aggiornata nel file JSON
                    with open('Gioco di Scopa/dati.json', 'w') as file:
                        json.dump(dati, file)
                else:
                    # Se c'è stato un errore nella richiesta, visualizza un messaggio di errore generico
                    with open('Gioco di Scopa/dati.json', 'r') as file:
                        # Carica i dati dal file JSON in un dizionario
                        ris = json.load(file)['sconfitte']
            except requests.exceptions.ConnectionError:
                # Se non è possibile connettersi al server, visualizza un messaggio di errore
                with open('Gioco di Scopa/dati.json', 'r') as file:
                    # Carica i dati dal file JSON in un dizionario
                    ris = json.load(file)['sconfitte']
        
        return int(ris)
    
    def sconfittee(self):
        self.sconfitte_label.setText(f"{self.sconfitte()}")

    def nome(self):
        with open('Gioco di Scopa/dati.json', 'r') as file:
            # Carica i dati dal file JSON in un dizionario
            nome = json.load(file)['user_name']
        return nome
    
    def nomee(self):
        self.nome_label.setText(f"Ciao {self.nome()}")

    def percentuale(self):
        if self.vittorie()==0:
            ris=0
        else:
            numero = self.vittorie()/((self.vittorie()+self.sconfitte())/100)
            ris = round(numero, 2)
        return ris

    def percentualee(self):
        self.percentuale_label.setText(f"{self.percentuale()}%")

# 4 Classe per la pagina delle Impostazioni, eredita dalla classe Page
class ImpostazioniPage(Page):
    def __init__(self, stacked_layout, sound_manager, music_manager, parent=None):
        super().__init__(parent)
        self.stacked_layout = stacked_layout
        self.sound_manager = sound_manager
        self.music_manager = music_manager

        # Bottone per le impostazioni dell'account
        self.home_button = QPushButton()
        self.home_button.setStyleSheet(home)
        self.home_button.setFixedSize(100, 100)
        self.home_button.clicked.connect(self.torna_alla_home)

        # Aggiungi un'immagine di accesso
        self.account_image_label = QLabel()
        self.pixmap = QPixmap("Gioco di Scopa/Icone/impostazioe.png")
        self.account_image_label.setPixmap(self.pixmap.scaledToHeight(70))
        self.account_image_label.setAlignment(Qt.AlignCenter)

        # Aggiungi spazio
        self.spazio_label = QLabel(" ")
        self.spazio_label.setStyleSheet(testo)

        try:
            with open('Gioco di Scopa/dati.json', 'r') as file:
                # Carica i dati dal file JSON in un dizionario
                musica = json.load(file)['musica']
        except (FileNotFoundError, KeyError):
            musica = 50

        # Aggiungi musica
        self.musica_label = QLabel("Volume musica:")
        self.musica_label.setStyleSheet(testo)
        self.musica_volume_slider = QSlider(Qt.Horizontal)
        self.musica_volume_slider.setMinimum(0)
        self.musica_volume_slider.setMaximum(100)
        self.musica_volume_slider.setValue(musica)  # Valore predefinito
        self.musica_volume_slider.setFixedHeight(50)
        self.musica_volume_slider.valueChanged.connect(self.on_musica_volume_changed)
        self.musica_volume_slider.setStyleSheet(slider_style)

        try:
            with open('Gioco di Scopa/dati.json', 'r') as file:
                # Carica i dati dal file JSON in un dizionario
                suono = json.load(file)['suono']
        except (FileNotFoundError, KeyError):
            suono = 50

        # Aggiungi suoni
        self.suoni_label = QLabel("Volume suoni:")
        self.suoni_label.setStyleSheet(testo)
        self.tasti_suono_slider = QSlider(Qt.Horizontal)
        self.tasti_suono_slider.setMinimum(0)
        self.tasti_suono_slider.setMaximum(100)
        self.tasti_suono_slider.setValue(suono)  # Valore predefinito
        self.tasti_suono_slider.setFixedHeight(50)
        self.tasti_suono_slider.valueChanged.connect(self.on_tasti_suono_changed)
        self.tasti_suono_slider.setStyleSheet(slider_style)

        # Seleziona le vittorie
        self.vittorie_label = QLabel("Punti per la vittoria:")
        self.vittorie_label.setStyleSheet(testo)
        
        # Seleziona i punti necessari alla vittoria
        self.button1 = QPushButton('11', self)
        self.button1.setFixedSize(75, 75)
        self.button1.setCheckable(True)
        self.button1.setChecked(True)  # Preseleziona il bottone '11'
        self.button1.clicked.connect(self.buttonClicked)

        self.button2 = QPushButton('21', self)
        self.button2.setFixedSize(75, 75)
        self.button2.setCheckable(True)
        self.button2.clicked.connect(self.buttonClicked)

        try:
            with open('Gioco di Scopa/dati.json', 'r') as file:
                # Carica i dati dal file JSON in un dizionario
                ris = json.load(file)['Punti_Vittoria']
        except (FileNotFoundError, KeyError):
            ris = 11

        if ris == 11:
            self.button1.setStyleSheet("color: #FFFFFF; font: 30pt Arial Black; background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #F6F84B, stop:1 #F07A39) ;border-radius: 15px;")

            self.button2.setStyleSheet("color: #FFFFFF; font: 30pt Arial Black; background-color: #4298EF; border-radius: 15px;")
        else:
            self.button1.setStyleSheet("color: #FFFFFF; font: 30pt Arial Black; background-color: #4298EF; border-radius: 15px;")

            self.button2.setStyleSheet("color: #FFFFFF; font: 30pt Arial Black; background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #F6F84B, stop:1 #F07A39) ;border-radius: 15px;")

        # Visualizza il regolamento
        self.impostazioni_button = QPushButton()
        self.impostazioni_button.setStyleSheet(info)
        self.impostazioni_button.setFixedSize(50, 50)
        self.impostazioni_button.clicked.connect(self.regolamento)

        # Aggiungi un'immagine di regolamento
        self.regolamento_image_label = QLabel()
        self.pixmap = QPixmap("Gioco di Scopa/Icone/regolamento.png")
        self.regolamento_image_label.setPixmap(self.pixmap.scaledToHeight(50))
        self.regolamento_image_label.setAlignment(Qt.AlignLeft)

        # Creazione di un layout orizzontale per gli elementi
        home_button_layout = QHBoxLayout()
        home_button_layout.addWidget(self.home_button)
        home_button_layout.setAlignment(Qt.AlignLeft)

        home_button_layout_top = QHBoxLayout()
        home_button_layout_top.addLayout(home_button_layout)
        home_button_layout_top.setAlignment(Qt.AlignTop)

        # Creazione di un layout orizzontale per gli elementi
        account_image_label_layout = QHBoxLayout()
        account_image_label_layout.addWidget(self.account_image_label)
        account_image_label_layout.setAlignment(Qt.AlignCenter)

        # Creazione di un layout orizzontale per gli elementi
        top_buttons_layout = QHBoxLayout()
        top_buttons_layout.addLayout(home_button_layout_top)
        top_buttons_layout.addLayout(account_image_label_layout)
        top_buttons_layout.setAlignment(Qt.AlignTop)

        #per mettere i bottoni in gigha
        hbox = QHBoxLayout()
        hbox.addWidget(self.button1)
        hbox.addWidget(self.button2)

        # Creazione di un layout verticale per il volume della musica e il volume dei suoni
        label_layout = QVBoxLayout()
        label_layout.addWidget(self.spazio_label)
        label_layout.addWidget(self.musica_label)
        label_layout.addWidget(self.musica_volume_slider)
        label_layout.addWidget(self.suoni_label)
        label_layout.addWidget(self.tasti_suono_slider)
        label_layout.addWidget(self.vittorie_label)
        label_layout.addLayout(hbox)
        label_layout.addWidget(self.spazio_label)
        label_layout.setAlignment(Qt.AlignTop)

        # Creazione di un layout orizzontale per gli elementi
        impostazioni_button_layout = QHBoxLayout()
        impostazioni_button_layout.addWidget(self.impostazioni_button)
        impostazioni_button_layout.setAlignment(Qt.AlignLeft)

        impostazioni_button_layout_top = QHBoxLayout()
        impostazioni_button_layout_top.addLayout(impostazioni_button_layout)
        impostazioni_button_layout_top.setAlignment(Qt.AlignLeft)

        # Creazione di un layout orizzontale per gli elementi
        regolamento_image_label_layout = QHBoxLayout()
        regolamento_image_label_layout.addWidget(self.regolamento_image_label)
        regolamento_image_label_layout.setAlignment(Qt.AlignLeft)

        # Creazione di un layout orizzontale per gli elementi
        top_buttons_layout2 = QHBoxLayout()
        top_buttons_layout2.addLayout(impostazioni_button_layout_top)
        top_buttons_layout2.addLayout(regolamento_image_label_layout)
        top_buttons_layout2.addWidget(self.spazio_label)
        top_buttons_layout2.setAlignment(Qt.AlignCenter)

        # Crea un nuovo layout per disporre gli elementi a sinistra
        left_buttons_layout = QHBoxLayout()
        left_buttons_layout.addLayout(top_buttons_layout2)
        left_buttons_layout.setAlignment(Qt.AlignLeft)

        # Layout base
        layout_base = QVBoxLayout()
        layout_base.addLayout(top_buttons_layout)
        layout_base.addLayout(label_layout)
        layout_base.addLayout(left_buttons_layout)
        layout_base.setAlignment(Qt.AlignTop)

        # Aggiunta dei layout al layout verticale principale
        self.layout.addLayout(layout_base)

    def regolamento(self):
        self.sound_manager.play_click_sound()
        self.stacked_layout.setCurrentIndex(12)

    def torna_alla_home(self):
        self.sound_manager.play_click_sound()
        self.stacked_layout.setCurrentIndex(2)

    def on_musica_volume_changed(self, value):
        self.music_manager.set_background_volume(value)
        # Carica i dati dal file JSON in un dizionario
        with open('Gioco di Scopa/dati.json', 'r') as file:
            dati = json.load(file)

        # Aggiorna o aggiungi il dato desiderato
        dati['musica'] = value

        # Scrivi la struttura dati aggiornata nel file JSON
        with open('Gioco di Scopa/dati.json', 'w') as file:
            json.dump(dati, file)
        
        self.musica_volume_slider.setValue(value)

    def on_tasti_suono_changed(self, value):
        self.sound_manager.set_click_volume(value)
        # Carica i dati dal file JSON in un dizionario
        with open('Gioco di Scopa/dati.json', 'r') as file:
            dati = json.load(file)

        # Aggiorna o aggiungi il dato desiderato
        dati['suono'] = value

        # Scrivi la struttura dati aggiornata nel file JSON
        with open('Gioco di Scopa/dati.json', 'w') as file:
            json.dump(dati, file)
        
        self.tasti_suono_slider.setValue(value) 
    
    def get_vittorie(self):
        with open('Gioco di Scopa/dati.json', 'r') as file:
            # Carica i dati dal file JSON
            user_name = json.load(file)['user_name']

        # Dati da inviare al server
        data_to_send = {
            'user_name': user_name,
        }

        try:
            # Invia i dati al server tramite una richiesta POST
            response= requests.post('http://localhost:8080/Vitt', data=data_to_send)
            if response.status_code == 200:
                # Carica i dati dal file JSON in un dizionario
                with open('Gioco di Scopa/dati.json', 'r') as file:
                    dati = json.load(file)

                # Aggiorna o aggiungi il dato desiderato
                ris = response.json()['val'][0]
                dati['Punti_Vittoria'] = int(ris)

                # Scrivi la struttura dati aggiornata nel file JSON
                with open('Gioco di Scopa/dati.json', 'w') as file:
                    json.dump(dati, file)
            else:
                pass
        except requests.exceptions.ConnectionError:
            pass
        
        if ris == 11:
            self.button1.setStyleSheet("color: #FFFFFF; font: 30pt Arial Black; background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #F6F84B, stop:1 #F07A39); border-radius: 15px;")
            self.button2.setChecked(False)
            self.button2.setStyleSheet("color: #FFFFFF; font: 30pt Arial Black; background-color: #4298EF; border-radius: 15px;")
        else:
            self.button2.setStyleSheet("color: #FFFFFF; font: 30pt Arial Black; background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #F6F84B, stop:1 #F07A39); border-radius: 15px;")
            self.button1.setChecked(False)
            self.button1.setStyleSheet("color: #FFFFFF; font: 30pt Arial Black; background-color: #4298EF; border-radius: 15px;")
            
    def buttonClicked(self):
        self.sound_manager.play_click_sound()
        sender = self.sender()
        sender.setStyleSheet("color: #FFFFFF; font: 30pt Arial Black; background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #F6F84B, stop:1 #F07A39); border-radius: 15px;")
        other_button = self.button1 if sender == self.button2 else self.button2
        other_button.setChecked(False)
        other_button.setStyleSheet("color: #FFFFFF; font: 30pt Arial Black; background-color: #4298EF; border-radius: 15px;")

        with open('Gioco di Scopa/dati.json', 'r') as file:
            # Carica i dati dal file JSON
            user_name = json.load(file)['user_name']

        value = 21 if sender == self.button2 else 11

        # Dati da inviare al server
        data_to_send = {
            'user_name': user_name,
            'value': value
        }

        try:
            # Invia i dati al server tramite una richiesta POST
            response= requests.post('http://localhost:8080/UP', data=data_to_send)
            if response.status_code == 200:
                # Carica i dati dal file JSON in un dizionario
                with open('Gioco di Scopa/dati.json', 'r') as file:
                    dati = json.load(file)

                # Aggiorna o aggiungi il dato desiderato
                dati['Punti_Vittoria'] = value

                # Scrivi la struttura dati aggiornata nel file JSON
                with open('Gioco di Scopa/dati.json', 'w') as file:
                    json.dump(dati, file)
            else:
                pass
        except requests.exceptions.ConnectionError:
            pass

# 5 Classe per la pagina deli Giocatori, eredita dalla classe Page
class GiocatoriPage(Page):
    def __init__(self, stacked_layout, sound_manager, parent=None):
        super().__init__(parent)
        self.stacked_layout = stacked_layout
        self.sound_manager = sound_manager

        # Bottone per le impostazioni dell'account
        self.home_button = QPushButton()
        self.home_button.setStyleSheet(home)
        self.home_button.setFixedSize(100, 100)
        self.home_button.clicked.connect(self.torna_alla_home)

        # Aggiungi un'immagine di accesso
        self.giocatori_image_label = QLabel()
        self.pixmap = QPixmap("Gioco di Scopa/Icone/Giocatori.png")
        self.giocatori_image_label.setPixmap(self.pixmap.scaledToHeight(70))
        self.giocatori_image_label.setAlignment(Qt.AlignCenter)

        # Aggiungi spazio
        self.spazio_label = QLabel(" ")
        self.spazio_label.setStyleSheet(testo)
        
        # Seleziona i punti necessari alla vittoria
        self.button1 = QPushButton('2', self)
        self.button1.setFixedSize(75, 75)
        self.button1.setCheckable(True)
        self.button1.setChecked(True)
        self.button1.clicked.connect(self.buttonClicked)
        self.button1.setStyleSheet("color: #FFFFFF; font: 30pt Arial Black; background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #F6F84B, stop:1 #F07A39) ;border-radius: 15px;")

        self.button2 = QPushButton('3', self)
        self.button2.setFixedSize(75, 75)
        self.button2.setCheckable(True)
        self.button2.clicked.connect(self.buttonClicked)
        self.button2.setStyleSheet("color: #FFFFFF; font: 30pt Arial Black; background-color: #4298EF; border-radius: 15px;")

        self.button3 = QPushButton('4', self)
        self.button3.setFixedSize(75, 75)
        self.button3.setCheckable(True)
        self.button3.clicked.connect(self.buttonClicked)
        self.button3.setStyleSheet("color: #FFFFFF; font: 30pt Arial Black; background-color: #4298EF; border-radius: 15px;")

        # Avanti
        self.avanti_button = QPushButton("Avanti")
        self.avanti_button.setStyleSheet(bottone)
        self.avanti_button.clicked.connect(self.avanti)

        # Creazione di un layout orizzontale per gli elementi
        home_button_layout = QHBoxLayout()
        home_button_layout.addWidget(self.home_button)
        home_button_layout.setAlignment(Qt.AlignLeft)

        home_button_layout_top = QHBoxLayout()
        home_button_layout_top.addLayout(home_button_layout)
        home_button_layout_top.setAlignment(Qt.AlignTop)

        # Creazione di un layout orizzontale per gli elementi
        giocatori_image_label_layout = QHBoxLayout()
        giocatori_image_label_layout.addWidget(self.giocatori_image_label)
        giocatori_image_label_layout.setAlignment(Qt.AlignCenter)

        # Creazione di un layout orizzontale per gli elementi
        top_buttons_layout = QHBoxLayout()
        top_buttons_layout.addLayout(home_button_layout_top)
        top_buttons_layout.addLayout(giocatori_image_label_layout)
        top_buttons_layout.addWidget(self.spazio_label)
        top_buttons_layout.setAlignment(Qt.AlignTop)

        #per mettere i bottoni in gigha
        hbox = QHBoxLayout()
        hbox.addWidget(self.button1)
        hbox.addWidget(self.button2)
        hbox.addWidget(self.button3)

        # Creazione di un layout verticale per il volume della musica e il volume dei suoni
        label_layout = QVBoxLayout()
        label_layout.addWidget(self.spazio_label)
        label_layout.addWidget(self.spazio_label)
        label_layout.addWidget(self.spazio_label)
        label_layout.addWidget(self.spazio_label)
        label_layout.addWidget(self.spazio_label)
        label_layout.addWidget(self.spazio_label)
        label_layout.addLayout(hbox)
        label_layout.addWidget(self.spazio_label)
        label_layout.addWidget(self.spazio_label)
        label_layout.addWidget(self.spazio_label)
        label_layout.addWidget(self.spazio_label)
        label_layout.addWidget(self.spazio_label)
        label_layout.addWidget(self.spazio_label)
        label_layout.addWidget(self.avanti_button)
        label_layout.setAlignment(Qt.AlignTop)

        # Layout base
        layout_base = QVBoxLayout()
        layout_base.addLayout(top_buttons_layout)
        layout_base.addLayout(label_layout)
        layout_base.setAlignment(Qt.AlignTop)

        # Aggiunta dei layout al layout verticale principale
        self.layout.addLayout(layout_base)

    def torna_alla_home(self):
        self.sound_manager.play_click_sound()
        self.stacked_layout.setCurrentIndex(2)
       
    def buttonClicked(self):
        self.sound_manager.play_click_sound()
        sender = self.sender()
        sender.setStyleSheet("color: #FFFFFF; font: 30pt Arial Black; background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #F6F84B, stop:1 #F07A39); border-radius: 15px;")
        if sender == self.button1:
            other_button1 = self.button2
            other_button1.setChecked(False)
            other_button1.setStyleSheet("color: #FFFFFF; font: 30pt Arial Black; background-color: #4298EF; border-radius: 15px;")
            other_button2 = self.button3
            other_button2.setChecked(False)
            other_button2.setStyleSheet("color: #FFFFFF; font: 30pt Arial Black; background-color: #4298EF; border-radius: 15px;")
            value = 2
        elif sender == self.button2:
            other_button1 = self.button1
            other_button1.setChecked(False)
            other_button1.setStyleSheet("color: #FFFFFF; font: 30pt Arial Black; background-color: #4298EF; border-radius: 15px;")
            other_button2 = self.button3
            other_button2.setChecked(False)
            other_button2.setStyleSheet("color: #FFFFFF; font: 30pt Arial Black; background-color: #4298EF; border-radius: 15px;")
            value = 3
        else:
            other_button1 = self.button1
            other_button1.setChecked(False)
            other_button1.setStyleSheet("color: #FFFFFF; font: 30pt Arial Black; background-color: #4298EF; border-radius: 15px;")
            other_button2 = self.button2
            other_button2.setChecked(False)
            other_button2.setStyleSheet("color: #FFFFFF; font: 30pt Arial Black; background-color: #4298EF; border-radius: 15px;")
            value = 4

        with open('Gioco di Scopa/dati.json', 'r') as file:
            dati = json.load(file)

        # Aggiorna o aggiungi il dato desiderato
        dati['Giocatori'] = value

        # Scrivi la struttura dati aggiornata nel file JSON
        with open('Gioco di Scopa/dati.json', 'w') as file:
            json.dump(dati, file)

    def avanti(self):
        self.sound_manager.play_click_sound()
        self.stacked_layout.setCurrentIndex(6)

# 6 Classe per la pagina del TipoDiGioco, eredita dalla classe Page
class TipoDiGiocoPage(Page):
    def __init__(self, stacked_layout, sound_manager, attesa_page, parent=None):
        super().__init__(parent)
        self.stacked_layout = stacked_layout
        self.sound_manager = sound_manager
        self.attesa_page = attesa_page

        # Bottone per le impostazioni dell'account
        self.d_button = QPushButton()
        self.d_button.setStyleSheet(d)
        self.d_button.setFixedSize(100, 100)
        self.d_button.clicked.connect(self.torna_Giocatori)

        # Aggiungi un'immagine di accesso
        self.tipo_image_label = QLabel()
        self.pixmap = QPixmap("Gioco di Scopa/Icone/tipo.png")
        self.tipo_image_label.setPixmap(self.pixmap.scaledToHeight(58))
        self.tipo_image_label.setAlignment(Qt.AlignCenter)

        # Aggiungi spazio
        self.spazio_label = QLabel(" ")
        self.spazio_label.setStyleSheet(testo)
        
        # Bot
        self.bot_button = QPushButton("Bot")
        self.bot_button.setStyleSheet(bottone)
        self.bot_button.clicked.connect(self.bot)
        # Online
        self.online_button = QPushButton("Online")
        self.online_button.setStyleSheet(bottone)
        self.online_button.clicked.connect(self.online)

        # Creazione di un layout orizzontale per gli elementi
        d_button_layout = QHBoxLayout()
        d_button_layout.addWidget(self.d_button)
        d_button_layout.setAlignment(Qt.AlignLeft)

        d_button_layout_top = QHBoxLayout()
        d_button_layout_top.addLayout(d_button_layout)
        d_button_layout_top.setAlignment(Qt.AlignTop)

        # Creazione di un layout orizzontale per gli elementi
        tipo_image_label_layout = QHBoxLayout()
        tipo_image_label_layout.addWidget(self.tipo_image_label)
        tipo_image_label_layout.setAlignment(Qt.AlignCenter)

        # Creazione di un layout orizzontale per gli elementi
        top_buttons_layout = QHBoxLayout()
        top_buttons_layout.addLayout(d_button_layout_top)
        top_buttons_layout.addLayout(tipo_image_label_layout)
        top_buttons_layout.setAlignment(Qt.AlignTop)

        #per mettere i bottoni in gigha
        hbox = QHBoxLayout()
        hbox.addWidget(self.bot_button)
        hbox.addWidget(self.online_button)

        # Creazione di un layout verticale per il volume della musica e il volume dei suoni
        label_layout = QVBoxLayout()
        label_layout.addWidget(self.spazio_label)
        label_layout.addWidget(self.spazio_label)
        label_layout.addWidget(self.spazio_label)
        label_layout.addWidget(self.spazio_label)
        label_layout.addWidget(self.spazio_label)
        label_layout.addWidget(self.spazio_label)
        label_layout.addLayout(hbox)
        label_layout.addWidget(self.spazio_label)
        label_layout.addWidget(self.spazio_label)
        label_layout.addWidget(self.spazio_label)
        label_layout.addWidget(self.spazio_label)
        label_layout.addWidget(self.spazio_label)
        label_layout.addWidget(self.spazio_label)
        label_layout.setAlignment(Qt.AlignTop)

        # Layout base
        layout_base = QVBoxLayout()
        layout_base.addLayout(top_buttons_layout)
        layout_base.addLayout(label_layout)
        layout_base.setAlignment(Qt.AlignTop)

        # Aggiunta dei layout al layout verticale principale
        self.layout.addLayout(layout_base)

    def torna_Giocatori(self):
        self.sound_manager.play_click_sound()
        self.stacked_layout.setCurrentIndex(5)

    def online(self):
        self.sound_manager.play_click_sound()
        
        with open('Gioco di Scopa/dati.json', 'r') as file:
            # Carica i dati dal file JSON
            user_name = json.load(file)['user_name']

        with open('Gioco di Scopa/dati.json', 'r') as file:
            # Carica i dati dal file JSON
            num_players = json.load(file)['Giocatori']

        with open('Gioco di Scopa/dati.json', 'r') as file:
            # Carica i dati dal file JSON
            Punti = json.load(file)['Punti_Vittoria']

        # Dati da inviare al server
        data_to_send = {
            'user_name': user_name,  # Chiave corretta per l'utente
            'num_players':num_players,
            'Punti':Punti
        }

        try:
            # Invia i dati al server tramite una richiesta POST
            response = requests.post('http://localhost:8080/start_game', data=data_to_send)
            # Verifica lo stato della risposta
            if response.status_code == 200:
                # Carica i dati dal file JSON in un dizionario
                with open('Gioco di Scopa/dati.json', 'r') as file:
                    dati = json.load(file)

                # Aggiorna o aggiungi il dato desiderato
                dati['stato'] = response.json()['player']
                dati['numero'] = response.json()['player']

                # Scrivi la struttura dati aggiornata nel file JSON
                with open('Gioco di Scopa/dati.json', 'w') as file:
                    json.dump(dati, file)

                self.attesa_page.setstatus()

                self.stacked_layout.setCurrentIndex(7)
                self.attesa_page.start_controls()
            else:
                pass
        except requests.exceptions.ConnectionError:
            pass

    def bot(self):
        self.sound_manager.play_click_sound()
        self.stacked_layout.setCurrentIndex(10)


class WaitThread(QThread):
    wait_finished = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

# 7 Classe per la pagina dell'Attesa, eredita dalla classe Page
class AttesaPage(Page):
    def __init__(self, stacked_layout, sound_manager, parent=None):
        super().__init__(parent)
        self.stacked_layout = stacked_layout
        self.sound_manager = sound_manager
        self.user_name = None  # Aggiunto attributo user_name
        self.wait_thread = None

        # Aggiungi un'immagine di accesso
        self.tipo_image_label = QLabel()
        self.pixmap = QPixmap("Gioco di Scopa/Icone/attesa.png")
        self.tipo_image_label.setPixmap(self.pixmap.scaledToHeight(50))
        self.tipo_image_label.setAlignment(Qt.AlignCenter)

        # Aggiungi spazio
        self.spazio_label = QLabel(" ")
        self.spazio_label.setStyleSheet(testo)

        # Carica i dati dal file JSON in un dizionario
        with open('Gioco di Scopa/dati.json', 'r') as file:
            data = json.load(file)
            giocatori = data['Giocatori']
            stato = data['stato']
            self.user_name = data['user_name']  # Assegna user_name

        # Aggiungi spazio
        self.giocatori_label = QLabel(f"Giocatori Trovati: {stato}/{giocatori}")
        self.giocatori_label.setStyleSheet(testo)

        # Crea un QLabel per visualizzare la GIF
        self.gif_label = QLabel(self)
        movie = QMovie("Gioco di Scopa/Icone/caricamento.gif")
        self.gif_label.setMovie(movie)
        movie.start()
        self.gif_label.setScaledContents(True)
        self.gif_label.setAlignment(Qt.AlignCenter)

        # Aggiungi timer
        self.timer_label = QLabel(" ")
        self.timer_label.setStyleSheet(testo)

        # Esci
        self.esci_button = QPushButton("Esci")
        self.esci_button.setStyleSheet(bottone)
        self.esci_button.clicked.connect(self.esci)

        giocatori_label_layout = QHBoxLayout()
        giocatori_label_layout.addWidget(self.giocatori_label)
        giocatori_label_layout.setAlignment(Qt.AlignCenter)

        gif_label_layout = QHBoxLayout()
        gif_label_layout.addWidget(self.gif_label)
        gif_label_layout.setAlignment(Qt.AlignCenter)

        timer_layout = QHBoxLayout()
        timer_layout.addWidget(self.timer_label)
        timer_layout.setAlignment(Qt.AlignCenter)

        esci_button_layout = QHBoxLayout()
        esci_button_layout.addWidget(self.esci_button)
        esci_button_layout.setAlignment(Qt.AlignRight)

        # Creazione di un layout orizzontale per gli elementi
        top_buttons_layout = QHBoxLayout()
        top_buttons_layout.addWidget(self.spazio_label)
        top_buttons_layout.addLayout(timer_layout)
        top_buttons_layout.addLayout(esci_button_layout)
        top_buttons_layout.setAlignment(Qt.AlignTop)

        # Creazione di un layout verticale per il volume della musica e il volume dei suoni
        label_layout = QVBoxLayout()
        label_layout.addWidget(self.tipo_image_label)
        label_layout.addLayout(giocatori_label_layout)
        label_layout.addWidget(self.spazio_label)
        label_layout.addWidget(self.spazio_label)
        label_layout.addWidget(self.spazio_label)
        label_layout.addLayout(gif_label_layout)
        label_layout.addWidget(self.spazio_label)
        label_layout.addWidget(self.spazio_label)
        label_layout.addWidget(self.spazio_label)
        label_layout.addWidget(self.spazio_label)
        label_layout.addLayout(top_buttons_layout)
        label_layout.setAlignment(Qt.AlignTop)

        # Layout base
        layout_base = QVBoxLayout()
        layout_base.addLayout(label_layout)
        layout_base.setAlignment(Qt.AlignTop)

        # Aggiunta dei layout al layout verticale principale
        self.layout.addLayout(layout_base)

        # Timer per il polling
        self.polling_timer = QTimer()
        self.polling_timer.timeout.connect(self.check_status)

        # Timer per il conto alla rovescia
        self.countdown_timer = QTimer()
        self.countdown_timer.timeout.connect(self.update_countdown)
        self.countdown_seconds = 0

    def start_controls(self):
        # Avvia i controlli solo se il numero della pagina corrisponde a 7
        if self.stacked_layout.currentIndex() == 7:
            print("Starting controls...")
            self.polling_timer.start(2000)  # Poll ogni 2 secondi

    def stop_controls(self):
        # Interrompe i controlli
        print("Stopping controls...")
        self.polling_timer.stop()
        self.countdown_timer.stop()

    def check_status(self):
        user_name = self.user_name
        status = self.status(user_name)
        if status == 'ricerca':
            self.stato()
        elif status == 'ricerca conclusa' and not self.countdown_timer.isActive():
            # Avvia il conto alla rovescia solo se non è già attivo
            self.countdown_seconds = 5
            self.timer_label.setText(str(self.countdown_seconds))
            self.countdown_timer.start(1000)
        elif status == 'in corso':
            self.on_wait_finished()
        # Aggiorna il layout dei giocatori ogni volta che viene effettuato il polling dello stato
        self.stato()

    def update_countdown(self):
        self.countdown_seconds -= 1
        if self.countdown_seconds > 0:
            self.timer_label.setText(str(self.countdown_seconds))
        else:
            self.timer_label.setText('')
            self.countdown_timer.stop()
            self.on_wait_finished()

    def on_wait_finished(self):
        user_name = self.user_name
        data_send = {'user_name': user_name}
        status = self.status(user_name)
        if status in ['ricerca conclusa', 'in corso']:
            try:
                response = requests.post('http://localhost:8080/gioca', data=data_send)
                if response.status_code == 200:
                    with open('Gioco di Scopa/dati.json', 'r') as file:
                        dati = json.load(file)
                    partita = {}
                    partita['mano'] = response.json()['player_hand']
                    partita['terra'] = response.json()['terra']
                    partita['presa'] = []
                    partita['punti'] = 0
                    partita['numero'] = dati['numero']
                    if dati['numero'] == 1:
                        partita['token'] = True
                    else:
                        partita['token'] = False

                    with open('Gioco di Scopa/partita.json', 'w') as file:
                        json.dump(partita, file)

                    self.stop_controls()
                    print("cambio a index 8")
                    self.stacked_layout.setCurrentIndex(8)
            except requests.exceptions.ConnectionError:
                pass

    def setstatus(self):
        with open('Gioco di Scopa/dati.json', 'r') as file:
            # Carica i dati dal file JSON in un dizionario
            giocatori = json.load(file)['Giocatori']
        with open('Gioco di Scopa/dati.json', 'r') as file:
            # Carica i dati dal file JSON in un dizionario
            stato = json.load(file)['stato']
        self.giocatori_label.setText(f"Giocatori Trovati: {stato}/{giocatori}")

    def esci(self):
        self.sound_manager.play_click_sound()
        data_to_send = {'user_name': self.user_name}
        try:
            response = requests.post('http://localhost:8080/exit_game', data=data_to_send)
            if response.status_code == 200:
                with open('Gioco di Scopa/dati.json', 'r') as file:
                    dati = json.load(file)
                dati['stato'] = response.json()['player']
                dati['numero'] = response.json()['player']
                with open('Gioco di Scopa/dati.json', 'w') as file:
                    json.dump(dati, file)

                self.stato()
                self.stacked_layout.setCurrentIndex(2)
                print("Stopping controls...")
        except requests.exceptions.ConnectionError:
            pass

    def stato(self):
        with open('Gioco di Scopa/dati.json', 'r') as file:
            # Carica i dati dal file JSON
            user_name = json.load(file)['user_name']
        # Dati da inviare al server
        data_to_send = {
            'user_name': user_name  # Chiave corretta per l'utente
        }
        try:
            # Invia i dati al server tramite una richiesta POST
            response = requests.post('http://localhost:8080/stato', data=data_to_send)
            # Verifica lo stato della risposta
            if response.status_code == 200:
                # Carica i dati dal file JSON in un dizionario
                with open('Gioco di Scopa/dati.json', 'r') as file:
                    dati = json.load(file)
                # Aggiorna o aggiungi il dato desiderato
                dati['stato'] = response.json()['stato']
                # Scrivi la struttura dati aggiornata nel file JSON
                with open('Gioco di Scopa/dati.json', 'w') as file:
                    json.dump(dati, file)
                self.setstatus()
            else:
                pass
        except requests.exceptions.ConnectionError:
            pass

    def status(self, user_name):
        data_to_send = {'user_name': user_name}
        try:
            response = requests.post('http://localhost:8080/status', data=data_to_send)
            if response.status_code == 200:
                ris = response.json()['status']
            else:
                ris = ''
        except requests.exceptions.ConnectionError:
            ris = ''
        return ris

# 8 Classe per la pagina del Game Online, eredita dalla classe Page
class GameOnlinePage(Page):
    aggiorna_tutto_quanto_signal = pyqtSignal(list, list, list, int)
    aggiorna_tutto_quanto_signal2 = pyqtSignal(list, list, list, int)
    nuova_mano_signal = pyqtSignal(list)
    my_signal = pyqtSignal()
    my_signal2 = pyqtSignal()
    my_signal3 = pyqtSignal()
    def __init__(self, stacked_layout, sound_manager, parent=None):
        super().__init__(parent)
        self.stacked_layout = stacked_layout  # Salva il layout impilato
        self.sound_manager = sound_manager
        self.aggiorna_tutto_quanto_signal.connect(self.aggiorna_tutto_quanto)
        self.aggiorna_tutto_quanto_signal2.connect(self.aggiorna_tutto_quanto2)
        self.nuova_mano_signal.connect(self.nuova_mano)
        self.my_signal.connect(self.prendo_tutto)
        self.my_signal2.connect(self.create_endgame_screen)
        self.my_signal3.connect(self.create_endgame_data)
        self.animation_queue = []
        self.animation_in_progress = False
        self.punti = [0,0]

        with open('Gioco di Scopa/dati.json', 'r') as file:
            self.user_name = json.load(file)['user_name']

        self.setWindowTitle("Animazione di Carte")
        self.setGeometry(100, 100, 600, 1000)

        # Creare un QLabel per lo sfondo
        self.background_label = QLabel(self)
        self.background_label.setStyleSheet("background-color: #52B488;")
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        self.background_label.lower()  # Assicurarsi che l'etichetta di sfondo sia dietro gli altri widget

        # Leggi i dati dal file JSON
        self.load_data()

        # Crea i label per le carte a terra, in mano e il retro delle carte
        self.create_labels()

        # Posiziona i label sul widget
        self.position_labels()

        self.countdown_timer = QTimer()

        self.countdown_timer1 = QTimer()

        self.countdown_timer2 = QTimer()

        self.countdown_timer3 = QTimer()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Aggiorna la dimensione dell'etichetta di sfondo quando la finestra viene ridimensionata
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        self.update()

    def showEvent(self, event):
        super().showEvent(event)
        self.reload_page()
        self.start_animation()
        threading.Thread(target=self.run_controlli_asincroni).start()

    def load_data(self):
        with open("Gioco di Scopa/partita.json", "r") as file:
            self.data = json.load(file)

    def reload_page(self):
        print("Reloading page...")
        self.clear_labels()
        self.load_data()
        self.create_labels()
        self.position_labels()
        print("Page reloaded.")

    def clear_labels(self):
        for label in getattr(self, 'terra_labels', []):
            label.deleteLater()
        for label in getattr(self, 'mano_labels', []):
            label.deleteLater()
        for label in getattr(self, 'retro_labels', []):
            label.deleteLater()
        if hasattr(self, 'presa_label'):
            self.presa_label.deleteLater()
        if hasattr(self, 'presa_label2'):
            self.presa_label2.deleteLater()
        if hasattr(self, 'label_nome_cattivo'):
            self.label_nome_cattivo.deleteLater()
        if hasattr(self, 'label_punti_cattivo'):
            self.label_punti_cattivo.deleteLater()
        if hasattr(self, 'label_nome'):
            self.label_nome.deleteLater()
        if hasattr(self, 'label_punti'):
            self.label_punti.deleteLater()
            
    def create_labels(self):
        print("Creating labels...")
        # Crea i label per le carte a terra
        self.terra_labels = []
        for carta in self.data["terra"]:
            label = QLabel(self)
            pixmap = QPixmap(f"Gioco di Scopa/Carte/{carta[1]}/{carta[0]}.png")
            label.setPixmap(pixmap.scaled(100, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            label.setProperty('card_id', f"{carta[1]}/{carta[0]}")
            label.setStyleSheet("background-color: none;")
            self.terra_labels.append(label)
            label.setGeometry(-150, int(self.height() / 2 - 75), 100, 150)

        # Aggiungi gli eventi di entrata e uscita del mouse per ogni label delle carte in mano
        for i, label in enumerate(self.terra_labels):
            label.hover_rect = QRectF(int(self.width() / 2 - (len(self.terra_labels) * 100 + (len(self.terra_labels) - 5) * 10) / 2) + i * (100 + 10), int(self.height() / 2 - 150)+20, 100, 150)  # Posizione di hover
            label.end_rect = QRectF(int(self.width() / 2 - (len(self.terra_labels) * 100 + (len(self.terra_labels) - 5) * 10) / 2) + i * (100 + 10), int(self.height() / 2 - 150), 100, 150)  # Posizione finale
            label.enterEvent = lambda event, lbl=label: self.on_card_hover_enter(event, lbl)
            label.leaveEvent = lambda event, lbl=label: self.on_card_hover_leave(event, lbl)

        # Crea i label per le carte in mano
        self.mano_labels = []
        for carta in self.data["mano"]:
            label = QLabel(self)
            pixmap = QPixmap(f"Gioco di Scopa/Carte/{carta[1]}/{carta[0]}.png")
            label.setPixmap(pixmap.scaled(150, 225, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            label.setProperty('card_id', f"{carta[1]}/{carta[0]}")
            label.setStyleSheet("background-color: none;")
            self.mano_labels.append(label)
            label.mousePressEvent = lambda event, lbl=label: self.on_card_press(event, lbl)
            label.mouseReleaseEvent = lambda event, lbl=label: self.on_card_release(event, lbl)
            label.setGeometry(-150, int(self.height() / 2 - 75), 100, 150)

        centro_basso_x = int(self.width() / 2 - (len(self.mano_labels) * 150 + (len(self.mano_labels) - 1) * 10) / 2) + 15  # 
        centro_basso_y = self.height() - 225  # Assumi che questa sia la posizione y corretta

        # Aggiungi gli eventi di entrata e uscita del mouse per ogni label delle carte in mano
        for i, label in enumerate(self.mano_labels):
            label.hover_rect = QRectF(centro_basso_x + i * (150 + 10), centro_basso_y - 20, 150, 225)  # Posizione di hover
            label.end_rect = QRectF(centro_basso_x + i * (150 + 10), centro_basso_y, 150, 225)  # Posizione finale
            label.enterEvent = lambda event, lbl=label: self.on_card_hover_enter(event, lbl)
            label.leaveEvent = lambda event, lbl=label: self.on_card_hover_leave(event, lbl)

        # Crea i label per il retro delle carte
        self.retro_labels = []
        for _ in range(3):
            label = QLabel(self)
            pixmap = QPixmap("Gioco di Scopa/Carte/0.png")
            label.setPixmap(pixmap.scaled(50, 75, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            label.setStyleSheet("background-color: none;")
            self.retro_labels.append(label)
            label.setGeometry(-150, int(self.height() / 2 - 75), 100, 150)

        self.presa_label = QLabel(self)
        pixmap = QPixmap("Gioco di Scopa/Carte/0.png")
        self.presa_label.setPixmap(pixmap.scaled(100, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.presa_label.setStyleSheet("background-color: none;")
        self.presa_label.setGeometry(-150, 1100, 100, 150)
        self.presa_label.move(-100, 1000)

        self.presa_label2 = QLabel(self)
        pixmap = QPixmap("Gioco di Scopa/Carte/0.png")
        self.presa_label2.setPixmap(pixmap.scaled(60, 90, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.presa_label2.setStyleSheet("background-color: none;")
        self.presa_label2.setGeometry(600, -250, 60, 90)
        self.presa_label2.move(500, -200)

        self.nomecattivo = 'nemico'
        data_to_send = {'user_name': self.user_name}
        try:
            response = requests.post('http://localhost:8080/nomecattivo', data=data_to_send)
            if response.status_code == 200:
                self.nomecattivo = response.json()['nomecattivo'][0]
        except requests.exceptions.ConnectionError:
            self.nomecattivo = 'nemico'

        # Crea i label per il nome cattivo e i punti
        self.label_nome_cattivo = QLabel(f"{self.nomecattivo} \nPunti:", self)
        self.label_nome_cattivo.setStyleSheet(testoo)
        self.label_nome_cattivo.adjustSize()  # Ridimensiona il QLabel in base al contenuto del testo

        self.label_punti_cattivo = QLabel(str(self.punti[1]), self)
        self.label_punti_cattivo.setStyleSheet(testoo)
        self.label_punti_cattivo.adjustSize()  # Ridimensiona il QLabel in base al contenuto del testo

        # Crea i label per il nome e i punti
        self.label_nome = QLabel("Punti:", self)
        self.label_nome.setStyleSheet(titoloo)
        self.label_nome.adjustSize()  # Ridimensiona il QLabel in base al contenuto del testo

        self.label_punti = QLabel(str(self.punti[0]), self)
        self.label_punti.setStyleSheet(titoloo)
        self.label_punti.adjustSize()  # Ridimensiona il QLabel in base al contenuto del testo

        print("Labels created.")

    def position_labels(self):
        print("Positioning labels...")
        # Implementa la logica per posizionare i QLabel creati
        for i, label in enumerate(self.terra_labels):
            label.setGeometry(-150, int(self.height() / 2 - 75), 100, 150)
            label.show()
        for i, label in enumerate(self.mano_labels):
            label.setGeometry(-150, int(self.height() / 2 - 75), 100, 150)
            label.show()
        for i, label in enumerate(self.retro_labels):
            label.setGeometry(-150, int(self.height() / 2 - 75), 100, 150)
            label.show()
        self.presa_label.setGeometry(-150, 1100, 100, 150)
        self.presa_label.move(-100, 1000)
        self.presa_label.show()

        self.presa_label2.setGeometry(600, -250, 60, 90)
        self.presa_label2.move(500, -200)
        self.presa_label2.show()

        self.label_nome_cattivo.move(10, 10)
        self.label_punti_cattivo.move(10, 60)

        self.label_nome.move(self.width() - self.label_nome_cattivo.width() - 60, 560)
        self.label_punti.move(self.width() - self.label_punti.width() - 10, 620)
        
        self.label_nome_cattivo.show()
        self.label_punti_cattivo.show()
        self.label_nome.show()
        self.label_punti.show()
        
        print("Labels positioned.")


    def run_controlli_asincroni(self):
        asyncio.run(self.controlli_asincroni())

    async def controlli_asincroni(self):
        with open("Gioco di Scopa/partita.json", "r") as file:
            token = json.load(file)['token']
        while not token:
            data_to_send = {'user_name': self.user_name}
            try:
                response = requests.post('http://localhost:8080/con_questo_ho_finito', data=data_to_send)
                if response.status_code == 200:
                    print(response.json()['finito'])
                    print(response.json()['finito_tutto'])
                    if response.json()['finito'] and response.json()['finito_tutto']:
                        print('sono passato di quí')
                        data_to_send = {'user_name': self.user_name}
                        try:
                            response = requests.post('http://localhost:8080/nome_ultima_presa', data=data_to_send)
                            if response.status_code == 200:
                                nome_ultima_presa = response.json()['nome_ultima_presa']
                                if nome_ultima_presa == self.user_name:
                                    print("mi prendo tutto io ")
                                    try:
                                        response = requests.post('http://localhost:8080/dammi_tutto', data=data_to_send)
                                        if response.status_code == 200:
                                            
                                            with open("Gioco di Scopa/dati.json", "r") as file:
                                                n = json.load(file)['numero']
                                            with open("Gioco di Scopa/dati.json", "r") as file:
                                                max = json.load(file)['Giocatori']

                                            print(n)
                                            print(max)
                                            print(response.json()['numero'])
                                            if (((response.json()['numero'] + 1) == n) or ((response.json()['numero'] == max) and (n == 1))):
                                                with open("Gioco di Scopa/partita.json", "r") as file:
                                                    dati = json.load(file)
                                                dati['token'] = True
                                                print(dati['token'])
                                                with open("Gioco di Scopa/partita.json", "w") as file:
                                                    json.dump(dati, file)
                                            else:
                                                print("no buono")
                                                pass

                                            response_json = response.json()
                                            self.aggiorna_tutto_quanto_signal.emit(
                                                response_json['terra'],
                                                response_json['carta_mano'],
                                                response_json['carte_prese'],
                                                response_json['numero']
                                            )
                                    except requests.exceptions.ConnectionError:
                                        pass
                                    try:
                                        response = requests.post('http://localhost:8080/fatto', data=data_to_send)
                                        if response.status_code == 200:
                                            terraa1 = response.json()['terra']
                                    except requests.exceptions.ConnectionError:
                                        pass
                                    with open("Gioco di Scopa/partita.json", "r") as file:
                                        terraa = json.load(file)['terra']
                                    if terraa == terraa1:
                                        print("ok tra 4 secondi")
                                        await asyncio.sleep(4)
                                        self.schedule_prendi_tutto()
                                else:
                                    try:
                                        response = requests.post('http://localhost:8080/dammi_tutto', data=data_to_send)
                                        if response.status_code == 200:
                                            
                                            with open("Gioco di Scopa/dati.json", "r") as file:
                                                n = json.load(file)['numero']
                                            with open("Gioco di Scopa/dati.json", "r") as file:
                                                max = json.load(file)['Giocatori']

                                            print(n)
                                            print(max)
                                            print(response.json()['numero'])
                                            if (((response.json()['numero'] + 1) == n) or ((response.json()['numero'] == max) and (n == 1))):
                                                with open("Gioco di Scopa/partita.json", "r") as file:
                                                    dati = json.load(file)
                                                dati['token'] = True
                                                print(dati['token'])
                                                with open("Gioco di Scopa/partita.json", "w") as file:
                                                    json.dump(dati, file)
                                            else:
                                                print("no buono")
                                                pass

                                            response_json = response.json()
                                            self.aggiorna_tutto_quanto_signal2.emit(
                                                response_json['terra'],
                                                response_json['carta_mano'],
                                                response_json['carte_prese'],
                                                response_json['numero']
                                            )
                                    except requests.exceptions.ConnectionError:
                                        pass
                        except requests.exceptions.ConnectionError:
                            pass
                        print("se va qui siamo a posto")
                        await asyncio.sleep(3)
                        self.create_endgame_screen_asinc()
                        await asyncio.sleep(6)
                        self.create_endgame_data_asinc()
                    elif response.json()['finito'] and (not response.json()['finito_tutto']):
                        print("distribuzione delle nuove carte")
                        data_to_send = {'user_name': self.user_name}
                        try:
                            response = requests.post('http://localhost:8080/fatto', data=data_to_send)
                            if response.status_code == 200:
                                terraa1 = response.json()['terra']
                                with open("Gioco di Scopa/partita.json", "r") as file:
                                    terraa = json.load(file)['terra']
                                if terraa == terraa1:
                                    await asyncio.sleep(0.5)
                                    print("le carte a terra sono uguali")
                                else:
                                    print("ora non piu")
                                    data_to_send = {'user_name': self.user_name}
                                    try:
                                        response = requests.post('http://localhost:8080/dammi_tutto', data=data_to_send)
                                        if response.status_code == 200:
                                            
                                            with open("Gioco di Scopa/dati.json", "r") as file:
                                                n = json.load(file)['numero']
                                            with open("Gioco di Scopa/dati.json", "r") as file:
                                                max = json.load(file)['Giocatori']

                                            print(n)
                                            print(max)
                                            print(response.json()['numero'])
                                            if (((response.json()['numero'] + 1) == n) or ((response.json()['numero'] == max) and (n == 1))):
                                                with open("Gioco di Scopa/partita.json", "r") as file:
                                                    dati = json.load(file)
                                                dati['token'] = True
                                                print(dati['token'])
                                                with open("Gioco di Scopa/partita.json", "w") as file:
                                                    json.dump(dati, file)
                                            else:
                                                print("no buono")
                                                pass

                                            response_json = response.json()
                                            self.aggiorna_tutto_quanto_signal.emit(
                                                response_json['terra'],
                                                response_json['carta_mano'],
                                                response_json['carte_prese'],
                                                response_json['numero']
                                            )
                                    except requests.exceptions.ConnectionError:
                                        pass
                        except requests.exceptions.ConnectionError:
                            pass
                        data_to_send = {'user_name': self.user_name}
                        try:
                            response = requests.post('http://localhost:8080/distrubuisci_carte_nuove', data=data_to_send)
                            if response.status_code == 200:
                                print('ok')
                        except requests.exceptions.ConnectionError:
                            pass
                        try:
                            response = requests.post('http://localhost:8080/distrubuisci_carte', data=data_to_send)
                            if response.status_code == 200:
                                response_json = response.json()
                                mano_json = json.dumps(response_json['carte_mano'])
                                def ensure_list(decoded):
                                    while isinstance(decoded, str):
                                        try:
                                            decoded = json.loads(decoded)
                                        except json.JSONDecodeError as e:
                                            print("Error decoding JSON:", e)
                                            return None
                                    return decoded
                                mano = ensure_list(mano_json)
                                with open("Gioco di Scopa/partita.json", "r") as file:
                                    dati = json.load(file)
                                dati['mano'] = mano

                                # Aggiorna il file JSON
                                with open("Gioco di Scopa/partita.json", "w") as file:
                                    json.dump(dati, file)
                                self.nuova_mano(response_json['carte_mano'])
                        except requests.exceptions.ConnectionError:
                            pass
                    else:
                        print("continuo attesa")
                        data_to_send = {'user_name': self.user_name}
                        try:
                            response = requests.post('http://localhost:8080/fatto', data=data_to_send)
                            if response.status_code == 200:
                                terraa1 = response.json()['terra']
                                with open("Gioco di Scopa/partita.json", "r") as file:
                                    terraa = json.load(file)['terra']
                                if terraa == terraa1:
                                    await asyncio.sleep(0.5)
                                    print("le carte a terra sono uguali")
                                else:
                                    print("ora non piu")
                                    data_to_send = {'user_name': self.user_name}
                                    try:
                                        response = requests.post('http://localhost:8080/dammi_tutto', data=data_to_send)
                                        if response.status_code == 200:
                                            
                                            with open("Gioco di Scopa/dati.json", "r") as file:
                                                n = json.load(file)['numero']
                                            with open("Gioco di Scopa/dati.json", "r") as file:
                                                max = json.load(file)['Giocatori']

                                            print(n)
                                            print(max)
                                            print(response.json()['numero'])
                                            if (((response.json()['numero'] + 1) == n) or ((response.json()['numero'] == max) and (n == 1))):
                                                with open("Gioco di Scopa/partita.json", "r") as file:
                                                    dati = json.load(file)
                                                dati['token'] = True
                                                print(dati['token'])
                                                with open("Gioco di Scopa/partita.json", "w") as file:
                                                    json.dump(dati, file)
                                            else:
                                                print("no buono")
                                                pass

                                            response_json = response.json()
                                            self.aggiorna_tutto_quanto_signal.emit(
                                                response_json['terra'],
                                                response_json['carta_mano'],
                                                response_json['carte_prese'],
                                                response_json['numero']
                                            )
                                    except requests.exceptions.ConnectionError:
                                        pass
                        except requests.exceptions.ConnectionError:
                            pass
            except requests.exceptions.ConnectionError:
                pass
            with open("Gioco di Scopa/partita.json", "r") as file:
                token = json.load(file)['token']
    
    # Metodo per impostare l'indice della vista, eseguito nel thread principale
    @pyqtSlot(int)
    def set_index(self, index):
        self.stacked_layout.setCurrentIndex(index)

    def schedule_prendi_tutto(self):
        self.my_signal.emit()

    @pyqtSlot()
    def prendo_tutto(self):
        # Legge le carte a terra dal file JSON
        with open("Gioco di Scopa/partita.json", "r") as file:
            terra = json.load(file)["terra"]
        self.prendi_carte_fine(terra)
        self.start_move_animation_fine(terra)
    
    def prendi_carte_fine(self, carte_prendibili):
        # Implementa la logica per prendere le carte dal tavolo
        # Questo è un esempio, dovrai adattarlo alle regole del tuo gioco
        for carta in carte_prendibili:
            self.rimuovi_carta_da_terra(carta)
        # Aggiorna il punteggio o lo stato del gioco se necessario

    
    def on_card_hover_enter(self, event, label):
        # Crea un'animazione per spostare il QLabel verso l'alto
        self.animation_up = QPropertyAnimation(label, b'geometry')
        self.animation_up.setDuration(150)
        self.animation_up.setEndValue(label.hover_rect)
        self.animation_up.start()

    def on_card_hover_leave(self, event, label):
        # Crea un'animazione per riportare il QLabel nella posizione finale
        self.animation_down = QPropertyAnimation(label, b'geometry')
        self.animation_down.setDuration(150)
        self.animation_down.setEndValue(label.end_rect)
        self.animation_down.start()


    def on_card_press(self, event, label):
        self.long_press_timer = QTimer(self)
        self.long_press_timer.setSingleShot(True)
        self.long_press_timer.timeout.connect(lambda: self.on_long_press(event, label))
        self.long_press_timer.start(1000)  # Regola il tempo di attesa per considerare un click come "click lungo"

    def on_card_release(self, event, label):
        if self.long_press_timer.isActive():
            self.long_press_timer.stop()
            self.handle_card_click(event, label)

    def handle_card_click(self, event, label):
        print("handle_card_click started")
        self.sound_manager.play_click_sound()
        
        try:
            with open("Gioco di Scopa/partita.json", "r") as file:
                token = json.load(file)['token']
        except Exception as e:
            print(f"Error loading JSON: {e}")
            return
        
        if token:
            card_id = label.property('card_id')
            print(f"Card clicked: {card_id}")
            
            try:
                card_id_vett = card_id.strip().split('/')
                seme = card_id_vett[0]
                valore = int(card_id_vett[1])
                carta_mano = [card_id_vett[1], seme]

                carte_a_terra = self.get_carte_a_terra()
                print(f"Carte a terra: {carte_a_terra}")

                carte_prendibili = self.get_carte_prendibili(card_id_vett, carte_a_terra)
                print(f"Carte prendibili: {carte_prendibili}")
            except Exception as e:
                print(f"Error processing card: {e}")
                return
            
            data_to_send = {'user_name': self.user_name}
            quasi_finito = False
            
            try:
                response = requests.post('http://localhost:8080/quasi_finito', data=data_to_send)
                if response.status_code == 200:
                    quasi_finito = response.json().get('quasi_finito', False)
            except requests.exceptions.ConnectionError as e:
                print(f"Connection error: {e}")
            
            print(f"Quasi finito: {quasi_finito}")
            
            if quasi_finito:
                nome_ultima_presa = None
                try:
                    response = requests.post('http://localhost:8080/nome_ultima_presa', data=data_to_send)
                    if response.status_code == 200:
                        nome_ultima_presa = response.json().get('nome_ultima_presa')
                except requests.exceptions.ConnectionError as e:
                    print(f"Connection error: {e}")
                time.sleep(0.2)
                if nome_ultima_presa == self.user_name or carte_prendibili:
                    print('sono stato io l ultimo a prendere')
                    self.prendi_carte(carta_mano, carte_a_terra)
                    self.start_move_animation4(carta_mano, carte_a_terra)
                    self.push_new_data(carta_mano, carte_a_terra)
                else:
                    print('e invece no è stato l altro tizio')
                    self.metti_a_terra(carta_mano)
                    self.start_move_animation2(carta_mano)
                    self.push_data(carta_mano)
            else:
                if carte_prendibili:
                    if valore > 7:
                        comb = [combinazione for combinazione in carte_prendibili if len(combinazione) == 1]
                        if comb:
                            carte_prendibili = comb
                    if len(carte_prendibili) > 1:
                        self.show_combination_options(carta_mano, carte_prendibili)
                    else:
                        self.prendi_carte(carta_mano, carte_prendibili[0])
                        self.start_move_animation(carta_mano, carte_prendibili[0])
                        self.push_new_data(carta_mano, carte_prendibili[0])
                else:
                    self.metti_a_terra(carta_mano)
                    self.start_move_animation2(carta_mano)
                    self.push_data(carta_mano)
        else:
            self.aspetta_turno()

        print("handle_card_click ended")

    def on_long_press(self, event, label):
        print(f"Long press detected on card: {label.property('card_id')}")
        # Gestisci il caso di click lungo qui
        pass


    def aspetta_turno(self):
        
        # Crea un QLabel trasparente che copre tutto
        self.cover_label = QLabel(self)
        self.cover_label.resize(self.width(), self.height())
        self.cover_label.setStyleSheet("background-color: rgba(0, 0, 0, 100);")

        # Crea un QPixmap con l'immagine che vuoi mostrare al centro
        center_pixmap = QPixmap("Gioco di Scopa/Icone/tuoturno.png")
        center_pixmap = center_pixmap.scaled(500, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.cover_label2 = QLabel(self)
        self.cover_label2.resize(self.width(), self.height())
        self.cover_label2.setStyleSheet("background-color: none;")

        # Crea un altro QLabel per l'immagine centrale
        self.center_image_label = QLabel(self.cover_label2)
        self.center_image_label.setPixmap(center_pixmap)
        self.center_image_label.setAlignment(Qt.AlignCenter)
        self.center_image_label.setGeometry(
            (self.width() - center_pixmap.width()) // 2,
            (self.height() - center_pixmap.height()) // 2,
            center_pixmap.width(),
            center_pixmap.height()
        )

        self.cover_label.show()
        self.cover_label2.show()

        # Inizia l'animazione di dissolvenza
        self.fade_in_animation = QPropertyAnimation(self.cover_label2, b"opacity")
        self.fade_in_animation.setDuration(2000)
        self.fade_in_animation.setStartValue(0.0)
        self.fade_in_animation.setEndValue(1.0)
        self.fade_in_animation.setEasingCurve(QEasingCurve.Linear)

        # Quando l'animazione di opacità è finita, rimuovi i QLabel
        self.fade_in_animation.finished.connect(self.remove_labelllls)

        # Avvia l'animazione di opacità
        self.fade_in_animation.start()

    def remove_labelllls(self):
        labels = ['cover_label', 'cover_label2', 'center_image_label']
        for label in labels:
            if hasattr(self, label):
                getattr(self, label).hide()
                getattr(self, label).deleteLater()
                delattr(self, label)


    def start_next_animation(self):
        if self.animation_queue:
            next_item = self.animation_queue.pop(0)
            self.animation_in_progress = True
            if callable(next_item):
                next_item()
            else:
                next_item.start()

    def on_animation_finished(self):
        self.animation_in_progress = False
        self.start_next_animation()


    @pyqtSlot(list)
    def nuova_mano(self, mano):
        mano_json = json.dumps(mano)
        QMetaObject.invokeMethod(self, "queue_setup_ui_elements", Qt.QueuedConnection, Q_ARG(str, mano_json))

    @pyqtSlot(str)
    def queue_setup_ui_elements(self, mano_json):
        # Aggiungi la funzione setup_ui_elements alla coda di animazioni
        self.animation_queue.append(lambda: self.setup_ui_elements(mano_json))
        if not self.animation_in_progress:
            print('perfetto')
            self.start_next_animation()
        else:
            print('no buono')

    @pyqtSlot(str)
    def setup_ui_elements(self, mano_json):
        
        labels = ['cover_label3', 'cover_label23', 'center_image_label2']
        for label in labels:
            if hasattr(self, label):
                try:
                    label_obj = getattr(self, label)
                    label_obj.hide()
                    label_obj.deleteLater()
                    delattr(self, label)
                except RuntimeError as e:
                    print(f"RuntimeError for label {label}: {e}")
                except AttributeError as e:
                    print(f"AttributeError for label {label}: {e}")
        
        with open("Gioco di Scopa/partita.json", "r") as file:
            datti = json.load(file)
        mano_json = datti['mano']

        print("Received mano_json:", mano_json)

        def ensure_list(decoded):
            while isinstance(decoded, str):
                try:
                    decoded = json.loads(decoded)
                except json.JSONDecodeError as e:
                    print("Error decoding JSON:", e)
                    return None
            return decoded

        mano = ensure_list(mano_json)

        if mano is None:
            print("mano is None after decoding")
            return

        print("Decoded mano:", mano)
        print("Type of mano:", type(mano))

        if not isinstance(mano, list):
            print("Error: mano is not a list")
            return
        for carta in mano:
            if not (isinstance(carta, (list, tuple)) and len(carta) >= 2):
                print("Error: Invalid carta format:", carta)
                return

        def update_pixmap(label, pixmap):
            print("Updating pixmap for label", label)
            try:
                if label:
                    label.setPixmap(pixmap.scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            except RuntimeError as e:
                print(f"RuntimeError: {e}. The QLabel object might have been deleted.")


        # Nascondi etichette esistenti prima di aggiornare
        for label in getattr(self, 'mano_labels', []):
            label.hide()
        for label in getattr(self, 'retro_labels', []):
            label.hide()

        print("Updating self.data with mano")
        self.data["mano"] = mano
        print("Updated self.data:", self.data)

        for label in getattr(self, 'mano_labels', []):
            label.deleteLater()
        for label in getattr(self, 'retro_labels', []):
            label.deleteLater()

        # Crea i label per le carte in mano
        self.mano_labels = []
        for carta in self.data["mano"]:
            label = QLabel(self)
            pixmap = QPixmap(f"Gioco di Scopa/Carte/{carta[1]}/{carta[0]}.png")
            label.setPixmap(pixmap.scaled(150, 225, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            label.setProperty('card_id', f"{carta[1]}/{carta[0]}")
            label.setStyleSheet("background-color: none;")
            self.mano_labels.append(label)
            label.mousePressEvent = lambda event, lbl=label: self.on_card_press(event, lbl)
            label.mouseReleaseEvent = lambda event, lbl=label: self.on_card_release(event, lbl)
            label.setGeometry(-150, int(self.height() / 2 - 75), 100, 150)

        centro_basso_x = int(self.width() / 2 - (len(self.mano_labels) * 150 + (len(self.mano_labels) - 1) * 10) / 2) + 15  # 
        centro_basso_y = self.height() - 225  # Assumi che questa sia la posizione y corretta

        # Aggiungi gli eventi di entrata e uscita del mouse per ogni label delle carte in mano
        for i, label in enumerate(self.mano_labels):
            label.hover_rect = QRectF(centro_basso_x + i * (150 + 10), centro_basso_y - 20, 150, 225)  # Posizione di hover
            label.end_rect = QRectF(centro_basso_x + i * (150 + 10), centro_basso_y, 150, 225)  # Posizione finale
            label.enterEvent = lambda event, lbl=label: self.on_card_hover_enter(event, lbl)
            label.leaveEvent = lambda event, lbl=label: self.on_card_hover_leave(event, lbl)

        # Crea i label per il retro delle carte
        self.retro_labels = []
        for _ in range(3):
            label = QLabel(self)
            pixmap = QPixmap("Gioco di Scopa/Carte/0.png")
            label.setPixmap(pixmap.scaled(50, 75, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            label.setStyleSheet("background-color: none;")
            self.retro_labels.append(label)
            label.setGeometry(-150, int(self.height() / 2 - 75), 100, 150)

        # Crea un QLabel trasparente che copre tutto
        self.cover_label3 = QLabel(self)
        self.cover_label3.resize(self.width(), self.height())  # Assicurati che copra tutto il widget
        self.cover_label3.setStyleSheet("background-color: rgba(0, 0, 0, 100);")  # Imposta un colore di sfondo trasparente

        # Crea un QPixmap con l'immagine che vuoi mostrare al centro
        center_pixmap = QPixmap("Gioco di Scopa/Icone/giro.png")
        center_pixmap = center_pixmap.scaled(500, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Ridimensiona l'immagine se necessario

        self.cover_label23 = QLabel(self.cover_label3)
        self.cover_label23.resize(self.width(), self.height())  # Assicurati che copra tutto il widget
        self.cover_label23.setStyleSheet("background-color: none;")  # Imposta un colore di sfondo trasparente

        # Crea un altro QLabel per l'immagine centrale
        self.center_image_label2 = QLabel(self.cover_label23)
        self.center_image_label2.setPixmap(center_pixmap)
        self.center_image_label2.setAlignment(Qt.AlignCenter)  # Centra l'immagine
        self.center_image_label2.setGeometry(
            (self.width() - center_pixmap.width()) // 2,
            (self.height() - center_pixmap.height()) // 2,
            center_pixmap.width(),
            center_pixmap.height()
        )
        self.cover_label3.show()
        self.cover_label23.show()

        self.animations_group = QSequentialAnimationGroup()

        self.mano_animations = []
        for i, label in enumerate(self.mano_labels):
            animation = QPropertyAnimation(label, b"geometry")
            animation.setDuration(250)
            animation.setStartValue(QRectF(-150, int(self.height() / 2 - 75), 100, 150))
            end_rect = QRectF(centro_basso_x + i * (150 + 10), centro_basso_y, 150, 225)
            animation.setEndValue(end_rect)
            animation.setEasingCurve(QEasingCurve.InOutQuad)
            card_id = label.property('card_id')
            animation.valueChanged.connect(partial(update_pixmap, label=label, pixmap=QPixmap(f"Gioco di Scopa/Carte/{card_id}.png")))
            self.mano_animations.append(animation)

        self.retro_animations = []
        for i, label in enumerate(self.retro_labels):
            animation = QPropertyAnimation(label, b"geometry")
            animation.setDuration(250)
            animation.setStartValue(QRectF(-150, int(self.height() / 2 - 75), 100, 150))
            end_rect = QRectF(int(self.width() / 2 - 100 + i * 75), 10, 75, 112.5)
            animation.setEndValue(end_rect)
            animation.setEasingCurve(QEasingCurve.InOutQuad)
            animation.valueChanged.connect(partial(update_pixmap, label=label, pixmap=QPixmap("Gioco di Scopa/Carte/0.png")))
            self.retro_animations.append(animation)

        x = max(len(self.mano_animations), len(self.retro_animations))

        for i in range(x):
            if i < len(self.mano_animations):
                self.animations_group.addAnimation(self.mano_animations[i])
            if i < len(self.retro_animations):
                self.animations_group.addAnimation(self.retro_animations[i])

        print("Animations group initialized with animations")

        if hasattr(self, 'cover_label3'):
            print("self.cover_label3 exists:", self.cover_label3)
        else:
            print("self.cover_label3 does not exist")

        self.animations_group.finished.connect(self.on_animation_finished)
        self.animations_group.finished.connect(self.animation_finishedd)
        self.animations_group.start()
        print("Animations group started")

        # Mostra le nuove etichette
        for label in self.mano_labels:
            label.show()
        for label in self.retro_labels:
            label.show()

    def animation_finishedd(self):
        try:
            if self.cover_label3 is None:
                print("Error: cover_label3 is None in animation_finishedd")
                return

            if self.center_image_label2 is None:
                print("Error: center_image_label2 is None in animation_finishedd")
                return

            print("Starting fade animation")

            self.cover_opacity_effect = QGraphicsOpacityEffect(self.cover_label3)
            self.cover_label3.setGraphicsEffect(self.cover_opacity_effect)

            self.center_opacity_effect = QGraphicsOpacityEffect(self.center_image_label2)
            self.center_image_label2.setGraphicsEffect(self.center_opacity_effect)

            self.fade_animation = QPropertyAnimation(self.cover_opacity_effect, b"opacity")
            self.fade_animation.setDuration(1000)
            self.fade_animation.setStartValue(1.0)
            self.fade_animation.setEndValue(0.0)
            self.fade_animation.setEasingCurve(QEasingCurve.Linear)

            self.fade_animation.valueChanged.connect(lambda value: self.set_label_opacity(value))

            self.fade_animation.finished.connect(lambda: self.remove_labelss())

            self.fade_animation.start()
        except AttributeError as e:
            print(f"AttributeError in animation_finishedd: {e}")
            pass

    def set_label_opacity(self, value):
        if self.cover_opacity_effect:
            self.cover_opacity_effect.setOpacity(value)
        if self.center_opacity_effect:
            self.center_opacity_effect.setOpacity(value)
        self.update()

    def remove_labelss(self):
        print("remove_labels called")
        labels = ['cover_label3', 'cover_label23', 'center_image_label2']
        for label in labels:
            if hasattr(self, label):
                getattr(self, label).hide()
                getattr(self, label).deleteLater()
                delattr(self, label)


    @pyqtSlot(list, list, list, int)
    def aggiorna_tutto_quanto(self, terra, carta_retro, carte_prese, numero):
        self.aggiorna_tutto_quantoo(terra, carta_retro, carte_prese, numero)

    def aggiorna_tutto_quantoo(self, terra, carta_retro, carte_prese, numero):

        labels = ['cover_label', 'cover_label2', 'center_image_label']
        for label in labels:
            if hasattr(self, label):
                try:
                    label_attr = getattr(self, label)
                    label_attr.hide()
                    label_attr.deleteLater()
                    delattr(self, label)
                except RuntimeError as e:
                    print(f"RuntimeError for {label}: {e}")
                except AttributeError as e:
                    print(f"AttributeError for {label}: {e}")

                
        def update_pixmap(label, pixmap):
            label.setPixmap(pixmap.scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        def realign_cards_wrapper():
            self.realign_cards2()

        # Aggiungi una label trasparente che copre tutto
        self.cover_label = QLabel(self)
        self.cover_label.setGeometry(0, 0, self.width(), self.height())
        self.cover_label.setStyleSheet("background-color: rgba(0, 0, 0, 1%);")
        self.cover_label.show()

        with open("Gioco di Scopa/partita.json", "r") as file:
            dati = json.load(file)
        dati['terra'] = terra

        # Aggiorna il file JSON
        with open("Gioco di Scopa/partita.json", "w") as file:
            json.dump(dati, file)

        print(self.data)
        retroooo = []
        retroooo.append(carta_retro)
        self.data["retro"] = retroooo
        print(self.data)

        # Individua la carta della retro
        retro_index = self.data["retro"].index(carta_retro)
        retro_label = self.retro_labels[retro_index]

        # Rimuovi la carta dai retro_labels
        retro_label.hide()
        self.retro_labels.remove(retro_label)

        # Aggiungi una nuova carta con l'immagine corretta
        nuova_carta_label = QLabel(self)
        pixmap = QPixmap(f"Gioco di Scopa/Carte/{carta_retro[1]}/{carta_retro[0]}.png")
        nuova_carta_label.setPixmap(pixmap.scaled(75, 112, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        nuova_carta_label.setProperty('card_id', f"{carta_retro[1]}/{carta_retro[0]}")
        nuova_carta_label.setGeometry(retro_label.geometry())
        nuova_carta_label.show()

        def create_animation_group():
            if carte_prese:
                # Anima la nuova carta verso il basso e ingrandirla
                self.retro_animation = QPropertyAnimation(nuova_carta_label, b"geometry")
                self.retro_animation.setDuration(1000)
                end_rect_terra = QRectF(self.width() / 2 - 50, self.height() / 2 - 300, 100, 150)
                self.retro_animation.setStartValue(nuova_carta_label.geometry())
                self.retro_animation.setEndValue(end_rect_terra)
                self.retro_animation.setEasingCurve(QEasingCurve.InOutQuad)
                self.retro_animation.valueChanged.connect(lambda _, l=nuova_carta_label: update_pixmap(l, QPixmap(f"Gioco di Scopa/Carte/{l.property('card_id')}.png")))

                # Animazioni per carte a terra
                self.terra_animations = []
                for carta_terra in carte_prese:
                    terra_index = self.data["terra"].index(carta_terra)
                    terra_label = self.terra_labels[terra_index]
                    terra_animation = QPropertyAnimation(terra_label, b"geometry")
                    terra_animation.setDuration(1000)
                    terra_animation.setStartValue(terra_label.geometry())
                    terra_animation.setEndValue(end_rect_terra)
                    terra_animation.setEasingCurve(QEasingCurve.InOutQuad)
                    self.terra_animations.append(terra_animation)

                # Animazione generale
                self.group_animation = QParallelAnimationGroup()
                self.group_animation.addAnimation(self.retro_animation)
                for terra_animation in self.terra_animations:
                    self.group_animation.addAnimation(terra_animation)

                # Sposta le carte verso le coordinate (500, -200) e ridimensionale
                self.retro_animation2 = QPropertyAnimation(nuova_carta_label, b"geometry")
                self.retro_animation2.setDuration(1000)
                self.retro_animation2.setStartValue(end_rect_terra)
                self.retro_animation2.setEndValue(QRectF(500, -200, 60, 90))
                self.retro_animation2.setEasingCurve(QEasingCurve.InOutQuad)
                self.retro_animation2.valueChanged.connect(lambda _, l=nuova_carta_label: update_pixmap(l, QPixmap(f"Gioco di Scopa/Carte/{l.property('card_id')}.png")))

                self.terra_animations2 = []
                for carta_terra in carte_prese:
                    terra_index = self.data["terra"].index(carta_terra)
                    terra_label = self.terra_labels[terra_index]
                    terra_animation2 = QPropertyAnimation(terra_label, b"geometry")
                    terra_animation2.setDuration(1000)
                    terra_animation2.setStartValue(end_rect_terra)
                    terra_animation2.setEndValue(QRectF(500, -200, 60, 90))
                    terra_animation2.setEasingCurve(QEasingCurve.InOutQuad)
                    terra_animation2.valueChanged.connect(lambda _, l=terra_label: update_pixmap(l, QPixmap(f"Gioco di Scopa/Carte/{l.property('card_id')}.png")))
                    self.terra_animations2.append(terra_animation2)

                self.group_animation2 = QParallelAnimationGroup()
                self.group_animation2.addAnimation(self.retro_animation2)
                for terra_animation2 in self.terra_animations2:
                    self.group_animation2.addAnimation(terra_animation2)

                self.presa_animation = QPropertyAnimation(self.presa_label2, b"geometry")
                self.presa_animation.setDuration(1000)
                start_rect = self.presa_label2.geometry()
                self.presa_animation.setStartValue(start_rect)
                self.presa_animation.setEndValue(QRectF(420, -30, 60, 90))
                self.presa_animation.setEasingCurve(QEasingCurve.InOutQuad)

                self.group_animation3 = QSequentialAnimationGroup()
                self.group_animation3.addAnimation(self.group_animation)
                self.group_animation3.addAnimation(self.group_animation2)
                self.group_animation3.addAnimation(self.presa_animation)

                self.group_animation3.finished.connect(lambda: self.cleanup_labels2([nuova_carta_label], [self.terra_labels[self.data["terra"].index(carta)] for carta in carte_prese]))
                self.group_animation3.finished.connect(realign_cards_wrapper)
                self.group_animation3.finished.connect(self.on_animation_finished)

                return self.group_animation3
            else:
                # Anima la nuova carta verso il basso e ingrandirla
                self.retro_animation = QPropertyAnimation(nuova_carta_label, b"geometry")
                self.retro_animation.setDuration(1000)
                end_rect_terra = QRectF(self.width() / 2 - 50, self.height() / 2 - 300, 100, 150)
                self.retro_animation.setStartValue(nuova_carta_label.geometry())
                self.retro_animation.setEndValue(end_rect_terra)
                self.retro_animation.setEasingCurve(QEasingCurve.InOutQuad)
                self.retro_animation.valueChanged.connect(lambda _, l=nuova_carta_label: update_pixmap(l, QPixmap(f"Gioco di Scopa/Carte/{l.property('card_id')}.png")))

                # Aggiungi la carta a terra dopo l'animazione
                def add_card_to_terra():
                    self.data["terra"].append(carta_retro)
                    self.terra_labels.append(nuova_carta_label)
                    nuova_carta_label.setParent(self)
                    nuova_carta_label.show()

                    # Imposta gli eventi di hover e fine per la nuova carta
                    terra_start_x = int(self.width() / 2 - (len(self.terra_labels) * 100 + (len(self.terra_labels) - 1) * 10) / 2)
                    terra_y = self.height() // 2 - 150
                    i = self.terra_labels.index(nuova_carta_label)
                    nuova_carta_label.hover_rect = QRectF(terra_start_x + i * 110, terra_y + 20, 100, 150)
                    nuova_carta_label.end_rect = QRectF(terra_start_x + i * 110, terra_y, 100, 150)
                    nuova_carta_label.enterEvent = lambda event, lbl=nuova_carta_label: self.on_card_hover_enter(event, lbl)
                    nuova_carta_label.leaveEvent = lambda event, lbl=nuova_carta_label: self.on_card_hover_leave(event, lbl)

                    realign_cards_wrapper()

                self.retro_animation.finished.connect(add_card_to_terra)
                self.retro_animation.finished.connect(self.on_animation_finished)

                return self.retro_animation

        animation = create_animation_group()
        self.animation_queue.append(animation)
        
        self.start_next_animation()

    def realign_cards2(self):
        self.realign_animation = QParallelAnimationGroup()

        # Aggiungi una label trasparente che copre tutto
        self.cover_labell = QLabel(self)
        self.cover_labell.setGeometry(0, 0, self.width(), self.height())
        self.cover_labell.setStyleSheet("background-color: rgba(0, 0, 0, 1%);")
        self.cover_labell.show()

        # Filtra le carte rimanenti nella retro e a terra
        retro_remaining = [label for label in self.retro_labels if label.isVisible()]
        terra_remaining = [label for label in self.terra_labels if label.isVisible()]

        # Calcola la nuova posizione per le carte rimanenti nella retro
        retro_width = len(retro_remaining) * 75 + (len(retro_remaining) - 1) * 10
        retro_start_x = (self.width() - retro_width) // 2
        for i, label in enumerate(retro_remaining):
            anim = QPropertyAnimation(label, b"geometry")
            anim.setDuration(1000)
            anim.setStartValue(label.geometry())
            anim.setEndValue(QRect(retro_start_x + i * 75, 10, 75, 112))
            self.realign_animation.addAnimation(anim)

        # Calcola la nuova posizione per le carte rimanenti a terra
        terra_width = len(terra_remaining) * 100 + (len(terra_remaining) - 1) * 10
        terra_start_x = (self.width() - terra_width) // 2
        terra_y = self.height() // 2 - 150
        for i, label in enumerate(terra_remaining):
            anim = QPropertyAnimation(label, b"geometry")
            anim.setDuration(1000)
            anim.setStartValue(label.geometry())
            anim.setEndValue(QRect(terra_start_x + i * 110, terra_y, 100, 150))
            self.realign_animation.addAnimation(anim)
            # Aggiorna le posizioni di hover e fine
            label.hover_rect = QRectF(terra_start_x + i * 110, terra_y + 20, 100, 150)
            label.end_rect = QRectF(terra_start_x + i * 110, terra_y, 100, 150)

        # Aggiungi l'animazione della scopa se non ci sono più carte a terra
        if not terra_remaining:
            scopa_animation = self.create_scopa_animation2()
            self.realign_animation.addAnimation(scopa_animation)
        
        self.realign_animation.finished.connect(lambda: self.cover_labell.hide())
        self.realign_animation.finished.connect(self.remove_cover_label)
        self.realign_animation.start()

    def cleanup_labels2(self, retro_labels_to_remove, terra_labels_to_remove):
        for label in retro_labels_to_remove:
            label.hide()
        for label in terra_labels_to_remove:
            label.hide()
        for label in self.retro_labels + self.terra_labels:
            label.setEnabled(True)

    def create_scopa_animation2(self):
        def update_pixmap(label, pixmap):
            label.setPixmap(pixmap.scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        # Creazione di un'etichetta per lo sfondo trasparente rosso che copre tutto lo schermo
        background_label = QLabel(self)
        background_label.setGeometry(0, 0, self.width(), self.height())
        background_label.setStyleSheet("background-color: rgba(255, 0, 0, 100);")
        background_label.show()

        # Creazione di un'etichetta per l'immagine della scopa
        scopa_label = QLabel(self)
        scopa_pixmap = QPixmap("Gioco di Scopa/Icone/Scopa.png")
        scopa_label.setGeometry((self.width() - 600) // 2, (self.height() - 140) // 2, 600, 140)
        update_pixmap(scopa_label, scopa_pixmap)
        scopa_label.show()

        # Nascondi le etichette dopo 1.5 secondi
        QTimer.singleShot(1700, background_label.hide)
        QTimer.singleShot(1700, scopa_label.hide)

        # Ottieni il valore attuale dell'etichetta dei punti
        punti_attuali = int(self.label_punti_cattivo.text())

        # Incrementa i punti
        punti_attuali += 1

        # Aggiorna l'etichetta dei punti
        self.label_punti_cattivo.setText(str(punti_attuali))

        # Forza l'aggiornamento dell'interfaccia utente
        self.label_punti_cattivo.repaint()

        # Crea un'animazione vuota che dura quanto l'etichetta della scopa è visibile
        animation = QPropertyAnimation(scopa_label, b"opacity")
        animation.setDuration(1700)
        animation.setStartValue(1)
        animation.setEndValue(1)

        return animation

    def remove_cover_label(self):
        if hasattr(self, 'cover_label'):
            self.cover_label.hide()
            self.cover_label.deleteLater()
            del self.cover_label

    @pyqtSlot(list, list, list, int)
    def aggiorna_tutto_quanto2(self, terra, carta_retro, carte_prese, numero):
        self.aggiorna_tutto_quantoo2(terra, carta_retro, carte_prese, numero)

    def aggiorna_tutto_quantoo2(self, terra, carta_retro, carte_prese, numero):

        labels = ['cover_label', 'cover_label2', 'center_image_label']
        for label in labels:
            if hasattr(self, label):
                try:
                    label_attr = getattr(self, label)
                    label_attr.hide()
                    label_attr.deleteLater()
                    delattr(self, label)
                except RuntimeError as e:
                    print(f"RuntimeError for {label}: {e}")
                except AttributeError as e:
                    print(f"AttributeError for {label}: {e}")

                
        def update_pixmap(label, pixmap):
            label.setPixmap(pixmap.scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        def realign_cards_wrapper2():
            self.realign_cards22()

        # Aggiungi una label trasparente che copre tutto
        self.cover_label = QLabel(self)
        self.cover_label.setGeometry(0, 0, self.width(), self.height())
        self.cover_label.setStyleSheet("background-color: rgba(0, 0, 0, 1%);")
        self.cover_label.show()

        with open("Gioco di Scopa/partita.json", "r") as file:
            dati = json.load(file)
        dati['terra'] = terra

        # Aggiorna il file JSON
        with open("Gioco di Scopa/partita.json", "w") as file:
            json.dump(dati, file)

        print(self.data)
        retroooo = []
        retroooo.append(carta_retro)
        self.data["retro"] = retroooo
        print(self.data)

        # Individua la carta della retro
        retro_index = self.data["retro"].index(carta_retro)
        retro_label = self.retro_labels[retro_index]

        # Rimuovi la carta dai retro_labels
        retro_label.hide()
        self.retro_labels.remove(retro_label)

        # Aggiungi una nuova carta con l'immagine corretta
        nuova_carta_label = QLabel(self)
        pixmap = QPixmap(f"Gioco di Scopa/Carte/{carta_retro[1]}/{carta_retro[0]}.png")
        nuova_carta_label.setPixmap(pixmap.scaled(75, 112, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        nuova_carta_label.setProperty('card_id', f"{carta_retro[1]}/{carta_retro[0]}")
        nuova_carta_label.setGeometry(retro_label.geometry())
        nuova_carta_label.show()

        def create_animation_group():
            # Anima la nuova carta verso il basso e ingrandirla
            self.retro_animation = QPropertyAnimation(nuova_carta_label, b"geometry")
            self.retro_animation.setDuration(1000)
            end_rect_terra = QRectF(self.width() / 2 - 50, self.height() / 2 - 300, 100, 150)
            self.retro_animation.setStartValue(nuova_carta_label.geometry())
            self.retro_animation.setEndValue(end_rect_terra)
            self.retro_animation.setEasingCurve(QEasingCurve.InOutQuad)
            self.retro_animation.valueChanged.connect(lambda _, l=nuova_carta_label: update_pixmap(l, QPixmap(f"Gioco di Scopa/Carte/{l.property('card_id')}.png")))

            # Animazioni per carte a terra
            self.terra_animations = []
            for carta_terra in carte_prese:
                terra_index = self.data["terra"].index(carta_terra)
                terra_label = self.terra_labels[terra_index]
                terra_animation = QPropertyAnimation(terra_label, b"geometry")
                terra_animation.setDuration(1000)
                terra_animation.setStartValue(terra_label.geometry())
                terra_animation.setEndValue(end_rect_terra)
                terra_animation.setEasingCurve(QEasingCurve.InOutQuad)
                self.terra_animations.append(terra_animation)

            # Animazione generale
            self.group_animation = QParallelAnimationGroup()
            self.group_animation.addAnimation(self.retro_animation)
            for terra_animation in self.terra_animations:
                self.group_animation.addAnimation(terra_animation)

            # Sposta le carte verso le coordinate (500, -200) e ridimensionale
            self.retro_animation2 = QPropertyAnimation(nuova_carta_label, b"geometry")
            self.retro_animation2.setDuration(1000)
            self.retro_animation2.setStartValue(end_rect_terra)
            self.retro_animation2.setEndValue(QRectF(500, -200, 60, 90))
            self.retro_animation2.setEasingCurve(QEasingCurve.InOutQuad)
            self.retro_animation2.valueChanged.connect(lambda _, l=nuova_carta_label: update_pixmap(l, QPixmap(f"Gioco di Scopa/Carte/{l.property('card_id')}.png")))

            self.terra_animations2 = []
            for carta_terra in carte_prese:
                terra_index = self.data["terra"].index(carta_terra)
                terra_label = self.terra_labels[terra_index]
                terra_animation2 = QPropertyAnimation(terra_label, b"geometry")
                terra_animation2.setDuration(1000)
                terra_animation2.setStartValue(end_rect_terra)
                terra_animation2.setEndValue(QRectF(500, -200, 60, 90))
                terra_animation2.setEasingCurve(QEasingCurve.InOutQuad)
                terra_animation2.valueChanged.connect(lambda _, l=terra_label: update_pixmap(l, QPixmap(f"Gioco di Scopa/Carte/{l.property('card_id')}.png")))
                self.terra_animations2.append(terra_animation2)

            self.group_animation2 = QParallelAnimationGroup()
            self.group_animation2.addAnimation(self.retro_animation2)
            for terra_animation2 in self.terra_animations2:
                self.group_animation2.addAnimation(terra_animation2)

            self.presa_animation = QPropertyAnimation(self.presa_label2, b"geometry")
            self.presa_animation.setDuration(1000)
            start_rect = self.presa_label2.geometry()
            self.presa_animation.setStartValue(start_rect)
            self.presa_animation.setEndValue(QRectF(420, -30, 60, 90))
            self.presa_animation.setEasingCurve(QEasingCurve.InOutQuad)

            self.group_animation3 = QSequentialAnimationGroup()
            self.group_animation3.addAnimation(self.group_animation)
            self.group_animation3.addAnimation(self.group_animation2)
            self.group_animation3.addAnimation(self.presa_animation)

            self.group_animation3.finished.connect(lambda: self.cleanup_labels2([nuova_carta_label], [self.terra_labels[self.data["terra"].index(carta)] for carta in carte_prese]))
            self.group_animation3.finished.connect(realign_cards_wrapper2)
            self.group_animation3.finished.connect(self.on_animation_finished)

            return self.group_animation3

        animation = create_animation_group()
        self.animation_queue.append(animation)
        
        self.start_next_animation()

    def realign_cards22(self):
        self.realign_animation = QParallelAnimationGroup()

        # Aggiungi una label trasparente che copre tutto
        self.cover_labell = QLabel(self)
        self.cover_labell.setGeometry(0, 0, self.width(), self.height())
        self.cover_labell.setStyleSheet("background-color: rgba(0, 0, 0, 1%);")
        self.cover_labell.show()

        # Filtra le carte rimanenti nella retro e a terra
        retro_remaining = [label for label in self.retro_labels if label.isVisible()]
        terra_remaining = [label for label in self.terra_labels if label.isVisible()]

        # Calcola la nuova posizione per le carte rimanenti nella retro
        retro_width = len(retro_remaining) * 75 + (len(retro_remaining) - 1) * 10
        retro_start_x = (self.width() - retro_width) // 2
        for i, label in enumerate(retro_remaining):
            anim = QPropertyAnimation(label, b"geometry")
            anim.setDuration(1000)
            anim.setStartValue(label.geometry())
            anim.setEndValue(QRect(retro_start_x + i * 75, 10, 75, 112))
            self.realign_animation.addAnimation(anim)

        # Calcola la nuova posizione per le carte rimanenti a terra
        terra_width = len(terra_remaining) * 100 + (len(terra_remaining) - 1) * 10
        terra_start_x = (self.width() - terra_width) // 2
        terra_y = self.height() // 2 - 150
        for i, label in enumerate(terra_remaining):
            anim = QPropertyAnimation(label, b"geometry")
            anim.setDuration(1000)
            anim.setStartValue(label.geometry())
            anim.setEndValue(QRect(terra_start_x + i * 110, terra_y, 100, 150))
            self.realign_animation.addAnimation(anim)
            # Aggiorna le posizioni di hover e fine
            label.hover_rect = QRectF(terra_start_x + i * 110, terra_y + 20, 100, 150)
            label.end_rect = QRectF(terra_start_x + i * 110, terra_y, 100, 150)
        
        self.realign_animation.finished.connect(lambda: self.cover_labell.hide())
        self.realign_animation.finished.connect(self.remove_cover_label)
        self.realign_animation.start()


    def aggiorna_tutto_quanto_fine(self, carte_prese):
            
        labels = ['cover_label', 'cover_label2', 'center_image_label', 'retro_labels', 'cover_label3', 'cover_label2', 'center_image_label2']
        for label in labels:
            if hasattr(self, label):
                try:
                    label_attr = getattr(self, label)
                    if isinstance(label_attr, list):
                        for lbl in label_attr:
                            lbl.hide()
                            lbl.deleteLater()
                    else:
                        label_attr.hide()
                        label_attr.deleteLater()
                    delattr(self, label)
                except (RuntimeError, AttributeError) as e:
                    print(f"Error for {label}: {e}")

        def update_pixmap(label, pixmap):
            label.setPixmap(pixmap.scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        # Aggiungi una label trasparente che copre tutto
        self.cover_label = QLabel(self)
        self.cover_label.setGeometry(0, 0, self.width(), self.height())
        self.cover_label.setStyleSheet("background-color: rgba(0, 0, 0, 1%);")
        self.cover_label.show()

        with open("Gioco di Scopa/partita.json", "r") as file:
            dati = json.load(file)
        dati['terra'] = []

        # Aggiorna il file JSON
        with open("Gioco di Scopa/partita.json", "w") as file:
            json.dump(dati, file)

        end_rect_terra = QRectF(self.width() / 2 - 50, self.height() / 2 - 300, 100, 150)

        # Animazioni per carte a terra
        self.terra_animations = []
        for carta_terra in carte_prese:
            terra_index = self.data["terra"].index(carta_terra)
            terra_label = self.terra_labels[terra_index]
            terra_animation = QPropertyAnimation(terra_label, b"geometry")
            terra_animation.setDuration(1000)
            terra_animation.setStartValue(terra_label.geometry())
            terra_animation.setEndValue(end_rect_terra)
            terra_animation.setEasingCurve(QEasingCurve.InOutQuad)
            self.terra_animations.append(terra_animation)

        # Animazione generale
        self.group_animation = QParallelAnimationGroup()
        for terra_animation in self.terra_animations:
            self.group_animation.addAnimation(terra_animation)

        self.terra_animations2 = []
        for carta_terra in carte_prese:
            terra_index = self.data["terra"].index(carta_terra)
            terra_label = self.terra_labels[terra_index]
            terra_animation2 = QPropertyAnimation(terra_label, b"geometry")
            terra_animation2.setDuration(1000)
            terra_animation2.setStartValue(end_rect_terra)
            terra_animation2.setEndValue(QRectF(500, -200, 60, 90))
            terra_animation2.setEasingCurve(QEasingCurve.InOutQuad)
            terra_animation2.valueChanged.connect(lambda _, l=terra_label: update_pixmap(l, QPixmap(f"Gioco di Scopa/Carte/{l.property('card_id')}.png")))
            self.terra_animations2.append(terra_animation2)

        self.group_animation2 = QParallelAnimationGroup()
        for terra_animation2 in self.terra_animations2:
            self.group_animation2.addAnimation(terra_animation2)

        self.presa_animation = QPropertyAnimation(self.presa_label2, b"geometry")
        self.presa_animation.setDuration(1000)
        start_rect = self.presa_label2.geometry()
        self.presa_animation.setStartValue(start_rect)
        self.presa_animation.setEndValue(QRectF(420, -30, 60, 90))
        self.presa_animation.setEasingCurve(QEasingCurve.InOutQuad)

        self.group_animation3 = QSequentialAnimationGroup()
        self.group_animation3.addAnimation(self.group_animation)
        self.group_animation3.addAnimation(self.group_animation2)
        self.group_animation3.addAnimation(self.presa_animation)

        self.group_animation3.finished.connect(lambda: self.cleanup_labels2_fine([self.terra_labels[self.data["terra"].index(carta)] for carta in carte_prese]))
        self.group_animation3.finished.connect(self.on_animation_finished)

        self.group_animation3.start()
        
    def cleanup_labels2_fine(self, terra_labels_to_remove):
        for label in terra_labels_to_remove:
            label.hide()
        for label in self.terra_labels:
            label.setEnabled(True)
        self.create_endgame_screen()
        print('se sono passato di qua sono troppissimo forte e ho vinto caciopalla')
        self.countdown_timer3.setSingleShot(True)
        self.countdown_timer3.timeout.connect(lambda: self.create_endgame_data())
        self.countdown_timer3.start(6000)
        print("Completato cleanup_labels2_fine")


    def push_new_data(self, carta_mano, carte_prendibili):
        with open("Gioco di Scopa/partita.json", "r") as file:
            dati = json.load(file)
        
        data_to_send = {
            'terra': dati['terra'],
            'carta_mano': carta_mano,
            'carte_prese': carte_prendibili,
            'numero': dati['numero'],
            'user_name': self.user_name
        }
        try:
            response = requests.post('http://localhost:8080/push_new_data', json=data_to_send)
            if response.status_code == 200:

                with open("Gioco di Scopa/partita.json", "r") as file:
                    dati = json.load(file)

                dati['token']=False
                # Aggiorna il file JSON
                with open("Gioco di Scopa/partita.json", "w") as file:
                    json.dump(dati, file)

                data_to_send = {'user_name': self.user_name}
                try:
                    response = requests.post('http://localhost:8080/con_questo_ho_finito', data=data_to_send)
                    if response.status_code == 200:
                        print(response.json()['finito'])
                        print(response.json()['finito_tutto'])
                        if response.json()['finito'] and response.json()['finito_tutto']:
                            print('se sono passato di qua sono troppissimo forte')
                            pass
                        elif response.json()['finito'] and (not response.json()['finito_tutto']):
                            time.sleep(0.7)
                            print("distribuzione delle nuove carte")
                            data_to_send = {'user_name': self.user_name}
                            try:
                                response = requests.post('http://localhost:8080/distrubuisci_carte_nuove', data=data_to_send)
                                if response.status_code == 200:
                                    print('ok')
                            except requests.exceptions.ConnectionError:
                                pass
                            try:
                                response = requests.post('http://localhost:8080/distrubuisci_carte', data=data_to_send)
                                if response.status_code == 200:
                                    response_json = response.json()
                                    mano_json = json.dumps(response_json['carte_mano'])
                                    def ensure_list(decoded):
                                        while isinstance(decoded, str):
                                            try:
                                                decoded = json.loads(decoded)
                                            except json.JSONDecodeError as e:
                                                print("Error decoding JSON:", e)
                                                return None
                                        return decoded
                                    mano = ensure_list(mano_json)
                                    with open("Gioco di Scopa/partita.json", "r") as file:
                                        dati = json.load(file)
                                    dati['mano'] = mano

                                    # Aggiorna il file JSON
                                    with open("Gioco di Scopa/partita.json", "w") as file:
                                        json.dump(dati, file)
                                    self.countdown_timer.setSingleShot(True)
                                    self.countdown_timer.timeout.connect(lambda: self.setup_ui_elements(mano))
                                    self.countdown_timer.start(4000)
                            except requests.exceptions.ConnectionError:
                                pass
                            time.sleep(0.5)
                            threading.Thread(target=self.run_controlli_asincroni).start()
                        else:
                            threading.Thread(target=self.run_controlli_asincroni).start()
                except requests.exceptions.ConnectionError:
                    pass
        except requests.exceptions.ConnectionError:
            pass

    def push_data(self, carta_mano):
        with open("Gioco di Scopa/partita.json", "r") as file:
            dati = json.load(file)
        
        data_to_send = {
            'terra': dati['terra'],
            'carta_mano': carta_mano,
            'numero': dati['numero'],
            'user_name': self.user_name
        }
        try:
            response = requests.post('http://localhost:8080/push_data', json=data_to_send)
            if response.status_code == 200:

                with open("Gioco di Scopa/partita.json", "r") as file:
                    dati = json.load(file)

                dati['token']=False
                # Aggiorna il file JSON
                with open("Gioco di Scopa/partita.json", "w") as file:
                    json.dump(dati, file)

                data_to_send = {'user_name': self.user_name}
                try:
                    response = requests.post('http://localhost:8080/con_questo_ho_finito', data=data_to_send)
                    if response.status_code == 200:
                        print(response.json()['finito'])
                        print(response.json()['finito_tutto'])
                        if response.json()['finito'] and response.json()['finito_tutto']:
                            with open("Gioco di Scopa/partita.json", "r") as file:
                                ct = json.load(file)['terra']
                            self.countdown_timer.setSingleShot(True)
                            self.countdown_timer.timeout.connect(lambda: self.aggiorna_tutto_quanto_fine(ct))
                            self.countdown_timer.start(4000)
                            print('se sono passato di qua sono troppissimo forte')
                        elif response.json()['finito'] and (not response.json()['finito_tutto']):
                            time.sleep(0.6)
                            print("distribuzione delle nuove carte")
                            data_to_send = {'user_name': self.user_name}
                            try:
                                response = requests.post('http://localhost:8080/distrubuisci_carte_nuove', data=data_to_send)
                                if response.status_code == 200:
                                    print('ok')
                            except requests.exceptions.ConnectionError:
                                pass
                            try:
                                response = requests.post('http://localhost:8080/distrubuisci_carte', data=data_to_send)
                                if response.status_code == 200:
                                    response_json = response.json()
                                    mano_json = json.dumps(response_json['carte_mano'])
                                    def ensure_list(decoded):
                                        while isinstance(decoded, str):
                                            try:
                                                decoded = json.loads(decoded)
                                            except json.JSONDecodeError as e:
                                                print("Error decoding JSON:", e)
                                                return None
                                        return decoded
                                    mano = ensure_list(mano_json)
                                    with open("Gioco di Scopa/partita.json", "r") as file:
                                        dati = json.load(file)
                                    dati['mano'] = mano

                                    # Aggiorna il file JSON
                                    with open("Gioco di Scopa/partita.json", "w") as file:
                                        json.dump(dati, file)
                                    self.countdown_timer.setSingleShot(True)
                                    self.countdown_timer.timeout.connect(lambda: self.setup_ui_elements(mano))
                                    self.countdown_timer.start(3000)
                            except requests.exceptions.ConnectionError:
                                pass
                            time.sleep(0.5)
                            threading.Thread(target=self.run_controlli_asincroni).start()
                        else:
                            threading.Thread(target=self.run_controlli_asincroni).start()
                except requests.exceptions.ConnectionError:
                    pass
        except requests.exceptions.ConnectionError:
            pass


    def get_carte_a_terra(self):
        # Legge le carte a terra dal file JSON
        with open("Gioco di Scopa/partita.json", "r") as file:
            partita_data = json.load(file)
        return partita_data["terra"]

    def show_combination_options(self, carta_mano, combinazioni):
        # Crea un widget centrale per contenere le opzioni
        self.options_widget = QWidget(self)
        self.options_widget.setStyleSheet("background: rgba(0, 0, 0, 0.5); border-radius: 10px;")
        self.options_layout = QVBoxLayout(self.options_widget)

        for combinazione in combinazioni:
            option_label = QLabel(self.options_widget)
            
            # Creare l'immagine di combinazione con il segno "+"
            combined_pixmap = self.create_combined_pixmap(combinazione)
            
            option_label.setPixmap(combined_pixmap)
            option_label.setAlignment(Qt.AlignCenter)
            option_label.mousePressEvent = lambda event, combo=combinazione: self.on_combination_selected(carta_mano, combo)
            self.options_layout.addWidget(option_label)

        # Ridimensiona e posiziona il widget centrale
        self.options_widget.setFixedSize(600, 1000)
        self.options_widget.move((self.width() - self.options_widget.width()) // 2, 
                                (self.height() - self.options_widget.height()) // 2)
        self.options_widget.show()

    def create_combined_pixmap(self, combinazione):
        # Carica le immagini delle carte e crea un pixmap combinato con segni "+"
        card_images = [QPixmap(f"Gioco di Scopa/Carte/{c[1]}/{c[0]}.png").scaled(100, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation) for c in combinazione]
        plus_sign = QPixmap(30, 30)
        plus_sign.fill(Qt.transparent)

        # Disegna il segno "+" bianco su un pixmap trasparente
        painter = QPainter(plus_sign)
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(QFont("Arial", 20))
        painter.drawText(plus_sign.rect(), Qt.AlignCenter, "+")
        painter.end()

        width = sum(image.width() for image in card_images) + (len(card_images) - 1) * plus_sign.width()
        height = max(image.height() for image in card_images)
        combined_pixmap = QPixmap(width, height)
        combined_pixmap.fill(Qt.transparent)  # Rendi lo sfondo trasparente

        painter = QPainter(combined_pixmap)
        x_offset = 0
        for i, image in enumerate(card_images):
            painter.drawPixmap(x_offset, 0, image)
            x_offset += image.width()
            if i < len(card_images) - 1:
                painter.drawPixmap(x_offset, (height - plus_sign.height()) // 2, plus_sign)
                x_offset += plus_sign.width()
        painter.end()

        return combined_pixmap

    def on_combination_selected(self, carta_mano, combinazione):
        # Nascondi tutte le opzioni e rimuovi il widget centrale
        self.options_widget.hide()
        self.options_widget.deleteLater()
        self.options_widget = None

        # Prendi le carte
        self.prendi_carte(carta_mano, combinazione)
        self.start_move_animation(carta_mano, combinazione)
        self.push_new_data(carta_mano, combinazione)

    def get_carte_prendibili(self, card_id, carte_a_terra):
        # Inizializza una lista vuota per le carte prendibili
        carte_prendibili = []

        # Estrai il valore dalla tupla card_id
        valore = int(card_id[1])

        # Controlla se la carta cliccata può prendere una singola carta a terra con lo stesso valore
        for carta in carte_a_terra:
            valore_terra = int(carta[0])
            if valore == valore_terra:
                print(valore_terra)
                carte_prendibili.append([carta])

        # Controlla se la carta cliccata può prendere combinazioni di carte a terra
        # che sommano al suo valore
        for i in range(2, len(carte_a_terra) + 1):
            for combo in combinations(carte_a_terra, i):
                if sum(int(c[0]) for c in combo) == valore:
                    carte_prendibili.append(list(combo))
                    print(combo)

        # Restituisce la lista delle carte prendibili
        print(carte_prendibili)
        return carte_prendibili

    def prendi_carte(self, carta_mano, carte_prendibili):
        # Implementa la logica per prendere le carte dal tavolo
        # Questo è un esempio, dovrai adattarlo alle regole del tuo gioco
        self.rimuovi_carta_da_mano(carta_mano)
        for carta in carte_prendibili:
            self.rimuovi_carta_da_terra(carta)
        # Aggiorna il punteggio o lo stato del gioco se necessario

    def rimuovi_carta_da_terra(self, carta):
        with open("Gioco di Scopa/partita.json", "r") as file:
            dati = json.load(file)
        # Rimuove la carta specificata dall'elenco delle carte a terra
        # Questo è un esempio, dovrai adattarlo alle regole del tuo gioco
        dati['terra'].remove(carta)
        dati['presa'].append(carta)
        # Aggiorna il file JSON
        with open("Gioco di Scopa/partita.json", "w") as file:
            json.dump(dati, file)

    def rimuovi_carta_da_mano(self, carta):
        with open("Gioco di Scopa/partita.json", "r") as file:
            dati = json.load(file)
        # Rimuove la carta specificata dall'elenco delle carte a terra
        # Questo è un esempio, dovrai adattarlo alle regole del tuo gioco
        dati['mano'].remove(carta)
        dati['presa'].append(carta)
        # Aggiorna il file JSON
        with open("Gioco di Scopa/partita.json", "w") as file:
            json.dump(dati, file)
    
    def metti_a_terra(self, carta):
        with open("Gioco di Scopa/partita.json", "r") as file:
            dati = json.load(file)
        # Rimuove la carta specificata dall'elenco delle carte a terra
        # Questo è un esempio, dovrai adattarlo alle regole del tuo gioco
        dati['mano'].remove(carta)
        dati['terra'].append(carta)
        # Aggiorna il file JSON
        with open("Gioco di Scopa/partita.json", "w") as file:
            json.dump(dati, file)
    

    def realign_cards(self):
        self.realign_animation = QParallelAnimationGroup()

        # Filtra le carte rimanenti nella mano e a terra
        mano_remaining = [label for label in self.mano_labels if label.isVisible()]
        terra_remaining = [label for label in self.terra_labels if label.isVisible()]

        # Calcola la nuova posizione per le carte rimanenti nella mano
        mano_width = len(mano_remaining) * 150 + (len(mano_remaining) - 1) * 10
        mano_start_x = (self.width() - mano_width) // 2
        mano_y = self.height() - 225
        for i, label in enumerate(mano_remaining):
            anim = QPropertyAnimation(label, b"geometry")
            anim.setDuration(1000)
            anim.setStartValue(label.geometry())
            anim.setEndValue(QRect(mano_start_x + i * 160, mano_y, 150, 225))
            self.realign_animation.addAnimation(anim)
            # Aggiorna le posizioni di hover e fine
            label.hover_rect = QRectF(mano_start_x + i * 160, mano_y - 20, 150, 225)
            label.end_rect = QRectF(mano_start_x + i * 160, mano_y, 150, 225)

        # Calcola la nuova posizione per le carte rimanenti a terra
        terra_width = len(terra_remaining) * 100 + (len(terra_remaining) - 1) * 10
        terra_start_x = (self.width() - terra_width) // 2
        terra_y = self.height() // 2 - 150
        for i, label in enumerate(terra_remaining):
            anim = QPropertyAnimation(label, b"geometry")
            anim.setDuration(1000)
            anim.setStartValue(label.geometry())
            anim.setEndValue(QRect(terra_start_x + i * 110, terra_y, 100, 150))
            self.realign_animation.addAnimation(anim)
            # Aggiorna le posizioni di hover e fine
            label.hover_rect = QRectF(terra_start_x + i * 110, terra_y + 20, 100, 150)
            label.end_rect = QRectF(terra_start_x + i * 110, terra_y, 100, 150)

        # Aggiungi l'animazione della scopa se non ci sono più carte a terra
        if not terra_remaining:
            scopa_animation = self.create_scopa_animation()
            self.realign_animation.addAnimation(scopa_animation)

        self.realign_animation.finished.connect(self.remove_cover_label)
        self.realign_animation.start()

    def create_scopa_animation(self):
        scopa_label = QLabel(self)
        scopa_label.setPixmap(QPixmap("Gioco di Scopa/Icone/Scopa.png"))
        scopa_label.setScaledContents(True)
        scopa_label.setGeometry((self.width() - 600) // 2, (self.height() - 200) // 2, 600, 140)
        scopa_label.setStyleSheet("background: transparent;")
        scopa_label.show()

        # Nascondi l'etichetta dopo 1.5 secondi
        QTimer.singleShot(1700, scopa_label.hide)

        # Aggiorna i punti nel file JSON e l'etichetta dei punti
        with open("Gioco di Scopa/partita.json", "r") as file:
            dati = json.load(file)

        # Incrementa i punti
        dati['punti'] += 1

        # Aggiorna l'etichetta dei punti
        self.label_punti.setText(str(dati['punti']))

        # Forza l'aggiornamento dell'interfaccia utente
        self.label_punti.repaint()

        # Aggiorna il file JSON
        with open("Gioco di Scopa/partita.json", "w") as file:
            json.dump(dati, file)

        # Crea un'animazione vuota che dura quanto l'etichetta della scopa è visibile
        animation = QPropertyAnimation(scopa_label, b"opacity")
        animation.setDuration(1700)
        animation.setStartValue(1)
        animation.setEndValue(1)

        return animation


    def start_move_animation(self, carta_mano, carte_terra_interessate):
        def update_pixmap(label, pixmap):
            label.setPixmap(pixmap.scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        def realign_cards_wrapper():
            self.realign_cards()

        # Aggiungi la sovrapposizione di stile per il label semitrasparente
        self.cover_label = QLabel(self)
        self.cover_label.resize(self.width(), self.height())
        self.cover_label.setStyleSheet("background-color: rgba(0, 0, 0, 1%);")
        self.cover_label.show()

        print(carta_mano)

        # Carta della mano
        mano_index = self.data["mano"].index(carta_mano)
        mano_label = self.mano_labels[mano_index]

        self.mano_animation = QPropertyAnimation(mano_label, b"geometry")
        self.mano_animation.setDuration(1000)
        start_rect = mano_label.geometry()
        self.mano_animation.setStartValue(start_rect)
        end_rect = QRectF(self.width() / 2 - 50, self.height() / 2 - 75, 100, 150)
        self.mano_animation.setEndValue(end_rect)
        self.mano_animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.mano_animation.valueChanged.connect(lambda _, l=mano_label: update_pixmap(l, QPixmap(f"Gioco di Scopa/Carte/{l.property('card_id')}.png")))

        # Carte a terra
        self.terra_animations = []
        for carta_terra in carte_terra_interessate:
            terra_index = self.data["terra"].index(carta_terra)
            terra_label = self.terra_labels[terra_index]
            terra_animation = QPropertyAnimation(terra_label, b"geometry")
            terra_animation.setDuration(1000)
            start_rect = terra_label.geometry()
            terra_animation.setStartValue(start_rect)
            terra_animation.setEndValue(end_rect)
            terra_animation.setEasingCurve(QEasingCurve.InOutQuad)
            self.terra_animations.append(terra_animation)

        # Animazione generale
        self.group_animation = QParallelAnimationGroup()
        self.group_animation.addAnimation(self.mano_animation)
        for terra_animation in self.terra_animations:
            self.group_animation.addAnimation(terra_animation)

        # Carta della mano
        self.mano_animation2 = QPropertyAnimation(mano_label, b"geometry")
        self.mano_animation2.setDuration(1000)
        self.mano_animation2.setStartValue(end_rect)
        self.mano_animation2.setEndValue(QRectF(-100, 1000, 100, 150))
        self.mano_animation2.setEasingCurve(QEasingCurve.InOutQuad)

        # Carte a terra
        self.terra_animations2 = []
        for carta_terra in carte_terra_interessate:
            terra_index = self.data["terra"].index(carta_terra)
            terra_label = self.terra_labels[terra_index]
            terra_animation2 = QPropertyAnimation(terra_label, b"geometry")
            terra_animation2.setDuration(1000)
            terra_animation2.setStartValue(end_rect)
            terra_animation2.setEndValue(QRectF(-100, 1000, 100, 150))
            terra_animation2.setEasingCurve(QEasingCurve.InOutQuad)
            self.terra_animations2.append(terra_animation2)

        # Animazione generale
        self.group_animation2 = QParallelAnimationGroup()
        self.group_animation2.addAnimation(self.mano_animation2)
        for terra_animation2 in self.terra_animations2:
            self.group_animation2.addAnimation(terra_animation2)

        self.presa_animation = QPropertyAnimation(self.presa_label, b"geometry")
        self.presa_animation.setDuration(1000)
        start_rect = self.presa_label.geometry()
        self.presa_animation.setStartValue(start_rect)
        self.presa_animation.setEndValue(QRectF(-15, 860, 100, 150))
        self.presa_animation.setEasingCurve(QEasingCurve.InOutQuad)

        self.group_animation3 = QSequentialAnimationGroup()
        self.group_animation3.addAnimation(self.group_animation)
        self.group_animation3.addAnimation(self.group_animation2)
        self.group_animation3.addAnimation(self.presa_animation)

        # Inizia l'animazione
        self.cover_animation = QPropertyAnimation(self.cover_label, b"opacity")
        self.cover_animation.setStartValue(0)
        self.cover_animation.setEndValue(1)
        self.cover_animation.finished.connect(lambda: self.group_animation3.start())

        self.group_animation3.finished.connect(lambda: self.cleanup_labels([mano_label], [self.terra_labels[self.data["terra"].index(carta)] for carta in carte_terra_interessate]))
        self.group_animation3.finished.connect(realign_cards_wrapper)

        self.cover_animation.start()

    def remove_cover_label(self):
        try:
            if hasattr(self, 'cover_label') and self.cover_label is not None:
                self.cover_label.hide()
                self.cover_label.deleteLater()
                self.cover_label = None
        except RuntimeError:
            pass


    def cleanup_labels(self, mano_labels_to_remove, terra_labels_to_remove):
        for label in mano_labels_to_remove:
            label.hide()
        for label in terra_labels_to_remove:
            label.hide()
        for label in self.mano_labels + self.terra_labels:
            label.setEnabled(True)


    def start_move_animation2(self, carta_mano):
        def update_pixmap(label, pixmap):
            label.setPixmap(pixmap.scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        def realign_cards_wrapper():
            self.realign_cards()

        # Aggiungi la sovrapposizione di stile per il label semitrasparente
        self.cover_label = QLabel(self)  # Rinomina la cover_label per evitare conflitti
        self.cover_label.resize(self.width(), self.height())
        self.cover_label.setStyleSheet("background-color: rgba(0, 0, 0, 1%);")
        self.cover_label.show()

        print(carta_mano)

        # Individua la carta della mano
        mano_index = self.data["mano"].index(carta_mano)
        mano_label = self.mano_labels[mano_index]

        # Anima la carta dalla mano a terra
        self.move_animation = QPropertyAnimation(mano_label, b"geometry")
        self.move_animation.setDuration(1000)
        start_rect = mano_label.geometry()
        end_rect = QRectF(self.width() / 2 - 50, self.height() / 2 - 75, 100, 150)  # Posizione centrale per l'animazione
        self.move_animation.setStartValue(start_rect)
        self.move_animation.setEndValue(end_rect)
        self.move_animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.move_animation.valueChanged.connect(lambda _, l=mano_label: update_pixmap(l, QPixmap(f"Gioco di Scopa/Carte/{l.property('card_id')}.png")))

        # Aggiungi la carta a terra dopo l'animazione
        def add_card_to_terra():
            try:
                if carta_mano in self.data["mano"]:
                    self.data["mano"].remove(carta_mano)
                else:
                    print(f"Warning: carta_mano {carta_mano} not in self.data['mano']")

                if mano_label in self.mano_labels:
                    self.mano_labels.remove(mano_label)
                else:
                    print(f"Warning: mano_label {mano_label} not in self.mano_labels")

                self.data["terra"].append(carta_mano)
                self.terra_labels.append(mano_label)
                mano_label.setParent(self)
                mano_label.show()
                realign_cards_wrapper()

            except Exception as e:
                print(f"Error in add_card_to_terra: {e}")


        self.move_animation.finished.connect(add_card_to_terra)

        # Inizia l'animazione
        self.cover_animation = QPropertyAnimation(self.cover_label, b"windowOpacity")
        self.cover_animation.setStartValue(0)
        self.cover_animation.setEndValue(1)
        self.cover_animation.finished.connect(lambda: self.move_animation.start())

        self.cover_animation.start()


    def start_move_animation_fine(self, carte_terra_interessate):

        # Aggiungi la sovrapposizione di stile per il label semitrasparente
        self.cover_label = QLabel(self)
        self.cover_label.resize(self.width(), self.height())
        self.cover_label.setStyleSheet("background-color: rgba(0, 0, 0, 1%);")
        self.cover_label.show()

        end_rect = QRectF(self.width() / 2 - 50, self.height() / 2 - 75, 100, 150)

        # Carte a terra
        self.terra_animations = []
        for carta_terra in carte_terra_interessate:
            terra_index = self.data["terra"].index(carta_terra)
            terra_label = self.terra_labels[terra_index]
            terra_animation = QPropertyAnimation(terra_label, b"geometry")
            terra_animation.setDuration(1000)
            start_rect = terra_label.geometry()
            terra_animation.setStartValue(start_rect)
            terra_animation.setEndValue(end_rect)
            terra_animation.setEasingCurve(QEasingCurve.InOutQuad)
            self.terra_animations.append(terra_animation)

        # Animazione generale
        self.group_animation = QParallelAnimationGroup()
        self.group_animation.addAnimation(self.mano_animation)
        for terra_animation in self.terra_animations:
            self.group_animation.addAnimation(terra_animation)

        # Carte a terra
        self.terra_animations2 = []
        for carta_terra in carte_terra_interessate:
            terra_index = self.data["terra"].index(carta_terra)
            terra_label = self.terra_labels[terra_index]
            terra_animation2 = QPropertyAnimation(terra_label, b"geometry")
            terra_animation2.setDuration(1000)
            terra_animation2.setStartValue(end_rect)
            terra_animation2.setEndValue(QRectF(-100, 1000, 100, 150))
            terra_animation2.setEasingCurve(QEasingCurve.InOutQuad)
            self.terra_animations2.append(terra_animation2)

        # Animazione generale
        self.group_animation2 = QParallelAnimationGroup()
        self.group_animation2.addAnimation(self.mano_animation2)
        for terra_animation2 in self.terra_animations2:
            self.group_animation2.addAnimation(terra_animation2)

        self.presa_animation = QPropertyAnimation(self.presa_label, b"geometry")
        self.presa_animation.setDuration(1000)
        start_rect = self.presa_label.geometry()
        self.presa_animation.setStartValue(start_rect)
        self.presa_animation.setEndValue(QRectF(-15, 860, 100, 150))
        self.presa_animation.setEasingCurve(QEasingCurve.InOutQuad)

        self.group_animation3 = QSequentialAnimationGroup()
        self.group_animation3.addAnimation(self.group_animation)
        self.group_animation3.addAnimation(self.group_animation2)
        self.group_animation3.addAnimation(self.presa_animation)

        # Inizia l'animazione
        self.cover_animation = QPropertyAnimation(self.cover_label, b"opacity")
        self.cover_animation.setStartValue(0)
        self.cover_animation.setEndValue(1)
        self.cover_animation.finished.connect(lambda: self.group_animation3.start())

        self.group_animation3.finished.connect(lambda: self.cleanup_labels_fine([self.terra_labels[self.data["terra"].index(carta)] for carta in carte_terra_interessate]))

        self.cover_animation.start()
    
    def cleanup_labels_fine(self, terra_labels_to_remove):
        for label in terra_labels_to_remove:
            label.hide()
        for label in self.mano_labels + self.terra_labels:
            label.setEnabled(True)



    def realign_cards4(self):
        self.realign_animation = QParallelAnimationGroup()

        # Filtra le carte rimanenti nella mano e a terra
        mano_remaining = [label for label in self.mano_labels if label.isVisible()]
        terra_remaining = [label for label in self.terra_labels if label.isVisible()]

        # Calcola la nuova posizione per le carte rimanenti nella mano
        mano_width = len(mano_remaining) * 150 + (len(mano_remaining) - 1) * 10
        mano_start_x = (self.width() - mano_width) // 2
        mano_y = self.height() - 225
        for i, label in enumerate(mano_remaining):
            anim = QPropertyAnimation(label, b"geometry")
            anim.setDuration(1000)
            anim.setStartValue(label.geometry())
            anim.setEndValue(QRect(mano_start_x + i * 160, mano_y, 150, 225))
            self.realign_animation.addAnimation(anim)
            # Aggiorna le posizioni di hover e fine
            label.hover_rect = QRectF(mano_start_x + i * 160, mano_y - 20, 150, 225)
            label.end_rect = QRectF(mano_start_x + i * 160, mano_y, 150, 225)

        # Calcola la nuova posizione per le carte rimanenti a terra
        terra_width = len(terra_remaining) * 100 + (len(terra_remaining) - 1) * 10
        terra_start_x = (self.width() - terra_width) // 2
        terra_y = self.height() // 2 - 150
        for i, label in enumerate(terra_remaining):
            anim = QPropertyAnimation(label, b"geometry")
            anim.setDuration(1000)
            anim.setStartValue(label.geometry())
            anim.setEndValue(QRect(terra_start_x + i * 110, terra_y, 100, 150))
            self.realign_animation.addAnimation(anim)
            # Aggiorna le posizioni di hover e fine
            label.hover_rect = QRectF(terra_start_x + i * 110, terra_y + 20, 100, 150)
            label.end_rect = QRectF(terra_start_x + i * 110, terra_y, 100, 150)

        self.realign_animation.finished.connect(self.remove_cover_label4)
        self.realign_animation.start()

    def start_move_animation4(self, carta_mano, carte_terra_interessate):
        def update_pixmap(label, pixmap):
            label.setPixmap(pixmap.scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        def realign_cards_wrapper():
            self.realign_cards4()

        # Aggiungi la sovrapposizione di stile per il label semitrasparente
        self.cover_label = QLabel(self)
        self.cover_label.resize(self.width(), self.height())
        self.cover_label.setStyleSheet("background-color: rgba(0, 0, 0, 1%);")
        self.cover_label.show()

        print(carta_mano)

        # Carta della mano
        mano_index = self.data["mano"].index(carta_mano)
        mano_label = self.mano_labels[mano_index]

        self.mano_animation = QPropertyAnimation(mano_label, b"geometry")
        self.mano_animation.setDuration(1000)
        start_rect = mano_label.geometry()
        self.mano_animation.setStartValue(start_rect)
        end_rect = QRectF(self.width() / 2 - 50, self.height() / 2 - 75, 100, 150)
        self.mano_animation.setEndValue(end_rect)
        self.mano_animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.mano_animation.valueChanged.connect(lambda _, l=mano_label: update_pixmap(l, QPixmap(f"Gioco di Scopa/Carte/{l.property('card_id')}.png")))

        # Carte a terra
        self.terra_animations = []
        for carta_terra in carte_terra_interessate:
            terra_index = self.data["terra"].index(carta_terra)
            terra_label = self.terra_labels[terra_index]
            terra_animation = QPropertyAnimation(terra_label, b"geometry")
            terra_animation.setDuration(1000)
            start_rect = terra_label.geometry()
            terra_animation.setStartValue(start_rect)
            terra_animation.setEndValue(end_rect)
            terra_animation.setEasingCurve(QEasingCurve.InOutQuad)
            self.terra_animations.append(terra_animation)

        # Animazione generale
        self.group_animation = QParallelAnimationGroup()
        self.group_animation.addAnimation(self.mano_animation)
        for terra_animation in self.terra_animations:
            self.group_animation.addAnimation(terra_animation)

        # Carta della mano
        self.mano_animation2 = QPropertyAnimation(mano_label, b"geometry")
        self.mano_animation2.setDuration(1000)
        self.mano_animation2.setStartValue(end_rect)
        self.mano_animation2.setEndValue(QRectF(-100, 1000, 100, 150))
        self.mano_animation2.setEasingCurve(QEasingCurve.InOutQuad)

        # Carte a terra
        self.terra_animations2 = []
        for carta_terra in carte_terra_interessate:
            terra_index = self.data["terra"].index(carta_terra)
            terra_label = self.terra_labels[terra_index]
            terra_animation2 = QPropertyAnimation(terra_label, b"geometry")
            terra_animation2.setDuration(1000)
            terra_animation2.setStartValue(end_rect)
            terra_animation2.setEndValue(QRectF(-100, 1000, 100, 150))
            terra_animation2.setEasingCurve(QEasingCurve.InOutQuad)
            self.terra_animations2.append(terra_animation2)

        # Animazione generale
        self.group_animation2 = QParallelAnimationGroup()
        self.group_animation2.addAnimation(self.mano_animation2)
        for terra_animation2 in self.terra_animations2:
            self.group_animation2.addAnimation(terra_animation2)

        self.presa_animation = QPropertyAnimation(self.presa_label, b"geometry")
        self.presa_animation.setDuration(1000)
        start_rect = self.presa_label.geometry()
        self.presa_animation.setStartValue(start_rect)
        self.presa_animation.setEndValue(QRectF(-15, 860, 100, 150))
        self.presa_animation.setEasingCurve(QEasingCurve.InOutQuad)

        self.group_animation3 = QSequentialAnimationGroup()
        self.group_animation3.addAnimation(self.group_animation)
        self.group_animation3.addAnimation(self.group_animation2)
        self.group_animation3.addAnimation(self.presa_animation)

        # Inizia l'animazione
        self.cover_animation = QPropertyAnimation(self.cover_label, b"opacity")
        self.cover_animation.setStartValue(0)
        self.cover_animation.setEndValue(1)
        self.cover_animation.finished.connect(lambda: self.group_animation3.start())

        self.group_animation3.finished.connect(lambda: self.cleanup_labels([mano_label], [self.terra_labels[self.data["terra"].index(carta)] for carta in carte_terra_interessate]))
        self.group_animation3.finished.connect(realign_cards_wrapper)

        self.cover_animation.start()

    def remove_cover_label4(self):
        try:
            if hasattr(self, 'cover_label') and self.cover_label is not None:
                self.cover_label.hide()
                self.cover_label.deleteLater()
                self.cover_label = None
        except RuntimeError:
            pass
        self.create_endgame_screen()
        print('se sono passato di qua sono troppissimo forte e ho vinto caciopalla')
        self.countdown_timer3.setSingleShot(True)
        self.countdown_timer3.timeout.connect(lambda: self.create_endgame_data())
        self.countdown_timer3.start(6000)


    def create_endgame_screen_asinc(self):
        self.my_signal2.emit()

    @pyqtSlot()
    def create_endgame_screen(self):
        print('sia lodato quel P**** D* G***')

        labels = ['cover_label', 'cover_label2', 'center_image_label']
        for label in labels:
            if hasattr(self, label):
                try:
                    label_attr = getattr(self, label)
                    label_attr.hide()
                    label_attr.deleteLater()
                    delattr(self, label)
                except RuntimeError as e:
                    print(f"RuntimeError for {label}: {e}")
                except AttributeError as e:
                    print(f"AttributeError for {label}: {e}")

        if self.data["numero"] == 1:
            data_to_send = {'user_name': self.user_name, 'user_name2': self.nomecattivo}
            try:
                response = requests.post('http://localhost:8080/update_punti', data=data_to_send)
                if response.status_code == 200:
                    pass
            except requests.exceptions.ConnectionError:
                pass
            data_to_send = {'user_name': self.user_name}
            try:
                response = requests.post('http://localhost:8080/nuova_partita', data=data_to_send)
                if response.status_code == 200:
                    pass
            except requests.exceptions.ConnectionError:
                pass
            time.sleep(0.5)
        else:
            time.sleep(1)

        # Crea un background semi-trasparente
        self.background_label = QLabel(self)
        self.background_label.setStyleSheet("background-color: rgba(0, 0, 0, 100);")
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        self.background_label.show()

        # Crea l'etichetta con l'immagine "fine"
        self.fine_label = QLabel(self)
        self.fine_label.setPixmap(QPixmap("Gioco di Scopa/Icone/fine.png"))
        self.fine_label.setScaledContents(True)
        self.fine_label.setGeometry((self.width() - 600) // 2, 50, 600, 140)
        self.fine_label.setStyleSheet("background: transparent;")
        self.fine_label.show()

        # Crea l'etichetta per "Punti"
        self.punti_label = QLabel("Punti:", self)
        self.punti_label.setStyleSheet("color: white; font-size: 24px;")
        self.punti_label.adjustSize()
        self.punti_label.setGeometry(self.width() - self.punti_label.width() - 20, self.height() // 2 - 100, self.punti_label.width(), self.punti_label.height())
        self.punti_label.show()

        data_to_send = {'user_name': self.user_name}
        try:
            response = requests.post('http://localhost:8080/punti', data=data_to_send)
            if response.status_code == 200:
                self.punti[0]=(int(response.json()['punti']))
        except requests.exceptions.ConnectionError:
            pass

        # Crea l'etichetta per il tuo username e punteggio
        self.my_label = QLabel(f"{self.user_name}: {self.punti[0]}", self)
        self.my_label.setStyleSheet("color: white; font-size: 18px;")
        self.my_label.adjustSize()
        self.my_label.setGeometry(self.width() - self.my_label.width() - 20, self.height() // 2 - 50, self.my_label.width(), self.my_label.height())
        self.my_label.show()

        data_to_send = {'user_name': self.nomecattivo}
        try:
            response = requests.post('http://localhost:8080/punti', data=data_to_send)
            if response.status_code == 200:
                self.punti[1]=(int(response.json()['punti']))
        except requests.exceptions.ConnectionError:
            pass

        # Crea l'etichetta per l'username dell'avversario e il punteggio
        self.opponent_label = QLabel(f"{self.nomecattivo}: {self.punti[1]}", self)
        self.opponent_label.setStyleSheet("color: white; font-size: 18px;")
        self.opponent_label.adjustSize()
        self.opponent_label.setGeometry(self.width() - self.opponent_label.width() - 20, self.height() // 2, self.opponent_label.width(), self.opponent_label.height())
        self.opponent_label.show()

        # Nascondi lo schermo dopo 5 secondi
        QTimer.singleShot(6000, self.background_label.hide)
        QTimer.singleShot(6000, self.fine_label.hide)
        QTimer.singleShot(6000, self.punti_label.hide)
        QTimer.singleShot(6000, self.my_label.hide)
        QTimer.singleShot(6000, self.opponent_label.hide)

        # Crea un'animazione di opacità per il background semi-trasparente
        self.animation = QPropertyAnimation(self.background_label, b"opacity")
        self.animation.setDuration(6000)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)

        self.animation.start


    def create_endgame_data_asinc(self):
        self.my_signal3.emit()

    @pyqtSlot()
    def create_endgame_data(self):

        print('ok ora sono passato di qui porco cane')

        with open('Gioco di Scopa/dati.json', 'r') as file:
            Punti_Vittoria = int(json.load(file)['Punti_Vittoria'])

        ti = False
        for i, punto in enumerate(self.punti):
            if punto >= Punti_Vittoria:
                ti=True

        print('ok ora sono passati secondi')

        if ti:
            for i, punto in enumerate(self.punti):
                if punto >= Punti_Vittoria:
                    if all(p >= Punti_Vittoria for p in self.punti):
                        if self.punti.count(max(self.punti)) > 1:
                            print('pareggio')
                            self.set_index(15)
                        else:
                            if self.punti[i] == max(self.punti):
                                if (i+1) == self.data["numero"]:
                                    print('hai vinto')
                                    self.set_index(9)
                                else:
                                    print('hai perso')
                                    self.set_index(14)
                    else:
                        if (i+1) == self.data["numero"]:
                            print('hai vinto')
                            self.set_index(9)
                        else:
                            print('hai perso')
                            self.set_index(14)
        else:
            data_to_send = {'user_name': self.user_name}
            try:
                response = requests.post('http://localhost:8080/nuova_partita_nuovi_dati', data=data_to_send)
                if response.status_code == 200:
                    with open('Gioco di Scopa/dati.json', 'r') as file:
                        dati = json.load(file)
                    partita = {}
                    partita['mano'] = response.json()['player_hand']
                    partita['terra'] = response.json()['terra']
                    partita['presa'] = []
                    partita['punti'] = self.punti[(self.data["numero"]-1)]
                    partita['numero'] = dati['numero']
                    if dati['numero'] == 1:
                        partita['token'] = True
                    else:
                        partita['token'] = False

                    with open('Gioco di Scopa/partita.json', 'w') as file:
                        json.dump(partita, file)
                    time.sleep(0.5)
                    self.reload_page()
                    self.start_animation()
                    threading.Thread(target=self.run_controlli_asincroni).start()
            except requests.exceptions.ConnectionError:
                pass




    def start_animation(self):
        # Crea un QLabel trasparente che copre tutto
        self.cover_label = QLabel(self)
        self.cover_label.resize(self.width(), self.height())  # Assicurati che copra tutto il widget
        self.cover_label.setStyleSheet("background-color: rgba(0, 0, 0, 100);")  # Imposta un colore di sfondo trasparente

        # Crea un QPixmap con l'immagine che vuoi mostrare al centro
        center_pixmap = QPixmap("Gioco di Scopa/Icone/via.png")
        center_pixmap = center_pixmap.scaled(500, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Ridimensiona l'immagine se necessario

        self.cover_label2 = QLabel(self)
        self.cover_label2.resize(self.width(), self.height())  # Assicurati che copra tutto il widget
        self.cover_label2.setStyleSheet("background-color: none;")  # Imposta un colore di sfondo trasparente

        # Crea un altro QLabel per l'immagine centrale
        self.center_image_label = QLabel(self.cover_label2)
        self.center_image_label.setPixmap(center_pixmap)
        self.center_image_label.setAlignment(Qt.AlignCenter)  # Centra l'immagine
        self.center_image_label.setGeometry((self.width() - center_pixmap.width()) // 2, (self.height() - center_pixmap.height()) // 2, center_pixmap.width(), center_pixmap.height())
        self.cover_label.show()
        self.cover_label2.show()

        # Inizia l'animazione
        self.animations_group = QSequentialAnimationGroup()  # Modifica qui

        # Definisci una funzione di aggiornamento per ridimensionare l'immagine
        def update_pixmap(label, pixmap):
            label.setPixmap(pixmap.scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        # Calcola la posizione centrale in basso
        centro_basso_x = int(self.width() / 2 - (len(self.mano_labels) * 150 + (len(self.mano_labels) - 1) * 10) / 2) + 15  # 
        centro_basso_y = self.height() - 225  # Posiziona l'immagine in basso

        # Crea le animazioni per le carte della mano
        self.mano_animations = []
        for i, label in enumerate(self.mano_labels):
            animation = QPropertyAnimation(label, b"geometry")
            animation.setDuration(250)
            animation.setStartValue(QRectF(-150, int(self.height() / 2 - 75), 100, 150))
            # Aggiusta la posizione x per centrare le carte
            end_rect = QRectF(centro_basso_x + i * (150 + 10), centro_basso_y, 150, 225)
            animation.setEndValue(end_rect)
            animation.setEasingCurve(QEasingCurve.InOutQuad)
            animation.valueChanged.connect(lambda _, l=label: update_pixmap(l, QPixmap(f"Gioco di Scopa/Carte/{l.property('card_id')}.png")))
            self.mano_animations.append(animation)

        self.terra_animations = []
        for i, label in enumerate(self.terra_labels):
            animation = QPropertyAnimation(label, b"geometry")
            animation.setDuration(250)
            animation.setStartValue(QRectF(-150, int(self.height() / 2 - 75), 100, 150))
            # Calcola la posizione finale per le carte a terra
            end_rect = QRectF(int(self.width() / 2 - (len(self.terra_labels) * 100 + (len(self.terra_labels) - 5) * 10) / 2) + i * (100 + 10), int(self.height() / 2 - 150), 100, 150)
            animation.setEndValue(end_rect)
            animation.setEasingCurve(QEasingCurve.InOutQuad)
            self.terra_animations.append(animation)

        # Crea le animazioni per i retro delle carte
        self.retro_animations = []
        for i, label in enumerate(self.retro_labels):
            animation = QPropertyAnimation(label, b"geometry")
            animation.setDuration(250)
            animation.setStartValue(QRectF(-150, int(self.height() / 2 - 75), 100, 150))
            # Calcola la posizione finale per i retro delle carte
            end_rect = QRectF(int(self.width() / 2 - 100 + i * 75), 10, 75, 112.5)
            animation.setEndValue(end_rect)
            animation.setEasingCurve(QEasingCurve.InOutQuad)
            animation.valueChanged.connect(lambda _, l=label: update_pixmap(l, QPixmap(f"Gioco di Scopa/Carte/0.png")))
            self.retro_animations.append(animation)

        x = max(len(self.mano_animations), len(self.terra_animations), len(self.retro_animations))

        for i in range(x):
            if i < len(self.mano_animations):
                self.animations_group.addAnimation(self.mano_animations[i])
            if i < len(self.terra_animations):
                self.animations_group.addAnimation(self.terra_animations[i])
            if i < len(self.retro_animations):
                self.animations_group.addAnimation(self.retro_animations[i])
        
        # Connetti il segnale finished dell'animations_group con il metodo animation_finished
        self.animations_group.finished.connect(self.animation_finished)
        self.animations_group.start()

    def animation_finished(self):
        # Crea un effetto di opacità per il QLabel trasparente
        self.cover_opacity_effect = QGraphicsOpacityEffect(self.cover_label)
        self.cover_label.setGraphicsEffect(self.cover_opacity_effect)

        # Crea un effetto di opacità per l'immagine centrale
        self.center_opacity_effect = QGraphicsOpacityEffect(self.center_image_label)
        self.center_image_label.setGraphicsEffect(self.center_opacity_effect)

        # Crea un'animazione di opacità per il QLabel trasparente
        self.fade_animation = QPropertyAnimation(self.cover_opacity_effect, b"opacity")
        self.fade_animation.setDuration(1000)  # Durata dell'effetto di dissolvenza
        self.fade_animation.setStartValue(1.0)  # Inizia completamente visibile
        self.fade_animation.setEndValue(0.0)  # Finisce completamente trasparente
        self.fade_animation.setEasingCurve(QEasingCurve.Linear)  # Velocità costante

        # Collega l'animazione di opacità al cambiamento di opacità del QLabel
        self.fade_animation.valueChanged.connect(lambda value: self.set_label_opacity(value))

        # Quando l'animazione di opacità è finita, rimuovi i QLabel
        self.fade_animation.finished.connect(lambda: self.center_image_label.deleteLater())
        self.fade_animation.finished.connect(lambda: self.cover_label.deleteLater())

         # Quando l'animazione di opacità è finita, rimuovi i QLabel
        self.fade_animation.finished.connect(self.remove_labels)

        # Avvia l'animazione di opacità
        self.fade_animation.start()

    def remove_labels(self):
        # Rimuove i QLabel dalla memoria
        labels = ['cover_label', 'cover_label2', 'center_image_label']
        for label in labels:
            if hasattr(self, label):
                try:
                    label_attr = getattr(self, label)
                    label_attr.hide()
                    label_attr.deleteLater()
                    delattr(self, label)
                except RuntimeError as e:
                    print(f"RuntimeError for {label}: {e}")
                except AttributeError as e:
                    print(f"AttributeError for {label}: {e}")

    def set_label_opacity(self, value):
        # Imposta l'opacità del QLabel trasparente e dell'immagine centrale
        self.cover_opacity_effect.setOpacity(value)
        self.center_opacity_effect.setOpacity(value)

# 9 Classe per la pagina dele Win Online, eredita dalla classe Page
class WinOnlinePage(Page):
    def __init__(self, stacked_layout, sound_manager, parent=None):
        super().__init__(parent)
        self.stacked_layout = stacked_layout
        self.sound_manager = sound_manager

        self.giocatori_label = QLabel("vittoria")
        self.giocatori_label.setStyleSheet(testo)

        self.layout = QVBoxLayout()  # Assicurati di avere un layout
        self.layout.addWidget(self.giocatori_label)
        self.setLayout(self.layout)  # Imposta il layout per questa pagina

    def esci(self):
        self.sound_manager.play_click_sound()
        self.stacked_layout.setCurrentIndex(2)

    def Gioca_ancora(self):
        self.sound_manager.play_click_sound()
        self.stacked_layout.setCurrentIndex(7)

# 14 Classe per la pagina dele Lose Online, eredita dalla classe Page
class LoseOnlinePage(Page):
    def __init__(self, stacked_layout, sound_manager, parent=None):
        super().__init__(parent)
        self.stacked_layout = stacked_layout
        self.sound_manager = sound_manager

        self.giocatori_label = QLabel("sconfitta")
        self.giocatori_label.setStyleSheet(testo)

        self.layout = QVBoxLayout()  # Assicurati di avere un layout
        self.layout.addWidget(self.giocatori_label)
        self.setLayout(self.layout)  # Imposta il layout per questa pagina

    def esci(self):
        self.sound_manager.play_click_sound()
        self.stacked_layout.setCurrentIndex(2)

    def Gioca_ancora(self):
        self.sound_manager.play_click_sound()
        self.stacked_layout.setCurrentIndex(7)

# 15 Classe per la pagina dele Pareggio Online, eredita dalla classe Page
class ParOnlinePage(Page):
    def __init__(self, stacked_layout, sound_manager, parent=None):
        super().__init__(parent)
        self.stacked_layout = stacked_layout
        self.sound_manager = sound_manager

        self.giocatori_label = QLabel("pareggio")
        self.giocatori_label.setStyleSheet(testo)

        self.layout = QVBoxLayout()  # Assicurati di avere un layout
        self.layout.addWidget(self.giocatori_label)
        self.setLayout(self.layout)  # Imposta il layout per questa pagina

    def esci(self):
        self.sound_manager.play_click_sound()
        self.stacked_layout.setCurrentIndex(2)

    def Gioca_ancora(self):
        self.sound_manager.play_click_sound()
        self.stacked_layout.setCurrentIndex(7)



# 10 Classe per la pagina del Game Bot, eredita dalla classe Page
class GameBotPage(Page):
    def __init__(self, stacked_layout, sound_manager, parent=None):
        super().__init__(parent)
        self.stacked_layout = stacked_layout  # Salva il layout impilato
        self.sound_manager = sound_manager

        self.setWindowTitle("Animazione di Carte")
        self.setGeometry(100, 100, 600, 1000)

        # Creare un QLabel per lo sfondo
        self.background_label = QLabel(self)
        self.background_label.setStyleSheet("background-color: #52B488;")
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        self.background_label.lower()  # Assicurarsi che l'etichetta di sfondo sia dietro gli altri widget

        # Leggi i dati dal file JSON
        with open("Gioco di Scopa/partita.json", "r") as file:
            self.data = json.load(file)

        # Crea i label per le carte a terra, in mano e il retro delle carte
        self.create_labels()

        # Posiziona i label sul widget
        self.position_labels()

        # Aggiungi un pulsante per tornare alla home
        self.create_back_button()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Aggiorna la dimensione dell'etichetta di sfondo quando la finestra viene ridimensionata
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        self.update()

    def showEvent(self, event):
        super().showEvent(event)
        self.start_animation() 

    def create_back_button(self):
        back_button = QPushButton("Home", self)
        back_button.setGeometry(10, 10, 100, 50)
        back_button.clicked.connect(self.go_to_home)

    def go_to_home(self):
        if self.stacked_layout:
            self.sound_manager.play_click_sound()
            self.stacked_layout.setCurrentIndex(2)  # Indice della HomePage

    def create_labels(self):
        # Crea i label per le carte a terra
        self.terra_labels = []
        for carta in self.data["terra"]:
            label = QLabel(self)
            pixmap = QPixmap(f"Gioco di Scopa/Carte/{carta[1]}/{carta[0]}.png")
            label.setPixmap(pixmap.scaled(100, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            label.setProperty('card_id', f"{carta[1]}/{carta[0]}")
            label.setStyleSheet("background-color: none;")
            self.terra_labels.append(label)
            label.mousePressEvent = lambda event, lbl=label: self.on_card_click(event, lbl)
            label.setGeometry(-150, int(self.height() / 2 - 75), 100, 150)

        # Aggiungi gli eventi di entrata e uscita del mouse per ogni label delle carte in mano
        for i, label in enumerate(self.terra_labels):
            label.hover_rect = QRectF(int(self.width() / 2 - (len(self.terra_labels) * 100 + (len(self.terra_labels) - 5) * 10) / 2) + i * (100 + 10), int(self.height() / 2 - 150)+20, 100, 150)  # Posizione di hover
            label.end_rect = QRectF(int(self.width() / 2 - (len(self.terra_labels) * 100 + (len(self.terra_labels) - 5) * 10) / 2) + i * (100 + 10), int(self.height() / 2 - 150), 100, 150)  # Posizione finale
            label.enterEvent = lambda event, lbl=label: self.on_card_hover_enter(event, lbl)
            label.leaveEvent = lambda event, lbl=label: self.on_card_hover_leave(event, lbl)

        # Crea i label per le carte in mano
        self.mano_labels = []
        for carta in self.data["mano"]:
            label = QLabel(self)
            pixmap = QPixmap(f"Gioco di Scopa/Carte/{carta[1]}/{carta[0]}.png")
            label.setPixmap(pixmap.scaled(150, 225, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            label.setProperty('card_id', f"{carta[1]}/{carta[0]}")
            label.setStyleSheet("background-color: none;")
            self.mano_labels.append(label)
            label.mousePressEvent = lambda event, lbl=label: self.on_card_click(event, lbl)
            label.setGeometry(-150, int(self.height() / 2 - 75), 100, 150)

        centro_basso_x = int(self.width() / 2 - (len(self.mano_labels) * 150 + (len(self.mano_labels) - 1) * 10) / 2) + 15  # 
        centro_basso_y = self.height() - 225  # Assumi che questa sia la posizione y corretta

        # Aggiungi gli eventi di entrata e uscita del mouse per ogni label delle carte in mano
        for i, label in enumerate(self.mano_labels):
            label.hover_rect = QRectF(centro_basso_x + i * (150 + 10), centro_basso_y - 20, 150, 225)  # Posizione di hover
            label.end_rect = QRectF(centro_basso_x + i * (150 + 10), centro_basso_y, 150, 225)  # Posizione finale
            label.enterEvent = lambda event, lbl=label: self.on_card_hover_enter(event, lbl)
            label.leaveEvent = lambda event, lbl=label: self.on_card_hover_leave(event, lbl)

        # Crea i label per il retro delle carte
        self.retro_labels = []
        for _ in range(3):
            label = QLabel(self)
            pixmap = QPixmap("Gioco di Scopa/Carte/0.png")
            label.setPixmap(pixmap.scaled(50, 75, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            label.setStyleSheet("background-color: none;")
            self.retro_labels.append(label)
            label.setGeometry(-150, int(self.height() / 2 - 75), 100, 150)

        self.presa_label = QLabel(self)
        pixmap = QPixmap("Gioco di Scopa/Carte/0.png")
        self.presa_label.setPixmap(pixmap.scaled(100, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.presa_label.setStyleSheet("background-color: none;")
        self.presa_label.setGeometry(-150, 1100, 100, 150)
        self.presa_label.move(-100, 1000)

        # Crea i label per il nome cattivo e i punti
        self.label_nome_cattivo = QLabel(f"Nome Cattivo \nPunti:", self)
        self.label_nome_cattivo.setStyleSheet(testoo)
        self.label_nome_cattivo.adjustSize()  # Ridimensiona il QLabel in base al contenuto del testo

        self.label_punti_cattivo = QLabel(str(self.data["punti"]), self)
        self.label_punti_cattivo.setStyleSheet(testoo)
        self.label_punti_cattivo.adjustSize()  # Ridimensiona il QLabel in base al contenuto del testo

        # Crea i label per il nome e i punti
        self.label_nome = QLabel("Punti:", self)
        self.label_nome.setStyleSheet(titoloo)
        self.label_nome.adjustSize()  # Ridimensiona il QLabel in base al contenuto del testo

        self.label_punti = QLabel(str(self.data["punti"]), self)
        self.label_punti.setStyleSheet(titoloo)
        self.label_punti.adjustSize()  # Ridimensiona il QLabel in base al contenuto del testo


    def on_card_hover_enter(self, event, label):
        # Crea un'animazione per spostare il QLabel verso l'alto
        self.animation_up = QPropertyAnimation(label, b'geometry')
        self.animation_up.setDuration(150)
        self.animation_up.setEndValue(label.hover_rect)
        self.animation_up.start()

    def on_card_hover_leave(self, event, label):
        # Crea un'animazione per riportare il QLabel nella posizione finale
        self.animation_down = QPropertyAnimation(label, b'geometry')
        self.animation_down.setDuration(150)
        self.animation_down.setEndValue(label.end_rect)
        self.animation_down.start()


    def on_card_click(self, event, label):
        # Ottieni l'identificatore della carta cliccata dal label passato
        card_id = label.property('card_id')
        
        # Estrai seme e valore dalla stringa
        card_id_vett = card_id.strip().split('/') 
        seme = card_id_vett[0]
        valore = int(card_id_vett[1])
        carta_mano = [card_id_vett[1], seme]

        # Recupera le carte a terra dal file JSON
        carte_a_terra = self.get_carte_a_terra()

        # Calcola le carte prendibili
        carte_prendibili = self.get_carte_prendibili(card_id_vett, carte_a_terra)

        if carte_prendibili:
            # Controllo per carta con valore superiore a 7
            if valore > 7:
                for combinazione in carte_prendibili:
                    if len(combinazione) == 1:
                        self.prendi_carte(carta_mano, combinazione)
                        self.start_move_animation(carta_mano, combinazione)
                        return
            
            if len(carte_prendibili) > 1:
                self.show_combination_options(carta_mano, carte_prendibili)
            else:
                # Prendi le carte
                self.prendi_carte(carta_mano, carte_prendibili[0])
                self.start_move_animation(carta_mano, carte_prendibili[0])
        else:
            self.metti_a_terra(carta_mano)
            self.start_move_animation2(carta_mano)

    def show_combination_options(self, carta_mano, combinazioni):
        # Crea un widget centrale per contenere le opzioni
        self.options_widget = QWidget(self)
        self.options_widget.setStyleSheet("background: rgba(0, 0, 0, 0.5); border-radius: 10px;")
        self.options_layout = QVBoxLayout(self.options_widget)

        for combinazione in combinazioni:
            option_label = QLabel(self.options_widget)
            
            # Creare l'immagine di combinazione con il segno "+"
            combined_pixmap = self.create_combined_pixmap(combinazione)
            
            option_label.setPixmap(combined_pixmap)
            option_label.setAlignment(Qt.AlignCenter)
            option_label.mousePressEvent = lambda event, combo=combinazione: self.on_combination_selected(carta_mano, combo)
            self.options_layout.addWidget(option_label)

        # Ridimensiona e posiziona il widget centrale
        self.options_widget.setFixedSize(600, 1000)
        self.options_widget.move((self.width() - self.options_widget.width()) // 2, 
                                (self.height() - self.options_widget.height()) // 2)
        self.options_widget.show()

    def create_combined_pixmap(self, combinazione):
        # Carica le immagini delle carte e crea un pixmap combinato con segni "+"
        card_images = [QPixmap(f"Gioco di Scopa/Carte/{c[1]}/{c[0]}.png").scaled(100, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation) for c in combinazione]
        plus_sign = QPixmap(30, 30)
        plus_sign.fill(Qt.transparent)

        # Disegna il segno "+" bianco su un pixmap trasparente
        painter = QPainter(plus_sign)
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(QFont("Arial", 20))
        painter.drawText(plus_sign.rect(), Qt.AlignCenter, "+")
        painter.end()

        width = sum(image.width() for image in card_images) + (len(card_images) - 1) * plus_sign.width()
        height = max(image.height() for image in card_images)
        combined_pixmap = QPixmap(width, height)
        combined_pixmap.fill(Qt.transparent)  # Rendi lo sfondo trasparente

        painter = QPainter(combined_pixmap)
        x_offset = 0
        for i, image in enumerate(card_images):
            painter.drawPixmap(x_offset, 0, image)
            x_offset += image.width()
            if i < len(card_images) - 1:
                painter.drawPixmap(x_offset, (height - plus_sign.height()) // 2, plus_sign)
                x_offset += plus_sign.width()
        painter.end()

        return combined_pixmap

    def on_combination_selected(self, carta_mano, combinazione):
        # Nascondi tutte le opzioni e rimuovi il widget centrale
        self.options_widget.hide()
        self.options_widget.deleteLater()
        self.options_widget = None

        # Prendi le carte
        self.prendi_carte(carta_mano, combinazione)
        self.start_move_animation(carta_mano, combinazione)

    def get_carte_prendibili(self, card_id, carte_a_terra):
        # Inizializza una lista vuota per le carte prendibili
        carte_prendibili = []

        # Estrai il valore dalla tupla card_id
        valore = int(card_id[1])

        # Controlla se la carta cliccata può prendere una singola carta a terra con lo stesso valore
        for carta in carte_a_terra:
            valore_terra = int(carta[0])
            if valore == valore_terra:
                print(valore_terra)
                carte_prendibili.append([carta])

        # Controlla se la carta cliccata può prendere combinazioni di carte a terra
        # che sommano al suo valore
        for i in range(2, len(carte_a_terra) + 1):
            for combo in combinations(carte_a_terra, i):
                if sum(int(c[0]) for c in combo) == valore:
                    carte_prendibili.append(list(combo))
                    print(combo)

        # Restituisce la lista delle carte prendibili
        print(carte_prendibili)
        return carte_prendibili


    def get_carte_a_terra(self):
        # Legge le carte a terra dal file JSON
        with open("Gioco di Scopa/partita.json", "r") as file:
            partita_data = json.load(file)
        return partita_data["terra"]

    def prendi_carte(self, carta_mano, carte_prendibili):
        # Implementa la logica per prendere le carte dal tavolo
        # Questo è un esempio, dovrai adattarlo alle regole del tuo gioco
        self.rimuovi_carta_da_mano(carta_mano)
        for carta in carte_prendibili:
            self.rimuovi_carta_da_terra(carta)
        # Aggiorna il punteggio o lo stato del gioco se necessario

    def rimuovi_carta_da_terra(self, carta):
        with open("Gioco di Scopa/partita.json", "r") as file:
            dati = json.load(file)
        # Rimuove la carta specificata dall'elenco delle carte a terra
        # Questo è un esempio, dovrai adattarlo alle regole del tuo gioco
        dati['terra'].remove(carta)
        dati['presa'].append(carta)
        # Aggiorna il file JSON
        with open("Gioco di Scopa/partita.json", "w") as file:
            json.dump(dati, file)

    def rimuovi_carta_da_mano(self, carta):
        with open("Gioco di Scopa/partita.json", "r") as file:
            dati = json.load(file)
        # Rimuove la carta specificata dall'elenco delle carte a terra
        # Questo è un esempio, dovrai adattarlo alle regole del tuo gioco
        dati['mano'].remove(carta)
        dati['presa'].append(carta)
        # Aggiorna il file JSON
        with open("Gioco di Scopa/partita.json", "w") as file:
            json.dump(dati, file)
    
    def metti_a_terra(self, carta):
        with open("Gioco di Scopa/partita.json", "r") as file:
            dati = json.load(file)
        # Rimuove la carta specificata dall'elenco delle carte a terra
        # Questo è un esempio, dovrai adattarlo alle regole del tuo gioco
        dati['mano'].remove(carta)
        dati['terra'].append(carta)
        # Aggiorna il file JSON
        with open("Gioco di Scopa/partita.json", "w") as file:
            json.dump(dati, file)
    


    def realign_cards(self):
        self.realign_animation = QParallelAnimationGroup()

        # Filtra le carte rimanenti nella mano e a terra
        mano_remaining = [label for label in self.mano_labels if label.isVisible()]
        terra_remaining = [label for label in self.terra_labels if label.isVisible()]

        # Calcola la nuova posizione per le carte rimanenti nella mano
        mano_width = len(mano_remaining) * 150 + (len(mano_remaining) - 1) * 10
        mano_start_x = (self.width() - mano_width) // 2
        mano_y = self.height() - 225
        for i, label in enumerate(mano_remaining):
            anim = QPropertyAnimation(label, b"geometry")
            anim.setDuration(1000)
            anim.setStartValue(label.geometry())
            anim.setEndValue(QRect(mano_start_x + i * 160, mano_y, 150, 225))
            self.realign_animation.addAnimation(anim)
            # Aggiorna le posizioni di hover e fine
            label.hover_rect = QRectF(mano_start_x + i * 160, mano_y - 20, 150, 225)
            label.end_rect = QRectF(mano_start_x + i * 160, mano_y, 150, 225)

        # Calcola la nuova posizione per le carte rimanenti a terra
        terra_width = len(terra_remaining) * 100 + (len(terra_remaining) - 1) * 10
        terra_start_x = (self.width() - terra_width) // 2
        terra_y = self.height() // 2 - 150
        for i, label in enumerate(terra_remaining):
            anim = QPropertyAnimation(label, b"geometry")
            anim.setDuration(1000)
            anim.setStartValue(label.geometry())
            anim.setEndValue(QRect(terra_start_x + i * 110, terra_y, 100, 150))
            self.realign_animation.addAnimation(anim)
            # Aggiorna le posizioni di hover e fine
            label.hover_rect = QRectF(terra_start_x + i * 110, terra_y + 20, 100, 150)
            label.end_rect = QRectF(terra_start_x + i * 110, terra_y, 100, 150)

        # Aggiungi l'animazione della scopa se non ci sono più carte a terra
        if not terra_remaining:
            scopa_animation = self.create_scopa_animation()
            self.realign_animation.addAnimation(scopa_animation)

        self.realign_animation.finished.connect(self.remove_cover_label)
        self.realign_animation.start()

    def create_scopa_animation(self):
        scopa_label = QLabel(self)
        scopa_label.setPixmap(QPixmap("Gioco di Scopa/Icone/Scopa.png"))
        scopa_label.setScaledContents(True)
        scopa_label.setGeometry((self.width() - 600) // 2, (self.height() - 200) // 2, 600, 140)
        scopa_label.setStyleSheet("background: transparent;")
        scopa_label.show()

        # Nascondi l'etichetta dopo 1.5 secondi
        QTimer.singleShot(1700, scopa_label.hide)

        # Aggiorna i punti nel file JSON e l'etichetta dei punti
        with open("Gioco di Scopa/partita.json", "r") as file:
            dati = json.load(file)

        # Incrementa i punti
        dati['punti'] += 1

        # Aggiorna l'etichetta dei punti
        self.label_punti.setText(str(dati['punti']))

        # Forza l'aggiornamento dell'interfaccia utente
        self.label_punti.repaint()

        # Aggiorna il file JSON
        with open("Gioco di Scopa/partita.json", "w") as file:
            json.dump(dati, file)

        # Crea un'animazione vuota che dura quanto l'etichetta della scopa è visibile
        animation = QPropertyAnimation(scopa_label, b"opacity")
        animation.setDuration(1700)
        animation.setStartValue(1)
        animation.setEndValue(1)

        return animation



    def start_move_animation(self, carta_mano, carte_terra_interessate):
        def update_pixmap(label, pixmap):
            label.setPixmap(pixmap.scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        def realign_cards_wrapper():
            self.realign_cards()

        # Carta della mano
        mano_index = self.data["mano"].index(carta_mano)
        mano_label = self.mano_labels[mano_index]
        self.mano_animation = QPropertyAnimation(mano_label, b"geometry")
        self.mano_animation.setDuration(1000)
        start_rect = mano_label.geometry()
        self.mano_animation.setStartValue(start_rect)
        end_rect = QRectF(self.width() / 2 - 50, self.height() / 2 - 75, 100, 150)
        self.mano_animation.setEndValue(end_rect)
        self.mano_animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.mano_animation.valueChanged.connect(lambda _, l=mano_label: update_pixmap(l, QPixmap(f"Gioco di Scopa/Carte/{l.property('card_id')}.png")))

        # Carte a terra
        self.terra_animations = []
        for carta_terra in carte_terra_interessate:
            terra_index = self.data["terra"].index(carta_terra)
            terra_label = self.terra_labels[terra_index]
            terra_animation = QPropertyAnimation(terra_label, b"geometry")
            terra_animation.setDuration(1000)
            start_rect = terra_label.geometry()
            terra_animation.setStartValue(start_rect)
            terra_animation.setEndValue(end_rect)
            terra_animation.setEasingCurve(QEasingCurve.InOutQuad)
            self.terra_animations.append(terra_animation)

        # Animazione generale
        self.group_animation = QParallelAnimationGroup()
        self.group_animation.addAnimation(self.mano_animation)
        for terra_animation in self.terra_animations:
            self.group_animation.addAnimation(terra_animation)

        # Carta della mano
        self.mano_animation2 = QPropertyAnimation(mano_label, b"geometry")
        self.mano_animation2.setDuration(1000)
        self.mano_animation2.setStartValue(end_rect)
        self.mano_animation2.setEndValue(QRectF(-100, 1000, 100, 150))
        self.mano_animation2.setEasingCurve(QEasingCurve.InOutQuad)

        # Carte a terra
        self.terra_animations2 = []
        for carta_terra in carte_terra_interessate:
            terra_index = self.data["terra"].index(carta_terra)
            terra_label = self.terra_labels[terra_index]
            terra_animation2 = QPropertyAnimation(terra_label, b"geometry")
            terra_animation2.setDuration(1000)
            terra_animation2.setStartValue(end_rect)
            terra_animation2.setEndValue(QRectF(-100, 1000, 100, 150))
            terra_animation2.setEasingCurve(QEasingCurve.InOutQuad)
            self.terra_animations2.append(terra_animation2)

        # Animazione generale
        self.group_animation2 = QParallelAnimationGroup()
        self.group_animation2.addAnimation(self.mano_animation2)
        for terra_animation2 in self.terra_animations2:
            self.group_animation2.addAnimation(terra_animation2)

        self.presa_animation = QPropertyAnimation(self.presa_label, b"geometry")
        self.presa_animation.setDuration(1000)
        start_rect = self.presa_label.geometry()
        self.presa_animation.setStartValue(start_rect)
        self.presa_animation.setEndValue(QRectF(-15, 860, 100, 150))
        self.presa_animation.setEasingCurve(QEasingCurve.InOutQuad)

        self.group_animation3 = QSequentialAnimationGroup()
        self.group_animation3.addAnimation(self.group_animation)
        self.group_animation3.addAnimation(self.group_animation2)
        self.group_animation3.addAnimation(self.presa_animation)

        # Aggiungi la sovrapposizione di stile per il label semitrasparente
        self.cover_label = QLabel(self)
        self.cover_label.resize(self.width(), self.height())
        self.cover_label.setStyleSheet("background-color: rgba(0, 0, 0, 1%);")
        self.cover_label.show()

        # Inizia l'animazione
        self.cover_animation = QPropertyAnimation(self.cover_label, b"opacity")
        self.cover_animation.setDuration(200)
        self.cover_animation.setStartValue(0)
        self.cover_animation.setEndValue(1)
        self.cover_animation.finished.connect(lambda: self.group_animation3.start())

        self.group_animation3.finished.connect(lambda: self.cleanup_labels([mano_label], [self.terra_labels[self.data["terra"].index(carta)] for carta in carte_terra_interessate]))
        self.group_animation3.finished.connect(realign_cards_wrapper)

        self.cover_animation.start()

    def remove_cover_label(self):
        if hasattr(self, 'cover_label') and self.cover_label:
            self.cover_label.hide()
            self.cover_label.deleteLater()
            self.cover_label = None

    def cleanup_labels(self, mano_labels_to_remove, terra_labels_to_remove):
        for label in mano_labels_to_remove:
            label.hide()
        for label in terra_labels_to_remove:
            label.hide()
        for label in self.mano_labels + self.terra_labels:
            label.setEnabled(True)



    def start_move_animation2(self, carta_mano):
        def update_pixmap(label, pixmap):
            label.setPixmap(pixmap.scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        def realign_cards_wrapper():
            self.realign_cards()

        # Aggiungi la sovrapposizione di stile per il label semitrasparente
        self.cover_label = QLabel(self)  # Rinomina la cover_label per evitare conflitti
        self.cover_label.resize(self.width(), self.height())
        self.cover_label.setStyleSheet("background-color: rgba(0, 0, 0, 1%);")
        self.cover_label.show()

        # Individua la carta della mano
        mano_index = self.data["mano"].index(carta_mano)
        mano_label = self.mano_labels[mano_index]

        # Anima la carta dalla mano a terra
        self.move_animation = QPropertyAnimation(mano_label, b"geometry")
        self.move_animation.setDuration(1000)
        start_rect = mano_label.geometry()
        end_rect = QRectF(self.width() / 2 - 50, self.height() / 2 - 75, 100, 150)  # Posizione centrale per l'animazione
        self.move_animation.setStartValue(start_rect)
        self.move_animation.setEndValue(end_rect)
        self.move_animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.move_animation.valueChanged.connect(lambda _, l=mano_label: update_pixmap(l, QPixmap(f"Gioco di Scopa/Carte/{l.property('card_id')}.png")))

        # Aggiungi la carta a terra dopo l'animazione
        def add_card_to_terra():
            self.data["mano"].remove(carta_mano)
            self.mano_labels.remove(mano_label)
            self.data["terra"].append(carta_mano)
            self.terra_labels.append(mano_label)
            mano_label.setParent(self)
            mano_label.show()
            realign_cards_wrapper()

        self.move_animation.finished.connect(add_card_to_terra)

        # Inizia l'animazione
        self.cover_animation = QPropertyAnimation(self.cover_label, b"windowOpacity")
        self.cover_animation.setDuration(200)
        self.cover_animation.setStartValue(0)
        self.cover_animation.setEndValue(1)
        self.cover_animation.finished.connect(lambda: self.move_animation.start())

        self.cover_animation.start()






    def position_labels(self):
        # Posiziona i label del nome cattivo e dei punti
        self.label_nome_cattivo.move(10, 10)
        self.label_punti_cattivo.move(10, 60)

        self.label_nome.move(self.width() - self.label_nome_cattivo.width() - 60, 560)
        self.label_punti.move(self.width() - self.label_punti.width() - 10, 620)

    def start_animation(self):
        # Crea un QLabel trasparente che copre tutto
        self.cover_label = QLabel(self)
        self.cover_label.resize(self.width(), self.height())  # Assicurati che copra tutto il widget
        self.cover_label.setStyleSheet("background-color: rgba(0, 0, 0, 100);")  # Imposta un colore di sfondo trasparente

        # Crea un QPixmap con l'immagine che vuoi mostrare al centro
        center_pixmap = QPixmap("Gioco di Scopa/Icone/via.png")
        center_pixmap = center_pixmap.scaled(500, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Ridimensiona l'immagine se necessario

        self.cover_label2 = QLabel(self)
        self.cover_label2.resize(self.width(), self.height())  # Assicurati che copra tutto il widget
        self.cover_label2.setStyleSheet("background-color: none;")  # Imposta un colore di sfondo trasparente

        # Crea un altro QLabel per l'immagine centrale
        self.center_image_label = QLabel(self.cover_label2)
        self.center_image_label.setPixmap(center_pixmap)
        self.center_image_label.setAlignment(Qt.AlignCenter)  # Centra l'immagine
        self.center_image_label.setGeometry((self.width() - center_pixmap.width()) // 2, (self.height() - center_pixmap.height()) // 2, center_pixmap.width(), center_pixmap.height())
        self.cover_label.show()
        self.cover_label2.show()

        # Inizia l'animazione
        self.animations_group = QSequentialAnimationGroup()  # Modifica qui

        # Definisci una funzione di aggiornamento per ridimensionare l'immagine
        def update_pixmap(label, pixmap):
            label.setPixmap(pixmap.scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        # Calcola la posizione centrale in basso
        centro_basso_x = int(self.width() / 2 - (len(self.mano_labels) * 150 + (len(self.mano_labels) - 1) * 10) / 2) + 15  # 
        centro_basso_y = self.height() - 225  # Posiziona l'immagine in basso

        # Crea le animazioni per le carte della mano
        self.mano_animations = []
        for i, label in enumerate(self.mano_labels):
            animation = QPropertyAnimation(label, b"geometry")
            animation.setDuration(250)
            animation.setStartValue(QRectF(-150, int(self.height() / 2 - 75), 100, 150))
            # Aggiusta la posizione x per centrare le carte
            end_rect = QRectF(centro_basso_x + i * (150 + 10), centro_basso_y, 150, 225)
            animation.setEndValue(end_rect)
            animation.setEasingCurve(QEasingCurve.InOutQuad)
            animation.valueChanged.connect(lambda _, l=label: update_pixmap(l, QPixmap(f"Gioco di Scopa/Carte/{l.property('card_id')}.png")))
            self.mano_animations.append(animation)

        self.terra_animations = []
        for i, label in enumerate(self.terra_labels):
            animation = QPropertyAnimation(label, b"geometry")
            animation.setDuration(250)
            animation.setStartValue(QRectF(-150, int(self.height() / 2 - 75), 100, 150))
            # Calcola la posizione finale per le carte a terra
            end_rect = QRectF(int(self.width() / 2 - (len(self.terra_labels) * 100 + (len(self.terra_labels) - 5) * 10) / 2) + i * (100 + 10), int(self.height() / 2 - 150), 100, 150)
            animation.setEndValue(end_rect)
            animation.setEasingCurve(QEasingCurve.InOutQuad)
            self.terra_animations.append(animation)

        # Crea le animazioni per i retro delle carte
        self.retro_animations = []
        for i, label in enumerate(self.retro_labels):
            animation = QPropertyAnimation(label, b"geometry")
            animation.setDuration(250)
            animation.setStartValue(QRectF(-150, int(self.height() / 2 - 75), 100, 150))
            # Calcola la posizione finale per i retro delle carte
            end_rect = QRectF(int(self.width() / 2 - 100 + i * 75), 10, 75, 112.5)
            animation.setEndValue(end_rect)
            animation.setEasingCurve(QEasingCurve.InOutQuad)
            animation.valueChanged.connect(lambda _, l=label: update_pixmap(l, QPixmap(f"Gioco di Scopa/Carte/0.png")))
            self.retro_animations.append(animation)

        x = max(len(self.mano_animations), len(self.terra_animations), len(self.retro_animations))

        for i in range(x):
            if i < len(self.mano_animations):
                self.animations_group.addAnimation(self.mano_animations[i])
            if i < len(self.terra_animations):
                self.animations_group.addAnimation(self.terra_animations[i])
            if i < len(self.retro_animations):
                self.animations_group.addAnimation(self.retro_animations[i])
        
        # Connetti il segnale finished dell'animations_group con il metodo animation_finished
        self.animations_group.finished.connect(self.animation_finished)
        self.animations_group.start()

    def animation_finished(self):
        # Crea un effetto di opacità per il QLabel trasparente
        self.cover_opacity_effect = QGraphicsOpacityEffect(self.cover_label)
        self.cover_label.setGraphicsEffect(self.cover_opacity_effect)

        # Crea un effetto di opacità per l'immagine centrale
        self.center_opacity_effect = QGraphicsOpacityEffect(self.center_image_label)
        self.center_image_label.setGraphicsEffect(self.center_opacity_effect)

        # Crea un'animazione di opacità per il QLabel trasparente
        self.fade_animation = QPropertyAnimation(self.cover_opacity_effect, b"opacity")
        self.fade_animation.setDuration(1000)  # Durata dell'effetto di dissolvenza
        self.fade_animation.setStartValue(1.0)  # Inizia completamente visibile
        self.fade_animation.setEndValue(0.0)  # Finisce completamente trasparente
        self.fade_animation.setEasingCurve(QEasingCurve.Linear)  # Velocità costante

        # Collega l'animazione di opacità al cambiamento di opacità del QLabel
        self.fade_animation.valueChanged.connect(lambda value: self.set_label_opacity(value))

        # Quando l'animazione di opacità è finita, rimuovi i QLabel
        self.fade_animation.finished.connect(lambda: self.center_image_label.deleteLater())
        self.fade_animation.finished.connect(lambda: self.cover_label.deleteLater())

         # Quando l'animazione di opacità è finita, rimuovi i QLabel
        self.fade_animation.finished.connect(self.remove_labels)

        # Avvia l'animazione di opacità
        self.fade_animation.start()

    def remove_labels(self):
        # Rimuove i QLabel dalla memoria
        self.center_image_label.deleteLater()
        self.cover_label.deleteLater()
        self.cover_label2.deleteLater()

    def set_label_opacity(self, value):
        # Imposta l'opacità del QLabel trasparente e dell'immagine centrale
        self.cover_opacity_effect.setOpacity(value)
        self.center_opacity_effect.setOpacity(value)

# 11 Classe per la pagina del End Bot, eredita dalla classe Page
class EndBotPage(Page):
    def __init__(self, stacked_layout, sound_manager, parent=None):
        super().__init__(parent)
        self.stacked_layout = stacked_layout
        self.sound_manager = sound_manager




    def open_account_settings(self):
        self.sound_manager.play_click_sound()
        self.stacked_layout.setCurrentIndex(2)

    def open_account_settings(self):
        self.sound_manager.play_click_sound()
        self.stacked_layout.setCurrentIndex(10)


# 12 Classe per la pagina del regolamento, eredita dalla classe Page
class RegolamentoPage(Page):
    def __init__(self, stacked_layout, sound_manager, parent=None):
        super().__init__(parent)
        self.stacked_layout = stacked_layout
        self.sound_manager = sound_manager

        # Bottone per le impostazioni 
        self.impostazioni_button = QPushButton()
        self.impostazioni_button.setStyleSheet(d)
        self.impostazioni_button.setFixedSize(50, 80)
        self.impostazioni_button.clicked.connect(self.torna_alle_impostazioni)

        # Aggiungi un'immagine di regolamento
        self.regolamento_image_label = QLabel()
        self.pixmap = QPixmap("Gioco di Scopa/Icone/regolamento.png")
        self.regolamento_image_label.setPixmap(self.pixmap.scaledToHeight(80))
        self.regolamento_image_label.setAlignment(Qt.AlignCenter)

        # Aggiungi spazio
        self.spazio_label = QLabel(" ")
        self.spazio_label.setStyleSheet(testo)

        # Testo del regolamento della Scopa
        testo_regolamento = """
Regolamento della Scopa

    Obiettivo del gioco:
        Il gioco della Scopa si svolge con un mazzo di carte italiane tradizionali, e l'obiettivo è fare punti acquisendo le carte dal tavolo con le carte della propria mano.

    Preparazione:

        Il mazzo è composto da 40 carte divise in quattro semi: denari, coppe, spade e bastoni. Ogni seme ha dieci carte numerate dall'1 al 7 e tre carte figurate: fante (8), cavallo (9) e re (10).
        Il gioco si svolge tra due giocatori o tra due squadre di due giocatori ciascuna.
        All'inizio della partita, si distribuiscono tre carte a testa ai giocatori e quattro carte sul tavolo, scoperte.

    Svolgimento del gioco:

        Il primo giocatore gioca una carta dalla propria mano.
        Il secondo giocatore risponde con una carta.
        Se il valore della carta giocata dal secondo giocatore è uguale a quello di una o più carte sul tavolo, il secondo giocatore prende tutte le carte corrispondenti (scopa).
        Se il valore della carta giocata dal secondo giocatore è diverso da quello di tutte le carte sul tavolo, le carte sul tavolo rimangono sul tavolo.
        Si continua a giocare alternando i turni fino a quando entrambi i giocatori hanno esaurito le carte della propria mano.
    
    Punteggio:

        Ogni scopa vale 1 punto.
        Al termine del gioco, vengono assegnati punti aggiuntivi per aver raccolto determinate combinazioni di carte:
        Sette di denari: 1 punto (se stai seriamente leggendo tutto sei un pazzo ma ti voglio bene)
        Primiera: punti attribuiti al giocatore o alla squadra con il maggior numero di carte del sette (21 punti in totale)
        Settebello: 1 punto aggiuntivo per il giocatore o la squadra che ha raccolto il sette di denari
        Se si raccolgono tutte le carte sul tavolo (scopa d'assi), si ottiene un punto aggiuntivo.
    
    Vincita:
        Il gioco termina quando tutte le carte sono state giocate. Vince il giocatore o la squadra che ha totalizzato il maggior numero di punti.

    Conclusione:
        Queste sono le regole di base per il gioco della Scopa. Esistono molte varianti regionali e personali, quindi è possibile adattare il regolamento in base alle preferenze dei giocatori.
        """

        # Creazione del widget QTextEdit con il testo del regolamento
        text_edit = QTextEdit()
        text_edit.setPlainText(testo_regolamento)
        text_edit.setStyleSheet("font: 15px Arial; color: white; background-color: #0076BA;")
        text_edit.setReadOnly(True)

        # Creazione dell'area di scorrimento e aggiunta del QTextEdit ad essa
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(text_edit)

        # Creazione di un layout orizzontale per gli elementi
        impostazioni_button_layout = QHBoxLayout()
        impostazioni_button_layout.addWidget(self.impostazioni_button)
        impostazioni_button_layout.setAlignment(Qt.AlignLeft)

        impostazioni_button_layout_top = QHBoxLayout()
        impostazioni_button_layout_top.addLayout(impostazioni_button_layout)
        impostazioni_button_layout_top.setAlignment(Qt.AlignTop)

        # Creazione di un layout orizzontale per gli elementi
        regolamento_image_label_layout = QHBoxLayout()
        regolamento_image_label_layout.addWidget(self.regolamento_image_label)
        regolamento_image_label_layout.setAlignment(Qt.AlignCenter)

        # Creazione di un layout orizzontale per gli elementi
        top_buttons_layout = QHBoxLayout()
        top_buttons_layout.addLayout(impostazioni_button_layout_top)
        top_buttons_layout.addLayout(regolamento_image_label_layout)
        top_buttons_layout.addWidget(self.spazio_label)
        top_buttons_layout.setAlignment(Qt.AlignTop)

        # layout base
        layout_base = QVBoxLayout()
        layout_base.addLayout(top_buttons_layout)
        layout_base.addWidget(scroll_area)
        layout_base.setAlignment(Qt.AlignTop)

        # Aggiunta dei layout al layout verticale principale
        self.layout.addLayout(layout_base)


    def torna_alle_impostazioni(self):
        self.sound_manager.play_click_sound()
        self.stacked_layout.setCurrentIndex(4)

# 13 Classe per la pagina di login2, eredita dalla classe Page
class Login2Page(Page):
    def __init__(self, stacked_layout, sound_manager, account_page, impostazioni_page, parent=None):
        super().__init__(parent)
        self.stacked_layout = stacked_layout
        self.sound_manager = sound_manager
        self.account_page = account_page
        self.impostazioni_page = impostazioni_page

        # Bottone per le impostazioni 
        self.d_button = QPushButton()
        self.d_button.setStyleSheet(d)
        self.d_button.setFixedSize(50, 80)
        self.d_button.clicked.connect(self.torna_al_account)

        # Aggiungi un'immagine di accesso
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.pixmap = QPixmap("Gioco di Scopa/Icone/accedi.png")
        self.image_label.setPixmap(self.pixmap.scaledToHeight(80))

        # Aggiungi spazio
        self.spazio_label = QLabel(" ")
        self.spazio_label.setStyleSheet(testo)

        # Creazione di un layout orizzontale per gli elementi
        d_button_layout = QHBoxLayout()
        d_button_layout.addWidget(self.d_button)
        d_button_layout.setAlignment(Qt.AlignLeft)

        d_button_layout_top = QHBoxLayout()
        d_button_layout_top.addLayout(d_button_layout)
        d_button_layout_top.setAlignment(Qt.AlignTop)

        # Creazione di un layout orizzontale per gli elementi
        image_label_layout = QHBoxLayout()
        image_label_layout.addWidget(self.image_label)
        image_label_layout.setAlignment(Qt.AlignCenter)

        # Creazione di un layout orizzontale per gli elementi
        top_buttons_layout = QHBoxLayout()
        top_buttons_layout.addLayout(d_button_layout_top)
        top_buttons_layout.addLayout(image_label_layout)
        top_buttons_layout.addWidget(self.spazio_label)
        top_buttons_layout.setAlignment(Qt.AlignTop)

        self.layout.addLayout(top_buttons_layout)

        # Aggiungi etichette e campi di inserimento per l'utente, l'email e la password
        self.user_name_label = QLabel("Inserisci l'User Name:")
        self.layout.addWidget(self.user_name_label)
        self.user_name_label.setStyleSheet(testo)
        self.user_name_entry = QLineEdit()
        self.user_name_entry.setStyleSheet(textinput)
        self.layout.addWidget(self.user_name_entry)

        self.email_label = QLabel("Inserisci l'Email:")
        self.layout.addWidget(self.email_label)
        self.email_label.setStyleSheet(testo)
        self.email_entry = QLineEdit()
        self.email_entry.setStyleSheet(textinput)
        self.layout.addWidget(self.email_entry)

        self.password_label = QLabel("Inserisci la Password:")
        self.password_label.setStyleSheet(testo)
        self.layout.addWidget(self.password_label)
        self.password_entry = QLineEdit()
        self.password_entry.setStyleSheet(textinput)
        # Imposta lo stile per nascondere i caratteri della password
        self.password_entry.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.password_entry)

        # Crea un layout orizzontale per organizzare i bottoni affiancati
        self.button_layout = QHBoxLayout()

        # Aggiungi pulsanti per accedere e registrarsi
        self.access_button = QPushButton("Accedi")
        self.access_button.setStyleSheet(bottone)
        self.access_button.clicked.connect(self.access)
        self.button_layout.addWidget(self.access_button)

        self.register_button = QPushButton("Registrati")
        self.register_button.setStyleSheet(bottone)
        self.register_button.clicked.connect(self.register)
        self.button_layout.addWidget(self.register_button)

        # Aggiunta dei layout al layout verticale principale
        self.layout.addLayout(self.button_layout)

        # Aggiungi una label per visualizzare eventuali risultati o messaggi
        self.result_label = QLabel("")
        self.result_label.setStyleSheet(testo)
        self.layout.addWidget(self.result_label)

    # Funzione per verificare se una stringa è un'email valida
    def is_valid_email(self, email):
        if email:
            # Definisci un'espressione regolare per la validazione dell'email
            regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            # Verifica se l'email corrisponde all'espressione regolare
            return re.match(regex, email) is not None
        else:
            return True

    def access(self):
        self.sound_manager.play_click_sound()
        credenziali_corrette = False
        # Ottieni i dati inseriti dall'utente
        user_name = self.user_name_entry.text()
        email = self.email_entry.text()
        pwd = self.password_entry.text()
        password = hashlib.md5(pwd.encode()).hexdigest()

        # Verifica se l'email è valida
        if not self.is_valid_email(email):
            self.result_label.setText("Inserisci un'email valida")
            return

        # Dati da inviare al server
        data_to_send = {
            'user_name': user_name,  # Chiave corretta per l'utente
            'email': email,          # Indirizzo email
            'password': password     # Password
        }

        try:
            # Invia i dati al server tramite una richiesta POST
            response = requests.post('http://localhost:8080/access', data=data_to_send)
            # Verifica lo stato della risposta
            if response.status_code == 200:
                # Se la richiesta ha avuto successo, visualizza il messaggio di risposta dal server
                self.result_label.setText(response.json()['message'])
                credenziali_corrette = response.json()['accesso_effettuato']
                if credenziali_corrette:
                    self.stacked_layout.setCurrentIndex(1)  # Mostra la pagina di verifica
                    with open('Gioco di Scopa/dati.json', 'r') as file:
                        dati = json.load(file)

                    # Aggiorna o aggiungi il dato desiderato
                    dati['user_name'] = user_name
                    dati['email'] = email
                    dati['password'] = password

                    # Scrivi la struttura dati aggiornata nel file JSON
                    with open('Gioco di Scopa/dati.json', 'w') as file:
                        json.dump(dati, file)
            else:
                # Se c'è stato un errore nella richiesta, visualizza un messaggio di errore generico
                self.result_label.setText('Errore durante la richiesta al server')
        except requests.exceptions.ConnectionError:
            # Se non è possibile connettersi al server, visualizza un messaggio di errore
            self.result_label.setText('Errore durante la connessione al server')

    def register(self):
        self.sound_manager.play_click_sound()
        credenziali_corrette = False
        # Ottieni i dati inseriti dall'utente
        user_name = self.user_name_entry.text()
        email = self.email_entry.text()
        pwd = self.password_entry.text()
        password = hashlib.md5(pwd.encode()).hexdigest()

        # Verifica se l'email è valida
        if not self.is_valid_email(email):
            self.result_label.setText("Inserisci un'email valida")
            return

        # Dati da inviare al server
        data_to_send = {
            'user_name': user_name,  # Chiave corretta per l'utente
            'email': email,          # Indirizzo email
            'password': password     # Password
        }

        try:
            # Invia i dati al server tramite una richiesta POST
            response = requests.post('http://localhost:8080/register', data=data_to_send)
            # Verifica lo stato della risposta
            if response.status_code == 200:
                # Se la richiesta ha avuto successo, visualizza il messaggio di risposta dal server
                self.result_label.setText(response.json()['message'])
                credenziali_corrette = response.json()['accesso_effettuato']
                if credenziali_corrette:
                    self.stacked_layout.setCurrentIndex(1)  # Mostra la pagina di verifica
                    with open('Gioco di Scopa/dati.json', 'r') as file:
                        dati = json.load(file)

                    # Aggiorna o aggiungi il dato desiderato
                    dati['user_name'] = user_name
                    dati['email'] = email
                    dati['password'] = password

                    # Scrivi la struttura dati aggiornata nel file JSON
                    with open('Gioco di Scopa/dati.json', 'w') as file:
                        json.dump(dati, file)
            else:
                # Se c'è stato un errore nella richiesta, visualizza un messaggio di errore generico
                self.result_label.setText('Errore durante la richiesta al server')
        except requests.exceptions.ConnectionError:
            # Se non è possibile connettersi al server, visualizza un messaggio di errore
            self.result_label.setText('Errore durante la connessione al server')

    def torna_al_account(self):
        self.sound_manager.play_click_sound()
        self.stacked_layout.setCurrentIndex(3)
        with open('Gioco di Scopa/dati2.json', 'r') as file:
            dati = json.load(file)

        # Scrivi la struttura dati aggiornata nel file JSON
        with open('Gioco di Scopa/dati.json', 'w') as file:
            json.dump(dati, file)

        # Elimina il veccio file
        os.remove('Gioco di Scopa/dati2.json')

        self.account_page.nomee()
        self.account_page.vittoriee()
        self.account_page.sconfittee()
        self.account_page.percentualee()
        self.impostazioni_page.on_musica_volume_changed(50)
        self.impostazioni_page.on_tasti_suono_changed(50)
        self.impostazioni_page.get_vittorie()



# Classe principale per la finestra principale dell'applicazione
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GIOCO DI SCOPA")
        # self.setStyleSheet("background-color: #0076BA;")
        self.setGeometry(100, 100, 600, 1000)
        self.setFixedSize(600, 1000)  # Imposta una dimensione fissa più adatta ai telefoni

        self.background_label = QLabel(self)
        self.setBackgroundImage("Gioco di Scopa/Icone/si.png")  # Sostituisci "sfondo.jpg" con il percorso dell'immagine desiderata

        self.music_manager = MusicManager()
        self.music_manager.play_background_music()
        self.sound_manager = SoundManager()

        # Utilizza un layout verticale per gestire le pagine in modo dinamico
        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.setContentsMargins(0, 0, 0, 0)

        # Creazione di un layout impilato per gestire le pagine
        self.stacked_layout = QStackedLayout()

        # Creazione delle istanze delle pagine
        self.login_page = LoginPage(self.stacked_layout, self.sound_manager)
        self.home_page = HomePage(self.stacked_layout, self.sound_manager)
        self.account_page = AccountPage(self.stacked_layout, self.sound_manager)
        self.impostazioni_page = ImpostazioniPage(self.stacked_layout, self.sound_manager, self.music_manager)
        self.verification_page = VerificationPage(self.stacked_layout, self.sound_manager, self.account_page, self.impostazioni_page)
        self.giocatori_page = GiocatoriPage(self.stacked_layout, self.sound_manager)
        self.attesa_page = AttesaPage(self.stacked_layout, self.sound_manager)
        self.tipo_di_gioco_page = TipoDiGiocoPage(self.stacked_layout, self.sound_manager, self.attesa_page)
        self.game_online_page = GameOnlinePage(self.stacked_layout, self.sound_manager)
        self.win_online_page = WinOnlinePage(self.stacked_layout, self.sound_manager)
        self.game_bot_page = GameBotPage(self.stacked_layout, self.sound_manager)
        self.end_bot_page = EndBotPage(self.stacked_layout, self.sound_manager)
        self.regolamento_page = RegolamentoPage(self.stacked_layout, self.sound_manager)
        self.login2_page = Login2Page(self.stacked_layout, self.sound_manager, self.account_page, self.impostazioni_page)
        self.lose_online_page = LoseOnlinePage(self.stacked_layout, self.sound_manager)
        self.par_online_page = ParOnlinePage(self.stacked_layout, self.sound_manager)

        # Aggiunta delle pagine al layout impilato
        self.stacked_layout.addWidget(self.login_page)
        self.stacked_layout.addWidget(self.verification_page)
        self.stacked_layout.addWidget(self.home_page)
        self.stacked_layout.addWidget(self.account_page)
        self.stacked_layout.addWidget(self.impostazioni_page)
        self.stacked_layout.addWidget(self.giocatori_page)
        self.stacked_layout.addWidget(self.tipo_di_gioco_page)
        self.stacked_layout.addWidget(self.attesa_page)
        self.stacked_layout.addWidget(self.game_online_page)
        self.stacked_layout.addWidget(self.win_online_page)
        self.stacked_layout.addWidget(self.game_bot_page)
        self.stacked_layout.addWidget(self.end_bot_page)
        self.stacked_layout.addWidget(self.regolamento_page)
        self.stacked_layout.addWidget(self.login2_page)
        self.stacked_layout.addWidget(self.lose_online_page)
        self.stacked_layout.addWidget(self.par_online_page)

        with open('Gioco di Scopa/dati.json', 'r') as file:
            # Carica i dati dal file JSON
            user_name = json.load(file)['user_name']

        if user_name == "":
            if os.path.exists('Gioco di Scopa/dati2.json'):
                self.stacked_layout.setCurrentIndex(13)
            else:
                self.stacked_layout.setCurrentIndex(0)
        else:
            self.stacked_layout.setCurrentIndex(2)

        # Impostazione del layout impilato come layout centrale della finestra
        central_widget = QWidget()
        central_widget.setLayout(self.stacked_layout)
        self.setCentralWidget(central_widget)

    def setBackgroundImage(self, image_path):
        pixmap = QPixmap(image_path)
        self.background_label.setPixmap(pixmap)
        self.background_label.setGeometry(0, 0, self.width(), self.height())

    def resizeEvent(self, event):
        # Ridimensiona l'immagine di sfondo ogni volta che la finestra viene ridimensionata
        self.setBackgroundImage("Gioco di Scopa/Icone/si.png")

    # All'interno della classe MainWindow aggiungi il seguente metodo
    def closeEvent(self, event):
        # Chiamare la funzione esci solo se la pagina corrente è la pagina di attesa (indice 7)
        if self.stacked_layout.currentIndex() == 7:
            # Dati da inviare al server
            data_to_send = {
                'user_name': self.attesa_page.user_name  # Chiave corretta per l'utente
            }
            try:
                # Invia i dati al server tramite una richiesta POST
                response = requests.post('http://localhost:8080/exit_game', data=data_to_send)
                # Verifica lo stato della risposta
                if response.status_code == 200:
                    # Carica i dati dal file JSON in un dizionario
                    with open('Gioco di Scopa/dati.json', 'r') as file:
                        dati = json.load(file)
                    # Aggiorna o aggiungi il dato desiderato
                    dati['stato'] = response.json()['player']
                    dati['numero'] = response.json()['player']
                    # Scrivi la struttura dati aggiornata nel file JSON
                    with open('Gioco di Scopa/dati.json', 'w') as file:
                        json.dump(dati, file)

                    self.attesa_page.setstatus()
                    self.stacked_layout.setCurrentIndex(2)
                    print("Stopping controls...")
                    print("sono stato io ")
                else:
                    pass
            except requests.exceptions.ConnectionError:
                pass
            event.accept()
        else:
            print("fottiti")


# Blocco principale per avviare l'applicazione
if __name__ == "__main__":
    import sys

    # Creazione dell'applicazione Qt
    app = QApplication(sys.argv)

    # Creazione della finestra principale e visualizzazione
    window = MainWindow()
    window.show()

    # Esecuzione dell'applicazione Qt
    sys.exit(app.exec_())