from unittest.mock import MagicMock
from app.services.ml_service import MLService,FEATURE_COLUMNS
from app.schemas.flow import NetworkFlow
import pytest
@pytest.fixture
def sample_flow():
    return NetworkFlow(
        src_ip="192.168.1.100",
        dst_ip="104.28.14.89",
        src_port=54321,
        dst_port=80,
        protocol="6",               
        flow_duration=150000.0,     
        total_fwd_packets=10,
        total_bwd_packets=8,
        total_length_fwd_packets=500.0,
        total_length_bwd_packets=3200.0,
        fwd_packet_length_mean=50.0,
        bwd_packet_length_mean=400.0,
        flow_bytes_per_sec=24666.66,
        flow_packets_per_sec=120.0,
        flow_iat_mean=8333.33,
        flow_iat_std=1250.5,
        fwd_psh_flags=0,
        bwd_psh_flags=0,
        fin_flag_count=0,
        syn_flag_count=1,           
        rst_flag_count=0,
        psh_flag_count=1,           
        ack_flag_count=1,           
        urg_flag_count=0,
        init_win_bytes_fwd=29200,   
        init_win_bytes_bwd=256
        )
   
@pytest.fixture
def ml_service_with_mocks():
    ml_service = MLService()
    ml_service._binary_model = MagicMock()
    ml_service._label_encoder = MagicMock()
    ml_service._multiclass_model = MagicMock()
    ml_service._feature_columns = FEATURE_COLUMNS
    return ml_service
   

def test_predict_normal(ml_service_with_mocks,sample_flow):
    ml_service_with_mocks._binary_model.predict_proba.return_value = [[0.2,0.1]]
    pred = ml_service_with_mocks.predict(sample_flow)

    assert pred['is_anomaly'] == False
    

def test_predict_anomaly(ml_service_with_mocks,sample_flow):
    ml_service_with_mocks._binary_model.predict_proba.return_value = [[0.1,0.9]]
    prediction = ml_service_with_mocks.predict(sample_flow)
    

    assert prediction["is_anomaly"] == True


def test_treshold_value(ml_service_with_mocks,sample_flow):
    ml_service_with_mocks._binary_model.predict_proba.return_value = [[0.65,0.35]]
    prediction = ml_service_with_mocks.predict(sample_flow)

    assert prediction["is_anomaly"] == True