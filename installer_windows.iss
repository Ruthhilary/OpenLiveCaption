; Inno Setup Script for OpenLiveCaption
; Creates Windows installer with uninstaller

#define MyAppName "OpenLiveCaption"
#define MyAppVersion "2.0.0"
#define MyAppPublisher "OpenLiveCaption Team"
#define MyAppURL "https://github.com/yourusername/openlivecaption"
#define MyAppExeName "OpenLiveCaption.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
AppId={{8A9B3C4D-5E6F-7A8B-9C0D-1E2F3A4B5C6D}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=LICENSE.txt
OutputDir=dist\installer
OutputBaseFilename=OpenLiveCaption-{#MyAppVersion}-Windows-Setup
SetupIconFile=assets\icon.ico
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
PrivilegesRequired=admin
UninstallDisplayIcon={app}\{#MyAppExeName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "LICENSE.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md.txt"; DestDir: "{app}"; Flags: ignoreversion; DestName: "README.txt"

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{userappdata}\OpenLiveCaption"

[Code]
function InitializeSetup(): Boolean;
var
  ResultCode: Integer;
begin
  Result := True;
  
  // Check if application is running
  if CheckForMutexes('OpenLiveCaptionMutex') then
  begin
    if MsgBox('OpenLiveCaption is currently running. Please close it before continuing installation.', mbError, MB_OKCANCEL) = IDOK then
    begin
      Result := False;
    end;
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Create config directory
    CreateDir(ExpandConstant('{userappdata}\OpenLiveCaption'));
  end;
end;

function InitializeUninstall(): Boolean;
begin
  Result := True;
  
  // Check if application is running
  if CheckForMutexes('OpenLiveCaptionMutex') then
  begin
    if MsgBox('OpenLiveCaption is currently running. Please close it before continuing uninstallation.', mbError, MB_OKCANCEL) = IDOK then
    begin
      Result := False;
    end;
  end;
end;
