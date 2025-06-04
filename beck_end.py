from flask import Flask, request, jsonify
from flask_mail import Mail, Message
import sqlite3
import random
import hashlib
import json

#cercare in https://myaccount.google.com/security "Accesso meno sicuro delle app" e prendere l'opzione "Passwuord per le App" generare la password e inserirla
app = Flask(__name__)
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='giovanni.gpr5@gmail.com',
    MAIL_PASSWORD='pzqv tgyn imii vvzf',
    MAIL_DEFAULT_SENDER='giovanni.gpr5@gmail.com'
)
mail = Mail(app)

# Funzione per inizializzare il database e la tabella degli utenti
# User(User_Name, Email, Password, Vittorie, Sconfitte, Punti_Vittoria, tipo, Code)
# Partita(ID_Partita, Mazzo, Terra, Giocatori, Stato)
# Giocatore(ID_Giocatore, ID_Partita, User_Name, Mano, Carte, Punti)
def initialize_database():
    conn = sqlite3.connect('Gioco di Scopa/database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS User (
                    User_Name TEXT PRIMARY KEY,
                    Email TEXT UNIQUE NOT NULL,
                    Password TEXT NOT NULL,
                    Vittorie INTEGER DEFAULT 0,
                    Sconfitte INTEGER DEFAULT 0,
                    Punti_Vittoria TEXT CHECK(Punti_Vittoria IN ('11', '21')) DEFAULT '11',
                    tipo TEXT CHECK(tipo IN ('1', '2', '3')) DEFAULT '1',
                    Code TEXT
                )
                ''')
    c.execute('DROP TABLE Partita')
    c.execute('''CREATE TABLE IF NOT EXISTS Partita (
                    ID_Partita INTEGER PRIMARY KEY AUTOINCREMENT,
                    Mazzo BLOB,
                    Terra BLOB,
                    Giocatori TEXT CHECK(Giocatori IN ('2', '3', '4')),
                    Punti TEXT CHECK(Punti IN ('11', '21')),
                    Giocatori_Online INTEGER,
                    Ultima_Mossa TEXT CHECK(Ultima_Mossa IN ('1', '2', '3', '4')),
                    Ultima_Presa INTEGER,
                    carta_mano BLOB,
                    carte_prese BLOB,
                    Stato TEXT CHECK(Stato IN ('ricerca', 'ricerca conclusa', 'in corso', 'finita')) DEFAULT 'ricerca'
                )
                ''')
    c.execute('DROP TABLE Giocatore')
    c.execute('''CREATE TABLE IF NOT EXISTS Giocatore (
                    ID_Giocatore INTEGER PRIMARY KEY AUTOINCREMENT,
                    ID_Partita INTEGER,
                    User_Name TEXT,
                    Mano BLOB,
                    Carte BLOB,
                    Punt INTEGER,
                    Numero TEXT CHECK(Numero IN ('1', '2', '3', '4')),
                    FOREIGN KEY(ID_Partita) REFERENCES Partita(ID_Partita) ON DELETE CASCADE,
                    FOREIGN KEY(User_Name) REFERENCES User(User_Name) ON DELETE CASCADE
                )
                ''')
    conn.commit()
    conn.close()


# Funzione per effettuare il login dell'utente
def Log_in(user_name, email, password):
    conn = sqlite3.connect('Gioco di Scopa/database.db')
    c = conn.cursor()
    c.execute("SELECT User_Name FROM User WHERE User_Name=? AND Email=? AND Password=?", (user_name, email, password))
    result = c.fetchone()
    conn.close()
    return result is not None

# Funzione per verificare l'esistenza dell'User Name nel database
def user_name_exists(user_name):
    conn = sqlite3.connect('Gioco di Scopa/database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM User WHERE User_Name=?", (user_name,))
    result = c.fetchone()
    conn.close()
    return result is not None

# Funzione per verificare l'esistenza dell'email nel database
def email_exists(email):
    conn = sqlite3.connect('Gioco di Scopa/database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM User WHERE Email=?", (email,))
    result = c.fetchone()
    conn.close()
    return result is not None

# Funzione per verificare l'esistenza della password nel database
def password_exists(password):
    conn = sqlite3.connect('Gioco di Scopa/database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM User WHERE Password=?", (password,))
    result = c.fetchone()
    conn.close()
    return result is not None

# Funzione per registrare un nuovo utente nel database
def Sing_in(user_name, email, password):
    conn = sqlite3.connect('Gioco di Scopa/database.db')
    c = conn.cursor()
    c.execute("INSERT INTO User(User_Name, Email, Password) VALUES (?, ?, ?)", (user_name, email, password))
    conn.commit()
    conn.close()

# Funzione per inviare l'email di registrazione
def send_registration_email(user_name, email):
    # Genera tre cifre casuali
    prima_parte = str(random.randint(1, 999)).zfill(3)
    seconda_parte = str(random.randint(1, 999)).zfill(3)

    # Combina le due parti in un'unica stringa
    codice = f"{prima_parte} {seconda_parte}"
    msg = Message('Benvenuto nel nostro gioco di Scopa!', recipients=[email])
    msg.html = f'''
    <div style="background-color: #52B488; padding: 20px; text-align: center;">
        <img src="https://i.ibb.co/bRS8CDz/logo.png" style="width: 100px; height: 70px;">
        <h2 style="color: white;">Benvenuto {user_name}!</h2>
        <p style="color: white;">Grazie per esserti unito a noi nel fantastico mondo della Scopa online!</p>
        <p style="color: white;">Per completare la tua registrazione, inserisci il seguente codice di verifica:</p>
        <h1 style="color: #FFFFFF;">{codice}</h1>
        <p style="color: white;">Grazie per unirti a noi e buon divertimento!</p>
    </div>
    '''# grazie Adriano Catuogno per far caricare l'immagine nella mail
    mail.send(msg)

    cod = f"{prima_parte}{seconda_parte}"
    codice_verifica = hashlib.md5(cod.encode()).hexdigest()

    # Aggiorna il codice di verifica nel database
    conn = sqlite3.connect('Gioco di Scopa/database.db')
    c = conn.cursor()
    c.execute("UPDATE User SET Code=? WHERE Email=?", (codice_verifica, email))
    conn.commit()
    conn.close()

# Funzione per verificare l'esistenza della password nel database
def codice_verifica(email, codice):
    conn = sqlite3.connect('Gioco di Scopa/database.db')
    c = conn.cursor()
    c.execute("SELECT Code FROM User WHERE Email=?", (email,))
    result = c.fetchone()
    conn.close()
    if str(result[0])==str(codice):
        return True
    else:
        return False

# Endpoint per gestire le richieste di accesso
@app.route('/register', methods=['POST'])
def register():
    user_name = request.form.get('user_name')
    email = request.form.get('email')
    password = request.form.get('password')

    if user_name and email and password:
        if user_name_exists(user_name) or email_exists(email):        
            if user_name_exists(user_name) and email_exists(email):
                return jsonify({'message': 'User Name e Email già esistenti', 'accesso_effettuato': False})
            
            elif user_name_exists(user_name):
                return jsonify({'message': 'User Name già esistente', 'accesso_effettuato': False})

            elif email_exists(email):
                    return jsonify({'message': 'Email già esistente', 'accesso_effettuato': False})
        else:
            Sing_in(user_name, email, password)
            send_registration_email(user_name, email)
            return jsonify({'message': 'Account realizzato con successo', 'accesso_effettuato': True})

    else:
        if user_name:
            if email:
                return jsonify({'message': 'Password mancante', 'accesso_effettuato': False})
            elif password:
                return jsonify({'message': 'Email mancante', 'accesso_effettuato': False})
            else:
                return jsonify({'message': 'Email e Password mancanti', 'accesso_effettuato': False})

        elif email:
            if user_name:
                return jsonify({'message': 'Password mancante', 'accesso_effettuato': False})
            elif password:
                return jsonify({'message': 'User Name mancante', 'accesso_effettuato': False})
            else:
                return jsonify({'message': 'User Name e Password mancanti', 'accesso_effettuato': False})

        elif password:
            if user_name:
                return jsonify({'message': 'Email mancante', 'accesso_effettuato': False})
            elif email:
                return jsonify({'message': 'User Name mancante', 'accesso_effettuato': False})
            else:
                return jsonify({'message': 'User Name e Email mancanti', 'accesso_effettuato': False})
        
        else:
            return jsonify({'message': 'User Name, Email e Password mancanti', 'accesso_effettuato': False})

# Endpoint per gestire le richieste di accesso
@app.route('/access', methods=['POST'])
def access():
    user_name = request.form.get('user_name')
    email = request.form.get('email')
    password = request.form.get('password')

    if user_name and email and password:
        if Log_in(user_name, email, password):
            send_registration_email(user_name, email)
            return jsonify({'message': 'Log in effettuato con successo', 'accesso_effettuato': True})
        else:
            if user_name_exists(user_name):
                if email_exists(email):
                    return jsonify({'message': 'Password non valido', 'accesso_effettuato': False})
                elif password_exists(password):
                    return jsonify({'message': 'Email non valido', 'accesso_effettuato': False})
                else:
                    return jsonify({'message': 'Email e Password non validi', 'accesso_effettuato': False})

            elif email_exists(email):
                if user_name_exists(user_name):
                    return jsonify({'message': 'Password non valido', 'accesso_effettuato': False})
                elif password_exists(password):
                    return jsonify({'message': 'User Name non valido', 'accesso_effettuato': False})
                else:
                    return jsonify({'message': 'User Name e Password non validi', 'accesso_effettuato': False})

            elif password_exists(password):
                if user_name_exists(user_name):
                    return jsonify({'message': 'Email non valido', 'accesso_effettuato': False})
                elif email_exists(email):
                    return jsonify({'message': 'User Name non valido', 'accesso_effettuato': False})
                else:
                    return jsonify({'message': 'User Name e Email non validi', 'accesso_effettuato': False})
            
            else:
                return jsonify({'message': 'User Name, Email e Password non validi', 'accesso_effettuato': False})

    else:
        if user_name:
            if email:
                return jsonify({'message': 'Password mancante', 'accesso_effettuato': False})
            elif password:
                return jsonify({'message': 'Email mancante', 'accesso_effettuato': False})
            else:
                return jsonify({'message': 'Email e Password mancanti', 'accesso_effettuato': False})

        elif email:
            if user_name:
                return jsonify({'message': 'Password mancante', 'accesso_effettuato': False})
            elif password:
                return jsonify({'message': 'User Name mancante', 'accesso_effettuato': False})
            else:
                return jsonify({'message': 'User Name e Password mancanti', 'accesso_effettuato': False})

        elif password:
            if user_name:
                return jsonify({'message': 'Email mancante', 'accesso_effettuato': False})
            elif email:
                return jsonify({'message': 'User Name mancante', 'accesso_effettuato': False})
            else:
                return jsonify({'message': 'User Name e Email mancanti', 'accesso_effettuato': False})
        
        else:
            return jsonify({'message': 'User Name, Email e Password mancanti', 'accesso_effettuato': False})

# Endpoint per gestire le richieste di accesso
@app.route('/verifica_codice', methods=['POST'])
def verifica_codice():
    cod = request.form.get('codice')
    codice = hashlib.md5(cod.encode()).hexdigest()
    email = request.form.get('email')

    if cod:
        if len(cod)==6:
            if codice_verifica(email, codice):
                codice_ver = 'NULL'
                conn = sqlite3.connect('Gioco di Scopa/database.db')
                c = conn.cursor()
                c.execute("UPDATE User SET Code=? WHERE Email=?", (codice_ver, email))
                conn.commit()
                conn.close()
                return jsonify({'message': 'codice inserito valido', 'codice_corretto': True})
            else:
                return jsonify({'message': 'il codice inserito non è valido', 'codice_corretto': False})
        else:
            return jsonify({'message': 'codice incompleto', 'codice_corretto': False})

    else:
        return jsonify({'message': 'inserisci prima il codice', 'codice_corretto': False})

# Endpoint per gestire le richieste di accesso
@app.route('/vittorie', methods=['POST'])
def vittorie():
    user_name = request.form.get('user_name')
    
    conn = sqlite3.connect('Gioco di Scopa/database.db')
    c = conn.cursor()
    c.execute("SELECT Vittorie FROM User WHERE User_Name=?", (user_name,))
    result = c.fetchone()
    conn.close()
    
    return jsonify({'val': result})

# Endpoint per gestire le richieste di accesso
@app.route('/sconfitte', methods=['POST'])
def sconfitte():
    user_name = request.form.get('user_name')
    
    conn = sqlite3.connect('Gioco di Scopa/database.db')
    c = conn.cursor()
    c.execute("SELECT Sconfitte FROM User WHERE User_Name=?", (user_name,))
    result = c.fetchone()
    conn.close()
    
    return jsonify({'val': result})

# Endpoint per gestire le richieste di accesso
@app.route('/Vitt', methods=['POST'])
def Vitt():
    user_name = request.form.get('user_name')
    
    conn = sqlite3.connect('Gioco di Scopa/database.db')
    c = conn.cursor()
    c.execute("SELECT Punti_Vittoria FROM User WHERE User_Name=?", (user_name,))
    result = c.fetchone()
    conn.close()
    
    return jsonify({'val': result})

# Endpoint per gestire le richieste di accesso
@app.route('/UP', methods=['POST'])
def UP():
    user_name = request.form.get('user_name')
    value = request.form.get('value')
    
    conn = sqlite3.connect('Gioco di Scopa/database.db')
    c = conn.cursor()
    c.execute("UPDATE User SET Punti_Vittoria=? WHERE User_Name=?", (str(value), user_name))
    conn.commit()
    conn.close()
    return jsonify({'val': 'result'})

# Endpoint per gestire le richieste lo start di una partita
@app.route('/start_game', methods=['POST'])
def start_game():
    user_name = request.form.get('user_name')
    num_players = request.form.get('num_players')
    Punti = request.form.get('Punti')

    conn = sqlite3.connect('Gioco di Scopa/database.db')
    c = conn.cursor()

    # Cerca una partita in attesa con lo stesso numero di giocatori
    c.execute("SELECT * FROM Partita WHERE Giocatori=? AND Stato=? AND Punti=?", (num_players, "ricerca", Punti))
    existing_game = c.fetchone()

    if existing_game:
        # Aggiungi l'utente alla partita esistente
        game_id = existing_game[0]
        players_online = int(existing_game[5]) + 1
        print(existing_game[5])
        print(players_online)
        if int(players_online) > int(num_players):
            c.execute("DELETE FROM Partita WHERE ID_Partita=?", (game_id,))
        else:
            # Aggiorna il numero di giocatori online nella partita
            c.execute("UPDATE Partita SET Giocatori_Online=? WHERE ID_Partita=?", (str(players_online), game_id))

            # Distribuisci le carte al nuovo giocatore
            deck = json.loads(existing_game[1])
            random.shuffle(deck)
            player_hand = deck[:3]
            deck = deck[3:]
            print(players_online)
            c.execute("INSERT INTO Giocatore(ID_Partita, User_Name, Mano, Carte, Numero) VALUES (?, ?, ?, ?, ?)",
                    (game_id, user_name, json.dumps(player_hand),'', str(players_online)))
            
            # Aggiorna il numero di giocatori online nella partita
            c.execute("UPDATE Partita SET Mazzo=? WHERE ID_Partita=?", (json.dumps(deck), game_id))

            # Se il numero di giocatori online è uguale al numero di giocatori, inizia la partita
            if str(players_online) == str(num_players):
                # Aggiorna lo stato della partita a "in corso"
                c.execute("UPDATE Partita SET Stato=? WHERE ID_Partita=?", 
                        ("ricerca conclusa", game_id))
    else:
        # Crea una nuova partita
        players_online = 1
        deck = create_deck()
        random.shuffle(deck)
        print(deck)
        terra = deck[:4]
        deck = deck[4:]
        deck_user = deck[:3]
        deck = deck[3:]
        c.execute("INSERT INTO Partita(Mazzo, Terra, Giocatori, Punti, Giocatori_Online) VALUES (?, ?, ?, ?, ?)",
                  (json.dumps(deck), json.dumps(terra), str(num_players), str(Punti), str(players_online)))
        game_id = c.lastrowid
        c.execute("INSERT INTO Giocatore(ID_Partita, User_Name, Mano, Carte, Numero) VALUES (?, ?, ?, ?, ?)",
                  (game_id, user_name, json.dumps(deck_user),'', str(players_online)))

    conn.commit()
    conn.close()

    return jsonify({'player': players_online})

def create_deck():
    # Crea un mazzo di carte da scopa
    deck = []
    for seme in ["bastoni", "coppe", "spade", "denari"]:
        for valore in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]:
            deck.append((valore, seme))
    return deck

# Endpoint per gestire le richieste lo start di una partita
@app.route('/exit_game', methods=['POST'])
def exit_game():
    user_name = request.form.get('user_name')
    
    conn = sqlite3.connect('Gioco di Scopa/database.db')
    c = conn.cursor()

    # Ottieni l'ID della partita del giocatore
    c.execute("SELECT ID_Partita FROM Giocatore WHERE User_Name=?", (user_name,))
    result = c.fetchone()
    if result:
        game_id = result[0]
        print(game_id)
        # Ottieni il numero di giocatori online nella partita
        c.execute("SELECT Giocatori_Online FROM Partita WHERE ID_Partita=?", (game_id,))
        players_row = c.fetchone()
        print(players_row)
        if players_row is not None:
            players_online = players_row[0]
        else:
            # Gestisci il caso in cui non ci sono giocatori online
            players_online = 0  # o un altro valore predefinito

        print(players_online)

        # Se il numero di giocatori online è 1 o meno, elimina la partita
        if int(players_online) <= 1:
            c.execute("DELETE FROM Partita WHERE ID_Partita=?", (game_id,))
        else:
            # Altrimenti, decrementa il numero di giocatori online nella partita
            c.execute("UPDATE Partita SET Giocatori_Online=? WHERE ID_Partita=?", (str(players_online - 1), game_id))
            c.execute("UPDATE Partita SET Stato=? WHERE ID_Partita=?", ("ricerca", game_id))

            # Ottieni la mano del giocatore che si sta uscendo
            c.execute("SELECT Mano FROM Giocatore WHERE ID_Partita=? AND User_Name=?", (game_id, user_name))
            player_hand = json.loads(c.fetchone()[0])

            # Ottieni il mazzo attuale della partita
            c.execute("SELECT Mazzo FROM Partita WHERE ID_Partita=?", (game_id,))
            deck = json.loads(c.fetchone()[0])

            # Aggiungi la mano del giocatore all'inizio del mazzo
            deck = player_hand + deck

            # Aggiorna il mazzo nella partita
            c.execute("UPDATE Partita SET Mazzo=? WHERE ID_Partita=?", (json.dumps(deck), game_id))

        # Elimina il giocatore dalla partita
        c.execute("DELETE FROM Giocatore WHERE ID_Partita=? AND User_Name=?", (game_id, user_name))
    else:
        players_online = 1
    conn.commit()
    conn.close()

    return jsonify({'player': players_online})

# Endpoint per gestire le richieste lo start di una partita
@app.route('/stato', methods=['POST'])
def stato():
    user_name = request.form.get('user_name')
    
    conn = sqlite3.connect('Gioco di Scopa/database.db')
    c = conn.cursor()

    # Ottieni l'ID della partita del giocatore
    c.execute("SELECT ID_Partita FROM Giocatore WHERE User_Name=?", (user_name,))
    game_id = c.fetchone()[0]
    print(game_id)
    # Ottieni il numero di giocatori online nella partita
    c.execute("SELECT Giocatori_Online FROM Partita WHERE ID_Partita=?", (game_id,))
    players_row = c.fetchone()
    players_online = players_row[0]
    
    conn.commit()
    conn.close()

    return jsonify({'stato': players_online})

# Endpoint per gestire le richieste lo start di una partita
@app.route('/status', methods=['POST'])
def status():
    user_name = request.form.get('user_name')
    
    conn = sqlite3.connect('Gioco di Scopa/database.db')
    c = conn.cursor()

    # Ottieni l'ID della partita del giocatore
    c.execute("SELECT ID_Partita FROM Giocatore WHERE User_Name=?", (user_name,))
    result = c.fetchone()
    if result:
        game_id = result[0]
        # Ottieni il numero di giocatori online nella partita
        c.execute("SELECT Stato FROM Partita WHERE ID_Partita=?", (game_id,))
        status = c.fetchone()[0]
    else:
        status = ''
        
    conn.commit()
    conn.close()

    return jsonify({'status': status})

# Endpoint per gestire le richieste lo start di una partita
@app.route('/gioca', methods=['POST'])
def gioca():
    user_name = request.form.get('user_name')
    
    conn = sqlite3.connect('Gioco di Scopa/database.db')
    c = conn.cursor()

    # Ottieni l'ID della partita del giocatore
    c.execute("SELECT ID_Partita FROM Giocatore WHERE User_Name=?", (user_name,))
    game_id = c.fetchone()[0] 
    print(game_id)

    # Aggiorna lo stato della partita a "in corso"
    c.execute("UPDATE Partita SET Stato=? WHERE ID_Partita=?", 
            ("in corso", game_id))
    
    # Ottieni la mano del giocatore che si sta uscendo
    c.execute("SELECT Mano FROM Giocatore WHERE ID_Partita=? AND User_Name=?", (game_id, user_name))
    player_hand = json.loads(c.fetchone()[0])

    # Ottieni il mazzo attuale della partita
    c.execute("SELECT Terra FROM Partita WHERE ID_Partita=?", (game_id,))
    terra = json.loads(c.fetchone()[0])

    conn.commit()
    conn.close()

    return jsonify({'player_hand': player_hand, 'terra': terra})


# Endpoint per gestire le richieste lo start di una partita
@app.route('/nomecattivo', methods=['POST'])
def nomecattivo():
    user_name = request.form.get('user_name')
    
    conn = sqlite3.connect('Gioco di Scopa/database.db')
    c = conn.cursor()

    # Ottieni l'ID della partita del giocatore
    c.execute("SELECT ID_Partita FROM Giocatore WHERE User_Name=?", (user_name,))
    game_id = c.fetchone()[0]
    print(game_id)

    # Ottieni tutti gli username dei giocatori nella partita
    c.execute("SELECT User_Name FROM Giocatore WHERE ID_Partita=?", (game_id,))
    all_names = [row[0] for row in c.fetchall()]
    print(all_names)

    # Filtra i nomi diversi da user_name
    filtered_names = [name for name in all_names if name != user_name]
    print(filtered_names)

    conn.commit()
    conn.close()

    return jsonify({'nomecattivo': filtered_names})

# Endpoint per gestire le richieste lo start di una partita
@app.route('/push_new_data', methods=['POST'])
def push_new_data():
    data = request.get_json()  # Ottieni i dati come JSON
    terra = data.get('terra')
    carta_mano = data.get('carta_mano')
    carte_prese = data.get('carte_prese')
    numero = data.get('numero')
    user_name = data.get('user_name')
    
    conn = sqlite3.connect('Gioco di Scopa/database.db')
    c = conn.cursor()

    try:
        # Ottieni l'ID della partita del giocatore
        c.execute("SELECT ID_Partita FROM Giocatore WHERE User_Name=?", (user_name,))
        result = c.fetchone()
        if not result:
            return jsonify({'error': 'User not found'}), 404

        game_id = result[0]

        # Serializza le liste in stringhe JSON
        terra_json = json.dumps(terra)
        carta_mano_json = json.dumps(carta_mano)
        carte_prese_json = json.dumps(carte_prese)

        print(terra_json)
        print(carta_mano_json)
        print(carte_prese_json)

        # Aggiorna lo stato della partita a "in corso"
        c.execute("UPDATE Partita SET Terra=?, carta_mano=?, carte_prese=?, Ultima_Mossa=?, Ultima_Presa=? WHERE ID_Partita=?", 
                  (terra_json, carta_mano_json, carte_prese_json, numero, user_name, game_id))

        # Gestisci le carte del giocatore
        c.execute("SELECT Mano, Carte FROM Giocatore WHERE User_Name=?", (user_name,))
        giocatore = c.fetchone()
        if not giocatore:
            return jsonify({'error': 'Giocatore not found'}), 404

        mano = json.loads(giocatore[0]) if giocatore[0] else []
        carte = json.loads(giocatore[1]) if giocatore[1] else []

        print(mano)
        print(carte)

        # Rimuovi carta_mano da Mano
        if carta_mano in mano:
            mano.remove(carta_mano)

        print(mano)

        # Aggiungi carte_prese e carta_mano a Carte
        carte.extend(carte_prese)
        carte.append(carta_mano)

        print(carte)

        # Serializza di nuovo le liste
        mano_json = json.dumps(mano)
        carte_json = json.dumps(carte)

        print(mano)
        print(carte)

        # Gestisci le carte del giocatore
        c.execute("SELECT Punt FROM Giocatore WHERE User_Name=?", (user_name,))
        result = c.fetchone()
        if not result or result[0] is None:
            punti = 0  # Valore predefinito se non esiste alcun punteggio
            print('no')
        else:
            punti = int(result[0])
            print('si')

        terra = json.loads(terra_json)

        print(len(terra))
        if len(terra) == 0:
            print(punti)
            punti += 1

        print(punti)
        # Aggiorna le informazioni del giocatore
        c.execute("UPDATE Giocatore SET Mano=?, Carte=?, Punt=? WHERE User_Name=?", (mano_json, carte_json, punti, user_name))

        conn.commit()
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

    return jsonify({'ok': 'ok'})

# Endpoint per gestire le richieste lo start di una partita
@app.route('/push_data', methods=['POST'])
def push_data():
    data = request.get_json()  # Ottieni i dati come JSON
    terra = data.get('terra')
    carta_mano = data.get('carta_mano')
    numero = data.get('numero')
    user_name = data.get('user_name')
    carte_prese = []
    
    conn = sqlite3.connect('Gioco di Scopa/database.db')
    c = conn.cursor()

    try:
        # Ottieni l'ID della partita del giocatore
        c.execute("SELECT ID_Partita FROM Giocatore WHERE User_Name=?", (user_name,))
        result = c.fetchone()
        if not result:
            return jsonify({'error': 'User not found'}), 404

        game_id = result[0]

        # Serializza le liste in stringhe JSON
        terra_json = json.dumps(terra)
        carta_mano_json = json.dumps(carta_mano)
        carte_prese_json = json.dumps(carte_prese)

        print(terra_json)
        print(carta_mano_json)
        print(carte_prese_json)

        # Aggiorna lo stato della partita a "in corso"
        c.execute("UPDATE Partita SET Terra=?, carta_mano=?, carte_prese=?, Ultima_Mossa=? WHERE ID_Partita=?", 
                  (terra_json, carta_mano_json, carte_prese_json, numero, game_id))

        # Gestisci le carte del giocatore
        c.execute("SELECT Mano FROM Giocatore WHERE User_Name=?", (user_name,))
        giocatore = c.fetchone()
        if not giocatore:
            return jsonify({'error': 'Giocatore not found'}), 404

        mano = json.loads(giocatore[0]) if giocatore[0] else []

        print(mano)

        # Rimuovi carta_mano da Mano
        if carta_mano in mano:
            mano.remove(carta_mano)

        print(mano)

        # Serializza di nuovo le liste
        mano_json = json.dumps(mano)

        print(mano)

        # Aggiorna le informazioni del giocatore
        c.execute("UPDATE Giocatore SET Mano=? WHERE User_Name=?", (mano_json, user_name))

        conn.commit()
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

    return jsonify({'ok': 'ok'})

# Endpoint per gestire le richieste lo start di una partita
@app.route('/con_questo_ho_finito', methods=['POST'])
def con_questo_ho_finito():
    user_name = request.form.get('user_name')
    
    conn = sqlite3.connect('Gioco di Scopa/database.db')
    c = conn.cursor()

    # Ottieni l'ID della partita del giocatore
    c.execute("SELECT ID_Partita FROM Giocatore WHERE User_Name=?", (user_name,))
    game_id = c.fetchone()[0] 
    print(game_id)
    
    # Ottieni tutte le mani dei giocatori per una specifica partita
    c.execute("SELECT Mano FROM Giocatore WHERE ID_Partita=?", (game_id,))
    mani_giocatori = c.fetchall()

    # Combina tutte le mani in una sola lista
    Mano = []
    for mano in mani_giocatori:
        mano_lista = json.loads(mano[0]) if mano[0] else []
        if len(mano_lista) > 0:
            Mano.extend(mano_lista)
    print(Mano)

    # Verifica se Mano è vuoto
    if len(Mano) == 0:
        finito = True
    else:
        finito = False

    # Ottieni la mano del giocatore che si sta uscendo
    c.execute("SELECT Mazzo FROM Partita WHERE ID_Partita=?", (game_id,))
    Mazzo = json.loads(c.fetchone()[0])
    print(Mazzo)

    # Verifica se Mazzo è vuoto
    if len(Mazzo) == 0:
        finito_tutto = True
    else:
        finito_tutto = False

    conn.commit()
    conn.close()

    return jsonify({'finito': finito, 'finito_tutto': finito_tutto})

# Endpoint per gestire le richieste lo start di una partita
@app.route('/fatto', methods=['POST'])
def fatto():
    user_name = request.form.get('user_name')
    
    conn = sqlite3.connect('Gioco di Scopa/database.db')
    c = conn.cursor()

    # Ottieni l'ID della partita del giocatore
    c.execute("SELECT ID_Partita FROM Giocatore WHERE User_Name=?", (user_name,))
    game_id = c.fetchone()[0] 
    print(game_id)

    # Ottieni il mazzo attuale della partita
    c.execute("SELECT Terra FROM Partita WHERE ID_Partita=?", (game_id,))
    terra = json.loads(c.fetchone()[0])
    print(terra)

    conn.commit()
    conn.close()

    return jsonify({'terra': terra})

# Endpoint per gestire le richieste lo start di una partita
@app.route('/dammi_tutto', methods=['POST'])
def dammi_tutto():
    user_name = request.form.get('user_name')
    
    conn = sqlite3.connect('Gioco di Scopa/database.db')
    c = conn.cursor()

    # Ottieni l'ID della partita del giocatore
    c.execute("SELECT ID_Partita FROM Giocatore WHERE User_Name=?", (user_name,))
    game_id = c.fetchone()[0] 
    print(game_id)
    
    # Ottieni il mazzo attuale della partita
    c.execute("SELECT Terra FROM Partita WHERE ID_Partita=?", (game_id,))
    terra = json.loads(c.fetchone()[0])

    # Ottieni il mazzo attuale della partita
    c.execute("SELECT carta_mano FROM Partita WHERE ID_Partita=?", (game_id,))
    carta_mano = json.loads(c.fetchone()[0])

    # Ottieni il mazzo attuale della partita
    c.execute("SELECT carte_prese FROM Partita WHERE ID_Partita=?", (game_id,))
    carte_prese = json.loads(c.fetchone()[0])

    # Ottieni il mazzo attuale della partita
    c.execute("SELECT Ultima_Mossa FROM Partita WHERE ID_Partita=?", (game_id,))
    numero = json.loads(c.fetchone()[0])

    conn.commit()
    conn.close()

    return jsonify({'terra': terra, 'carta_mano': carta_mano, 'carte_prese': carte_prese, 'numero': numero})

# Endpoint per gestire le richieste lo start di una partita
@app.route('/distrubuisci_carte_nuove', methods=['POST'])
def distrubuisci_carte_nuove():
    user_name = request.form.get('user_name')

    conn = sqlite3.connect('Gioco di Scopa/database.db')
    c = conn.cursor()

    # Ottieni l'ID della partita del giocatore
    c.execute("SELECT ID_Partita FROM Giocatore WHERE User_Name=?", (user_name,))
    game_id = c.fetchone()[0]
    print(game_id)

    # Ottieni il mazzo di carte dalla partita
    c.execute("SELECT Mazzo FROM Partita WHERE ID_Partita=?", (game_id,))
    deck = json.loads(c.fetchone()[0])

    # Distribuisci le carte al giocatore
    random.shuffle(deck)
    player_hand = deck[:3]
    deck = deck[3:]
    c.execute("UPDATE Giocatore SET Mano=? WHERE User_Name=?", (json.dumps(player_hand), user_name))

    print(json.dumps(player_hand))
    
    # Aggiorna il numero di giocatori online nella partita
    c.execute("UPDATE Partita SET Mazzo=? WHERE ID_Partita=?", (json.dumps(deck), game_id))

    print(json.dumps(deck))

    conn.commit()
    conn.close()

    return jsonify({'ok': 'ok'})

# Endpoint per gestire le richieste lo start di una partita
@app.route('/distrubuisci_carte', methods=['POST'])
def distrubuisci_carte():
    user_name = request.form.get('user_name')
    
    conn = sqlite3.connect('Gioco di Scopa/database.db')
    c = conn.cursor()
    
    # Ottieni il mazzo attuale della partita
    c.execute("SELECT Mano FROM Giocatore WHERE User_Name=?", (user_name,))
    carte_mano = json.loads(c.fetchone()[0])

    print(json.dumps(carte_mano))

    conn.commit()
    conn.close()

    return jsonify({'carte_mano': json.dumps(carte_mano)})

# Endpoint per gestire le richieste lo start di una partita
@app.route('/quasi_finito', methods=['POST'])
def quasi_finito():
    user_name = request.form.get('user_name')
    
    conn = sqlite3.connect('Gioco di Scopa/database.db')
    c = conn.cursor()

    # Ottieni l'ID della partita del giocatore
    c.execute("SELECT ID_Partita FROM Giocatore WHERE User_Name=?", (user_name,))
    game_id = c.fetchone()[0] 
    print(game_id)
    
    # Ottieni tutte le mani dei giocatori per una specifica partita
    c.execute("SELECT Mano FROM Giocatore WHERE ID_Partita=?", (game_id,))
    mani_giocatori = c.fetchall()

    # Combina tutte le mani in una sola lista
    Mano = []
    for mano in mani_giocatori:
        mano_lista = json.loads(mano[0]) if mano[0] else []
        if len(mano_lista) > 0:
            Mano.extend(mano_lista)
    print(Mano)

    # Verifica se Mano è vuoto
    if len(Mano) == 1:
        finito = True
    else:
        finito = False

    # Ottieni la mano del giocatore che si sta uscendo
    c.execute("SELECT Mazzo FROM Partita WHERE ID_Partita=?", (game_id,))
    Mazzo = json.loads(c.fetchone()[0])
    print(Mazzo)

    # Verifica se Mazzo è vuoto
    if len(Mazzo) == 0:
        finito_tutto = True
    else:
        finito_tutto = False

    if finito and finito_tutto :
        quasi_finito = True
    else:
        quasi_finito = False

    conn.commit()
    conn.close()

    return jsonify({'quasi_finito': quasi_finito})

# Endpoint per gestire le richieste lo start di una partita
@app.route('/nome_ultima_presa', methods=['POST'])
def nome_ultima_presa():
    user_name = request.form.get('user_name')
    
    conn = sqlite3.connect('Gioco di Scopa/database.db')
    c = conn.cursor()

    # Ottieni l'ID della partita del giocatore
    c.execute("SELECT ID_Partita FROM Giocatore WHERE User_Name=?", (user_name,))
    game_id = c.fetchone()[0] 
    print(game_id)
    
    # Ottieni il mazzo attuale della partita
    c.execute("SELECT Ultima_Presa FROM Partita WHERE ID_Partita=?", (game_id,))
    Ultima_Presa = c.fetchone()[0]

    conn.commit()
    conn.close()

    return jsonify({'nome_ultima_presa': Ultima_Presa})

@app.route('/update_punti', methods=['POST'])
def update_punti():
    user_name = request.form.get('user_name')
    user_name2 = request.form.get('user_name2')
    
    conn = sqlite3.connect('Gioco di Scopa/database.db')
    c = conn.cursor()
    
    # Ottieni il punteggio attuale del giocatore
    c.execute("SELECT Punt FROM Giocatore WHERE User_Name=?", (user_name,))
    punti = c.fetchone()[0]
    punti = int(punti)
    print(punti)

    # Ottieni le carte prese del giocatore
    c.execute("SELECT Carte FROM Giocatore WHERE User_Name=?", (user_name,))
    result = c.fetchone()
    if result is None:
        return jsonify({'error': 'User not found'}), 404
    carte_prese = json.loads(result[0])
    print(carte_prese)

    # Calcolo punti supplementari
    if len(carte_prese) > 20:
        punti += 1

    denari = [carta for carta in carte_prese if carta[1] == 'denari']
    if len(denari) > 5:
        punti += 1

    set_denari = set([carta[0] for carta in denari])
    if len(set_denari) == 10:
        punti += 1

    # Ottieni il punteggio attuale del secondo giocatore
    c.execute("SELECT Punt FROM Giocatore WHERE User_Name=?", (user_name2,))
    punti2 = c.fetchone()[0]
    print(punti2)

    # Ottieni le carte prese del secondo giocatore
    c.execute("SELECT Carte FROM Giocatore WHERE User_Name=?", (user_name2,))
    result = c.fetchone()
    if result is None:
        return jsonify({'error': 'User not found'}), 404
    carte_prese2 = json.loads(result[0])
    print(carte_prese2)

    # Calcolo punti supplementari per il secondo giocatore
    if len(carte_prese2) > 20:
        punti2 += 1

    denari = [carta for carta in carte_prese2 if carta[1] == 'denari']
    if len(denari) > 5:
        punti2 += 1

    set_denari = set([carta[0] for carta in denari])
    if len(set_denari) == 10:
        punti2 += 1

    # Calcolo del punteggio "70"
    def calcola_punteggio_70(carte):
        punteggi_massimi = {'coppe': 0, 'bastoni': 0, 'spade': 0, 'denari': 0}
        valori = {'7': 21, '6': 18, '1': 16}
        
        for carta in carte:
            valore, seme = carta
            if valore.isdigit() and int(valore) <= 7:
                punteggio = valori.get(valore, 10 + int(valore))
            else:
                punteggio = 10
            if punteggio > punteggi_massimi[seme]:
                punteggi_massimi[seme] = punteggio

        return sum(punteggi_massimi.values())

    punteggio_70 = calcola_punteggio_70(carte_prese)
    punteggio_70_2 = calcola_punteggio_70(carte_prese2)

    if punteggio_70 > punteggio_70_2:
        punti += 1
    elif punteggio_70 < punteggio_70_2:
        punti2 += 1

    # Aggiorna il punteggio nel database per entrambi i giocatori
    c.execute("UPDATE Giocatore SET Punt=? WHERE User_Name=?", (punti, user_name))
    print(punti)
    c.execute("UPDATE Giocatore SET Punt=? WHERE User_Name=?", (punti2, user_name2))
    print(punti2)
    
    conn.commit()
    conn.close()

    return jsonify({'ok': 'ok'})

@app.route('/punti', methods=['POST'])
def punti():
    user_name = request.form.get('user_name')
    
    conn = sqlite3.connect('Gioco di Scopa/database.db')
    c = conn.cursor()

    # Ottieni il punteggio attuale del giocatore
    c.execute("SELECT Punt FROM Giocatore WHERE User_Name=?", (user_name,))
    punti = c.fetchone()[0]
    
    conn.commit()
    conn.close()

    return jsonify({'punti': punti})

# Endpoint per gestire le richieste lo start di una partita
@app.route('/nuova_partita', methods=['POST'])
def nuova_partita():
    user_name = request.form.get('user_name')
    
    conn = sqlite3.connect('Gioco di Scopa/database.db')
    c = conn.cursor()

    # Ottieni l'ID della partita del giocatore
    c.execute("SELECT ID_Partita FROM Giocatore WHERE User_Name=?", (user_name,))
    game_id = c.fetchone()[0] 
    print(game_id)

    deck = create_deck()
    random.shuffle(deck)
    print(deck)
    terra = deck[:4]
    print(terra)
    deck = deck[4:]
    print(deck)
    # Aggiorna il numero di giocatori online nella partita
    c.execute("UPDATE Partita SET Mazzo=?, Terra=? WHERE ID_Partita=?", (json.dumps(deck), json.dumps(terra), game_id))

    conn.commit()
    conn.close()

    return jsonify({'ok':'ok'})

# Endpoint per gestire le richieste lo start di una partita
@app.route('/nuova_partita_nuovi_dati', methods=['POST'])
def nuova_partita_nuovi_dati():
    user_name = request.form.get('user_name')
    
    conn = sqlite3.connect('Gioco di Scopa/database.db')
    c = conn.cursor()

    # Ottieni l'ID della partita del giocatore
    c.execute("SELECT ID_Partita FROM Giocatore WHERE User_Name=?", (user_name,))
    game_id = c.fetchone()[0] 
    print(game_id)

    # Ottieni il mazzo di carte dalla partita
    c.execute("SELECT Mazzo FROM Partita WHERE ID_Partita=?", (game_id,))
    deck = json.loads(c.fetchone()[0])

    Carte=[]

    # Distribuisci le carte al giocatore
    random.shuffle(deck)
    player_hand = deck[:3]
    deck = deck[3:]
    c.execute("UPDATE Giocatore SET Mano=?, Carte=? WHERE User_Name=?", (json.dumps(player_hand), json.dumps(Carte), user_name))

    print(json.dumps(player_hand))
    
    # Aggiorna il numero di giocatori online nella partita
    c.execute("UPDATE Partita SET Mazzo=? WHERE ID_Partita=?", (json.dumps(deck), game_id))

    print(json.dumps(deck))
    # Ottieni il mazzo attuale della partita
    c.execute("SELECT Terra FROM Partita WHERE ID_Partita=?", (game_id,))
    terra = json.loads(c.fetchone()[0])

    conn.commit()
    conn.close()

    return jsonify({'player_hand': player_hand, 'terra': terra})




def delete_all_games_and_players():
    try:
        conn = sqlite3.connect('Gioco di Scopa/database.db')
        c = conn.cursor()

        # Cancella tutte le partite
        c.execute("DELETE FROM Partita")

        # Cancella tutti i giocatori
        c.execute("DELETE FROM Giocatore")

        # Visualizza entrambe le tabelle dopo la cancellazione
        print("Dopo la cancellazione:")
        print("Tabella Partita:")
        c.execute("SELECT * FROM Partita")
        print(c.fetchall())
        print("Tabella Giocatore:")
        c.execute("SELECT * FROM Giocatore")
        print(c.fetchall())

        conn.commit()
        conn.close()
        
        print("Tutte le partite e tutti i giocatori sono stati cancellati con successo.")
    
    except sqlite3.Error as e:
        print("Si è verificato un errore durante la cancellazione delle partite e dei giocatori:", e)

# delete_all_games_and_players()
if __name__ == '__main__':
    initialize_database()  # Inizializza il database
    delete_all_games_and_players()
    app.run(host='0.0.0.0', port=8080, threaded=True)