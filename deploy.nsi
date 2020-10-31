;NSIS Modern User Interface
;Start Menu Folder Selection Example Script
;Written by Joost Verburg

;--------------------------------
;Include Modern UI

  !include "MUI2.nsh"

;--------------------------------
;General

  ;Name and file
  Name "Sagheb"
  OutFile "Sagheb-1.0-setup.exe"

  ;Default installation folder
  InstallDir "$PROGRAMFILES\Sagheb-1.0"
  
  ;Get installation folder from registry if available
  InstallDirRegKey HKCU "Software\Sagheb" ""

  ;Request application privileges for Windows Vista
  RequestExecutionLevel user

;--------------------------------
;Variables

  Var StartMenuFolder

;--------------------------------
;Interface Settings

!define MUI_ABORTWARNING
;!define MUI_ICON "F:\Pictures\2000px_tensorflow_logo_svg_1__V7d_icon.ico"
!define MUI_ICON "E:\Downloads\compassfinallarge_bQw_icon.ico"
!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_BITMAP "E:\Downloads\compass-rose-303605_960_720.bmp"
!define MUI_HEADERIMAGE_RIGHT
;--------------------------------
;Pages

  !insertmacro MUI_PAGE_LICENSE "F:\apps\startup\kasr\deploying\License.txt"
  !insertmacro MUI_PAGE_COMPONENTS
  !insertmacro MUI_PAGE_DIRECTORY
  
  ;Start Menu Folder Page Configuration
  !define MUI_STARTMENUPAGE_REGISTRY_ROOT "HKCU" 
  !define MUI_STARTMENUPAGE_REGISTRY_KEY "Software\Sagheb" 
  !define MUI_STARTMENUPAGE_REGISTRY_VALUENAME "Start Menu Folder"
  
  !insertmacro MUI_PAGE_STARTMENU Application $StartMenuFolder
  
  !insertmacro MUI_PAGE_INSTFILES
  
  !insertmacro MUI_UNPAGE_CONFIRM
  !insertmacro MUI_UNPAGE_INSTFILES

;--------------------------------
;Languages
 
  !insertmacro MUI_LANGUAGE "English"

;--------------------------------
;Installer Sections

Section "core" 

  SetOutPath "$INSTDIR"
  
  ;ADD YOUR OWN FILES HERE...
  ; Put file there
  File /r  /x *.nc  "app\*"
  ;File /r "\*"
  
  ;Store installation folder
  WriteRegStr HKCU "Software\Sagheb" "" $INSTDIR
  
  ;Create uninstaller
  WriteUninstaller "$INSTDIR\Uninstall.exe"
  
  !insertmacro MUI_STARTMENU_WRITE_BEGIN Application
    
    ;Create shortcuts
    CreateDirectory "$SMPROGRAMS\$StartMenuFolder"
    CreateShortcut "$SMPROGRAMS\$StartMenuFolder\Sagheb.lnk" "$INSTDIR\Sagheb.exe"
    CreateShortcut "$SMPROGRAMS\$StartMenuFolder\Uninstall.lnk" "$INSTDIR\Uninstall.exe"
	CreateShortcut "$desktop\Sagheb.lnk" "$INSTDIR\Sagheb.exe"
  
  !insertmacro MUI_STARTMENU_WRITE_END

SectionEnd

;--------------------------------
;Descriptions

  ;Language strings
 ; LangString DESC_SecDummy ${LANG_ENGLISH} "A test section."

  ;Assign language strings to sections
  ;!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
   ; !insertmacro MUI_DESCRIPTION_TEXT ${SecDummy} $(DESC_SecDummy)
 ; !insertmacro MUI_FUNCTION_DESCRIPTION_END
 
;--------------------------------
;Uninstaller Section

Section "Uninstall"
  ;ADD YOUR OWN FILES HERE...

  Delete "$INSTDIR\Uninstall.exe"
  
  Delete   "$desktop\Sagheb.lnk"

  RMDir /r  "$INSTDIR"
  
  !insertmacro MUI_STARTMENU_GETFOLDER Application $StartMenuFolder
    
  Delete "$SMPROGRAMS\$StartMenuFolder\Uninstall.lnk"
  Delete "$SMPROGRAMS\$StartMenuFolder\Sagheb.lnk"
  RMDir "$SMPROGRAMS\$StartMenuFolder"

  DeleteRegKey /ifempty HKCU "Software\Sagheb"

SectionEnd




