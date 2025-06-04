from PIL import Image

# Apre l'immagine
image_path = 'Gioco di Scopa/Icone/info_press.png'
image = Image.open(image_path)

# Ridimensiona l'immagine a 100x100 pixel
resized_image = image.resize((40, 40))

# Salva l'immagine ridimensionata
resized_image.save('Gioco di Scopa/Icone/info_press_resized.png')
