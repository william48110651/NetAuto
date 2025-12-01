from flask import Flask, render_template, request, redirect, url_for
from netmiko import ConnectHandler
import yaml

app = Flask(__name__)

# Load devices from YAML
with open("devices.yaml", "r") as f:
    devices = yaml.safe_load(f)["devices"]

@app.route("/")
def index():
    return render_template("index.html", devices=devices)

@app.route("/deploy", methods=["POST"])
def deploy():
    vlan_id = request.form["vlan_id"]
    vlan_name = request.form["vlan_name"]
    interface = "Ethernet1"
    selected_devices = request.form.getlist("devices")

    logs = []

    for host in selected_devices:
        device = next((d for d in devices if d["host"] == host), None)

        if not device:
            logs.append(f"❌ Device not found: {host}")
            continue

        try:
            logs.append(f"\n🔗 Connecting to {host} ...")

            net_connect = ConnectHandler(
            **device,
            fast_cli=False,
            global_delay_factor=2,
            conn_timeout=30,
            blocking_timeout=20,
            session_log="netmiko.log"
            )

            net_connect.enable()

            config_commands = [
                f"vlan {vlan_id}",
                f"name {vlan_name}",
                f"interface {interface}",
                f"switchport mode access",
                f"switchport access vlan {vlan_id}"
            ]

            output = net_connect.send_config_set(config_commands)
            logs.append(f"✅ Config applied on {host}:\n{output}")

            show_vlan = net_connect.send_command("show vlan brief")
            show_int = net_connect.send_command("show ip interface brief")

            logs.append(f"📌 VLAN Table on {host}:\n{show_vlan}")
            logs.append(f"📌 Interface Status on {host}:\n{show_int}")

            net_connect.disconnect()

        except Exception as e:
            logs.append(f"❌ Error on {host}: {e}")

    return render_template("index.html", devices=devices, logs="\n\n".join(logs))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
