import sys
import os
import asyncio
from datetime import datetime, timedelta, timezone

current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
sys.path.append(backend_dir)

from app.core.database import AsyncSessionLocal 
from app.models.alert import Alert

async def seed_alerts():
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    
    sample_alerts =[
        # --- ZBIÓR: Volume-based DDoS / DoS (Zalewowe sieciowe) ---
        Alert(timestamp=now - timedelta(hours=2, minutes=15), src_ip="172.16.0.1", dst_ip="192.168.10.50", src_port=51234, dst_port=80, protocol="TCP", anomaly_score=0.99, attack_type="DDoS", confidence=0.98),
        Alert(timestamp=now - timedelta(hours=2, minutes=14), src_ip="172.16.0.2", dst_ip="192.168.10.50", src_port=51235, dst_port=80, protocol="TCP", anomaly_score=0.98, attack_type="DDoS", confidence=0.99),
        Alert(timestamp=now - timedelta(hours=2, minutes=14), src_ip="172.16.0.3", dst_ip="192.168.10.50", src_port=51236, dst_port=80, protocol="TCP", anomaly_score=0.99, attack_type="DDoS", confidence=0.98),
        Alert(timestamp=now - timedelta(days=1, hours=3), src_ip="8.8.8.8", dst_ip="192.168.1.50", src_port=53, dst_port=59341, protocol="UDP", anomaly_score=0.97, attack_type="UDP Amplification", confidence=0.95),
        Alert(timestamp=now - timedelta(days=2), src_ip="192.168.5.5", dst_ip="192.168.1.1", src_port=None, dst_port=None, protocol="ICMP", anomaly_score=0.90, attack_type="ICMP Flood", confidence=0.85),
        Alert(timestamp=now - timedelta(hours=10), src_ip="203.0.113.15", dst_ip="10.0.0.10", src_port=44444, dst_port=443, protocol="TCP", anomaly_score=0.96, attack_type="SYN Flood", confidence=0.97),

        # --- ZBIÓR: DoS Aplikacyjne (L7) ---
        Alert(timestamp=now - timedelta(hours=5), src_ip="10.0.0.15", dst_ip="192.168.1.100", src_port=49152, dst_port=80, protocol="TCP", anomaly_score=0.88, attack_type="DoS Hulk", confidence=0.91),
        Alert(timestamp=now - timedelta(hours=5, minutes=1), src_ip="10.0.0.15", dst_ip="192.168.1.100", src_port=49153, dst_port=80, protocol="TCP", anomaly_score=0.89, attack_type="DoS Hulk", confidence=0.92),
        Alert(timestamp=now - timedelta(hours=18), src_ip="192.168.2.11", dst_ip="192.168.1.200", src_port=33211, dst_port=80, protocol="TCP", anomaly_score=0.93, attack_type="DoS GoldenEye", confidence=0.94),
        Alert(timestamp=now - timedelta(hours=18, minutes=5), src_ip="192.168.2.11", dst_ip="192.168.1.200", src_port=33212, dst_port=80, protocol="TCP", anomaly_score=0.92, attack_type="DoS GoldenEye", confidence=0.95),
        Alert(timestamp=now - timedelta(days=3), src_ip="104.28.14.89", dst_ip="172.16.0.10", src_port=55100, dst_port=443, protocol="TCP", anomaly_score=0.95, attack_type="DoS slowloris", confidence=0.96),

        # --- ZBIÓR: Rekonesans / Skanowanie (PortScan) ---
        Alert(timestamp=now - timedelta(hours=12, minutes=30), src_ip="192.168.2.55", dst_ip="192.168.1.10", src_port=54321, dst_port=22, protocol="TCP", anomaly_score=0.95, attack_type="PortScan", confidence=0.96),
        Alert(timestamp=now - timedelta(hours=12, minutes=30, seconds=1), src_ip="192.168.2.55", dst_ip="192.168.1.10", src_port=54321, dst_port=80, protocol="TCP", anomaly_score=0.94, attack_type="PortScan", confidence=0.95),
        Alert(timestamp=now - timedelta(hours=12, minutes=30, seconds=2), src_ip="192.168.2.55", dst_ip="192.168.1.10", src_port=54321, dst_port=443, protocol="TCP", anomaly_score=0.95, attack_type="PortScan", confidence=0.97),
        Alert(timestamp=now - timedelta(hours=12, minutes=30, seconds=3), src_ip="192.168.2.55", dst_ip="192.168.1.10", src_port=54321, dst_port=3306, protocol="TCP", anomaly_score=0.96, attack_type="PortScan", confidence=0.98),
        Alert(timestamp=now - timedelta(days=4), src_ip="198.51.100.33", dst_ip="10.10.10.25", src_port=60000, dst_port=161, protocol="UDP", anomaly_score=0.88, attack_type="UDP Scan", confidence=0.85),

        # --- ZBIÓR: Brute Force (Słownikowe zgadywanie haseł) ---
        Alert(timestamp=now - timedelta(minutes=45), src_ip="203.0.113.40", dst_ip="10.10.10.5", src_port=33451, dst_port=21, protocol="TCP", anomaly_score=0.85, attack_type="FTP-Patator", confidence=0.88),
        Alert(timestamp=now - timedelta(minutes=40), src_ip="203.0.113.40", dst_ip="10.10.10.5", src_port=33452, dst_port=22, protocol="TCP", anomaly_score=0.87, attack_type="SSH-Patator", confidence=0.89),
        Alert(timestamp=now - timedelta(days=1, hours=8), src_ip="185.15.2.22", dst_ip="192.168.1.30", src_port=12345, dst_port=3389, protocol="TCP", anomaly_score=0.91, attack_type="RDP Brute Force", confidence=0.92),
        
        # --- ZBIÓR: Ataki Webowe (Web Attack) ---
        Alert(timestamp=now - timedelta(hours=7), src_ip="45.33.22.11", dst_ip="192.168.1.100", src_port=55123, dst_port=80, protocol="TCP", anomaly_score=0.84, attack_type="Web Attack - Brute Force", confidence=0.86),
        Alert(timestamp=now - timedelta(hours=7, minutes=10), src_ip="45.33.22.11", dst_ip="192.168.1.100", src_port=55125, dst_port=80, protocol="TCP", anomaly_score=0.89, attack_type="Web Attack - XSS", confidence=0.85),
        Alert(timestamp=now - timedelta(hours=7, minutes=15), src_ip="45.33.22.11", dst_ip="192.168.1.100", src_port=55128, dst_port=443, protocol="TCP", anomaly_score=0.94, attack_type="Web Attack - Sql Injection", confidence=0.93),
        Alert(timestamp=now - timedelta(days=2, hours=1), src_ip="192.168.5.55", dst_ip="10.10.10.10", src_port=48999, dst_port=8080, protocol="TCP", anomaly_score=0.88, attack_type="Web Attack - LFI", confidence=0.82),

        # --- ZBIÓR: Malware, C2, Botnet, Infiltration ---
        Alert(timestamp=now - timedelta(days=1), src_ip="192.168.1.105", dst_ip="198.51.100.22", src_port=40120, dst_port=8080, protocol="TCP", anomaly_score=0.92, attack_type="Bot", confidence=0.90),
        Alert(timestamp=now - timedelta(minutes=10), src_ip="10.0.0.88", dst_ip="104.28.14.89", src_port=4444, dst_port=443, protocol="TCP", anomaly_score=0.81, attack_type="Infiltration", confidence=0.75),
        Alert(timestamp=now - timedelta(hours=14), src_ip="10.0.0.88", dst_ip="185.10.10.5", src_port=49155, dst_port=53, protocol="UDP", anomaly_score=0.86, attack_type="DNS Tunneling (Exfiltration)", confidence=0.88),
        Alert(timestamp=now - timedelta(days=5), src_ip="192.168.1.77", dst_ip="172.16.10.10", src_port=33333, dst_port=445, protocol="TCP", anomaly_score=0.98, attack_type="Ransomware Propagation (SMB)", confidence=0.99),
        Alert(timestamp=now - timedelta(days=5, minutes=2), src_ip="172.16.10.10", dst_ip="192.168.1.80", src_port=44512, dst_port=445, protocol="TCP", anomaly_score=0.97, attack_type="Ransomware Propagation (SMB)", confidence=0.98),

        # --- ZBIÓR: Vulnerability Exploitation (np. Heartbleed) ---
        Alert(timestamp=now - timedelta(days=6), src_ip="203.0.113.99", dst_ip="10.0.0.5", src_port=50001, dst_port=443, protocol="TCP", anomaly_score=0.95, attack_type="Heartbleed", confidence=0.99),
        Alert(timestamp=now - timedelta(days=6, seconds=30), src_ip="203.0.113.99", dst_ip="10.0.0.5", src_port=50002, dst_port=443, protocol="TCP", anomaly_score=0.96, attack_type="Heartbleed", confidence=0.98),

        # --- ZBIÓR: Ruch "Szary" (Podejrzany, z niższą pewnością, dobry do testowania paneli ML) ---
        Alert(timestamp=now - timedelta(minutes=55), src_ip="192.168.1.150", dst_ip="142.250.185.110", src_port=51222, dst_port=443, protocol="TCP", anomaly_score=0.65, attack_type="Suspicious Background Traffic", confidence=0.55),
        Alert(timestamp=now - timedelta(hours=3, minutes=20), src_ip="10.10.10.45", dst_ip="8.8.4.4", src_port=60555, dst_port=53, protocol="UDP", anomaly_score=0.55, attack_type="High Frequency DNS", confidence=0.60),
    ]

    for i in range(1, 11):
        sample_alerts.append(
            Alert(
                timestamp=now - timedelta(minutes=20, seconds=i*2), 
                src_ip="185.11.22.33", 
                dst_ip="192.168.1.5", 
                src_port=40000 + i, 
                dst_port=1000 + i, 
                protocol="TCP", 
                anomaly_score=0.88, 
                attack_type="PortScan", 
                confidence=0.90
            )
        )

    async with AsyncSessionLocal() as db:
        db.add_all(sample_alerts)
        await db.commit()
        print(f"Zaseedowano {len(sample_alerts)} alertów do bazy danych!")

if __name__ == "__main__":
    asyncio.run(seed_alerts())