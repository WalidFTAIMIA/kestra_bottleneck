# Pipeline BottleNeck avec Kestra

## Objectif

Orchestrer le traitement des sources ERP, WEB et LIAISON avec Kestra, Python et DuckDB. Le pipeline nettoie les sources, controle leur qualite, reconcilie les ventes, calcule le chiffre d'affaires et classe les produits selon leur Z-score.

## Sources

Les fichiers Excel sont dans `data/` :

- `Fichier_erp.xlsx`
- `Fichier_web.xlsx`
- `fichier_liaison.xlsx`

La base DuckDB persistante est `bottleneck.db`.

## Ordre du workflow

Le workflow est defini dans `workflows/bottleneck.yml` :

1. `import_sources` importe les trois fichiers dans DuckDB.
2. `clean_sources` cree `erp_clean`, `web_clean` et `liaison_clean`.
3. `test_erp`, `test_web` et `test_liaison` controlent la qualite des sources.
4. `reconciliation` cree la table `ventes`.
5. `test_reconciliation` verifie le volume, les doublons et les valeurs nulles.
6. `calcul_ca` cree `ca_produit` et `rapport_ca.xlsx`.
7. `test_ca` verifie le resultat du chiffre d'affaires.
8. `zscore` genere `premium.csv` et `ordinaire.csv`.
9. `test_zscore` verifie la classification.
10. Les taches d'export verifient la presence des fichiers produits.

Les tests sont des taches Kestra bloquantes : une assertion non satisfaite provoque l'echec de la tache et arrete le workflow.

## Resultats de validation

Execution validee  :

- ERP importe : 825 lignes
- WEB importe : 1513 lignes
- WEB nettoye : 714 lignes
- LIAISON nettoyee : 734 lignes
- Ventes reconciliees : 714 lignes
- Chiffre d'affaires : 70 568,60 EUR
- Produits premium : 30
- Produits ordinaires : 684
- Doublons ERP : 0
- Doublons WEB : 0
- Doublons reels `id_web` : 0

La source LIAISON contient 825 lignes, dont 91 avec un `id_web` manquant. Ces lignes correspondent a des produits ERP sans correspondance WEB. Elles sont exclues par `clean_liaison.sql`, ce qui laisse 734 lignes exploitables. Les 734 lignes ne deviennent pas toutes des ventes : la jointure avec les produits WEB et le filtre sur `total_sales` produisent finalement 714 lignes dans `ventes`. Les 91 lignes manquantes ne sont donc pas des doublons ; elles sont documentees comme des correspondances WEB absentes.

Les exports sont :

- `rapport_ca.xlsx`
- `premium.csv`
- `ordinaire.csv`

## Robustesse et supervision

Les etapes nominales `import_sources`, `clean_sources`, `reconciliation`, `calcul_ca` et `zscore` disposent d'un retry Kestra : trois tentatives maximum, avec un intervalle de 30 secondes. Cela protege le workflow contre une indisponibilite temporaire du fichier monte, de DuckDB ou d'une dependance Python.

Les logs Kestra constituent le monitoring de base : chaque tache est visible avec son statut, sa duree et sa sortie. En production, un echec du workflow doit declencher une alerte e-mail ou Slack via une regle d'alerte Kestra. Cette alerte doit contenir l'identifiant du flow, la tache en erreur et le lien vers les logs.

Une optimisation possible consiste a parallelliser les nettoyages ERP, WEB et LIAISON apres `import_sources`, car ils sont independants. Dans la version actuelle, ils restent regroupes dans `clean_sources` afin d'eviter les ecritures concurrentes dans le meme fichier DuckDB. Une mise en oeuvre parallele necessiterait une base ou des fichiers temporaires distincts, suivie d'une etape de consolidation.

## Execution locale

Depuis le dossier du projet :

```powershell
docker compose up -d
```

Le workflow peut ensuite etre importe ou colle dans Kestra depuis `workflows/bottleneck.yml`, puis lance manuellement pour validation.

Kestra est accessible sur `http://localhost:8080`.

## Planification

Le trigger Kestra est configure pour executer le workflow a 09:00 le 15 de chaque mois :

```yaml
cron: "0 9 15 * *"
timezone: Europe/Paris
```

Chaque execution relit les fichiers complets et recalcule les tables et les exports. Le pipeline n'est pas incremental.

## Difficultes et solutions

- `pip` n'etait pas disponible dans l'environnement virtuel Kestra. Les dependances sont installees avec `uv pip install` dans les taches Python.
- Les chemins relatifs des scripts necessitent une execution depuis `/project`.
- Les messages de `uv` et l'avertissement OpenPyXL peuvent apparaitre avec le niveau `ERROR` dans Kestra, mais l'execution reste reussie si la tache se termine avec le code 0.
- L'ouverture de `bottleneck.db` doit se faire avec un outil compatible DuckDB, et non avec SQLite.

## Journal de bord

- Importation des sources et persistence des tables DuckDB.
- Separation de l'importation, du nettoyage et de la reconciliation.
- Ajout des controles Python dans le workflow Kestra.
- Transformation des controles en tests bloquants avec `assert`.
- Validation du pipeline complet et generation des exports.
