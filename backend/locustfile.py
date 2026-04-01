from locust import HttpUser, task,between
from faker import Faker
flow = {
  "src_ip": "192.168.1.100",
  "dst_ip": "104.28.14.89",
  "src_port": 54321,
  "dst_port": 80,
  "protocol": "6",
  "flow_duration": 150000.0,
  "total_fwd_packets": 10,
  "total_bwd_packets": 8,
  "total_length_fwd_packets": 500.0,
  "total_length_bwd_packets": 3200.0,
  "fwd_packet_length_mean": 50.0,
  "bwd_packet_length_mean": 400.0,
  "flow_bytes_per_sec": 24666.66,
  "flow_packets_per_sec": 120.0,
  "flow_iat_mean": 8333.33,
  "flow_iat_std": 1250.5,
  "fwd_psh_flags": 0,
  "bwd_psh_flags": 0,
  "fin_flag_count": 0,
  "syn_flag_count": 1,
  "rst_flag_count": 0,
  "psh_flag_count": 1,
  "ack_flag_count": 1,
  "urg_flag_count": 0,
  "init_win_bytes_fwd": 29200,
  "init_win_bytes_bwd": 256
}
fake = Faker()
class NadsUser(HttpUser):
    wait_time = between(1,3)

    def on_start(self):
        username = fake.user_name()
        password = fake.password()
        email = fake.email()
        
        self.client.post("/auth/register", json={
            "username": username,
            "email": email,
            "password": password
        })

        response = self.client.post("/auth/login",data={
            "username":username,
            "password": password
        })
        if response.status_code == 200:
            self.token = response.json()["access_token"]
        else:
            self.token = None

    @task(3)
    def predict(self):
        if not self.token:
            return
        
        self.client.post("/predict",json= flow,
                         headers={"Authorization": f"Bearer {self.token}"})
        


    @task(1)
    def get_alerts(self):
        if not self.token:
            return
        
        response = self.client.get("/alerts",
                        headers={"Authorization": f"Bearer {self.token}"})
        
        if response.status_code != 200:
            print(response.json())




