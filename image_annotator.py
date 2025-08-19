import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
import tempfile

class ImageAnnotator:
    """
    Classe pour créer des images annotées avec les résultats d'analyse
    """
    
    def __init__(self):
        self.font_size = 24
        self.annotation_color = (255, 0, 0)  # Rouge pour les annotations
        self.text_color = (0, 255, 0)  # Vert pour le texte détecté
        self.hidden_color = (255, 255, 0)  # Jaune pour le texte caché
        
    def create_annotated_image(self, original_image_path, analysis_results):
        """
        Crée une image annotée avec les résultats d'analyse
        """
        try:
            # Charger l'image originale
            original_img = cv2.imread(original_image_path)
            if original_img is None:
                raise ValueError("Impossible de charger l'image originale")
            
            # Convertir en RGB pour PIL
            original_rgb = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(original_rgb)
            
            # Créer une copie pour les annotations
            annotated_image = pil_image.copy()
            draw = ImageDraw.Draw(annotated_image)
            
            # Charger une police
            try:
                font = ImageFont.truetype("arial.ttf", self.font_size)
                small_font = ImageFont.truetype("arial.ttf", 16)
            except IOError:
                font = ImageFont.load_default()
                small_font = ImageFont.load_default()
            
            # Dimensions de l'image
            width, height = pil_image.size
            
            # Ajouter les annotations basées sur les résultats d'analyse
            self._add_text_annotations(draw, analysis_results, width, height, font, small_font)
            self._add_analysis_overlay(draw, analysis_results, width, height, font, small_font)
            
            # Sauvegarder l'image annotée
            temp_dir = tempfile.mkdtemp()
            annotated_path = os.path.join(temp_dir, "annotated_result.png")
            annotated_image.save(annotated_path)
            
            return annotated_path, temp_dir
            
        except Exception as e:
            print(f"Erreur lors de la création de l'image annotée: {e}")
            return None, None
    
    def _add_text_annotations(self, draw, analysis_results, width, height, font, small_font):
        """
        Ajoute les annotations de texte détecté
        """
        # Simuler des zones de texte détecté (en pratique, cela viendrait de l'OCR)
        text_regions = [
            {"bbox": (50, 100, 300, 130), "text": "Texte principal", "type": "original"},
            {"bbox": (50, 200, 250, 230), "text": "Texte effacé", "type": "hidden"},
            {"bbox": (50, 300, 400, 330), "text": "Surcharge détectée", "type": "modified"}
        ]
        
        for region in text_regions:
            x1, y1, x2, y2 = region["bbox"]
            
            # Couleur selon le type
            if region["type"] == "original":
                color = self.text_color
                label = "TEXTE ORIGINAL"
            elif region["type"] == "hidden":
                color = self.hidden_color
                label = "TEXTE RESTAURÉ"
            else:
                color = self.annotation_color
                label = "MODIFICATION"
            
            # Dessiner le rectangle
            draw.rectangle([x1, y1, x2, y2], outline=color, width=3)
            
            # Ajouter le label
            draw.text((x1, y1-25), label, fill=color, font=small_font)
    
    def _add_analysis_overlay(self, draw, analysis_results, width, height, font, small_font):
        """
        Ajoute un overlay avec les informations d'analyse
        """
        # Créer un panneau d'informations en bas
        panel_height = 120
        panel_y = height - panel_height
        
        # Fond semi-transparent pour le panneau (simulé avec un rectangle)
        draw.rectangle([0, panel_y, width, height], fill=(0, 0, 0, 180), outline=(255, 255, 255))
        
        # Informations d'analyse
        confidence = analysis_results.get('confidence', 0)
        layers = analysis_results.get('layers_detected', 0)
        
        info_text = [
            f"Confiance: {confidence}%",
            f"Couches détectées: {layers}",
            f"Analyse spectrale: {'Réussie' if confidence > 70 else 'Partielle'}",
            f"Détection de pression: {'Active' if layers > 1 else 'Inactive'}"
        ]
        
        # Afficher les informations
        y_offset = panel_y + 10
        for i, text in enumerate(info_text):
            x_pos = 20 + (i % 2) * (width // 2)
            y_pos = y_offset + (i // 2) * 25
            draw.text((x_pos, y_pos), text, fill=(255, 255, 255), font=small_font)
        
        # Ajouter une légende des couleurs
        legend_x = width - 200
        legend_y = 20
        
        legend_items = [
            ("Texte Original", self.text_color),
            ("Texte Restauré", self.hidden_color),
            ("Modifications", self.annotation_color)
        ]
        
        # Fond pour la légende
        draw.rectangle([legend_x-10, legend_y-10, width-10, legend_y + len(legend_items)*25 + 10], 
                      fill=(255, 255, 255, 200), outline=(0, 0, 0))
        
        for i, (label, color) in enumerate(legend_items):
            y_pos = legend_y + i * 25
            # Carré de couleur
            draw.rectangle([legend_x, y_pos, legend_x+15, y_pos+15], fill=color)
            # Texte
            draw.text((legend_x + 20, y_pos), label, fill=(0, 0, 0), font=small_font)
    
    def create_comparison_image(self, original_path, annotated_path):
        """
        Crée une image de comparaison côte à côte
        """
        try:
            # Charger les deux images
            original = Image.open(original_path)
            annotated = Image.open(annotated_path)
            
            # Redimensionner si nécessaire pour qu'elles aient la même hauteur
            if original.size[1] != annotated.size[1]:
                target_height = min(original.size[1], annotated.size[1])
                original = original.resize((int(original.size[0] * target_height / original.size[1]), target_height))
                annotated = annotated.resize((int(annotated.size[0] * target_height / annotated.size[1]), target_height))
            
            # Créer l'image de comparaison
            total_width = original.size[0] + annotated.size[0] + 20  # 20px d'espacement
            comparison = Image.new('RGB', (total_width, original.size[1]), (255, 255, 255))
            
            # Coller les images
            comparison.paste(original, (0, 0))
            comparison.paste(annotated, (original.size[0] + 20, 0))
            
            # Ajouter des titres
            draw = ImageDraw.Draw(comparison)
            try:
                title_font = ImageFont.truetype("arial.ttf", 20)
            except IOError:
                title_font = ImageFont.load_default()
            
            draw.text((original.size[0]//2 - 50, 10), "ORIGINAL", fill=(0, 0, 0), font=title_font)
            draw.text((original.size[0] + 20 + annotated.size[0]//2 - 50, 10), "ANALYSÉ", fill=(0, 0, 0), font=title_font)
            
            # Sauvegarder
            temp_dir = tempfile.mkdtemp()
            comparison_path = os.path.join(temp_dir, "comparison.png")
            comparison.save(comparison_path)
            
            return comparison_path, temp_dir
            
        except Exception as e:
            print(f"Erreur lors de la création de l'image de comparaison: {e}")
            return None, None

# Fonction utilitaire pour l'intégration
def generate_annotated_results(original_image_path, analysis_results):
    """
    Génère toutes les images de résultats
    """
    annotator = ImageAnnotator()
    
    # Créer l'image annotée
    annotated_path, temp_dir1 = annotator.create_annotated_image(original_image_path, analysis_results)
    
    if annotated_path:
        # Créer l'image de comparaison
        comparison_path, temp_dir2 = annotator.create_comparison_image(original_image_path, annotated_path)
        
        return {
            'original_path': original_image_path,
            'annotated_path': annotated_path,
            'comparison_path': comparison_path,
            'temp_dirs': [temp_dir1, temp_dir2]
        }
    
    return None

# Test du module
if __name__ == "__main__":
    # Créer une image de test
    test_image = Image.new('RGB', (800, 600), color='white')
    draw = ImageDraw.Draw(test_image)
    
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        font = ImageFont.load_default()
    
    # Ajouter du texte de test
    draw.text((50, 100), "Texte principal visible", fill=(0, 0, 0), font=font)
    draw.text((50, 200), "Texte effacé (simulé)", fill=(150, 150, 150), font=font)
    draw.text((50, 300), "Surcharge de texte", fill=(0, 0, 0), font=font)
    
    # Sauvegarder l'image de test
    test_path = "test_document.png"
    test_image.save(test_path)
    
    # Tester l'annotation
    test_results = {
        'confidence': 85,
        'layers_detected': 3,
        'analysis': {
            'ocr': {'status': 'Succès'},
            'spectral': {'status': 'Succès'},
            'texture_pressure': {'status': 'Succès'}
        }
    }
    
    results = generate_annotated_results(test_path, test_results)
    if results:
        print(f"Images générées:")
        print(f"- Original: {results['original_path']}")
        print(f"- Annotée: {results['annotated_path']}")
        print(f"- Comparaison: {results['comparison_path']}")
    else:
        print("Erreur lors de la génération des images")

