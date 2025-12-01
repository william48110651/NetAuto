from netmiko import ConnectHandler

devices = [
    {"device_type": "arista_eos", "host": "192.168.216.11", "username": "admin", "password": "admin"},
    {"device_type": "arista_eos", "host": "192.168.216.12", "username": "admin", "password": "admin"},
]

for dev in devices:
    try:
        net_connect = ConnectHandler(**dev)
        print(f"link okay to {dev['host']}")
    except Exception as e:
        print(f"link failed to {dev['host']}", e)
