#ifndef MyAppVersion
#define MyAppVersion "1.6.2"
#endif

#define MyAppName "心动婷婷"
#define MyAppEnglishName "Tingting Heartbeat"
#define MyAppExeName "TingtingHeartbeat.exe"

[Setup]
AppId={{6E3D0C81-6DD6-42F8-94D4-C90FD24C8A31}
AppName={#MyAppName} / {#MyAppEnglishName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} / {#MyAppEnglishName} {#MyAppVersion}
AppPublisher=Tingting Heartbeat
DefaultDirName={localappdata}\Programs\TingtingHeartbeat
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputDir=release
OutputBaseFilename=TingtingHeartbeat-Setup-v{#MyAppVersion}
SetupIconFile=assets\tingting.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
MinVersion=10.0
CloseApplications=yes
RestartApplications=no
AppMutex=Local\TingtingHeartbeat-83A938C3
UsePreviousAppDir=yes
UsePreviousTasks=yes
VersionInfoVersion={#MyAppVersion}
VersionInfoProductName={#MyAppName} / {#MyAppEnglishName}
VersionInfoDescription={#MyAppEnglishName} Installer

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut / 创建桌面快捷方式"; GroupDescription: "Shortcuts / 快捷方式"; Flags: unchecked

[Files]
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.zh-CN.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "CHANGELOG.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch {#MyAppName} / 启动心动婷婷"; Flags: nowait postinstall skipifsilent

; User data intentionally remains in %APPDATA%\TingtingDesktopPet.
; No [UninstallDelete] entry targets that directory, so upgrades and uninstall preserve it.
