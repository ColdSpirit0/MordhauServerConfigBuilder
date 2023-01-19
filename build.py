import os
import time
import shutil
import re
from pathlib import Path



# configparser lib is painful to use with multiple identical keys
def parse_ini(path: Path):
    text = path.read_text()

    sections = dict()
    current_section_name = None

    for line in text.splitlines():
        # ignore comments
        if line.startswith(";") or line.startswith("#"):
            continue

        # try search section
        res = re.search(r"\[(.+)\]", line)
        if res is not None:
            current_section_name = res.group(1)

            # init section if not inited
            if current_section_name not in sections:
                sections[current_section_name] = dict()

        # try get key and value
        if "=" in line:
            k, v = (x.strip() for x in line.split("="))
            values = sections[current_section_name].setdefault(k, list())
            values.append(v)

    return sections


def get_ini_text(sections):
    lines = []
    for section, data in sections.items():
        lines.append(f"[{section}]")

        for key, values in data.items():
            for item in values:
                lines.append(f"{key}={item}")
        lines.append("")
    return "\n".join(lines)


def print_ini(sections):
    print(get_ini_text(sections))


def get_ini_value(sections, section, key):
    values = get_ini_values(sections, section, key)

    if values is not None and len(values) > 0:
        return values[0]

    return None

def get_ini_values(sections, section, key):
    data = sections.get(section)
    if data is None:
        return None

    values = data.get(key)
    if values is None:
        return None

    return values

def print_error(*messages: str):
    print("Error:", *messages)


def print_warning(*messages: str):
    print("Warning:", *messages)


def search_mod_configs(path: Path):
    print()
    if not path.is_dir():
        print_warning(path, "does not exist, skiping search mods there")
        return []

    print("Searching mods in", path, "...")
    mods = path.rglob("*.ini")

    # filter mods which name starts with '#'
    selected, ignored = [], []
    for mod in mods:
        if mod.stem.startswith("#"):
            ignored.append(mod)
        else:
            selected.append(mod)

    print("Found mods:", ", ".join([f.stem for f in selected]))
    print("Ignored mods:", ", ".join([f.stem for f in ignored]))

    return selected


def validate_configs_path(path: str):
    if path is None or len(path) == 0:
        return "Failed to read ConfigsPath from Builder.ini: parameter not exists or invalid"

    if not os.path.isdir(path):
        return str(f"Directory {path} does not exist")

    return True


def main():
    # default vars
    builder_config_path = Path("Builder.ini")
    create_backups = True
    backups_path = "Backups"
    game_template_path = "Game.Template.ini"
    mods_paths = ["Mods", "MyMods"]

    # read the Builder.ini
    config = parse_ini(builder_config_path)
    configs_dir_strpath = get_ini_value(config, "DEFAULT", "ConfigsPath")

    mods_paths = [Path(p) for p in (get_ini_values(config, "DEFAULT", "ModsDir") or mods_paths)]

    validation_result = validate_configs_path(configs_dir_strpath)
    if validation_result is not True:
        print_error(validation_result)
        return
    
    if (cb := get_ini_value(config, "DEFAULT", "CreateBackups")) is not None:
        if cb.lower() == "true":
            create_backups = True
        elif cb.lower() == "false":
            create_backups = False
        else:
            print_error("Builder.ini -> CreateBackups: wrong value, need True/False")
            return


    backups_path = Path(get_ini_value(config, "DEFAULT", "BackupsPath") or backups_path)
    game_template_path = Path(get_ini_value(config, "DEFAULT", "GameTemplatePath") or game_template_path)

    game_ini_path = Path(configs_dir_strpath) / "Game.ini"

    # check for Game.Template.ini exists
    if not game_template_path.is_file():
        print_error(game_template_path,
                    "does not exist, you should create it first")
        return

    # try backup
    if create_backups:
        # if Game.ini exists - copy it to "Backup" directory: Backups/timestamp.Game.ini
        if game_ini_path.is_file():
            backups_path.mkdir(exist_ok=True)

            dest_path = backups_path / f"{int(time.time())}.Game.ini"

            print("copying", game_ini_path.name, "into", dest_path)
            shutil.copy(game_ini_path, dest_path)

    # get list of all ini's in Mods and MyMods directories
    mods = []
    for path in mods_paths:
        mods.extend(search_mod_configs(path))

    config_combined = parse_ini(game_template_path)

    for mod in mods:
        parsed = parse_ini(mod)

        for section, section_data in parsed.items():
            comb_section = config_combined.setdefault(section, dict())

            for k, v in section_data.items():
                comb_data = comb_section.setdefault(k, list())
                comb_data.extend(v)

    print()
    print("Writing to Game.ini")
    # print_ini(config_combined)
    game_ini_path.write_text(get_ini_text(config_combined))
    print("Done")


if __name__ == "__main__":
    main()
