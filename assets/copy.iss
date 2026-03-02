; ===== VaultX Installer Script =====

#define MyAppName "VaultX"
#define MyAppVersion "1.0"
#define MyAppPublisher "VaultX"
#define MyAppURL "https://www.github.com/Swarnim-Dubey"
#define MyAppExeName "main.exe"

[Setup]
AppId={{B49B2FFC-874C-45B0-8631-E073AA04B2B8}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
UninstallDisplayIcon={app}\{#MyAppExeName}
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
DisableProgramGroupPage=yes
OutputBaseFilename=VaultX_Setup
SetupIconFile=D:\Code\02_Project\Password-Manager\assets\app_icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern dark

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create Desktop Shortcut"; GroupDescription: "Additional Icons"; Flags: unchecked

[Files]
Source: "..\dist\main.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent