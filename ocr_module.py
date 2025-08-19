
from PIL import Image
import pytesseract
import cv2
import numpy as np

# Assurez-vous que tesseract est dans votre PATH ou spécifiez le chemin ici
# pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

def advanced_ocr(image_path):
    """
    Effectue une OCR avancée sur une image, en tentant de simuler la détection
    de couches d'encre/crayon et de texte effacé.
    """
    try:
        img = cv2.imread(image_path)
        if img is None:
            raise FileNotFoundError(f"L'image à l'adresse {image_path} n'a pas pu être chargée.")

        # Convertir l'image en niveaux de gris
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # --- Simulation de la détection de couches d'encre/crayon ---
        # Cette partie est une SIMULATION. La détection réelle de couches
        # nécessiterait des techniques d'imagerie multispectrale ou hyperspectrale
        # et des algorithmes d'apprentissage automatique entraînés sur des données
        # spécifiques de types d'encre et de papier.
        # Pour cette simulation, nous allons tenter d'extraire le texte à différents
        # seuils pour simuler la détection de différentes couches.
        _, thresh_main = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        text_main = pytesseract.image_to_string(Image.fromarray(thresh_main), lang='fra')

        # Seuil plus doux pour tenter de capturer le texte effacé ou plus clair (crayon)
        # Cette valeur de seuil est heuristique et devrait être ajustée ou apprise
        # dans une implémentation réelle.
        _, thresh_light = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY) # Exemple: seuil à 150
        text_light = pytesseract.image_to_string(Image.fromarray(thresh_light), lang='fra')

        # Comparaison et fusion des résultats (logique simplifiée)
        # Dans une application réelle, une logique plus sophistiquée serait nécessaire
        # pour fusionner les résultats, par exemple en comparant les positions des mots.
        final_text = ""
        if text_main:
            final_text += "Texte principal (encre foncée) :\n" + text_main + "\n"
        if text_light and text_light != text_main: # Éviter la duplication si le texte est le même
            final_text += "Texte secondaire (effacé/crayon) :\n" + text_light + "\n"

        # --- Simulation de l'image annotée ---
        # Pour une image annotée réelle, on utiliserait les boîtes de délimitation
        # de Tesseract et on dessinerait dessus.
        # Ici, nous allons juste retourner l'image originale pour l'instant.
        annotated_image = img.copy()

        return final_text, annotated_image

    except FileNotFoundError as e:
        return str(e), None
    except Exception as e:
        return f"Une erreur est survenue lors de l'OCR : {e}", None

# Exemple d\'utilisation (pour les tests)
if __name__ == "__main__":
    # Créez une image factice pour le test
    dummy_image_path = "dummy_document_for_ocr.png"
    dummy_image = Image.new('RGB', (800, 600), color = 'white')
    from PIL import ImageDraw, ImageFont
    draw = ImageDraw.Draw(dummy_image)
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        font = ImageFont.load_default()
        print("Police arial.ttf non trouvée, utilisation de la police par défaut.")

    draw.text((50, 100), "Bonjour le monde!", fill=(0, 0, 0), font=font)
    draw.text((70, 200), "Texte effacé ou clair.", fill=(150, 150, 150), font=font) # Texte plus clair
    dummy_image.save(dummy_image_path)

    print(f"Image factice créée pour OCR : {dummy_image_path}")

    text_result, img_result = advanced_ocr(dummy_image_path)
    print("\nRésultat OCR :\n", text_result)

    if img_result is not None:
        output_annotated_path = "annotated_dummy_document.png"
        cv2.imwrite(output_annotated_path, img_result)
        print(f"Image annotée enregistrée : {output_annotated_path}")



