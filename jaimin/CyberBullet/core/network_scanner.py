import socket
import subprocess
import platform
import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed


def get_local_ip():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        ip = sock.getsockname()[0]
        sock.close()
        return ip
    except Exception:
        return "127.0.0.1"


def get_network_range():
    local_ip = get_local_ip()
    parts = local_ip.split(".")

    if len(parts) == 4:
        return f"{parts[0]}.{parts[1]}.{parts[2]}.0/24"

    return "127.0.0.0/24"


def ping_host(ip):
    system = platform.system().lower()

    if system == "windows":
        command = ["ping", "-n", "1", "-w", "250", ip]
    else:
        command = ["ping", "-c", "1", "-W", "1", ip]

    try:
        result = subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=1.5
        )

        return result.returncode == 0

    except Exception:
        return False


def get_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return "Unknown"


def check_host(ip):
    if ping_host(ip):
        return {
            "ip": ip,
            "hostname": get_hostname(ip),
            "status": "Online"
        }

    return None


def scan_network(network=None, max_workers=32):

    if network is None:
        network = get_network_range()

    results = []

    try:
        network_obj = ipaddress.ip_network(
            network,
            strict=False
        )

        hosts = [str(ip) for ip in network_obj.hosts()]

        with ThreadPoolExecutor(
            max_workers=max_workers
        ) as executor:

            futures = [
                executor.submit(check_host, ip)
                for ip in hosts
            ]

            for future in as_completed(futures):

                result = future.result()

                if result:
                    results.append(result)

        results.sort(
            key=lambda item: ipaddress.ip_address(item["ip"])
        )

        return {
            "network": network,
            "hosts": results
        }

    except Exception as error:

        return {
            "network": network,
            "hosts": [],
            "error": str(error)
        }