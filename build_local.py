import os
import sys
import shutil
import zipfile
import subprocess
from pathlib import Path

# Ensure UTF-8 output
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# Paths
ROOT_DIR = Path(__file__).parent.resolve()
DOWNLOADS_DIR = Path(r"C:\Users\akash\Downloads")
BUILD_DIR = ROOT_DIR / "build_output"
SCRATCH_DIR = ROOT_DIR / "scratch"
PATCHES_MPP = ROOT_DIR / "patches" / "patches.mpp"
MORPHE_JAR = Path(r"C:\Users\akash\Downloads\Project\Morphe\morphe-desktop-1.15.0-dev.2-all.jar")
STOCK_APK = DOWNLOADS_DIR / "BraveMonoarm64.apk"
OUTPUT_ZIP = DOWNLOADS_DIR / "BraveNightly-Root-Magisk-Module.zip"

def main():
    print("==================================================")
    print("  Brave Nightly Origin Root Module Local Builder  ")
    print("==================================================")

    # 1. Verify Stock APK exists or download
    if not STOCK_APK.exists():
        print(f"[1/5] Stock APK not found at {STOCK_APK}. Downloading latest from GitHub...")
        subprocess.run(["gh", "release", "download", "--repo", "brave/brave-browser", "--pattern", "BraveMonoarm64.apk", "--dir", str(DOWNLOADS_DIR)], check=True)
    else:
        print(f"[1/5] Found stock APK: {STOCK_APK} ({round(STOCK_APK.stat().st_size / (1024*1024), 2)} MB)")

    # 2. Setup build directory
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    MODULE_DIR = BUILD_DIR / "magisk-module"
    if MODULE_DIR.exists():
        shutil.rmtree(MODULE_DIR)
    MODULE_DIR.mkdir(parents=True, exist_ok=True)
    (MODULE_DIR / "META-INF" / "com" / "google" / "android").mkdir(parents=True, exist_ok=True)

    # 3. Patch APK with Morphe in --unsigned mode
    patched_apk = MODULE_DIR / "base.apk"
    print(f"[2/5] Patching BraveMonoarm64.apk with Morphe (mode: --unsigned)...")
    cmd = [
        "java", "-jar", str(MORPHE_JAR), "patch",
        f"-p={PATCHES_MPP}",
        "-e=Brave Origin",
        "-f",
        "--unsigned",
        f"-o={patched_apk}",
        str(STOCK_APK)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0 or not patched_apk.exists():
        print(f"Error during patching:\n{res.stdout}\n{res.stderr}")
        sys.exit(1)
    print(f"[OK] Successfully patched base.apk ({round(patched_apk.stat().st_size / (1024*1024), 2)} MB)")

    # 4. Generate Module Prop, Scripts and Metadata
    print("[3/5] Generating Magisk module metadata & scripts...")
    
    # module.prop
    (MODULE_DIR / "module.prop").write_text(
        "id=brave-nightly-origin\n"
        "name=Brave Nightly Origin (All-in-One Root)\n"
        "version=v1.96.42\n"
        "versionCode=20260905\n"
        "author=Akash\n"
        "description=All-in-One Magisk/KernelSU Module: Automatically mounts patched Brave Nightly with Brave Origin unlocked and preserves official signature.\n"
        "updateJson=https://raw.githubusercontent.com/Akash-Sriram/brave-nightly-patches/main/update.json\n",
        encoding="utf-8"
    )

    # customize.sh
    (MODULE_DIR / "customize.sh").write_text(
        'ui_print "************************************************"\n'
        'ui_print "*   Brave Nightly Origin All-in-One Installer  *"\n'
        'ui_print "************************************************"\n'
        'ui_print "- Configuring Brave Nightly Root Module..."\n\n'
        'PKG="com.brave.browser_nightly"\n'
        'APK_PATH=$(pm path $PKG 2>/dev/null | grep base.apk | head -n 1 | cut -d: -f2)\n\n'
        'if [ -n "$APK_PATH" ]; then\n'
        '    APP_DIR=$(dirname "$APK_PATH")\n'
        '    if [ -f "$APP_DIR/split_chrome.apk" ]; then\n'
        '        ui_print "- Cleaning conflicting Play Store split APKs..."\n'
        '        rm -f "$APP_DIR"/split_* "$APP_DIR"/oat/*/split_* 2>/dev/null\n'
        '    fi\n'
        'fi\n\n'
        'ui_print "- Setting permissions..."\n'
        'set_perm_recursive "$MODPATH" 0 0 0755 0644\n'
        'set_perm "$MODPATH/service.sh" 0 0 0755\n'
        'ui_print "✔ Installation complete! Reboot to activate mount."\n',
        encoding="utf-8"
    )

    # service.sh
    (MODULE_DIR / "service.sh").write_text(
        '#!/system/bin/sh\n'
        'MODDIR=${0%/*}\n'
        'PKG="com.brave.browser_nightly"\n\n'
        'while [ "$(getprop sys.boot_completed)" != "1" ]; do\n'
        '    sleep 1\n'
        'done\n\n'
        'APK_PATH=$(pm path $PKG 2>/dev/null | grep base.apk | head -n 1 | cut -d: -f2)\n'
        'if [ -n "$APK_PATH" ] && [ -f "$MODDIR/base.apk" ]; then\n'
        '    APP_DIR=$(dirname "$APK_PATH")\n'
        '    rm -f "$APP_DIR"/split_* "$APP_DIR"/oat/*/split_* 2>/dev/null\n'
        '    mount -o bind "$MODDIR/base.apk" "$APK_PATH"\n'
        '    chcon u:object_r:apk_data_file:s0 "$APK_PATH"\n'
        'fi\n',
        encoding="utf-8"
    )

    # updater-script
    (MODULE_DIR / "META-INF" / "com" / "google" / "android" / "updater-script").write_text("#MAGISK\n", encoding="utf-8")

    # update-binary
    (MODULE_DIR / "META-INF" / "com" / "google" / "android" / "update-binary").write_text(
        '#!/sbin/sh\n'
        'OUTFD=$2\n'
        'ZIPFILE=$3\n'
        'mount /data 2>/dev/null\n'
        'exec $(magisk --path)/magiskboot --unpack-zip "$ZIPFILE" customize.sh "$OUTFD"\n',
        encoding="utf-8"
    )

    # 5. Compress into ZIP using ZIP_STORED (No compression to avoid Magisk unzip memory/inflate error)
    print(f"[4/5] Packaging Magisk Module ZIP (ZIP_STORED) -> {OUTPUT_ZIP}...")
    with zipfile.ZipFile(OUTPUT_ZIP, 'w', zipfile.ZIP_STORED) as z:
        for root, dirs, files in os.walk(MODULE_DIR):
            for f in files:
                full = Path(root) / f
                rel = full.relative_to(MODULE_DIR)
                z.write(full, rel)
    print(f"[OK] Module ZIP created successfully: {OUTPUT_ZIP} ({round(OUTPUT_ZIP.stat().st_size / (1024*1024), 2)} MB)")

    # 6. Check ADB Device
    print("[5/5] Checking connected Android devices via ADB...")
    adb_res = subprocess.run(["adb", "devices"], capture_output=True, text=True)
    if "device\n" in adb_res.stdout or "\tdevice" in adb_res.stdout:
        print("[OK] Connected device detected. Transferring module to /sdcard/Download/...")
        subprocess.run(["adb", "push", str(OUTPUT_ZIP), "/sdcard/Download/BraveNightly-Root-Magisk-Module.zip"], check=True)
        print("[OK] Transferred to /sdcard/Download/BraveNightly-Root-Magisk-Module.zip on your phone!")
    else:
        print("[INFO] No ADB device connected. You can copy the ZIP manually from your Downloads folder.")

    print("\n==================================================")
    print("  BUILD COMPLETE! Ready to flash in Magisk/KernelSU ")
    print("==================================================")

if __name__ == "__main__":
    main()
