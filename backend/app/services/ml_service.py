import logging
from pathlib import Path
import joblib
import numpy as np
from app.core.config import settings
from app.schemas.flow import NetworkFlow

FEATURE_COLUMNS = [

    "flow_duration",
    "total_fwd_packets",
    "total_bwd_packets",
    "total_length_fwd_packets",
    "total_length_bwd_packets",
    "fwd_packet_length_mean",
    "bwd_packet_length_mean",
    "flow_bytes_per_sec",
    "flow_packets_per_sec",
    "flow_iat_mean",
    "flow_iat_std",
    "fwd_psh_flags",
    "bwd_psh_flags",
    "fin_flag_count",
    "syn_flag_count",
    "rst_flag_count",
    "psh_flag_count",
    "ack_flag_count",
    "urg_flag_count",
    "init_win_bytes_fwd",
    "init_win_bytes_bwd"
]

class MLService:
    def __init__(self):
        self._binary_model = None
        self._multiclass_model = None
        self._label_encoder = None
        self.binary_model_path = Path(settings.BINARY_MODEL_PATH)
        self.multiclass_model_path = Path(settings.MULTICLASS_MODEL_PATH)
        self.label_encoder_path = Path(settings.LABEL_ENCODER_PATH)
        self._threshold = settings.ANOMALY_THRESHOLD

    def load(self):
        if not (self.binary_model_path.exists() and self.label_encoder_path.exists() and self.multiclass_model_path.exists()):
            logging.warning("Model file not found at %s - running in stub mode")
            return
        else:
            self._binary_model = joblib.load(self.binary_model_path)
            self._multiclass_model = joblib.load(self.multiclass_model_path)
            self._label_encoder = joblib.load(self.label_encoder_path)
            logging.info("ML Model loaded") 

    
    def predict(self,flow : NetworkFlow):
        models = [self._binary_model,self._multiclass_model,self._label_encoder]
        if any(model is None for model in models):
            return self._stub_result()
        else:
            features = self._extract_features(flow)
            raw_score = float(self._binary_model.predict_proba(features)[0][1])
          
            is_anomaly = raw_score >= self._threshold
            confidence = round(min(1.0,abs(raw_score - 0.5) * 2),4)
            return {
                "is_anomaly": is_anomaly,
                "anomaly_score": round(raw_score, 4),
                "confidence": confidence,
                "attack_type": self._classify_attack(flow) if is_anomaly else None,
            }


    def _extract_features(self, flow: NetworkFlow) -> np.ndarray:
        
        
        var = [getattr(flow,col, 0.0) for col in FEATURE_COLUMNS]
        arr = np.asarray(var,dtype=np.float64).reshape(1,21)

        return arr

    def _normalise_score(self, raw_score : float) -> float:

        return  1 / (1 + np.exp(raw_score))
    
    def _classify_attack(self,flow: NetworkFlow) -> str:

        features = self._extract_features(flow)
        class_num = self._multiclass_model.predict(features)
        attack_name = self._label_encoder.inverse_transform(class_num)
        return attack_name[0]
    
    def _stub_result(self):
        return {
            "is_anomaly" : False,
            "anomaly_score" : 0,
            "confidence" : 0,
            "attack_type" : None
        }
    
ml_service = MLService()