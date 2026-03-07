from influxdb_client import InfluxDBClient,Point
from influxdb_client.client.write_api import SYNCHRONOUS
from app.schemas.flow import NetworkFlow
from app.core.config import settings
client = InfluxDBClient(url= settings.INFLUXDB_URL, 
                        token=settings.INFLUXDB_TOKEN,
                        org = 
                        settings.INFLUXDB_ORG)

api = client.write_api(write_options=SYNCHRONOUS)

def write_flow_metric(flow: NetworkFlow,prediction: dict):
    point = Point("network_flow").tag("src_ip",flow.src_ip) \
    .tag("dst_ip", flow.dst_ip) \
    .field("src_port", flow.src_port) \
    .field("dst_port", flow.dst_port) \
    .tag("protocol", flow.protocol) \
    .field("anomaly_score", prediction["anomaly_score"]) \
    .field("is_anomaly", prediction["is_anomaly"])

    api.write(bucket=settings.INFLUXDB_BUCKET,org = settings.INFLUXDB_ORG,record=point)
