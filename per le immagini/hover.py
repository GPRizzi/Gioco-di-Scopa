from PIL import Image

# Apre l'immagine
image_path = 'Gioco di Scopa/Icone/info_hover.png'
image = Image.open(image_path)

# Ridimensiona l'immagine a 100x100 pixel
resized_image = image.resize((48, 48))

# Salva l'immagine ridimensionata
resized_image.save('Gioco di Scopa/Icone/info_hover_resized.png')
