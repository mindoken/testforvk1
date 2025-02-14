import requests
import os
import winreg
import subprocess
import sys

def download_file(url, save_dir):
    """Скачивает файл из указанного URL и сохраняет его в заданной директории."""
    # Проверяем, существует ли директория, если нет, создаем
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)  # Создаем директорию, если она не существует
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверяем, успешен ли запрос (код 200)
        
        filename = os.path.join(save_dir, 'gg.reg')  # Имя файла для сохранения
        with open(filename, 'wb') as file:
            file.write(response.content)  # Записываем содержимое ответа в файл
        
        print(f"Файл сохранен как: {filename}")  # Уведомление о сохранении файла
        return filename  # Возвращаем путь к сохраненному файлу
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при скачивании файла: {e}")  # Обработка ошибок
        return None  # Возвращаем None в случае ошибки

def import_registry_file(reg_file_path):
    """Импортирует файл реестра в систему."""
    try:
        subprocess.run(['regedit.exe', '/s', reg_file_path], check=True)
        print(f"Файл реестра {reg_file_path} успешно импортирован.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при импорте файла реестра: {e}")

def add_to_registry(key, value_name, value):
    """Добавляет значение в реестр Windows."""
    try:
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(registry_key, value_name, 0, winreg.REG_SZ, value)
        winreg.CloseKey(registry_key)
        print(f"Значение {value_name} добавлено в реестр.")
    except Exception as e:
        print(f"Ошибка при добавлении в реестр: {e}")

def find_steam_path():
    """Определяет путь к Steam в системе."""
    # Стандартные пути установки Steam
    possible_paths = [
        r"C:\Program Files (x86)\Steam\steam.exe",
        r"C:\Program Files\Steam\steam.exe",
        os.path.join(os.environ["ProgramFiles(x86)"], "Steam", "steam.exe"),
        os.path.join(os.environ["ProgramFiles"], "Steam", "steam.exe")
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    raise FileNotFoundError("Steam не найден. Убедитесь, что он установлен.")

def launch_steam_and_game(steam_path, game_id):
    """Запускает Steam и игру по ID."""
    try:
        subprocess.Popen([steam_path])  # Запуск Steam
        print("Steam запущен.")
        
        # Запуск игры по ID
        subprocess.Popen([steam_path, f'steam://run/{game_id}'])
        print(f"Игра с ID {game_id} запущена.")
    except Exception as e:
        print(f"Ошибка при запуске Steam или игры: {e}")

def read_registry_file(filename):
    """Читает файл .reg и извлекает пары ключ-значение."""
    values = {}
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            # Пропускаем комментарии и пустые строки
            if line.startswith(';') or not line:
                continue
            # Извлекаем пары ключ-значение
            if '=' in line:
                key_value = line.split('=', 1)
                if len(key_value) == 2:
                    key = key_value[0].strip().strip('"')
                    value = key_value[1].strip().strip('"')
                    values[key] = value
    return values

def main():
    url = "https://drive.google.com/uc?export=download&id=18Yr6wfSAJZTqhttMFVDNx7pZkez2vJBq"  # Замените на вашу ссылку
    save_dir = os.path.join(os.getenv("TEMP"), "GameFiles")  # Сохраняем в временной директории
    game_id = "1568590"  # Замените на ID вашей игры

    # Скачиваем файл
    downloaded_file = download_file(url, save_dir)
    
    if downloaded_file:
        print(f"Файл скачан: {downloaded_file}")

        # Импортируем файл реестра
        import_registry_file(downloaded_file)

        # Находим путь к Steam и запускаем игру
        try:
            steam_path = find_steam_path()
            launch_steam_and_game(steam_path, game_id)
        except FileNotFoundError as e:
            print(e)

if __name__ == "__main__":
    main()
