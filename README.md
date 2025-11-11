# 🏦 Credit Scoring Application

## 📋 Table des Matières
- [Vue d'ensemble](#vue-densemble)
- [Fonctionnalités](#fonctionnalités)
- [Architecture du Projet](#architecture-du-projet)
- [Technologies Utilisées](#technologies-utilisées)
- [Installation et Déploiement](#installation-et-déploiement)
- [Modèles de Machine Learning](#modèles-de-machine-learning)
- [Utilisation de l'Application](#utilisation-de-lapplication)
- [Détails Techniques](#détails-techniques)
- [Résultats et Performance](#résultats-et-performance)
- [Améliorations Futures](#améliorations-futures)

---

## 🎯 Vue d'ensemble

Cette application de **Credit Scoring** permet de prédire la solvabilité des clients bancaires en utilisant des modèles de machine learning. Elle aide les institutions financières à évaluer le risque de défaut de paiement avant d'accorder un prêt.

### Problématique
- **Défi**: Identifier les clients susceptibles de ne pas rembourser leurs prêts
- **Solution**: Modèles prédictifs basés sur des caractéristiques financières et démographiques
- **Impact**: Réduction des risques financiers et amélioration de la prise de décision

---

## ✨ Fonctionnalités

### Interface Utilisateur
- 🖥️ **Interface Web Interactive** : Application Streamlit intuitive et responsive
- 📊 **Visualisations en Temps Réel** : Graphiques de probabilité et métriques de confiance
- 🔄 **Prédictions Multiples** : Comparaison de deux modèles simultanément
- 📈 **Analyse Détaillée** : Section technique pour comprendre les prédictions

### Capacités de Prédiction
- ✅ Classification binaire : Solvent / Non-Solvent
- 📊 Probabilités de prédiction pour chaque classe
- 🎯 Métriques de confiance pour chaque modèle
- 📉 Visualisation comparative des résultats

---

## 📁 Architecture du Projet

```
ClientBanKSollv/
│
├── .devcontainer/
│   └── devcontainer.json          # Configuration VS Code Dev Container
│
├── App/
│   └── app.py                     # Application Streamlit principale
│
├── models/                        # Modèles entraînés (à ajouter)
│   ├── ModeleKNNOptimise.pkl     # Modèle KNN personnalisé
│   ├── knn_model.pkl             # Modèle KNN standard
│   ├── logistic_model.pkl        # Modèle de régression logistique
│   └── scaler.pkl                # Scaler de standardisation
│
├── notebook/
│   └── untitled12 (2).py         # Notebook d'entraînement des modèles
│
├── requirements.exist             # Dépendances Python
└── README.md                      # Documentation (ce fichier)
```

---

## 🛠️ Technologies Utilisées

### Frontend & Interface
- **Streamlit 1.x** : Framework web pour applications de data science
- **Pandas** : Manipulation et analyse de données
- **Matplotlib/Seaborn** : Visualisations

### Machine Learning
- **Scikit-learn** : Bibliothèque principale de ML
  - Régression Logistique
  - K-Nearest Neighbors (KNN)
  - StandardScaler pour la normalisation
- **Imbalanced-learn** : Gestion du déséquilibre de classes (SMOTE)
- **Joblib** : Sérialisation des modèles

### Environnement de Développement
- **VS Code Dev Containers** : Environnement de développement reproductible
- **Python 3.11** : Version du langage
- **Docker** : Conteneurisation

---

## 🚀 Installation et Déploiement

### Prérequis
- Python 3.11+
- pip (gestionnaire de paquets Python)
- Git

### Installation Locale

1. **Cloner le repository**
```bash
git clone https://github.com/votre-username/ClientBanKSollv.git
cd ClientBanKSollv
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.exist
```

4. **Ajouter les modèles pré-entraînés**
Placez les fichiers `.pkl` dans le dossier `models/`:
- `ModeleKNNOptimise.pkl`
- `logistic_model.pkl`
- `scaler.pkl`
- `knn_model.pkl` (optionnel)

5. **Lancer l'application**
```bash
streamlit run App/app.py
```

L'application sera accessible à : `http://localhost:8501`

### Déploiement avec Dev Container

1. Ouvrir le projet dans VS Code
2. Installer l'extension "Dev Containers"
3. Appuyer sur `F1` → "Dev Containers: Reopen in Container"
4. L'application se lance automatiquement sur le port 8501

---

## 🤖 Modèles de Machine Learning

### 1. Régression Logistique

#### Description
Modèle statistique classique pour la classification binaire, idéal pour comprendre l'impact de chaque variable.

#### Caractéristiques Techniques
- **Algorithme** : Régression logistique avec pénalisation L1/L2
- **Optimisation** : GridSearchCV avec validation croisée (k=5)
- **Paramètres optimaux** :
  - `C` : Paramètre de régularisation (0.001 à 100)
  - `penalty` : L1 ou L2
  - `solver` : liblinear
  - `class_weight` : balanced (gestion du déséquilibre)

#### Prétraitement
```python
Pipeline:
1. Suppression des outliers (méthode IQR)
2. Standardisation (StandardScaler)
3. Équilibrage SMOTE
4. Entraînement avec seuil optimisé
```

#### Performance
- **Recall (classe 1)** : 78% - Capacité à identifier les clients non-solvables
- **AUC-ROC** : ~0.85 - Excellente discrimination
- **Seuil optimal** : Calculé via courbe Precision-Recall

#### Avantages
✅ Interprétable : Coefficients explicables
✅ Rapide à entraîner et prédire
✅ Robuste avec peu de données
✅ Probabilités calibrées

#### Limitations
❌ Assume une relation linéaire
❌ Sensible aux outliers (mitigé par prétraitement)

---

### 2. K-Nearest Neighbors (KNN) Optimisé

#### Description
Modèle non-paramétrique qui classe un client selon la majorité de ses k plus proches voisins dans l'espace des caractéristiques.

#### Caractéristiques Techniques
- **Architecture personnalisée** : `ModeleKNNOptimise`
- **Pipeline intégré** :
  ```python
  Pipeline([
      ('scaler', StandardScaler()),
      ('smote', SMOTE()),
      ('knn', KNeighborsClassifier(weights='distance'))
  ])
  ```
- **Pondération** : Distance (les voisins proches ont plus d'influence)
- **Optimisation du seuil** : Maximisation du F1-score

#### Paramètres
- **k** : Nombre de voisins (optimisé via validation croisée)
- **weights** : 'distance' (pondération inversement proportionnelle)
- **metric** : Distance euclidienne (par défaut)

#### Prétraitement
1. **Standardisation** : Essentielle pour KNN (sensible aux échelles)
2. **SMOTE** : Équilibrage des classes
3. **Optimisation du seuil** : Ajustement du seuil de décision

#### Performance
- **Flexibilité** : Capture les relations non-linéaires
- **Adaptabilité** : S'ajuste aux patterns locaux des données

#### Avantages
✅ Aucune hypothèse sur la distribution
✅ Capture les patterns complexes
✅ Simple à comprendre conceptuellement

#### Limitations
❌ Lent sur grands datasets (calcul de distances)
❌ Sensible au choix de k
❌ Nécessite beaucoup de mémoire (stocke tous les exemples)

---

### Comparaison des Modèles

| Critère | Régression Logistique | KNN Optimisé |
|---------|----------------------|--------------|
| **Interprétabilité** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Vitesse de prédiction** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Gestion non-linéarité** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Robustesse outliers** | ⭐⭐⭐⭐ | ⭐⭐ |
| **Besoin de données** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## 📊 Utilisation de l'Application

### Interface Principale

#### 1. Saisie des Informations Client
L'interface propose deux colonnes pour une saisie ergonomique :

**Colonne 1 - Informations Personnelles** :
- 👤 **Âge** : 18-100 ans
- 💍 **Statut Marital** : Single / Married / Divorced
- 💰 **Dépenses Mensuelles** : En euros

**Colonne 2 - Informations Financières** :
- 💵 **Revenu Mensuel** : En euros
- 🏦 **Montant du Prêt** : Somme demandée
- 🏠 **Valeur du Bien** : Prix de l'achat

#### 2. Prédiction
Cliquez sur **"Predict Solvency"** pour obtenir :
- Classification : Solvent ✅ / Non-Solvent 🚨
- Pourcentage de confiance
- Graphique de probabilités

#### 3. Résultats
Deux prédictions côte-à-côte :
- **Régression Logistique** : Modèle linéaire interprétable
- **KNN Optimisé** : Modèle non-linéaire flexible

### Interprétation des Résultats

#### Codes Couleur
- 🟢 **Vert (Solvent)** : Risque faible, prêt recommandé
- 🔴 **Rouge (Non-Solvent)** : Risque élevé, prêt déconseillé

#### Métriques de Confiance
- **90-100%** : Très haute confiance
- **70-89%** : Haute confiance
- **50-69%** : Confiance modérée
- **< 50%** : Incertitude élevée

#### Graphiques de Probabilité
- Barres comparatives entre les deux classes
- Permet de voir la "distance" à la décision

---

## 🔬 Détails Techniques

### Variables d'Entrée

| Variable | Type | Description | Rôle |
|----------|------|-------------|------|
| **Age** | Numérique | Âge du client (18-100) | Stabilité financière |
| **Marital** | Catégoriel | Statut marital (1=Single, 2=Married, 3=Divorced) | Responsabilités |
| **Expenses** | Numérique | Dépenses mensuelles (€) | Capacité d'épargne |
| **Income** | Numérique | Revenu mensuel (€) | Capacité de remboursement |
| **Amount** | Numérique | Montant du prêt (€) | Exposition au risque |
| **Price** | Numérique | Valeur du bien (€) | Collatéral |

### Pipeline de Prédiction

```python
1. Collecte des données utilisateur
   ↓
2. Transformation en DataFrame
   ↓
3. Standardisation (scaler.pkl)
   ↓
4. Prédiction Logistic Regression
   ↓
5. Prédiction KNN Optimisé
   ↓
6. Calcul des probabilités
   ↓
7. Affichage des résultats
```

### Gestion du Déséquilibre de Classes

**Problème Initial** :
- Classe 0 (Solvent) : 742 cas (73%)
- Classe 1 (Non-Solvent) : 273 cas (27%)

**Solutions Appliquées** :
1. **SMOTE** (Synthetic Minority Over-sampling) : Génération d'exemples synthétiques
2. **Class Weight Balancing** : Pénalisation ajustée dans la fonction de coût
3. **Optimisation du Seuil** : Seuil de décision ajusté pour maximiser le Recall

---

## 📈 Résultats et Performance

### Métriques d'Évaluation

#### Régression Logistique
```
Precision (classe 1) : ~75%
Recall (classe 1)    : ~78%  ← Métrique prioritaire
F1-Score (classe 1)  : ~76%
AUC-ROC              : ~0.85
```

#### KNN Optimisé
```
Performance comparable avec meilleure
capture des patterns non-linéaires
```

### Validation Croisée
- **Méthode** : K-Fold (k=5)
- **Objectif** : Éviter le sur-apprentissage
- **Résultat** : Stabilité des performances confirmée

### Matrice de Confusion (Exemple)
```
                 Prédit: 0    Prédit: 1
Réel: 0 (Solvent)    145          15
Réel: 1 (Non-Solv)    12          31
```
- **Vrais Positifs (TP)** : 31 clients non-solvables correctement identifiés
- **Faux Négatifs (FN)** : 12 clients à risque manqués ← À minimiser !

---

## 🎓 Méthodologie de Développement

### Phase 1 : Analyse Exploratoire (EDA)
1. Chargement des données (.sav format)
2. Analyse des distributions et outliers
3. Étude des corrélations (→ suppression de `Price` si multicolinéarité)
4. Détection du déséquilibre de classes

### Phase 2 : Prétraitement
1. Suppression des outliers (méthode IQR)
2. Standardisation des variables
3. Équilibrage avec SMOTE
4. Split train/test (80/20) avec stratification

### Phase 3 : Modélisation
1. Baseline : Régression Logistique simple
2. Optimisation avec GridSearchCV
3. Développement du KNN personnalisé
4. Comparaison et sélection

### Phase 4 : Déploiement
1. Sérialisation des modèles (joblib)
2. Développement de l'interface Streamlit
3. Conteneurisation (Dev Container)
4. Tests et validation

---

## 🔮 Améliorations Futures

### Court Terme
- [ ] Ajout de graphiques SHAP pour l'explicabilité
- [ ] Export des prédictions en PDF
- [ ] Historique des prédictions
- [ ] Mode batch (traitement de fichiers CSV)

### Moyen Terme
- [ ] Intégration de modèles avancés (XGBoost, Random Forest)
- [ ] API REST pour intégration système
- [ ] Dashboard analytique pour les gestionnaires
- [ ] Tests A/B entre modèles

### Long Terme
- [ ] Apprentissage en ligne (mise à jour continue)
- [ ] Détection de drift des données
- [ ] Système de monitoring MLOps
- [ ] Multi-tenancy pour plusieurs institutions

---

## 📝 Notes Importantes

### Considérations Éthiques
⚠️ **Biais Potentiels** : Les modèles peuvent hériter de biais présents dans les données historiques
⚠️ **Transparence** : Toujours expliquer les décisions aux clients
⚠️ **Conformité** : Respecter le RGPD et les réglementations bancaires

### Limites
- Les modèles sont aussi bons que les données d'entraînement
- Ne remplace pas l'expertise humaine
- Nécessite une maintenance et réentraînement réguliers

### Recommandations
✅ Utiliser comme outil d'aide à la décision, pas de décision automatique
✅ Réentraîner tous les 6 mois minimum
✅ Monitorer la performance en production
✅ Combiner avec l'analyse manuelle pour les cas limites

---

## 👥 Contribution

Les contributions sont les bienvenues ! Pour contribuer :
1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

---

## 📧 Contact & Support

Pour toute question ou problème :
- Ouvrir une issue sur GitHub
- Consulter la documentation Streamlit : https://docs.streamlit.io
- Documentation Scikit-learn : https://scikit-learn.org

---

## 📄 Licence

Ce projet est développé à des fins éducatives et de démonstration.

---

## 🙏 Remerciements

- Scikit-learn pour les outils de ML
- Streamlit pour le framework web
- La communauté open-source pour les bibliothèques utilisées

---

**Dernière mise à jour** : Novembre 2025
**Version** : 1.0.0
