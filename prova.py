import sys
import json
from itertools import combinations
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QMessageBox, QGraphicsOpacityEffect, QVBoxLayout
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont
from PyQt5.QtCore import Qt, QPropertyAnimation, QRectF, QParallelAnimationGroup, QEasingCurve, QSequentialAnimationGroup, QRect, QTimer

titolo = """
    background-color: none;
    font: 40px Arial Black;
    color: #85E7BB;
    padding: 5px;
"""
testo="""
    background-color: none;
    font: 20px Arial;
    color: #85E7BB;
    padding: 5px;
"""

class CardAnimation(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Animazione di Carte")
        self.setStyleSheet("QWidget { background-color: #52B488; }")
        self.setGeometry(100, 100, 600, 1000)

        # Leggi i dati dal file JSON
        with open("Gioco di Scopa/partita.json", "r") as file:
            self.data = json.load(file)

        # Crea i label per le carte a terra, in mano e il retro delle carte
        self.create_labels()

        # Posiziona i label sul widget
        self.position_labels()

        # Avvia l'animazione
        self.start_animation()

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
        self.label_nome_cattivo.setStyleSheet(testo)
        self.label_punti_cattivo = QLabel(str(self.data["punti"]), self)
        self.label_punti_cattivo.setStyleSheet(testo)

        # Crea i label per il nome cattivo e i punti
        self.label_nome = QLabel("Punti:", self)
        self.label_nome.setStyleSheet(titolo)
        self.label_punti = QLabel(str(self.data["punti"]), self)
        self.label_punti.setStyleSheet(titolo)

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

        # Aggiungi la sovrapposizione di stile per il label semitrasparente
        self.cover_label = QLabel(self)  # Rinomina la cover_label per evitare conflitti
        self.cover_label.resize(self.width(), self.height())
        self.cover_label.setStyleSheet("background-color: rgba(0, 0, 0, 1%);")
        self.cover_label.show()

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CardAnimation()
    window.show()
    sys.exit(app.exec_())
