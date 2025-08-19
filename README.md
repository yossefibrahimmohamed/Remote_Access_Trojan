# Remote_Access_Trojan

 Remote Controller 🖥️

A Remote Access Tool (RAT) built using Python and CustomTkinter for the GUI, allowing you to access a Remote Victim in the same network:

    Connect to a victim machine.

    List running applications.

    Could you send live typing keystrokes?

    Close specific programs.

    Take screenshots remotely.

    Shut down the victim's machine.

    Disconnect safely.

📂 Project Structure

This application is built using:

    customtkinter — For a modern dark/light themed GUI.

    socket — For client-server communication.

    pyperclip — To easily copy text.

    tkinter dialogs — For alerts and file operations.

    Pillow (PIL) — For image operations.

⚙️ Features
Feature	Description
Connect to Victim: Establish a TCP connection to the victim's IP address.
List Running Apps	Displays all running applications in a scrollable window.
Live Typing	: Type live remotely into the victim's computer.
Open Notepad	. Opens Notepad on the victim's device.
Close Specific App	: Close any selected running application.
Take a Screenshot	Capture the victim's screen and save it locally.
Shutdown	Shutdown victim's computer.
Disconnect	. Cleanly terminate the connection to the victim.
🛠️ How It Works

    The Attacker GUI connects to the Victim through a socket on the specified IP and PORT.

    Commands are sent over the socket to control the victim's device.

    Results, responses, screenshots, etc., are handled on the attacker's side.

📸 Screenshots

    You can paste screenshots here if you'd like!

🧩 Requirements

Install required modules:

pip install customtkinter pillow pyperclip

🏗️ Setup

    Make sure the victim machine is listening on the port you specify.

    Adjust VICTIM_IP and PORT inside the script:

VICTIM_IP = "192.168.x.x"
PORT = 5000

    Run the script:

python remote_controller.py

![Recording2025-04-30173030-ezgif com-resize](https://github.com/user-attachments/assets/f97d91a9-2c2f-44ef-bebe-2c0d379252a9)


📢 Important Notes

    This tool is for educational and authorized use only.

    Always ensure you have explicit permission to connect to and control a device remotely.

    Misuse of such tools can be illegal. Be ethical! ⚖️

🧑‍💻 Developed by

Yossef Ibrahim
