# Brave Nightly Origin Patches

Automated build and patch pipeline for **Brave Nightly Android (`arm64-v8a`)** using Morphe patcher.

## Features
* **Brave Origin Unlocked**: Enables Origin preference switches, subscription active state, and origin preferences in Brave Nightly.
* **Dual Release Architecture**:
  * **Non-Root**: Standalone signed APK (`BraveNightly-arm64-patched.apk`).
  * **Root**: Flashable Magisk / KernelSU / APatch Module ZIP (`BraveNightly-Root-Magisk-Module.zip`).

---

## Installation Guide

### Option 1: Root Users (Magisk / KernelSU / APatch) - Recommended
Retains Brave's official signature, automatic updates compatibility, and seamless sync.

1. Download and install the official stock **`BraveMonoarm64.apk`** from [Brave Browser Releases](https://github.com/brave/brave-browser/releases).
2. Download **`BraveNightly-Root-Magisk-Module.zip`** from the [Releases](https://github.com/) section of this repository.
3. Open **Magisk / KernelSU / APatch Manager** $\rightarrow$ **Modules** $\rightarrow$ **Install from storage**.
4. Select `BraveNightly-Root-Magisk-Module.zip` and flash it.
5. Reboot your device.

---

### Option 2: Non-Root Users
1. Download **`BraveNightly-arm64-patched.apk`** from the [Releases](https://github.com/) section.
2. Sideload and install the APK directly on your device.

---

## Automated CI/CD Workflow
The repository includes a GitHub Actions workflow (`.github/workflows/build-brave-nightly.yml`) that:
* Polls and fetches the latest Brave Nightly release from `brave/brave-browser`.
* Downloads `BraveMonoarm64.apk`.
* Compiles the patch bytecode bundle.
* Automatically generates and attaches both the Non-Root APK and the Root Magisk Module ZIP to GitHub Releases.

---

## Local Development & Building

### Prerequisites
* Java 21+
* Android SDK (`build-tools`, `platforms;android-34`)
* Morphe CLI (`morphe-desktop`)

### Build Patches
```bash
./gradlew :patches:buildAndroid
```

### Apply Patch Manually
```bash
java -jar morphe-desktop.jar patch \
  -p="patches/build/libs/patches-*.mpp" \
  -e="Brave Origin" \
  -f \
  -o="BraveNightly-patched.apk" \
  "BraveMonoarm64.apk"
```
