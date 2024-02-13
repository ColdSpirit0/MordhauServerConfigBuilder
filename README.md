# Mordhau Server Config Builder

Designed to help configuring server config, manage existing and your own mod configs.

### Table of Contents

1. [Introduction](#mordhau-server-config-builder)
1. [Functionality](#what-builder-do)
1. [Motivation](#why-i-made-builder-problems-with-editing-gameini)
1. [Benefits](#benefits)
1. [Example](#example)
1. [How to use](#how-to-use)
1. [Directory Structure](#existing-directory-structure)
1. [Sharing Templates](#how-to-share-templates-for-your-mod-or-default-template)



### What builder do:

* Searches for every *.ini file in directories and merges it to Game.Template.ini (you can specify your own directories).
* Backs up your existing Game.ini (this can be disabled).
* Copies the merged ini to Game.ini in the server's config directory.


### Why I made builder (problems with editing Game.ini):

* All configurations are in one file, which makes it hard to navigate when it is large.
* Adding a mod configuration requires editing different places in the file.
* Mods are specified by IDs, and if you use multiple mods and want to disable one temporarily, it is hard to find which ID you should remove. Additionally, you need to remove the rest of the config, such as mod-specific maps and mod init lines, which is not so easy to find.
* If you want to bring back a mod, you need to reinstall it from the beginning.
* Comments could help manage mods, but the server recreates Game.ini again and cleans it all.


### Benefits:

* You can split your config and use a single INI file for a single mod or config part.
* You can disable a mod or config part just by moving the file out of the search directory or by adding a "#" prefix to the filename.
* You can split your own mods you develop now and mods from different developers.
* You can make templates for your mod to share them with the server hosting community.
* You can write comments in your INI files.


### Example

<details>
<summary>Spoiler</summary>

#### Game. Template.ini

```ini
[/Script/Mordhau.MordhauGameMode]
bIsThirdPersonCameraDisabled=False
ConstrainAspectRatio=0.000000

[/Script/Mordhau.MordhauGameSession]
MaxSlots=8
BannedPlayers=()
MutedPlayers=()

[/Script/Engine.GameSession]
MaxPlayers=8
```

#### Default/HordeMaps.ini

```ini
[/Script/Mordhau.MordhauGameMode]
MapRotation=HRD_Crossroads
MapRotation=HRD_Castello
MapRotation=HRD_Camp
MapRotation=HRD_Grad
MapRotation=HRD_Taiga
MapRotation=HRD_MountainPeak
MapRotation=HRD_Feitoria
MapRotation=HRD_Noria
MapRotation=HRD_Dungeon
```

#### Mods/ServerSideCommands.ini

```ini
[/Script/Mordhau.MordhauGameMode]
SpawnServerActorsOnMapLoad=/ServerSideCmds/BP_ServerSideCMDs.BP_ServerSideCMDs_C

[/Script/Mordhau.MordhauGameSession]
Mods=1700790
```

#### Mods/YodaSeller.ini

```ini
[/Script/Mordhau.MordhauGameSession]
Mods=2713507

[/Script/Mordhau.MordhauGameMode]
SpawnServerActorsOnMapLoad=/YodaSeller/YodaSellerInit.YodaSellerInit_C
```

#### Game.ini output

```ini
[/Script/Mordhau.MordhauGameMode]
bIsThirdPersonCameraDisabled=False
ConstrainAspectRatio=0.000000
MapRotation=HRD_Crossroads
MapRotation=HRD_Castello
MapRotation=HRD_Camp
MapRotation=HRD_Grad
MapRotation=HRD_Taiga
MapRotation=HRD_MountainPeak
MapRotation=HRD_Feitoria
MapRotation=HRD_Noria
MapRotation=HRD_Dungeon
SpawnServerActorsOnMapLoad=/ServerSideCmds/BP_ServerSideCMDs.BP_ServerSideCMDs_C
SpawnServerActorsOnMapLoad=/YodaSeller/YodaSellerInit.YodaSellerInit_C

[/Script/Mordhau.MordhauGameSession]
MaxSlots=8
BannedPlayers=()
MutedPlayers=()
Mods=1700790
Mods=2713507

[/Script/Engine.GameSession]
MaxPlayers=8
```

</details>


### System requirements
* OS: Windows (just did not tested on linux)
* Python: 3.12


### How to use

1. Clone the project or download the archive to the directory of your choice.
1. In `Builder.ini`:
    - Specify the path to your `Game.ini` file.
    - Add or remove the `ModsDir` key-value pair to specify which directories the script will search for ini files.
1. Edit `Game.Template.ini` to use it as the base for `Game.ini`.
1. Uncomment (remove the `#` in the filename) the configs you want to include in the final config. Edit the configs if you want or add your own.
1. Run `build.bat`.
1. Check your `Game.ini` for changes.


### Existing directory structure

* `Builder.ini` - application config
* `config/Game.Template.ini` - base for your config
* `config/Backups` - backups of previous `Game.ini`
* `config/Default` - parts of vanilla config
* `config/Mods` - parts of modded config
* `config/MyMods` - parts for mods you developing now
* `config/Private` - parts you dont want to share, like server name, password, admin ids


### How to share templates for your mod (or default template)

1. Fork the project
2. Clone your fork
3. Make changes
4. Commit the changes
5. Push the changes to your fork
6. Create a pull request
