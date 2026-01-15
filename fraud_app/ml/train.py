import os
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
import joblib
import numpy as np

def train_and_save():
    # Chemin vers les données
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    data_path = os.path.join(base_dir, 'data', 'creditcard.csv')
    
    print(f"🔍 Recherche : {data_path}")
    
    if not os.path.exists(data_path):
        print("❌ ERREUR : creditcard.csv manquant !")
        return False
    
    print("✅ Chargement...")
    df = pd.read_csv(data_path)
    print(f"✅ {len(df)} transactions chargées")
    
    # NETTOYAGE DES NaN
    print("🧹 Nettoyage des données...")
    df = df.dropna()
    df['Class'] = df['Class'].fillna(0).astype(int)
    
    if len(df) < 10:
        print("❌ Trop peu de données ! Minimum 10 lignes")
        return False
    
    print(f"✅ {len(df)} transactions après nettoyage")
    
    X = df.drop('Class', axis=1)
    y = df['Class']
    
    print(f"📊 Classes: {y.value_counts().to_dict()}")
    
    # SPLIT SANS STRATIFY pour petits datasets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42  # 70/30 au lieu de 80/20
    )
    
    # Balance les classes pour l'entraînement
    scale_pos_weight = len(y_train[y_train == 0]) / max(len(y_train[y_train == 1]), 1)
    
    model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=4,
        learning_rate=0.1,
        scale_pos_weight=scale_pos_weight,
        random_state=42,
        n_jobs=-1
    )
    
    print("🚀 Entraînement...")
    model.fit(X_train, y_train)
    
    # Évaluation
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    
    model_path = os.path.join(os.path.dirname(__file__), 'model.xgb')
    joblib.dump(model, model_path)
    
    print("✅" * 20)
    print(f"✅ MODÈLE SAUVEGARDÉ : {model_path}")
    print(f"✅ Train accuracy: {train_score:.4f}")
    print(f"✅ Test accuracy:  {test_score:.4f}")
    print("✅" * 20)
    return True

if __name__ == "__main__":
    train_and_save()