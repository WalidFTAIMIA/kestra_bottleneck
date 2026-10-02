from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "presentation_bottleneck_kestra_avec_explication_91.pptx"
SCREENSHOT = ROOT / "capture d'écran" / "démarrer kestra interface.png"

NAVY = RGBColor(16, 28, 45)
INK = RGBColor(31, 42, 55)
TEAL = RGBColor(25, 145, 145)
ORANGE = RGBColor(235, 133, 61)
PALE = RGBColor(241, 245, 247)
WHITE = RGBColor(255, 255, 255)
MUTED = RGBColor(96, 112, 126)
GREEN = RGBColor(41, 142, 95)


def add_background(slide, color=PALE):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    slide.shapes._spTree.remove(shape._element)
    slide.shapes._spTree.insert(2, shape._element)


def add_header(slide, title, number):
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.16))
    bar.fill.solid()
    bar.fill.fore_color.rgb = ORANGE
    bar.line.fill.background()
    text(slide, title, 0.65, 0.48, 11.7, 0.55, 26, INK, bold=True)
    text(slide, f"BOTTleneck / {number:02d}", 11.55, 0.53, 1.1, 0.25, 9, MUTED, bold=True, align=PP_ALIGN.RIGHT)


def text(slide, value, x, y, w, h, size=18, color=INK, bold=False, align=PP_ALIGN.LEFT):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    frame = box.text_frame
    frame.clear()
    frame.word_wrap = True
    frame.margin_left = 0
    frame.margin_right = 0
    frame.margin_top = 0
    frame.margin_bottom = 0
    paragraph = frame.paragraphs[0]
    paragraph.alignment = align
    run = paragraph.add_run()
    run.text = value
    run.font.name = "Aptos"
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    return box


def bullet_list(slide, items, x, y, w, h, size=17, color=INK, gap=8):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    frame = box.text_frame
    frame.clear()
    frame.word_wrap = True
    frame.margin_left = 0
    frame.margin_right = 0
    for index, item in enumerate(items):
        paragraph = frame.paragraphs[0] if index == 0 else frame.add_paragraph()
        paragraph.text = f"•  {item}"
        paragraph.level = 0
        paragraph.font.name = "Aptos"
        paragraph.font.size = Pt(size)
        paragraph.font.color.rgb = color
        paragraph.space_after = Pt(gap)
    return box


def card(slide, title, value, detail, x, y, w, accent=TEAL):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(1.25))
    shape.fill.solid()
    shape.fill.fore_color.rgb = WHITE
    shape.line.color.rgb = RGBColor(220, 228, 232)
    stripe = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(0.09), Inches(1.25))
    stripe.fill.solid()
    stripe.fill.fore_color.rgb = accent
    stripe.line.fill.background()
    text(slide, title.upper(), x + 0.28, y + 0.18, w - 0.45, 0.2, 9, MUTED, bold=True)
    text(slide, value, x + 0.28, y + 0.42, w - 0.45, 0.4, 25, INK, bold=True)
    text(slide, detail, x + 0.28, y + 0.9, w - 0.45, 0.2, 10, MUTED)


prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank = prs.slide_layouts[6]

# 1. Cover
slide = prs.slides.add_slide(blank)
add_background(slide, NAVY)
accent = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.72), Inches(0.85), Inches(0.13), Inches(4.9))
accent.fill.solid(); accent.fill.fore_color.rgb = ORANGE; accent.line.fill.background()
text(slide, "BottleNeck", 1.15, 1.05, 8.5, 0.9, 46, WHITE, bold=True)
text(slide, "Orchestration d'un pipeline data avec Kestra", 1.18, 2.05, 8.5, 0.55, 25, RGBColor(203, 220, 226))
text(slide, "Python  •  DuckDB  •  SQL  •  Docker", 1.18, 2.85, 8.5, 0.35, 15, ORANGE, bold=True)
text(slide, "Import | Nettoyage | Contrôles | Réconciliation | Analyses", 1.18, 4.85, 8.8, 0.3, 14, RGBColor(203, 220, 226))
text(slide, "Projet Data Engineer", 1.18, 6.45, 4.2, 0.25, 11, RGBColor(160, 180, 190))
text(slide, "25 septembre 2026", 9.6, 6.45, 2.5, 0.25, 11, RGBColor(160, 180, 190), align=PP_ALIGN.RIGHT)

# 2. Context
slide = prs.slides.add_slide(blank); add_background(slide); add_header(slide, "Le besoin métier", 2)
text(slide, "Transformer trois sources hétérogènes en indicateurs fiables", 0.75, 1.35, 7.9, 0.55, 28, INK, bold=True)
bullet_list(slide, [
    "Centraliser les données ERP, WEB et la table de liaison.",
    "Éliminer les lignes invalides et contrôler la qualité des sources.",
    "Réconcilier les produits et les ventes avant toute analyse.",
    "Produire un chiffre d'affaires et une segmentation par Z-score.",
], 0.8, 2.2, 7.2, 3.3, 19)
if SCREENSHOT.exists():
    slide.shapes.add_picture(str(SCREENSHOT), Inches(8.7), Inches(1.35), width=Inches(3.9), height=Inches(3.0))
text(slide, "Kestra fournit le cadre d'orchestration et la visibilité sur chaque étape.", 8.75, 4.55, 3.7, 0.7, 13, MUTED)

# 3. Sources
slide = prs.slides.add_slide(blank); add_background(slide); add_header(slide, "Les données en entrée", 3)
card(slide, "Source 01", "ERP", "Produits, prix, stock", 0.8, 1.5, 3.7, TEAL)
card(slide, "Source 02", "WEB", "Produits publiés et ventes", 4.8, 1.5, 3.7, ORANGE)
card(slide, "Source 03", "LIAISON", "Correspondance product_id / id_web", 8.8, 1.5, 3.7, GREEN)
text(slide, "Fichiers Excel", 0.8, 3.3, 2.1, 0.3, 16, MUTED, bold=True)
text(slide, "Fichier_erp.xlsx     Fichier_web.xlsx     fichier_liaison.xlsx", 0.8, 3.75, 11.3, 0.45, 20, INK, bold=True)
text(slide, "Stockage cible : bottleneck.db", 0.8, 5.2, 5.2, 0.3, 18, TEAL, bold=True)
text(slide, "DuckDB conserve les tables sources, nettoyées et analytiques.", 0.8, 5.65, 8.5, 0.35, 16, MUTED)

# 4. Task flow diagram
slide = prs.slides.add_slide(blank); add_background(slide); add_header(slide, "Diagramme des flux de tâches", 4)
text(slide, "Version présentée dans Diagram.drawio", 0.8, 1.05, 5.0, 0.3, 14, MUTED)
flow = [
    ("Début", TEAL),
    ("Import ERP + WEB + LIAISON", TEAL),
    ("Nettoyage\nNA / doublons", GREEN),
    ("Tests qualité\nOK → suite | KO → arrêt", ORANGE),
    ("Jointure / réconciliation", GREEN),
    ("Test réconciliation\nvolumétrie / clés", ORANGE),
    ("Calcul CA + Z-score", GREEN),
    ("Tests CA / classification", ORANGE),
    ("Exports XLSX + CSV", ORANGE),
    ("Fin", TEAL),
]
for index, (label, color) in enumerate(flow):
    y = 1.45 + index * 0.49
    box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.15), Inches(y), Inches(4.95), Inches(0.36))
    box.fill.solid(); box.fill.fore_color.rgb = color; box.line.fill.background()
    text(slide, label, 4.3, y + 0.075, 4.65, 0.2, 11, WHITE, bold=True, align=PP_ALIGN.CENTER)
    if index < len(flow) - 1:
        arrow = slide.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, Inches(6.45), Inches(y + 0.36), Inches(0.35), Inches(0.16))
        arrow.fill.solid(); arrow.fill.fore_color.rgb = RGBColor(170, 185, 192); arrow.line.fill.background()
error = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.55), Inches(2.95), Inches(2.35), Inches(0.72))
error.fill.solid(); error.fill.fore_color.rgb = RGBColor(248, 206, 204); error.line.color.rgb = RGBColor(184, 84, 80)
text(slide, "KO → log + arrêt\n(notification)", 9.72, 3.12, 2.0, 0.35, 13, RGBColor(140, 45, 42), bold=True, align=PP_ALIGN.CENTER)
text(slide, "Les tests sont des points de décision : aucune donnée invalide ne poursuit le pipeline.", 0.8, 6.55, 11.7, 0.3, 16, INK, bold=True, align=PP_ALIGN.CENTER)

# 4. Evidence: Kestra and execution
# 5. Evidence: Kestra and execution
slide = prs.slides.add_slide(blank); add_background(slide); add_header(slide, "Preuves de mise en place", 5)
dashboard = ROOT / "capture d'écran" / "démarrer kestra interface.png"
execution = ROOT / "capture d'écran" / "valide l'installation de kestra avec un worklow simple avant de développer le worklow métier .png"
if dashboard.exists():
    slide.shapes.add_picture(str(dashboard), Inches(0.75), Inches(1.35), width=Inches(5.8), height=Inches(3.35))
    text(slide, "Interface Kestra disponible", 0.85, 4.9, 5.4, 0.3, 15, INK, bold=True, align=PP_ALIGN.CENTER)
if execution.exists():
    slide.shapes.add_picture(str(execution), Inches(6.8), Inches(1.35), width=Inches(5.8), height=Inches(3.35))
    text(slide, "Première exécution validée", 6.9, 4.9, 5.4, 0.3, 15, INK, bold=True, align=PP_ALIGN.CENTER)
text(slide, "Ces captures introduisent la prise en main de Kestra avant le détail du pipeline.", 1.0, 5.75, 11.3, 0.35, 17, MUTED, align=PP_ALIGN.CENTER)

# 6. Pipeline
slide = prs.slides.add_slide(blank); add_background(slide); add_header(slide, "Le pipeline orchestré", 6)
steps = [("01", "Import", TEAL), ("02", "Nettoyage", ORANGE), ("03", "Tests", GREEN), ("04", "Réconciliation", TEAL), ("05", "CA + Z-score", ORANGE), ("06", "Exports", GREEN)]
for i, (num, label, color) in enumerate(steps):
    x = 0.75 + i * 2.08
    circle = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(2.0), Inches(0.72), Inches(0.72))
    circle.fill.solid(); circle.fill.fore_color.rgb = color; circle.line.fill.background()
    text(slide, num, x, 2.2, 0.72, 0.2, 13, WHITE, bold=True, align=PP_ALIGN.CENTER)
    text(slide, label, x - 0.25, 3.0, 1.25, 0.45, 15, INK, bold=True, align=PP_ALIGN.CENTER)
    if i < len(steps) - 1:
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x + 0.75), Inches(2.34), Inches(1.28), Inches(0.06))
        line.fill.solid(); line.fill.fore_color.rgb = RGBColor(190, 205, 210); line.line.fill.background()
text(slide, "Chaque étape est une tâche Kestra observable et relançable.", 0.8, 5.15, 11.5, 0.4, 22, INK, bold=True, align=PP_ALIGN.CENTER)

# 7. Workflow
slide = prs.slides.add_slide(blank); add_background(slide); add_header(slide, "Le workflow Kestra", 7)
text(slide, "bottleneck.yml", 0.8, 1.25, 3.5, 0.4, 24, TEAL, bold=True)
bullet_list(slide, [
    "Déclenchement mensuel : le 15 à 09:00, fuseau Europe/Paris.",
    "Environnement Python isolé avec uv et dépendances pandas, duckdb, openpyxl.",
    "Exécution depuis /project pour garantir les chemins relatifs.",
    "Les tâches s'arrêtent immédiatement lorsqu'un test échoue.",
], 0.85, 2.0, 6.2, 3.5, 18)
shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.6), Inches(1.45), Inches(4.7), Inches(4.6))
shape.fill.solid(); shape.fill.fore_color.rgb = NAVY; shape.line.fill.background()
text(slide, "import_sources", 8.05, 1.85, 3.8, 0.25, 16, WHITE, bold=True)
text(slide, "↓", 8.05, 2.2, 3.8, 0.25, 18, ORANGE, bold=True)
text(slide, "clean_sources", 8.05, 2.65, 3.8, 0.25, 16, WHITE, bold=True)
text(slide, "↓", 8.05, 3.0, 3.8, 0.25, 18, ORANGE, bold=True)
text(slide, "tests qualité", 8.05, 3.45, 3.8, 0.25, 16, WHITE, bold=True)
text(slide, "↓", 8.05, 3.8, 3.8, 0.25, 18, ORANGE, bold=True)
text(slide, "reconciliation → calcul_ca → zscore", 8.05, 4.25, 3.8, 0.5, 16, WHITE, bold=True)
text(slide, "↓", 8.05, 4.95, 3.8, 0.25, 18, ORANGE, bold=True)
text(slide, "exports contrôlés", 8.05, 5.35, 3.8, 0.25, 16, WHITE, bold=True)

# 8. Architecture choices
slide = prs.slides.add_slide(blank); add_background(slide); add_header(slide, "Pourquoi ces choix techniques ?", 8)
card(slide, "Kestra", "Orchestration", "Planification et logs", 0.8, 1.55, 3.7, TEAL)
bullet_list(slide, ["Orchestration des tâches", "Planification mensuelle", "Logs et suivi des exécutions"], 1.1, 3.05, 3.1, 1.7, 16)
card(slide, "DuckDB", "SQL embarqué", "Rapide et simple à déployer", 4.8, 1.55, 3.7, ORANGE)
bullet_list(slide, ["Traitement SQL local", "Moteur rapide", "Base sans serveur"], 5.1, 3.05, 3.1, 1.7, 16)
card(slide, "Python", "Traitement", "Z-score et exports", 8.8, 1.55, 3.7, GREEN)
bullet_list(slide, ["Préparation des données", "Calcul du Z-score", "Exports CSV et XLSX"], 9.1, 3.05, 3.1, 1.7, 16)
text(slide, "Kestra orchestre, DuckDB stocke et interroge, Python transforme et exporte.", 0.9, 5.55, 11.4, 0.45, 18, INK, bold=True, align=PP_ALIGN.CENTER)

# 9. Scheduling
slide = prs.slides.add_slide(blank); add_background(slide); add_header(slide, "Planification du workflow", 9)
text(slide, "Déclenchement automatique mensuel", 0.8, 1.25, 11.7, 0.45, 28, INK, bold=True, align=PP_ALIGN.CENTER)
shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.2), Inches(2.05), Inches(4.9), Inches(0.95))
shape.fill.solid(); shape.fill.fore_color.rgb = NAVY; shape.line.fill.background()
text(slide, "cron: 0 9 15 * *", 4.45, 2.35, 4.4, 0.3, 24, WHITE, bold=True, align=PP_ALIGN.CENTER)
text(slide, "15 de chaque mois à 09h00", 0.8, 3.55, 11.7, 0.35, 22, ORANGE, bold=True, align=PP_ALIGN.CENTER)
text(slide, "↓", 0.8, 4.05, 11.7, 0.35, 24, TEAL, bold=True, align=PP_ALIGN.CENTER)
text(slide, "Kestra", 0.8, 4.5, 11.7, 0.35, 22, INK, bold=True, align=PP_ALIGN.CENTER)
text(slide, "↓", 0.8, 4.95, 11.7, 0.35, 24, TEAL, bold=True, align=PP_ALIGN.CENTER)
text(slide, "Workflow BottleNeck", 0.8, 5.4, 11.7, 0.35, 22, INK, bold=True, align=PP_ALIGN.CENTER)
text(slide, "Fuseau configuré : Europe/Paris", 0.8, 6.05, 11.7, 0.25, 13, MUTED, align=PP_ALIGN.CENTER)

# 10. Quality
slide = prs.slides.add_slide(blank); add_background(slide); add_header(slide, "La qualité comme garde-fou", 10)
text(slide, "Un test qui échoue arrête le workflow", 0.8, 1.25, 7.0, 0.5, 28, INK, bold=True)
card(slide, "ERP", "0 doublon", "assertion sur la qualité produit", 0.8, 2.1, 3.7, TEAL)
card(slide, "WEB", "714 lignes", "produits valides après filtrage", 4.8, 2.1, 3.7, ORANGE)
card(slide, "LIAISON", "0 doublon réel", "id_web non nul et unique", 8.8, 2.1, 3.7, GREEN)
text(slide, "91 id_web manquants dans la liaison : produits ERP sans correspondance WEB. Ils sont exclus du nettoyage de liaison, pas considérés comme des doublons.", 0.9, 3.55, 11.1, 0.55, 15, MUTED, align=PP_ALIGN.CENTER)
bullet_list(slide, [
    "test_reconciliation : volume, unicité et valeurs nulles.",
    "test_ca : présence de produits et CA non négatif.",
    "test_zscore : classification complète et scores non nuls.",
], 0.9, 4.3, 10.8, 1.5, 17)

# 11. Error handling
slide = prs.slides.add_slide(blank); add_background(slide); add_header(slide, "Gestion des erreurs", 11)
text(slide, "Aucune donnée invalide ne poursuit le pipeline", 0.8, 1.2, 11.7, 0.45, 27, INK, bold=True, align=PP_ALIGN.CENTER)
error_steps = [("Traitement", TEAL), ("Test", ORANGE), ("OK → étape suivante", GREEN), ("KO → arrêt workflow", RGBColor(184, 84, 80)), ("Logs Kestra", NAVY)]
for i, (label, color) in enumerate(error_steps):
    y = 1.95 + i * 0.82
    block = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.15), Inches(y), Inches(5.0), Inches(0.55))
    block.fill.solid(); block.fill.fore_color.rgb = color; block.line.fill.background()
    text(slide, label, 4.35, y + 0.16, 4.6, 0.22, 18, WHITE, bold=True, align=PP_ALIGN.CENTER)
    if i < len(error_steps) - 1:
        text(slide, "↓", 0.8, y + 0.57, 11.7, 0.22, 17, MUTED, bold=True, align=PP_ALIGN.CENTER)
text(slide, "Les assertions Python arrêtent la tâche. Retry : 3 tentatives espacées de 30 secondes. En production : alerte e-mail ou Slack sur échec.", 0.8, 6.2, 11.7, 0.35, 14, MUTED, align=PP_ALIGN.CENTER)

# 12. Evidence: tests
slide = prs.slides.add_slide(blank); add_background(slide); add_header(slide, "Preuves des contrôles qualité", 12)
duplicates = ROOT / "capture d'écran" / "test cle primaire .png"
missing = ROOT / "capture d'écran" / "valeurs manquantes web.png"
if duplicates.exists():
    slide.shapes.add_picture(str(duplicates), Inches(0.8), Inches(1.25), width=Inches(5.9), height=Inches(3.75))
    text(slide, "Test des doublons ERP : 0 doublon", 0.9, 5.2, 5.7, 0.3, 15, INK, bold=True, align=PP_ALIGN.CENTER)
if missing.exists():
    slide.shapes.add_picture(str(missing), Inches(6.75), Inches(1.25), width=Inches(5.9), height=Inches(3.75))
    text(slide, "Analyse des valeurs manquantes WEB", 6.85, 5.2, 5.7, 0.3, 15, INK, bold=True, align=PP_ALIGN.CENTER)
text(slide, "Les tests bloquants intégrés à Kestra arrêtent le workflow en cas d’anomalie critique.", 1.0, 5.9, 11.3, 0.35, 17, MUTED, align=PP_ALIGN.CENTER)

# 10. Missing liaison explanation
slide = prs.slides.add_slide(blank); add_background(slide); add_header(slide, "Comprendre les 91 id_web manquants", 13)
text(slide, "Une absence de correspondance, pas une anomalie de doublon", 0.8, 1.25, 11.7, 0.5, 27, INK, bold=True, align=PP_ALIGN.CENTER)
card(slide, "Source LIAISON", "825", "lignes importées", 0.85, 2.05, 3.45, TEAL)
card(slide, "Correspondance absente", "91", "id_web manquants", 4.95, 2.05, 3.45, ORANGE)
card(slide, "Après nettoyage", "734", "id_web non nuls", 9.05, 2.05, 3.45, GREEN)
text(slide, "825 - 91 = 734", 0.8, 3.85, 11.7, 0.5, 30, TEAL, bold=True, align=PP_ALIGN.CENTER)
bullet_list(slide, [
    "Les 91 produits existent dans l'ERP, mais aucun identifiant WEB ne permet de les relier au catalogue en ligne.",
    "La règle SQL id_web IS NOT NULL les écarte du périmètre réconciliable.",
    "Les 734 lignes restantes sont jointes avec WEB ; 714 ventes disposent finalement d'un total_sales exploitable.",
    "Le contrôle des doublons réels id_web retourne 0 : les 91 lignes ne sont donc pas des doublons.",
], 1.0, 4.6, 11.2, 1.7, 16, INK, gap=7)

# 11. Results
slide = prs.slides.add_slide(blank); add_background(slide); add_header(slide, "Résultats de l'exécution", 14)
card(slide, "Ventes", "714", "lignes réconciliées", 0.8, 1.45, 2.8, TEAL)
card(slide, "Chiffre d'affaires", "70 568,60 €", "calculé dans ca_produit", 3.85, 1.45, 3.3, ORANGE)
card(slide, "Premium", "30", "produits avec Z-score > 2", 7.4, 1.45, 2.35, GREEN)
card(slide, "Ordinaires", "684", "produits classifiés", 10.0, 1.45, 2.35, TEAL)
text(slide, "Les résultats sont reproductibles : les sources sont relues et les tables sont recréées à chaque exécution.", 0.9, 4.1, 11.0, 0.7, 22, INK, bold=True, align=PP_ALIGN.CENTER)
text(slide, "Validation réalisée le 25 septembre 2026", 0.9, 5.2, 11.0, 0.3, 14, MUTED, align=PP_ALIGN.CENTER)

# 12. Outputs
slide = prs.slides.add_slide(blank); add_background(slide); add_header(slide, "Les livrables", 15)
outputs = [("bottleneck.db", "Tables DuckDB : sources, ventes, CA", TEAL), ("rapport_ca.xlsx", "Détail du CA et total", ORANGE), ("premium.csv", "Produits premium", GREEN), ("ordinaire.csv", "Produits ordinaires", TEAL)]
for i, (name, desc, color) in enumerate(outputs):
    y = 1.35 + i * 1.12
    block = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(y), Inches(11.2), Inches(0.78))
    block.fill.solid(); block.fill.fore_color.rgb = WHITE; block.line.color.rgb = RGBColor(220, 228, 232)
    mark = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(1.25), Inches(y + 0.2), Inches(0.35), Inches(0.35))
    mark.fill.solid(); mark.fill.fore_color.rgb = color; mark.line.fill.background()
    text(slide, name, 1.85, y + 0.18, 3.1, 0.25, 18, INK, bold=True)
    text(slide, desc, 5.25, y + 0.2, 6.3, 0.25, 15, MUTED)

# 13. Conclusion
slide = prs.slides.add_slide(blank); add_background(slide, NAVY)
text(slide, "Bilan", 0.85, 0.8, 3.5, 0.6, 38, WHITE, bold=True)
text(slide, "Un pipeline lisible, contrôlé et automatisé", 0.85, 1.7, 9.5, 0.6, 28, RGBColor(203, 220, 226), bold=True)
bullet_list(slide, [
    "Les étapes métier et les tests sont intégrés dans Kestra.",
    "DuckDB assure la persistance et la traçabilité des résultats.",
    "Les exports sont générés automatiquement et vérifiés.",
    "Évolution possible : passer d'un retraitement complet à un chargement incrémental.",
], 0.95, 2.85, 10.3, 2.6, 20, WHITE, gap=12)
text(slide, "Merci", 10.4, 6.25, 2.0, 0.45, 24, ORANGE, bold=True, align=PP_ALIGN.RIGHT)

prs.save(OUTPUT)
print(OUTPUT)