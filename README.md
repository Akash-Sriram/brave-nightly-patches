# Brave Nightly Origin Patches

Automated build, patch, and release pipeline for **Brave Nightly Android (`arm64-v8a`)** powered by Morphe bytecode patching.

---

## 🚀 Features

* **Brave Origin Unlocked**: Full access to Origin flags, subscription toggles, and premium origin preference switches.
* **Dual Release Distribution**:
  * **Root Users (Magisk / KernelSU / APatch)**: Built-in system app overlay with authentic official release signatures (Passkeys, WebAuthn & Autofill fully functional).
  * **Non-Root Users**: Standalone signed APK (`BraveNightly-arm64-patched.apk`).
* **In-App Magisk Updates**: Module includes `updateJson` to notify and update directly inside Magisk / KernelSU / MMRL.
* **Automated CI/CD**: Checks for new official Brave Nightly releases every 6 hours and automatically publishes updated releases.

---

## 📥 Downloads & Installation

### 1. Root Users (Magisk / KernelSU / APatch) — Recommended

> **No stock APK required beforehand.** The module includes a complete system app overlay (`system/app/BraveNightly/BraveNightly.apk`) that Android registers as a built-in system browser on boot.

1. Download **[`BraveNightly-Root-Magisk-Module.zip`](https://github.com/Akash-Sriram/brave-nightly-patches/releases/latest/download/BraveNightly-Root-Magisk-Module.zip)** from the [Latest Release](https://github.com/Akash-Sriram/brave-nightly-patches/releases/latest).
2. Open **Magisk / KernelSU / APatch Manager** $\rightarrow$ **Modules** $\rightarrow$ **Install from storage**.
3. Select `BraveNightly-Root-Magisk-Module.zip` and flash it.
4. **Reboot** your device.

#### 💡 Future Updates for Root Users:
* When a new update is released, simply open **Magisk Manager** $\rightarrow$ **Modules** $\rightarrow$ tap **Update** $\rightarrow$ **Reboot**.

---

### 2. Non-Root Users (Standalone APK)

1. Download **[`BraveNightly-arm64-patched.apk`](https://github.com/Akash-Sriram/brave-nightly-patches/releases/latest/download/BraveNightly-arm64-patched.apk)**.
2. Sideload and install the APK directly on your device.

---

## 🛠️ Local Building

An all-in-one local build script is provided to patch and package the module locally on your PC:

### Quick Local Build:
```powershell
python build_local.py
```

`build_local.py` automatically:
1. Downloads the official `BraveMonoarm64.apk` from Brave's releases.
2. Applies the Brave Origin patch with Morphe in `--unsigned` mode.
3. Packages the uncompressed (`STORED`) Magisk module ZIP.
4. Automatically transfers the ZIP to `/sdcard/Download/` if your Android device is connected via ADB.

---

## 🔄 Automated CI/CD Workflow

The GitHub Actions workflow ([`.github/workflows/build-brave-nightly.yml`](.github/workflows/build-brave-nightly.yml)) runs on a 6-hour cron schedule:
1. Detects new release tags on `brave/brave-browser`.
2. Compiles patches and builds both Root & Non-Root artifacts.
3. Automatically updates `update.json` and publishes a new GitHub Release with SHA-256 checksums.

---

## 📜 License
GPL-3.0 License.
