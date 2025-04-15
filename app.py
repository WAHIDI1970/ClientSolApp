import streamlit as st
import pandas as pd
import joblib
import numpy as np
from sklearn.preprocessing import StandardScaler

# Configuration de l'application
st.set_page_config(page_title="Prédiction de Solvabilité", layout="centered")
st.title("🏦 Prédiction de Solvabilité Client")

# Solution pour l'erreur 'ModeleKNN'
class ModeleKNN:
    """Classe wrapper pour compatibilité"""
    def __init__(self, model):
        self.model = model
    
    def predict(self, X):
        return self.model.predict(X)
    
    def predict_proba(self, X):
        return self.model.predict_proba(X)

# Fonction de chargement des modèles corrigée
@st.cache_resource
def load_models_safe():
    try:
        # Chargement des composants
        scaler = joblib.load("scaler.pkl")
        
        # Chargement modèle Regression Logistique
        log_reg = joblib.load("Models\log_model.pkl")
        
        # Chargement modèle KNN avec gestion de l'erreur
        try:
            knn = joblib.load("Models\Knn.pkl")
        except AttributeError:
            # Solution de contournement si l'erreur persiste
            knn_data = joblib.load("Knn.pkl", mmap_mode='r')
            knn = ModeleKNN(knn_data)
        
        return {
            'scaler': scaler,
            'log_reg': log_reg,
            'knn': knn
        }
    except Exception as e:
        st.error(f"Erreur de chargement : {str(e)}")
        st.stop()

# Chargement initial des modèles
models = load_models_safe()

# Interface utilisateur
with st.sidebar:
    st.header("⚙️ Paramètres")
    model_choice = st.radio(
        "Sélection du modèle :",
        ["K-Nearest Neighbors","Régression Logistique"],
        index=0
    )

# Fonction de prédiction
def make_prediction(input_data):
    try:
        # Préparation des données
        df = pd.DataFrame([input_data])
        
        # Standardisation
        scaled_data = models['scaler'].transform(df)
        
        # Sélection du modèle
        if model_choice == "Régression Logistique":
            proba = models['log_reg'].predict_proba(scaled_data)[0][1]
        else:
            proba = models['knn'].predict_proba(scaled_data)[0][1]
        
        prediction = int(proba >= 0.5)
        return prediction, proba
    except Exception as e:
        st.error(f"Erreur de prédiction : {str(e)}")
        return None, None

# Formulaire principal
with st.form("main_form"):
    st.subheader("📋 Informations Client")
    
    age = st.number_input("Âge", min_value=18, max_value=100, value=35)
    marital = st.selectbox("Statut marital", [1, 2, 3], 
                         format_func=lambda x: {1: "Célibataire", 2: "Marié(e)", 3: "Divorcé(e)"}[x])
    expenses = st.number_input("Dépenses mensuelles (€)", min_value=0, value=500)
    income = st.number_input("Revenu mensuel (€)", min_value=0, value=2000)
    amount = st.number_input("Montant crédit (€)", min_value=0, value=10000)
    price = st.number_input("Prix achat (€)", min_value=0, value=12000)
    
    if st.form_submit_button("Prédire"):
        input_data = {
            'Age': age,
            'Marital': marital,
            'Expenses': expenses,
            'Income': income,
            'Amount': amount,
            'Price': price
        }
        
        prediction, proba = make_prediction(input_data)
        
        if prediction is not None:
            if prediction == 1:
                st.error(f"❌ Non Solvable (Probabilité: {proba:.1%})")
            else:
                st.success(f"✅ Solvable (Probabilité de défaut: {proba:.1%})")
            
            st.info(f"Modèle utilisé : {model_choice}")

# Pied de page
st.markdown("---")
st.caption("Système de prédiction de solvabilité - Projet de classe")