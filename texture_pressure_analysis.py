
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def analyze_texture_pressure(image_path):
    """
    Analyse la texture et la pression simulée sur le papier pour identifier les traces d'écriture.
    Cette fonction est une simplification et une simulation. Une analyse réelle
    nécessiterait des capteurs de pression ou des techniques d'imagerie 3D.
    """
    try:
        img = cv2.imread(image_path)
        if img is None:
            raise FileNotFoundError(f"L'image à l'adresse {image_path} n'a pas pu être chargée.")

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # --- Simulation de l'analyse de la topographie du papier (micro-sillons) ---
        # Utilisation d'un filtre de Sobel pour détecter les bords et les variations de gradient,
        # qui peuvent simuler les micro-sillons laissés par la pression.
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=5)
        gradient_magnitude = np.sqrt(sobelx**2 + sobely**2)
        gradient_magnitude = cv2.normalize(gradient_magnitude, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

        # --- Simulation de l'analyse de la granularité de l'encre ---
        # On peut simuler la granularité en analysant la variance locale de l'image.
        # Les zones avec une forte variance pourraient indiquer une encre plus dense ou des surcharges.
        # Utilisation d'un filtre de variance (non standard, on peut simuler avec un filtre de moyenne et soustraction)
        # Pour une vraie variance locale, on utiliserait une fenêtre glissante.
        # Ici, une approche simplifiée : soustraire une version floue de l'image.
        blurred_gray = cv2.GaussianBlur(gray, (21, 21), 0)
        granularity_map = cv2.absdiff(gray, blurred_gray)
        granularity_map = cv2.normalize(granularity_map, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

        # --- Combinaison des résultats pour une vue combinée ---
        # Pour l'instant, on va juste retourner les cartes de gradient et de granularité.
        # Dans une application réelle, on pourrait les fusionner ou les utiliser
        # comme caractéristiques pour un modèle d'apprentissage automatique.

        return {
            'original': img,
            'gradient_magnitude': gradient_magnitude,
            'granularity_map': granularity_map
        }

    except FileNotFoundError as e:
        print(e)
        return None
    except Exception as e:
        print(f"Une erreur est survenue lors de l\'analyse de texture/pression : {e}")
        return None

# Exemple d\'utilisation (pour les tests)
if __name__ == "__main__":
    # Créez une image factice pour le test
    dummy_image_path = "dummy_texture_pressure.png"
    dummy_image = Image.new("RGB", (800, 600), color="white")
    draw = ImageDraw.Draw(dummy_image)
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        font = ImageFont.load_default()
        print("Police arial.ttf non trouvée, utilisation de la police par défaut.")


    # Texte avec pression simulée (plus épais, plus sombre)
    draw.text((50, 100), "Texte avec forte pression", fill=(0, 0, 0), font=font)
    # Texte avec pression légère (plus fin, plus clair)
    draw.text((50, 200), "Texte avec faible pression", fill=(100, 100, 100), font=font)
    # Zone avec une texture de papier différente (simulée par un motif)
    for i in range(0, 800, 10):
        draw.line([(i, 300), (i+5, 310)], fill=(200, 200, 200), width=1)
    draw.text((50, 350), "Zone de texture différente", fill=(0, 0, 0), font=font)

    dummy_image.save(dummy_image_path)

    print(f"Image factice créée pour l\"analyse de texture/pression : {dummy_image_path}")

    results = analyze_texture_pressure(dummy_image_path)

    if results:
        for name, image in results.items():
            output_path = f"texture_pressure_{name}.png"
            cv2.imwrite(output_path, image)
            print(f"Image d\"analyse de texture/pression enregistrée : {output_path}")


