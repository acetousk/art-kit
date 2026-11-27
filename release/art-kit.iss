; Windows installer for Art Kit. release/build.py runs: ISCC /DVersion=x.y.z /DStage=<folder> art-kit.iss
; One install in Program Files\Art Kit: Art Kit, Krita, Blender, Sweet Home 3D. One uninstaller for all.
[Setup]
AppId=org.artkit.ArtKit
AppName=Art Kit
AppVersion={#Version}
AppPublisher=Art Kit
AppPublisherURL=https://github.com/acetousk/art-kit
DefaultDirName={autopf}\Art Kit
DefaultGroupName=Art Kit
DisableProgramGroupPage=yes
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
UninstallDisplayIcon={app}\Art Kit.exe
OutputBaseFilename=ArtKit-Setup-{#Version}
Compression=lzma2
SolidCompression=yes
WizardStyle=modern

[Tasks]
Name: desktopicon; Description: "Make a desktop icon for Art Kit"

[Files]
Source: "{#Stage}\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs ignoreversion
Source: "{#WebView2}"; DestDir: "{tmp}"; Flags: deleteafterinstall; Check: NoWebView2

[Icons]
Name: "{group}\Art Kit"; Filename: "{app}\Art Kit.exe"
Name: "{group}\Krita"; Filename: "{app}\Krita\bin\krita.exe"
Name: "{group}\Sweet Home 3D"; Filename: "{app}\Art Kit.exe"; Parameters: "--open ""Sweet Home 3D"""; IconFilename: "{app}\Sweet Home 3D\SweetHome3D.exe"
Name: "{group}\Blender"; Filename: "{app}\Blender\blender-launcher.exe"
Name: "{group}\Uninstall Art Kit"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Art Kit"; Filename: "{app}\Art Kit.exe"; Tasks: desktopicon

[Run]
; Art Kit shows its window with Microsoft Edge WebView2 (Windows 11 has it; some Windows 10 do not).
Filename: "{tmp}\MicrosoftEdgeWebview2Setup.exe"; Parameters: "/silent /install"; StatusMsg: "Installing Microsoft Edge WebView2..."; Check: NoWebView2
Filename: "{app}\Art Kit.exe"; Description: "Open Art Kit and get the books and pictures"; Flags: nowait postinstall skipifsilent

[Code]
// WebView2 is there if its "pv" version is set and not 0.0.0.0 (Microsoft's check, per machine or per user).
function NoWebView2: Boolean;
var v: String;
begin
  Result := not ((RegQueryStringValue(HKLM, 'SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}', 'pv', v) or
                  RegQueryStringValue(HKCU, 'Software\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}', 'pv', v))
                 and (v <> '') and (v <> '0.0.0.0'));
end;
