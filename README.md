# Post-Installer
Post Installer - небольшая утилита по автоматизации настройки Windows после её установки.
![изображение](https://github.com/NagibatorIgor/Post-Installer/assets/72355380/e31ce767-68a7-43a3-b26a-700d994c9cc3)
## Скачать
Перед скачиванием обезательно отключите все антивирусы! 
Github: https://github.com/NagibatorIgor/Post-Installer/releases
## FAQ
### Я хочу добавить то, то, или у меня какие-то проблемы. Как написать свои желания, идеи, проблемы?
Можете написать это через ресурсы комьюнити ConsoleCP:
- [Телеграм РУ](https://t.me/ccplru)
- [Вконтакте](https://vk.com/consolecp)
- [Discord](https://discord.gg/Nc6qDeSb9q)
### Почему нет автоудаления UWP и стора?
Качайте LTSC, где всё это официально и нормально вырезано.
### Почему нет выключателя всякой "слежки" в Windows?
Во первых сторонних инструментов для этого достаточно, во вторых некоторые вещи намертво отваливаются при этом, и в итоге приходится затевать чистую переустановку Windows. В третьих с такими мыслями используйте Linux дистрибутивы.

### Virustotal и защитник Windows ругают твою утилиту, ты что, хочешь нас заразить троянами?
Нет, весь исходный код программы тут выложен, вы в случае чего можете и сами скомпилировать утилиту с помощью pyinstaller, команда для компиляции выглядит так:
```
pyinstaller --noconfirm --onefile --windowed --icon "path/to/icon.ico" --uac-admin --add-data "path/to/icon.ico;." "path/to/Post_Installer.py"
```
### Почему заместо того чтоб качать qbittorent, 7zip, sharex через winget или вручную с оф. сайтов, сделать бы тебе WPI из них?
Эти программы обновляются регулярно, и добавляется регулярно новый функционал и исправления, а WPI сам себя обновлять не будет.
### На чём написано эта утилита?
Python.
### Какие минимальные системные требования?
Windows 7 SP1 x32 bit
### Почему это так важно?
![vmware_nWYypBfxPf](https://github.com/NagibatorIgor/Post-Installer/assets/72355380/2c789d8b-cdae-4123-9503-7acd82fd8e1e)

Причина описана здесь https://answers.microsoft.com/ru-ru/windows/forum/all/%D0%B8%D0%B7%D0%BC%D0%B5%D0%BD%D0%B5%D0%BD%D0%B8/a61b0771-8415-4e56-b6e0-2af04927003c
### Как поддержать проект?
+ Распространяйте - своим коллегам и знакомым
+ Пишите - свои предложения, проблемы и баги с Post Installer в сообщества, ссылки на них можно найти повыше
+ Материально поддержать - пока что можно через [трейд в Steam](https://steamcommunity.com/tradeoffer/new/?partner=1041043022&token=B7cef1Mr)
## Известные проблемы
+ Неверное отображение итерфейса утилиты при нестандартном масштабе в Windows
## Описание пунктов
### Выбрать всё
Автоматически выбирает все флажки.
### Выключить фаервол и его уведомления
Выключает фаервол с помощью команды
```
netsh advfirewall set allprofiles state off
```
И для отключения уведомлений применяет следующие твики в реестр:
```
[HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows Defender Security Center\Notifications]
"DisableNotifications"=dword:00000001
"DisableEnhancedNotifications"=dword:00000001
```
### Скачать и запустить установку VC редистов за все года
В %TEMP% скачивается скрипт автоустановки редистов [от сюда](https://www.techpowerup.com/download/visual-c-redistributable-runtime-package-all-in-one/), и собственно запускается в отдельном процессе.
### Скачать и запустить Microsft Activation Scripts
Вводится следующая команда:
```
irm https://massgrave.dev/get | iex
```
В случае с Windows 7 загружается на рабочий стол и запускается. [Ссылка на Microsoft Activation Scripts](https://github.com/massgravel/Microsoft-Activation-Scripts).
### Скачать Qbittorrent
Ставит его через winget. Если winget нету, то открывает официальный сайт загрузок.
### Скачать 7zip
Ставит его через winget. Если winget нету, то открывает официальный сайт загрузок.
### Грохнуть дефендр
Работает только на Windows 10, применяет следующие твики реестра:
```
[HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows Defender]
"DisableAntiSpyware"=dword:00000001

[HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection]
"DisableBehaviorMonitoring"=dword:00000001
"DisableOnAccessProtection"=dword:00000001
"DisableScanOnRealtimeEnable"=dword:00000001

[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\SecurityHealthService]
"Start"=dword:00000003
```
### Скачать ShareX
Ставит его через winget. Если winget нету, то открывает официальный сайт загрузок.
### Открыть настройки UAC
Открывает настройки user account control, для их отключения.
### Открыть управление компонентами Windows
Открывает меню управления компонентами Windows.
### Отключить быстрый запуск
Отключается он с помощью следующей команды:
```
powercfg /hibernate off
```
Этот флажок не доступен на Windows 7 так как быстрый запуск появился только в Windows 8.
### Удалить папку Объемные объекты из Этот компьютер
Работает только на Windows 10, скрывая с помощью следующего твика реестра из раздела Этот компьютер в проводнике папку Объемные объекты:
```
reg delete HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\MyComputer\NameSpace\{0DB7E03F-FC29-4DC6-9020-FF41B59E513A} /f
```
### Удалить все папки из компьютера в проводнике
Удаляет все папки из Этот компьютер с помощью следующих твиков реестра, работает на Windows 8 и 10:
```
reg delete HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\MyComputer\NameSpace\{088e3905-0323-4b02-9826-5d99428e115f} /f
reg delete HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\MyComputer\NameSpace\{24ad3ad4-a569-4530-98e1-ab02f9417aa8} /f
reg delete HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\MyComputer\NameSpace\{3dfdf296-dbec-4fb4-81d1-6a3438bcf4de} /f
reg delete HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\MyComputer\NameSpace\{d3162b92-9365-467a-956b-92703aca08af} /f
reg delete HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\MyComputer\NameSpace\{f86fa3ab-70d2-4fc7-9c99-fcbf05467f3a} /f
reg delete HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\MyComputer\NameSpace\{B4BFCC3A-DB2C-424C-B029-7FE99A87C641} /f
```
### Добавить компьютер на рабочий стол
Добавляет компьютер на рабочий стол с помощью следующих твиков в реестре и перезапускает проводник для применения изменений:
```
reg add "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\HideDesktopIcons\\NewStartPanel" /v "{20D04FE0-3AEA-1069-A2D8-08002B30309D}" /t REG_DWORD /d 0 /f
reg add "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\HideDesktopIcons\\ClassicStartMenu" /v "{20D04FE0-3AEA-1069-A2D8-08002B30309D}" /t REG_DWORD /d 0 /f
```
### Включить классический просмотровщик фотографий
Включает с помощью следующих твиков реестра просмотровщик фотографий из Windows 7 в Windows 10 и 11:
```
extensions = ['.jpg', '.jpeg', '.gif', '.png', '.bmp', '.tiff', '.ico']
reg add HKCU\Software\Classes\{extension} /ve /t REG_SZ /d PhotoViewer.FileAssoc.Tiff /f
```
### Установить сертификаты минцифры России
Скачивает сертификаты минцифры в %temp% из официального сайта госуслуг, и добавляет их в доверенные корневые сертификаты

### Установить goodbyedpi от замедления YouTube
Скачивает [goodbyedpi](https://github.com/ValdikSS/GoodbyeDPI) и устанавливает его согласно этой [инструкции](https://github.com/ValdikSS/GoodbyeDPI/issues/378)
