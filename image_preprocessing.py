
from PIL import Image
import cv2
import numpy as np

def preprocess_image(image_path):
    """
    Charge une image, corrige la perspective, normalise les couleurs et supprime le bruit.
    """
    # Charger l'image
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"L'image à l'adresse {image_path} n'a pas pu être chargée.")

    # Convertir en niveaux de gris pour certaines opérations
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # --- Correction de la perspective (simplifiée pour l'exemple) ---
    # Pour une correction réelle, il faudrait détecter les coins du document.
    # Ici, nous allons juste redimensionner pour un exemple.
    # Si le document est déjà bien scanné, cette étape peut être moins critique.
    # Pour une implémentation complète, on utiliserait des techniques comme la détection de contours
    # et la transformation de perspective (cv2.getPerspectiveTransform, cv2.warpPerspective).
    # Pour l'instant, nous allons supposer que l'image est relativement plate.

    # --- Normalisation des couleurs et de l'éclairage ---
    # Égalisation de l'histogramme pour améliorer le contraste
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced_gray = clahe.apply(gray)

    # Normalisation de la luminosité (simple ajustement gamma)
    gamma = 1.2 # Ajuster selon le besoin
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    normalized_img = cv2.LUT(img, table)

    # --- Suppression du bruit ---
    # Filtre médian pour réduire le bruit de sel et poivre
    denoised_img = cv2.medianBlur(normalized_img, 5) # Le noyau doit être impair

    return denoised_img

# Exemple d'utilisation (pour les tests)
if __name__ == "__main__":
    # Créez une image factice pour le test
    dummy_image_path = "dummy_document.png"
    dummy_image = Image.new('RGB', (800, 600), color = 'white')
    from PIL import ImageDraw, ImageFont
    draw = ImageDraw.Draw(dummy_image)
    try:
        font = ImageFont.truetype("arial.ttf", 40) # Assurez-vous que arial.ttf est disponible
    except IOError:
        font = ImageFont.load_default()
        print("Police arial.ttf non trouvée, utilisation de la police par défaut.")

    draw.text((50, 100), "Ceci est un texte de test.", fill=(0, 0, 0), font=font)
    draw.text((70, 200), "Texte effacé simulé.", fill=(150, 150, 150), font=font) # Texte plus clair pour simuler effacement
    dummy_image.save(dummy_image_path)

    print(f"Image factice créée : {dummy_image_path}")

    try:
        processed_image = preprocess_image(dummy_image_path)
        output_path = "processed_dummy_document.png"
        cv2.imwrite(output_path, processed_image)
        print(f"Image prétraitée enregistrée : {output_path}")
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"Une erreur est survenue lors du prétraitement : {e}")




