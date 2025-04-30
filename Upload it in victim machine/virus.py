import socket
import pyautogui
import os
import keyboard
import psutil
import subprocess

# إعداد السيرفر
HOST = "0.0.0.0"
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)
print(f"[*] Waiting for connection on {HOST}:{PORT}...")

client, addr = server.accept()
print(f"[*] Connected to: {addr}")

while True:
    try:
        command = client.recv(1024).decode().strip()
        if not command:
            continue

        print(f"[*] Received command: {command}")
        response = "Invalid command received"

        # قائمة التطبيقات المفتوحة
        if command == "list_apps":
            apps = [proc.info['name'] for proc in psutil.process_iter(['pid', 'name']) if proc.info['name']]
            response = "\n".join(apps) if apps else "No running applications found."

        # إغلاق تطبيق معين
        elif command.startswith("close_program "):
            try:
                _, app_name = command.split(" ", 1)
                found = False
                for proc in psutil.process_iter(['pid', 'name']):
                    if proc.info['name'].lower() == app_name.lower():
                        os.system(f"taskkill /F /PID {proc.info['pid']}")
                        response = f"Closed {app_name}"
                        found = True
                        break
                if not found:
                    response = f"Application {app_name} not found"
            except Exception as e:
                response = f"Error closing {app_name}: {e}"

        # إغلاق جميع التطبيقات غير الأساسية
        elif command == "close_all":
            closed_apps = []
            try:
                for proc in psutil.process_iter(['pid', 'name']):
                    app_name = proc.info['name'].lower()
                    if app_name not in ["explorer.exe", "taskmgr.exe"]:
                        os.system(f"taskkill /F /PID {proc.info['pid']}")
                        closed_apps.append(proc.info['name'])

                os.system("taskkill /F /IM explorer.exe")
                os.system("start explorer.exe")

                response = f"Closed applications: {', '.join(closed_apps)}" if closed_apps else "No applications closed."
            except Exception as e:
                response = f"Error closing applications: {e}"

        # إيقاف تشغيل الكمبيوتر
        elif command == "shutdown":
            os.system("shutdown /s /t 0")
            response = "Shutdown initiated."

        # تحريك الماوس
        elif command.startswith("mouse "):
            try:
                _, x, y = command.split()
                pyautogui.moveTo(int(x), int(y))
                response = f"Mouse moved to ({x}, {y})"
            except Exception as e:
                response = f"Error moving mouse: {e}"

        # كتابة نص
        elif command.startswith("type "):
            try:
                _, text = command.split(" ", 1)
                keyboard.write(text)
                response = f"Typed: {text}"
            except Exception as e:
                response = f"Error typing: {e}"

        # لقطة شاشة
        elif command == "screenshot":
            try:
                screenshot = pyautogui.screenshot()
                screenshot_path = "screenshot.png"
                screenshot.save(screenshot_path)

                with open(screenshot_path, "rb") as f:
                    screenshot_data = f.read()
                client.send(len(screenshot_data).to_bytes(8, "big"))
                client.sendall(screenshot_data)
                os.remove(screenshot_path)
                
            except Exception as e:
                client.send(b"\x00" * 8)
                client.send(str(e).encode())

        # فتح تطبيق
        elif command.startswith("open "):
            try:
                _, app_name = command.split(" ", 1)
                subprocess.Popen(app_name, shell=True)
                response = f"Opened {app_name}"
            except Exception as e:
                response = f"Error opening {app_name}: {e}"

        client.send(response.encode(errors="ignore"))
        
    except Exception as e:
        print(f"[ERROR] {e}")
        break
