from flask import Flask, request, jsonify, render_template
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
import logging

app = Flask(__name__)

class NetworkDevice:
    def __init__(self, ip, username, password, device_type='cisco_ios'):
        self.device = {
            'device_type': device_type,
            'host': ip,
            'username': username,
            'password': password,
            'port': 22,  # SSH port
            'timeout': 10,  # Connection timeout
        }
        self.connection = self.connect()

    def connect(self):
        # Attempt to establish an SSH connection to the network device
        try:
            print(f"Connecting to {self.device['host']} on port {self.device['port']} with username {self.device['username']}")
            return ConnectHandler(**self.device)
        except (NetmikoTimeoutException, NetmikoAuthenticationException) as e:
            print(f"Error connecting to device: {str(e)}")
            raise e

    def execute_commands(self, commands):
        # Execute a list of commands on the connected device
        try:
            output = ""
            for command in commands:
                output += self.connection.send_command(command) + "\n"
            return output
        except Exception as e:
            print(f"Error executing commands: {str(e)}")
            raise e

    def close(self):
        # Close the SSH connection
        self.connection.disconnect()

@app.route('/')
def index():
    # Render the main HTML page
    return render_template('index.html')

@app.route('/vlan', methods=['POST'])
def create_vlan():
    # Create a new VLAN on the network device
    data = request.get_json()
    try:
        device = NetworkDevice(data['ip'], data['username'], data['password'])
        commands = [
            f"vlan {data['vlan_id']}",
            f"name {data['vlan_name']}",
            "exit",
            f"interface {data['interface']}",
            "switchport mode access",
            f"switchport access vlan {data['vlan_id']}",
            "no shutdown",
            "exit"
        ]
        output = device.execute_commands(commands)
        device.close()
        return jsonify({"message": "VLAN created successfully", "output": output}), 200
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/vlan', methods=['DELETE'])
def delete_vlan():
    # Delete an existing VLAN from the network device
    data = request.get_json()
    try:
        device = NetworkDevice(data['ip'], data['username'], data['password'])
        commands = [
            f"no vlan {data['vlan_id']}"
        ]
        output = device.execute_commands(commands)
        device.close()
        return jsonify({"message": "VLAN deleted successfully", "output": output}), 200
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/vlans', methods=['POST'])
def list_vlans():
    # List all VLANs on the network device
    data = request.get_json()
    try:
        device = NetworkDevice(data['ip'], data['username'], data['password'])
        command = "show vlan brief"
        output = device.execute_commands([command])
        device.close()
        return jsonify({"vlans": output}), 200
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Configure logging and run the Flask application
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True)
