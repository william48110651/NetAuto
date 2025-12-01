from netmiko import ConnectHandler

eos_device = {
"device_type": "arista_eos",
"host": "192.168.216.11",
"username": "admin",
"password": "admin",
}

try:
    net_connect = ConnectHandler(**eos_device)
    print("link okay")

except Exception as e:
    print("link failed", e)


