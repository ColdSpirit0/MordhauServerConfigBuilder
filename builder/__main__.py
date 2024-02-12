from pathlib import Path
import shutil
import time

from .ini_parser import IniParser
from .config import Config

from .print_extra import print_warning, print_error
from .exceptions import ValidationError


def validate_file_exists(path: Path):
    # parent directory should be created
    if not path.is_file():
        raise ValidationError(f"File {path} does not exist")


def validate_dir_exists(path: Path):
    # parent directory should be created
    if not path.is_dir():
        raise ValidationError(f"Directory {path} does not exist")


def validate_can_create_file(path: Path):
    # should not be existing directory
    if path.is_dir():
        raise ValidationError(
            f"Provided path ({path}) is existing directory, cannot create file with same name")

    # parent directory should be created
    validate_dir_exists(path.parent)


def search_config_files(path: Path):
    print()
    if not path.is_dir():
        print_warning("Directory", path, "does not exist, skiping search configs there")
        return []

    print("Searching configs in", path, "...")
    config_files = path.rglob("*.ini")

    # filter configs which name starts with '#'
    selected, ignored = [], []
    for config_file in config_files:
        if config_file.stem.startswith("#"):
            ignored.append(config_file)
        else:
            selected.append(config_file)

    print("Found configs:", ", ".join([f.stem for f in selected]))

    return selected


def main():
    config = Config()

    try:
        config.read_ini()
        # print("\n".join([f"{k}={v}" for k, v in config.__dict__.items()]))
    except FileNotFoundError:
        print_error(
            f"File {config.builder_config_path} not found, exitting...")
        return

    # validate config paths
    validate_can_create_file(config.output_file_path)
    validate_file_exists(config.game_template_path)

    # try backup
    if config.create_backups:
        validate_dir_exists(config.backups_path.parent)

        # if output file exists - copy it to "Backups" directory: Backups/<timestamp>.<name>
        if config.output_file_path.is_file():
            config.backups_path.mkdir(exist_ok=True)

            dest_path = config.backups_path / f"{int(time.time())}.Game.ini"

            print("Copying", config.output_file_path.name, "into", dest_path)
            shutil.copy(config.output_file_path, dest_path)

    # combine all config files from different dirs in one list
    config_files = []
    for path in config.load_paths:
        config_files.extend(search_config_files(path))

    # read config parts into one scheme
    # parser = IniParser()
    # parser.read(config.game_template_path)
    # for config_file in config_files:
    #     parser.read(config_file)

    # parsers: list[IniParser] = []

    parser_combined = IniParser()
    parser_combined.read(config.game_template_path)

    for config_file in config_files:
        parser = IniParser()
        parser.read(config_file)
        parser_combined.extend(parser)

    # check if all requirements satisfied
    if len(parser_combined.requirements) > 0:
        strpaths = map(str, parser_combined.requirements)
        raise FileNotFoundError(f"Required config files [{', '.join(strpaths)}] are not loaded")


    print()
    print("Writing result to", config.output_file_path)
    # print_ini(config_combined)
    config.output_file_path.write_text(parser_combined.get_ini_text())
    print("Done")


if __name__ == "__main__":
    main()
