ui_print "************************************************"
ui_print "*   Brave Nightly Origin All-in-One Installer  *"
ui_print "************************************************"
ui_print "- Installing Brave Nightly as System Browser Overlay..."

PKG="com.brave.browser_nightly"
APK_PATH=$(pm path $PKG 2>/dev/null | grep base.apk | head -n 1 | cut -d: -f2)

if [ -n "$APK_PATH" ]; then
    APP_DIR=$(dirname "$APK_PATH")
    if [ -f "$APP_DIR/split_chrome.apk" ]; then
        ui_print "- Cleaning conflicting Play Store split APKs..."
        rm -f "$APP_DIR"/split_* "$APP_DIR"/oat/*/split_* 2>/dev/null
    fi
fi

ui_print "- Setting system app permissions..."
set_perm_recursive "$MODPATH/system" 0 0 0755 0644
set_perm_recursive "$MODPATH" 0 0 0755 0644
set_perm "$MODPATH/service.sh" 0 0 0755
ui_print "✔ Installation complete! Reboot to activate browser."
