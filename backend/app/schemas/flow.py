from pydantic import BaseModel


class NetworkFlow(BaseModel):
    """
    Feature vector sent from the Agent through Redis.
    Field names match CICIDS2017 dataset columns (simplified subset).
    """

    src_ip: str
    dst_ip: str
    src_port: int
    dst_port: int
    protocol: str  # TCP / UDP / ICMP

    # Flow duration in microseconds
    flow_duration: float

    # Packet counts
    total_fwd_packets: int
    total_bwd_packets: int

    # Byte stats
    total_length_fwd_packets: float
    total_length_bwd_packets: float

    # Packet length stats
    fwd_packet_length_mean: float
    bwd_packet_length_mean: float

    # Flow rate stats
    flow_bytes_per_sec: float
    flow_packets_per_sec: float

    # IAT – Inter-Arrival Time stats (microseconds)
    flow_iat_mean: float
    flow_iat_std: float

    # TCP flags
    fwd_psh_flags: int
    bwd_psh_flags: int
    fin_flag_count: int
    syn_flag_count: int
    rst_flag_count: int
    psh_flag_count: int
    ack_flag_count: int
    urg_flag_count: int

    # Window size
    init_win_bytes_fwd: int
    init_win_bytes_bwd: int
