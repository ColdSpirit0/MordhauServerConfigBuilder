# Mordhau Server Config Builder

Designed to help configuring server config, manage existing and your own mod configs.

#### Problem with editing Game.ini:
* All config in one file, when it big, it's hard to navigate.
* To add mod, you should edit different places in the file.
* Mods specified by ids, and if you use multiple mods, and want to disable one mod temporary, it hard to find which one id you should remove. Also need to remove rest of config, like mod specific maps, mod init lines, and it is not so easy to find it too.
* If you want return back mod again - you need install it from beginning.
* Comments could help to manage mods, but server recreates Game.ini again and clean it all.

#### What builder do:
* Searching for every *.ini file in directories and merges it to Game.Template.ini (you can specify your own directories).
* Do backup of your existing Game.ini (can be disabled).
* Copies merged ini to Game.ini.

#### Profit:
* You can split your config and use single ini file for single mod or config part.
* You can disable mod or config part just by moving file out of search directory or by adding prefix "#" in filename.
* You can split your own mods you develop now and mods from different devs.
* You can make templates for your mod to share it with server hosters community.
* You can write comments in your ini files.

### Example

<details>
<summary>Spoiler</summary>

#### Game.Template.ini
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

#### Default/HordeMaps.ini
```ini
[/Script/Mordhau.MordhauGameMode]
SpawnServerActorsOnMapLoad=/ServerSideCmds/BP_ServerSideCMDs.BP_ServerSideCMDs_C

[/Script/Mordhau.MordhauGameSession]
Mods=1700790
```

#### Default/HordeMaps.ini
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

### How to use
1. Clone project or download archive to directory you like.
1. In Builder.ini specify path to your "Game.ini" directory.
1. Add or remove ModsDir, to specify which directories script will search ini files.
1. Edit Game.Template.ini to make it base for Game.ini
1. Copy from Templates to Mods/Default (or dir you specified) configs you want to include to your config. Edit copied configs if you want.
1. Run build.bat
1. Check your Game.ini for changes.

### Existing directory structure
* Backups - backups of Game.ini
* Default - included parts of no modded config
* Mods - included parts of modded config
* Templates - not included parts for Mods and Default directories
* MyMods - parts for mods you developing now
* Private - parts you dont want to share, like server name, password
* Builder.ini - builder config
* Game.Template.ini - base for your config

### How to share templates for my mod (or default)
1. Make fork of project
1. Clone your project
1. Do changes
1. Commit
1. Push
1. Make pull request