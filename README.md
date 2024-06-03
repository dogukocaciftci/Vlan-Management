# VLAN Management System

This project is a VLAN management system that allows you to create, delete, and list VLANs on your network devices through a web interface. It is developed using Flask, Netmiko, and Paramiko.

### Project Screenshot

![Home Page](static/images/home_page.jpg)

## Requirements

- Python 3.x
- Flask
- Netmiko
- Paramiko

## Installation

1. Clone or download the project.
   ```bash
   git clone https://github.com/dogukocaciftci/Vlan-Management.git
   cd vlan-management
   ```

2. Install the required Python packages.
   ```bash
   pip install flask netmiko paramiko
   ```

## Usage

1. Start the Flask application.
   Use the following commands in PowerShell or CMD:
   
   PowerShell:
   ```powershell
   $env:FLASK_APP = "app.py"
   flask run
   ```

   CMD:
   ```cmd
   set FLASK_APP=app.py
   flask run
   ```

2. Open your web browser and go to `http://127.0.0.1:5000`.

3. Perform VLAN creation, deletion, and listing operations through the web interface.

## SSH Configuration on Cisco Device

To enable and properly configure the SSH service on your network device, follow these steps:

1. **Connect to Your Device via Console or Telnet:**

   Connect to your device using a console cable or Telnet.

2. **Enable and Configure the SSH Service:**

   Use the following commands to enable and configure the SSH service:

   ```bash
   enable
   configure terminal
   hostname Router
   ip domain-name example.com
   crypto key generate rsa
   ip ssh version 2
   line vty 0 15
   transport input ssh
   login local
   exit
   ```

3. **Create a User Account:**

   Create a user account to be used for SSH connections:

   ```bash
   username admin privilege 15 secret 0 password
   ```

4. **Save the Configuration:**

   Save the configuration changes:

   ```bash
   write memory
   ```

After completing these steps, your device will be ready to accept SSH connections.

## Web Interface

Fields to fill out in the web interface:

- **IP Address:** The IP address of your network device (e.g., `192.168.1.1`)
- **Username:** The SSH username for connecting to the device (e.g., `admin`)
- **Password:** The SSH user's password (e.g., `password`)
- **VLAN ID:** The ID of the VLAN you want to create (e.g., `10`)
- **VLAN Name:** The name of the VLAN you want to create (e.g., `TestVLAN`)
- **Interface:** The interface to assign the VLAN to (e.g., `GigabitEthernet0/1`)

## Project Directory Structure

```
vlan-management/
├── app.py
├── templates/
│   └── index.html
└── static/
    └── css/
        └── style.css
```

## Example Usage

### Creating a VLAN

Fill out the form and click the "Create VLAN" button.

### Deleting a VLAN

Enter the IP Address, Username, Password, and VLAN ID, then click the "Delete VLAN" button.

### Listing VLANs

Enter the IP Address, Username, and Password, then click the "List VLANs" button.
