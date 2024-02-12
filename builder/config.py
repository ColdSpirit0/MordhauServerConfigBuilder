from pathlib import Path
from .ini_parser import IniParser


class Config():
    # defaults
    builder_config_path = Path("Builder.ini")
    backups_path = Path("Backups")
    game_template_path = Path("configs/Game.Template.ini")

    load_paths = []
    create_backups = True

    def read_ini(self) -> None:
        parser = IniParser()
        parser.read(self.builder_config_path)

        self.output_file_path = parser.get_value("DEFAULT", "OutputFile", Path)

        self.load_paths = parser.get_values("DEFAULT", "LoadDir", Path, self.load_paths)
        self.create_backups = parser.get_value("DEFAULT", "CreateBackups", bool, self.create_backups)
        self.backups_path = parser.get_value("DEFAULT", "BackupsPath", Path, self.backups_path)
        self.game_template_path = parser.get_value("DEFAULT", "GameTemplatePath", Path, self.game_template_path)
