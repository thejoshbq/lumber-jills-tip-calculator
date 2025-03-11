[Setup]
AppName=Lumber Jill's Tip Calculator
AppVersion=1.0
DefaultDirName={autopf}\LumberJillsTipCalculator
DefaultGroupName=Lumber Jill's Tip Calculator
OutputBaseFilename=lumber-jills-tip-calculator-1.0-x64
SetupIconFile=assets\lumberjillslogo.ico
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\lumber-jills-tip-calculator\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Lumber Jill's Tip Calculator"; Filename: "{app}\lumber-jills-tip-calculator.exe"
