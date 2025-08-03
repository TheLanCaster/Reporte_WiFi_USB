import subprocess
import os
import ctypes
import sys
import time

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def get_wifi_profiles():
    try:
        output = subprocess.check_output(
            ["netsh", "wlan", "show", "profiles"],
            encoding="cp850"
        )
        profiles = []
        for line in output.split("\n"):
            if "Perfil de todos los usuarios" in line or "All User Profile" in line:
                profile = line.split(":")[1].strip()
                profiles.append(profile)
        return profiles
    except subprocess.CalledProcessError as e:
        print("Error al obtener perfiles WiFi:", e)
        return []

def get_wifi_password(profile):
    try:
        output = subprocess.check_output(
            ["netsh", "wlan", "show", "profile", profile, "key=clear"],
            encoding="cp850"
        )
        for line in output.split("\n"):
            if "Contenido de la clave" in line or "Key Content" in line:
                password = line.split(":")[1].strip()
                return password
        return "No encontrada"
    except subprocess.CalledProcessError:
        return "No disponible"

def main():
    if not is_admin():
        print("�Este programa necesita ser ejecutado como administrador!")
        ctypes.windll.user32.MessageBoxW(
            0,
            "�Debes ejecutar este programa como administrador!",
            "Permisos insuficientes",
            0x40
        )
        sys.exit()

    profiles = get_wifi_profiles()
    wifi_data = []
    for profile in profiles:
        password = get_wifi_password(profile)
        wifi_data.append((profile, password))

    # Guarda el archivo .txt en la misma ruta del .exe
    output_path = os.path.join(os.getcwd(), "WiFiPasswords.txt")
    with open(output_path, "w", encoding="utf-8") as file:
        for profile, password in wifi_data:
            file.write(f"SSID: {profile} | Contrase�a: {password}\n")
    
    print("�Las contrase�as se han guardado en:")
    print(output_path)
    input("Presiona Enter para cerrar...")

if __name__ == "__main__":
    main()

