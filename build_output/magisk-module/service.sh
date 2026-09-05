#!/system/bin/sh
MODDIR=${0%/*}
PKG="com.brave.browser_nightly"

while [ "$(getprop sys.boot_completed)" != "1" ]; do
    sleep 1
done

# If user installed from Play Store, mount patched base over it
APK_PATH=$(pm path $PKG 2>/dev/null | grep "/data/app" | grep base.apk | head -n 1 | cut -d: -f2)
if [ -n "$APK_PATH" ] && [ -f "$MODDIR/base.apk" ]; then
    APP_DIR=$(dirname "$APK_PATH")
    rm -f "$APP_DIR"/split_* "$APP_DIR"/oat/*/split_* 2>/dev/null
    mount -o bind "$MODDIR/base.apk" "$APK_PATH"
    chcon u:object_r:apk_data_file:s0 "$APK_PATH"
fi
