import os
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
import joblib

def train_and_save():
    # Chemin absolu vers les données
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'data', 'creditcard.csv')
    
    print("Chargement des données...")
    df = pd.read_csv(data_path)
    
    X = df.drop('Class', axis=1)
    y = df['Class']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
    
    # Poids pour déséquilibre
    scale_pos_weight = (len(y_train) - sum(y_train)) / sum(y_train)
    
    model = xgb.XGBClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.1,
        scale_pos_weight=scale_pos_weight,
        eval_metric='auc',
        random_state=42,
        n_jobs=-1
    )
    
    print("Entraînement en cours...")
    model.fit(X_train, y_train)
    
    # Sauvegarde
    model_dir = os.path.dirname(__file__)
    model_path = os.path.join(model_dir, 'model.xgb')
    joblib.dump(model, model_path)
    
    print(f"Modèle sauvegardé : {model_path}")
    print(f"AUC sur test : {model.score(X_test, y_test):.4f}")

if __name__ == "__main__":
    train_and_save()