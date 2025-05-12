[Setup]
AppName=File Compare
AppVersion=2.0
DefaultDirName={pf}\FileCompare
DefaultGroupName=File Compare
OutputDir=.
OutputBaseFilename=FileCompareSetup
Compression=lzma2
SolidCompression=yes
SetupIconFile=..\build\app_icon.ico

[Files]
Source: "..\build\file_compare.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\build\app_icon.ico"; DestDir: "{app}"; Flags: ignoreversion

Source: "..\resources\config.ini"; DestDir: "{app}\resources"; Flags: ignoreversion

Source: "..\resources\icons\*"; DestDir: "{app}\resources\icons"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\resources\themes\*"; DestDir: "{app}\resources\themes"; Flags: ignoreversion recursesubdirs createallsubdirs

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:"

[Icons]
Name: "{group}\File Compare"; Filename: "{app}\file_compare.exe"; IconFilename: "{app}\app_icon.ico"
Name: "{commondesktop}\File Compare"; Filename: "{app}\file_compare.exe"; IconFilename: "{app}\app_icon.ico"; Tasks: desktopicon

[Run]
Filename: "{app}\file_compare.exe"; Description: "Launch File Compare"; Flags: nowait postinstall skipifsilent