# Tingting Heartbeat / 心动婷婷

<p align="center">
  <img src="assets/tingting-heartbeat-icon.png" width="160" alt="Tingting Heartbeat icon">
</p>

<p align="center">
  A warm, interactive Windows desktop companion with touch reactions, activities, feeding, gifts, achievements, statistics, and optional AI chat.
</p>

<p align="center">
  <a href="README.zh-CN.md">简体中文</a> ·
  <a href="#download">Download</a> ·
  <a href="#privacy-and-local-data">Privacy</a> ·
  <a href="#license">License</a>
</p>

## Highlights

- Transparent, always-on-top desktop character that can be dragged around the screen.
- Different reactions for touching the hair, face, chest, arms, and dress, with varied dialogue and facial expressions.
- 28 character actions, including waving, dancing, working, thinking, sleeping, and celebrating.
- Natural idle sleep after five minutes without interaction.
- Feeding system with 20 dishes, including water spinach, poached shrimp, and beef.
- Gifts, recovery items, coins, offline rewards, inventory, mood, hunger, and energy.
- 37 achievements with claimable coin rewards.
- Companion-time, idle-time, touch, chat, feeding, gift, coin, and preference statistics.
- Optional OpenAI-compatible AI chat configured from the settings screen.
- Simplified Chinese and English interfaces.
- Adjustable character size and a custom heart-shaped pointer.
- Installer upgrades preserve local game data.

## Download

Download the latest Windows installer from the repository's **Releases** page.

The installer supports in-place upgrades. Save data is stored separately in:

```text
%APPDATA%\TingtingDesktopPet
```

Installing a newer version or using the standard uninstaller does not delete this folder.

## Controls

- Drag with the left mouse button: move Tingting.
- Click different body areas: trigger area-specific reactions.
- Double-click: open chat.
- Right-click: open the feature center.
- Hide or close the character: restore it from the system tray.

## AI chat

Open **Settings** and enter an API base URL, model name, and API key. The application accepts OpenAI-compatible endpoints.

The API key is never bundled into shared builds. On Windows it is stored locally using DPAPI encryption tied to the current user account. Without an API key, the chat window still offers a small set of offline responses.

## Privacy and local data

All game progress is stored locally. The build process rejects packaged `state.json` files and API-key-like source strings to reduce the risk of accidentally publishing personal data.

Before sharing a build, use the files produced in `release/`; do not copy your `%APPDATA%\TingtingDesktopPet` directory.

## Build from source

Requirements:

- Windows 10 or later
- Python 3.12+
- PowerShell
- Inno Setup 6 for the installer

Build the portable executable:

```powershell
.\build.ps1
```

Build the installer:

```powershell
.\build-installer.ps1 -Version 1.4.0
```

Run tests:

```powershell
python -m unittest discover -s tests -p "test_core.py"
python tests\gui_smoke.py
python tests\startup_splash_smoke.py
```

## License

The source code is licensed under the [MIT License](LICENSE).

The Tingting character likeness, sprite sheet, portraits, icons, and other character artwork are **not** covered by the MIT License. They are provided under the separate [Character Assets License](ASSETS_LICENSE.md), which permits personal, non-commercial use with this project but prohibits unauthorized commercial use or standalone redistribution.

This split keeps the code easy to study and reuse while protecting the personal character identity and artwork.
