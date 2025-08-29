
import cv2
import numpy as np
from skimage.restoration import unwrap_phase, wiener, richardson_lucy
from PIL import Image

def deblur_image_wiener(image_path, psf, balance=0.5):
    """
    Applique la déconvolution de Wiener pour déflouter une image.
    :param image_path: Chemin vers l'image à déflouter.
    :param psf: Fonction d'étalement de point (Point Spread Function).
    :param balance: Paramètre d'équilibre pour le filtre de Wiener (entre 0 et 1).
    :return: Image défloutée.
    """
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Image non trouvée à {image_path}")

    # Convertir l'image en float pour le traitement
    img_float = img.astype(np.float32) / 255.0

    # Appliquer le filtre de Wiener
    deblurred_img = wiener(img_float, psf, balance=balance)

    # Reconvertir en uint8
    deblurred_img = np.clip(deblurred_img * 255, 0, 255).astype(np.uint8)
    return Image.fromarray(deblurred_img)

def deblur_image_richardson_lucy(image_path, psf, num_iter=30):
    """
    Applique la déconvolution de Richardson-Lucy pour déflouter une image.
    :param image_path: Chemin vers l'image à déflouter.
    :param psf: Fonction d'étalement de point (Point Spread Function).
    :param num_iter: Nombre d'itérations.
    :return: Image défloutée.
    """
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Image non trouvée à {image_path}")

    # Convertir l'image en float pour le traitement
    img_float = img.astype(np.float32) / 255.0

    # Appliquer l'algorithme de Richardson-Lucy
    deblurred_img = richardson_lucy(img_float, psf, num_iter=num_iter)

    # Reconvertir en uint8
    deblurred_img = np.clip(deblurred_img * 255, 0, 255).astype(np.uint8)
    return Image.fromarray(deblurred_img)

def simulate_erased_text_restoration(image_path):
    """
    Simule la restauration de texte effacé en augmentant le contraste et en appliquant un seuillage adaptatif.
    Ceci est une approche simplifiée et peut nécessiter des techniques plus avancées (analyse spectrale réelle, etc.)
    pour des cas réels complexes.
    :param image_path: Chemin vers l'image contenant le texte effacé.
    :return: Image avec texte restauré simulé.
    """
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Image non trouvée à {image_path}")

    # Augmenter le contraste (CLAHE - Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced_img = clahe.apply(img)

    # Appliquer un seuillage adaptatif pour isoler le texte
    restored_img = cv2.adaptiveThreshold(enhanced_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
                                         cv2.THRESH_BINARY, 11, 2)

    return Image.fromarray(restored_img)

# Exemple d'utilisation (pour les tests)
if __name__ == "__main__":
    # Créer une image factice pour les tests
    from PIL import Image, ImageDraw, ImageFont
    import os

    # Créer une image avec du texte flou
    img_blur = Image.new('L', (400, 100), color = 'white')
    d_blur = ImageDraw.Draw(img_blur)
    try:
        fnt_blur = ImageFont.truetype("arial.ttf", 30)
    except IOError:
        fnt_blur = ImageFont.load_default()
    d_blur.text((10,10), "Texte Flou", font=fnt_blur, fill=0)
    img_blur.save("test_blurry.png")

    # Créer une image avec du texte effacé (simulé par un texte très clair)
    img_erased = Image.new('L', (400, 100), color = 'white')
    d_erased = ImageDraw.Draw(img_erased)
    try:
        fnt_erased = ImageFont.truetype("arial.ttf", 30)
    except IOError:
        fnt_erased = ImageFont.load_default()
    d_erased.text((10,10), "Texte Efface", font=fnt_erased, fill=150) # Gris clair pour simuler effacé
    img_erased.save("test_erased.png")

    # Simuler une PSF (Point Spread Function) pour le flou de mouvement
    psf = np.ones((5, 5)) / 25.0

    # Tester la déconvolution de Wiener
    deblurred_wiener = deblur_image_wiener("test_blurry.png", psf)
    deblurred_wiener.save("test_blurry_deblurred_wiener.png")
    print("Image floue défloutée (Wiener) enregistrée sous test_blurry_deblurred_wiener.png")

    # Tester la déconvolution de Richardson-Lucy
    deblurred_rl = deblur_image_richardson_lucy("test_blurry.png", psf)
    deblurred_rl.save("test_blurry_deblurred_rl.png")
    print("Image floue défloutée (Richardson-Lucy) enregistrée sous test_blurry_deblurred_rl.png")

    # Tester la restauration de texte effacé simulé
    restored_erased = simulate_erased_text_restoration("test_erased.png")
    restored_erased.save("test_erased_restored.png")
    print("Image avec texte effacé restauré enregistrée sous test_erased_restored.png")

    # Nettoyage des fichiers de test
    os.remove("test_blurry.png")
    os.remove("test_erased.png")
    os.remove("test_blurry_deblurred_wiener.png")
    os.remove("test_blurry_deblurred_rl.png")
    os.remove("test_erased_restored.png")


