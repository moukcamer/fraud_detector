import joblib
import pandas as pd
import os
from django.conf import settings

class FraudDetector:
    _model = None

    @classmethod
    def get_model(cls):
        if cls._model is None:
            model_path = os.path.join(settings.BASE_DIR, 'fraud_app', 'ml', 'model.xgb')
            if not os.path.exists(model_path):
                raise FileNotFoundError("Modèle non trouvé ! Lancez d'abord python fraud_app/ml/train.py")
            cls._model = joblib.load(model_path)
        return cls._model

    @classmethod
    def predict(cls, transaction_data: dict):
        model = cls.get_model()
        
        # On garde seulement les colonnes attendues par le modèle
        df = pd.DataFrame([transaction_data])
        expected_features = model.feature_names_in_
        df = df.reindex(columns=expected_features, fill_value=0)

        proba = model.predict_proba(df)[0][1]
        is_flagged = proba > 0.70  # Seuil ajustable

        return {
            'fraud_score': round(float(proba), 5),
            'is_flagged': bool(is_flagged)
        }