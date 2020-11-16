from dataclasses import dataclass, field
import constants
from typing import Literal


@dataclass
class DayZVersionData:
    version: str
    base_path: str = field(default=constants.data_folder)

    def __post_init__(self):
        if self.version not in constants.versions:
            raise ValueError(f"{self.version} not found")

    @property
    def path(self) -> str:
        return "/".join([self.base_path, self.version])


@dataclass
class DayZMapData(DayZVersionData):
    map: Literal["chernarus", "livonia"] = "chernarus"
    map_folder: Literal["dayzOffline.chernarusplus", "dayzOffline.enoch"] = "dayzOffline.chernarusplus"

    def __post_init__(self):
        if self.map == "livonia":
            self.map_folder = "dayzOffline.enoch"

    @property
    def path_map(self) -> str:
        return "/".join([self.path, self.map_folder])

    def path_file(self, file: str) -> str:
        return "/".join([self.path_map, file])

    @property
    def path_db(self) -> str:
        return "/".join([self.path_map, "db"])

    def path_db_file(self, file: str) -> str:
        return "/".join([self.path_db, file])

    @property
    def path_env(self) -> str:
        return "/".join([self.path_db, "env"])

    def path_env_file(self, file: str) -> str:
        return "/".join([self.path_env, file])


if __name__ == '__main__':
    data = DayZVersionData("1.10")

    data_map = DayZMapData(version="1.10", map="chernarus")
    print(data_map)
    print(data_map.path_db_file("types.xml"))
    print(data_map.path_env_file("pig_territories.xml"))
    print(data_map.path_file("db/types.xml"))

    data_map = DayZMapData(version="1.10", map="livonia")
    print(data_map)
    print(data_map.path_db_file("types.xml"))
    print(data_map.path_env_file("pig_territories.xml"))
    print(data_map.path_file("db/types.xml"))
