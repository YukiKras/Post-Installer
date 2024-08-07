# coding=utf-8

import tkinter as tk
from tkinter import *
from tkinter import ttk
import ctypes
import sys
import os
import subprocess
import webbrowser
import urllib.request
import zipfile
import platform
import multiprocessing
import re

os_version = platform.system()

def vcr():
    url = "https://cloud.kiselev.ru.net/s/vcplusplusr/download/vcr.zip"
    # Путь для сохранения временного файла
    file_path = os.path.join(os.getenv("TEMP"), "vcr.zip")
    # Путь для распаковки
    extract_path = os.path.join(os.getenv("TEMP"), "extracted")
    # Загрузка файла из интернета
    urllib.request.urlretrieve(url, file_path)
    # Распаковка файла
    with zipfile.ZipFile(file_path, "r") as zip_ref:
       zip_ref.extractall(extract_path)
    # Запуск скрипта install_all.bat
    subprocess.call(os.path.join(extract_path, "install_all.bat"))
    
def win_activation():
    if os_version == "Windows" and platform.release() == "7":
                   # Код для Windows 7
                   url = "https://github.com/massgravel/Microsoft-Activation-Scripts/archive/refs/heads/master.zip"
                   # Путь для сохранения временного файла
                   file_path = os.path.join(os.getenv("TEMP"), "Microsoft-Activation-Scripts-master.zip")
                   # Путь к скрипту
                   extract_path = os.path.join(os.path.expanduser("~"), "Desktop")
                   script_path = os.path.join(extract_path, "Microsoft-Activation-Scripts-master", "MAS", "All-In-One-Version", "MAS_AIO.cmd")
                   
                   # Загрузка файла из интернета
                   urllib.request.urlretrieve(url, file_path)

                   # Распаковка файла
                   with zipfile.ZipFile(file_path, "r") as zip_ref:
                     zip_ref.extractall(extract_path)

                   # Запуск скрипта MAS_AIO.cmd
                   subprocess.call(script_path)

    else:
                   # Код для других версий операционной системы
                   subprocess.run(["powershell", "-Command", "irm", "https://massgrave.dev/get", "|", "iex"])
                   
def install_certificate(url, certificate_name):
                # Создаем временный каталог в каталоге %temp%
                temp_dir = os.path.join(os.getenv("TEMP"))
                # Полный путь к временному файлу сертификата
                certificate_path = os.path.join(temp_dir, certificate_name)
                # Скачивание сертификата
                urllib.request.urlretrieve(url, certificate_path)
                # Установка сертификата
                subprocess.call(['certutil', '-addstore', 'Root', certificate_path])

processes = []
 
def is_valid_username(username):
    # Проверить, соответствует ли имя пользователя условиям
    if re.match(r'^[a-zA-Z0-9_\-]+$', username):
        return True
    else:
        return False

def select_all():
    for checkbox in checkboxes:
        # Получаем путь к директории TEMP
        temp_dir = os.environ['TEMP']
        # Создаем полный путь к файлу postinstaller.log
        log_file = os.path.join(temp_dir, 'postinstaller.log')
        # Открываем файл в режиме добавления (при существовании файла будет добавляться новая информация, а не перезаписываться)
        with open(log_file, 'a') as file:
            # Перенаправляем вывод в файл
            print(checkbox.cget("state"), file=file)
        if checkbox.cget("state") != "disabled":
            checkbox.state(['selected'])
            
def unselect_all():
    # Функция для снятия всех флажков
    for checkbox in checkboxes:
        checkbox.state(['!selected'])

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

if __name__ == "__main__":
    # Получить имя текущего пользователя Windows
    username = os.environ.get('USERNAME')

    # Проверить правильность имени пользователя
    if is_valid_username(username):
        print("Имя пользователя верно!")
    else:
        MessageBox = ctypes.windll.user32.MessageBoxW
        MessageBox(None, 'Создай пользователя с нормальным именем, с английскими буквами и без пробелов', 'Не будь националистом', 0)

def execute_code():
    for i, checkbox in enumerate(checkboxes_intvars):
        if checkbox.get() == 1:
            if i == 0:
                subprocess.run(["netsh", "advfirewall", "set", "allprofiles", "state", "off"])
                key_path = r"HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows Defender Security Center\\Notifications"
                # Команда для добавления значения DisableNotifications
                command_disable_notifications = f'reg add "{key_path}" /v "DisableNotifications" /t REG_DWORD /d 1 /f'
                # Команда для добавления значения DisableEnhancedNotifications
                command_disable_enhanced_notifications = f'reg add "{key_path}" /v "DisableEnhancedNotifications" /t REG_DWORD /d 1 /f'
                # Выполняем команды через subprocess
                subprocess.run(command_disable_notifications, shell=True)
                subprocess.run(command_disable_enhanced_notifications, shell=True)
            elif i == 1:
                MessageBox = ctypes.windll.user32.MessageBoxW
                MessageBox(None, 'Не закрывайте Post Installer пока не запустится установка редистов', 'Внимание', 0)
                process = multiprocessing.Process(target=vcr)
                processes.append(process)
            elif i == 2:
                process = multiprocessing.Process(target=win_activation)
                processes.append(process)
            elif i == 3:
                try:
                    # Проверяем наличие winget в системе
                    subprocess.run('winget --version', check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    # winget установлен, пробуем установить пакет qBittorrent
                    command = "winget install qBittorrent.qBittorrent -e"
                    subprocess.Popen(["cmd", "/c", "start", "cmd", "/k", command], shell=True)
                except FileNotFoundError:
                    # Ошибка FileNotFoundError, открываем ссылку на страницу загрузки qBittorrent в браузере
                    webbrowser.open("https://www.fosshub.com/qBittorrent.html")
            elif i == 4:
                try:
                    # Проверяем наличие winget в системе
                    subprocess.run('winget --version', check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    command = "winget install 7zip.7zip -e"
                    subprocess.Popen(["cmd", "/c", "start", "cmd", "/k", command], shell=True)
                except FileNotFoundError:
                    webbrowser.open("https://www.7-zip.org/download.html")
            elif i == 5:
                # Команды для внесения изменений в раздел [HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows Defender]
                command1 = 'REG ADD "HKLM\SOFTWARE\Policies\Microsoft\Windows Defender" /v "DisableAntiSpyware" /t REG_DWORD /d 1 /f'

                # Команды для внесения изменений в раздел [HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection]
                command2 = 'REG ADD "HKLM\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection" /v "DisableBehaviorMonitoring" /t REG_DWORD /d 1 /f'
                command3 = 'REG ADD "HKLM\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection" /v "DisableOnAccessProtection" /t REG_DWORD /d 1 /f'
                command4 = 'REG ADD "HKLM\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection" /v "DisableScanOnRealtimeEnable" /t REG_DWORD /d 1 /f'

                # Команды для внесения изменений в раздел [HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\SecurityHealthService]
                command5 = 'REG ADD "HKLM\SYSTEM\CurrentControlSet\Services\SecurityHealthService" /v "Start" /t REG_DWORD /d 3 /f'

                # Выполнение команд
                subprocess.run(command1, shell=True)
                subprocess.run(command2, shell=True)
                subprocess.run(command3, shell=True)
                subprocess.run(command4, shell=True)
                subprocess.run(command5, shell=True)
            elif i == 6:
                try:
                    # Проверяем наличие winget в системе
                    subprocess.run('winget --version', check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    command = "winget install sharex.sharex -e"
                    subprocess.Popen(["cmd", "/c", "start", "cmd", "/k", command], shell=True)
                except FileNotFoundError:
                    webbrowser.open("https://getsharex.com/downloads/")
            elif i == 7:
                subprocess.run(["UserAccountControlSettings.exe"])
            elif i == 8:
                subprocess.run(["Optionalfeatures.exe"])
            elif i == 9:
                subprocess.run(["powercfg", "/hibernate", "off"])
            elif i == 10:
                subprocess.run(["reg", "delete", "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\MyComputer\\NameSpace\\{0DB7E03F-FC29-4DC6-9020-FF41B59E513A}", "/f"])
            elif i == 11:
                commands = [
                    'reg delete "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\MyComputer\\NameSpace\\{088e3905-0323-4b02-9826-5d99428e115f}" /f',
                    'reg delete "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\MyComputer\\NameSpace\\{24ad3ad4-a569-4530-98e1-ab02f9417aa8}" /f',
                    'reg delete "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\MyComputer\\NameSpace\\{3dfdf296-dbec-4fb4-81d1-6a3438bcf4de}" /f',
                    'reg delete "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\MyComputer\\NameSpace\\{d3162b92-9365-467a-956b-92703aca08af}" /f',
                    'reg delete "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\MyComputer\\NameSpace\\{f86fa3ab-70d2-4fc7-9c99-fcbf05467f3a}" /f',
                    'reg delete "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\MyComputer\\NameSpace\\{B4BFCC3A-DB2C-424C-B029-7FE99A87C641}" /f'
                           ]
                # Выполнение команды для каждого элемента списка
                for command in commands:
                    subprocess.run(command, shell=True)
            elif i == 12:
                # Команда для NewStartPanel
                command21 = 'reg add "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\HideDesktopIcons\\NewStartPanel" /v "{20D04FE0-3AEA-1069-A2D8-08002B30309D}" /t REG_DWORD /d 0 /f'
                # Команда для ClassicStartMenu
                command22 = 'reg add "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\HideDesktopIcons\\ClassicStartMenu" /v "{20D04FE0-3AEA-1069-A2D8-08002B30309D}" /t REG_DWORD /d 0 /f'
                # Выполнение команд в командной строке
                subprocess.call(command21, shell=True)
                subprocess.call(command22, shell=True)
                # Завершаем процесс проводника
                subprocess.call("taskkill /f /im explorer.exe", shell=True)
                # Запускаем проводник снова
                subprocess.call("start explorer.exe", shell=True)
            elif i == 13:
                extensions = ['.jpg', '.jpeg', '.gif', '.png', '.bmp', '.tiff', '.ico']
                assoc_value = 'PhotoViewer.FileAssoc.Tiff'

                for extension in extensions:
                    command = f'reg add HKCU\Software\Classes\{extension} /ve /t REG_SZ /d {assoc_value} /f'
                    subprocess.run(command, shell=True)
            elif i == 14:
                # Установка корневого сертификата
                root_certificate_url = 'https://gu-st.ru/content/Other/doc/russian_trusted_root_ca.cer'
                root_certificate_name = 'Russian_Trusted_Root_CA.cer'
                install_certificate(root_certificate_url, root_certificate_name)
                # Установка выпускающего сертификата
                issuing_certificate_url = 'https://gu-st.ru/content/Other/doc/russian_trusted_sub_ca.cer'
                issuing_certificate_name = 'Russian_Trusted_Sub_CA.cer'
                install_certificate(issuing_certificate_url, issuing_certificate_name)      
            elif i == 15:
                url = "https://github.com/ValdikSS/GoodbyeDPI/releases/download/0.2.2/goodbyedpi-0.2.2.zip"
                file_path = os.path.join(os.getenv("TEMP"), "goodbyedpi-0.2.2.zip")
                extract_path = os.path.join(os.getenv("TEMP"), "extracted1")
                urllib.request.urlretrieve(url, file_path)
                with zipfile.ZipFile(file_path, "r") as zip_ref:
                  zip_ref.extractall(extract_path)
                subprocess.call(os.path.join(extract_path, "goodbyedpi-0.2.2", "1_russia_blacklist.cmd"))
                 
window = tk.Tk()
style = ttk.Style()
style.theme_use('vista')
window.title("Post Installer")
#window.resizable(False, False)
# Путь к файлу с иконкой
icon_path = resource_path("icon.ico")
# Установка иконки на окно
window.iconbitmap(default=icon_path)
window_width = 350
window_height = 480
# Определение координат верхнего левого угла окна, чтобы окно было по центру
x = (window.winfo_screenwidth() - window_width) // 2
y = (window.winfo_screenheight() - window_height) // 2
# Установка позиции окна
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

#Выбрать всё работает криво, потом фокшу
#select_all_var = tk.IntVar()
#select_all_checkbox = ttk.Checkbutton(window, text="Выбрать всё", variable=select_all_var)
#select_all_checkbox['command'] = lambda: select_all() if select_all_var.get() == 1 else unselect_all()
#select_all_checkbox.pack(anchor="w")

checkbox_texts = [
    "Выключить фаервол и его уведомления",                          #0
    "Скачать и запустить установку VC редистов за все года",        #1
    "Скачать и запустить Microsoft Activation Script",              #2
    "Скачать qBittorrent",                                          #3
    "Скачать 7zip",                                                 #4
    "*** Грохнуть дефендер",                                        #5
    "Скачать ShareX",                                               #6
    "Открыть настройки UAC",                                        #7
    "Открыть управление компонентами Windows",                      #8
    "Отключить быстрый запуск",                                     #9          
    "*** Удалить папку Объемные объекты из Этот компьютер",         #10
    "* Удалить все папки из компьютера в проводнике",               #11
    "** Добавить компьютер на рабочий стол",                        #12
    "Включить классический просмотровщик фотографий",               #13
    "Установить сертификаты минцифры России",                       #14
    "Установить goodbyedpi от замедления YouTube",                  #15
]

checkboxes_intvars = []
checkboxes = []
for i, text in enumerate(checkbox_texts):
    checkbox = tk.IntVar()
    checkbox_checkbutton = ttk.Checkbutton(window, text=text, variable=checkbox)
    checkbox_checkbutton.pack(anchor='w')
    checkboxes_intvars.append(checkbox)
    checkboxes.append(checkbox_checkbutton)
    if os_version == "Windows" and platform.release() == "7" and i in [5, 9, 10, 11, 13]:
        checkbox_checkbutton.configure(state="disabled")
    if os_version == "Windows" and platform.release() == "8" and i in [5, 10, 13]:
        checkbox_checkbutton.configure(state="disabled")
    if os_version == "Windows" and platform.release() == "8.1" and i in [5, 10, 13]:
        checkbox_checkbutton.configure(state="disabled")
    
label = ttk.Label(window, text=" ")
label.pack(anchor='w')
label = ttk.Label(window, text=" ")
label.pack(anchor='w')
label = ttk.Label(window, text="* Удалится всё кроме объемных объектов, так как для неё \n есть отдельный флажок")
label.pack(anchor='w')
label = ttk.Label(window, text="** При применении этого пункта проводник перезапустится")
label.pack(anchor='w')
label = ttk.Label(window, text="*** На Windows 11 такие пункты не работают")
label.pack(anchor='w')

execute_button = ttk.Button(window, text="Выполнить", command=execute_code)
execute_button.pack(anchor="n", side=tk.LEFT, padx=5)

def help_website():
    webbrowser.open('https://github.com/YukiKras/Post-Installer/')

help_button = ttk.Button(window, text="Почитать про пункты", command=help_website)
help_button.pack(anchor="n", side=tk.LEFT)

window.mainloop()
