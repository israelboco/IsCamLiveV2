import socket
import psutil

class GetNetworks:

    def get_networks(self):
        networks = []

        # Récupérer les informations de l'interface réseau
        networks.append({
            "interface": "WebCam",
            "ip_address": 0,
            "netmask": 'addr.netmask',
            "broadcast": 'addr.broadcast',
            "trailing_icon": 'webcam'
        })
        addrs = psutil.net_if_addrs()
        for interface_name, interface_addrs in addrs.items():
            for addr in interface_addrs:
                if addr.family == socket.AF_INET:
                    networks.append({
                        "interface": interface_name,
                        "ip_address": addr.address,
                        "netmask": addr.netmask,
                        "broadcast": addr.broadcast,
                        "trailing_icon": 'wifi'
                    })
        
        return networks

# Afficher les réseaux connectés
# connected_networks = get_networks()
# for network in connected_networks:
#     print(f"Interface: {network['interface']}")
#     print(f"IP Address: {network['ip_address']}")
#     print(f"Netmask: {network['netmask']}")
#     print(f"Broadcast: {network['broadcast']}")
#     print("-" * 20)
