import sys
import os
import asyncio
from datetime import datetime, timedelta, timezone # <-- DODANO timezone
# 2. Importy aplikacji
from app.core.database import AsyncSessionLocal 
from app.models.alert import Alert

# 1. Konfiguracja ścieżek
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
sys.path.append(backend_dir)


async def seed_alerts():
    # Użycie timezone.utc działa w każdej współczesnej wersji Pythona (3.8+)
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    
    sample_alerts =[
        # 1-3. Atak DDoS
        Alert(timestamp=now - timedelta(hours=2, minutes=15), src_ip="172.16.0.1", dst_ip="192.168.10.50", src_port=51234, dst_port=80, protocol="TCP", anomaly_score=0.99, attack_type="DDoS", confidence=0.98),
        Alert(timestamp=now - timedelta(hours=2, minutes=14), src_ip="172.16.0.2", dst_ip="192.168.10.50", src_port=51235, dst_port=80, protocol="TCP", anomaly_score=0.98, attack_type="DDoS", confidence=0.99),
        Alert(timestamp=now - timedelta(hours=2, minutes=14), src_ip="172.16.0.3", dst_ip="192.168.10.50", src_port=51236, dst_port=80, protocol="TCP", anomaly_score=0.99, attack_type="DDoS", confidence=0.98),
        
        # 4-5. DoS Hulk
        Alert(timestamp=now - timedelta(hours=5), src_ip="10.0.0.15", dst_ip="192.168.1.100", src_port=49152, dst_port=80, protocol="TCP", anomaly_score=0.88, attack_type="DoS Hulk", confidence=0.91),
        Alert(timestamp=now - timedelta(hours=5, minutes=1), src_ip="10.0.0.15", dst_ip="192.168.1.100", src_port=49153, dst_port=80, protocol="TCP", anomaly_score=0.89, attack_type="DoS Hulk", confidence=0.92),
        
        # 6-8. PortScan
        Alert(timestamp=now - timedelta(hours=12, minutes=30), src_ip="192.168.2.55", dst_ip="192.168.1.10", src_port=54321, dst_port=22, protocol="TCP", anomaly_score=0.95, attack_type="PortScan", confidence=0.96),
        Alert(timestamp=now - timedelta(hours=12, minutes=30, seconds=5), src_ip="192.168.2.55", dst_ip="192.168.1.10", src_port=54321, dst_port=80, protocol="TCP", anomaly_score=0.94, attack_type="PortScan", confidence=0.95),
        Alert(timestamp=now - timedelta(hours=12, minutes=30, seconds=10), src_ip="192.168.2.55", dst_ip="192.168.1.10", src_port=54321, dst_port=443, protocol="TCP", anomaly_score=0.95, attack_type="PortScan", confidence=0.97),
        
        # 9-10. FTP-Patator / SSH-Patator (Brute Force)
        Alert(timestamp=now - timedelta(minutes=45), src_ip="203.0.113.40", dst_ip="10.10.10.5", src_port=33451, dst_port=21, protocol="TCP", anomaly_score=0.85, attack_type="FTP-Patator", confidence=0.88),
        Alert(timestamp=now - timedelta(minutes=40), src_ip="203.0.113.40", dst_ip="10.10.10.5", src_port=33452, dst_port=22, protocol="TCP", anomaly_score=0.87, attack_type="SSH-Patator", confidence=0.89),

        # 11. Botnet
        Alert(timestamp=now - timedelta(days=1), src_ip="192.168.1.105", dst_ip="198.51.100.22", src_port=40120, dst_port=8080, protocol="TCP", anomaly_score=0.92, attack_type="Bot", confidence=0.90),

        # 12. Infiltration
        Alert(timestamp=now - timedelta(minutes=10), src_ip="10.0.0.88", dst_ip="104.28.14.89", src_port=4444, dst_port=443, protocol="TCP", anomaly_score=0.81, attack_type="Infiltration", confidence=0.75),

        # 13. Anomalia typu UDP
        Alert(timestamp=now - timedelta(minutes=5), src_ip="8.8.8.8", dst_ip="192.168.1.50", src_port=53, dst_port=59341, protocol="UDP", anomaly_score=0.97, attack_type="DDoS", confidence=0.95),
        
        # 14. ICMP Flood / Ping of Death
        Alert(timestamp=now - timedelta(hours=3), src_ip="192.168.5.5", dst_ip="192.168.1.1", src_port=None, dst_port=None, protocol="ICMP", anomaly_score=0.90, attack_type="DoS", confidence=0.85),
    ]

    async with AsyncSessionLocal() as db:
        db.add_all(sample_alerts)
        await db.commit()
        print(f"Zaseedowano {len(sample_alerts)} alertów do bazy danych!")

if __name__ == "__main__":
    asyncio.run(seed_alerts())