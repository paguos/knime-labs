import requests

import pandas as pd
import tempfile as tpf

from config import PenguinGender, PenguinSpecies


class PenguinStep:

    BASE_URL = "https://portal.edirepository.org/nis/dataviewer?packageid="

    URI_ADELIE = BASE_URL + \
        "knb-lter-pal.219.3&entityid=002f3893385f710df69eeebe893144ff"
    URI_CHINSTRAP = BASE_URL + \
        "knb-lter-pal.221.2&entityid=fe853aa8f7a59aa84cdd3197619ef462"
    URI_GENTOO = BASE_URL + \
        "knb-lter-pal.220.3&entityid=e03b43c924f226486f2f0ab6709d2381"

    def __init__(self, **kwargs) -> None:
        self.gender = PenguinGender[kwargs["gender"]]
        self.species = PenguinSpecies[kwargs["species"]]

    def execute(self):
        if (self.species == PenguinSpecies.ALL):
            df = self.__load_data(PenguinSpecies.ADELIE)
            df = pd.concat([df, self.__load_data(
                PenguinSpecies.CHINSTRAP)], ignore_index=True)
            df = pd.concat([df, self.__load_data(
                PenguinSpecies.GENTOO)], ignore_index=True)
        else:
            df = self.__load_data(self.species)

        if (self.gender != PenguinGender.ALL):
            df = df[df["Sex"] == self.gender.name]

        return df

    def __load_data(self, species):
        if species == PenguinSpecies.ADELIE:
            uri = self.URI_ADELIE
        elif species == PenguinSpecies.CHINSTRAP:
            uri = self.URI_CHINSTRAP
        elif species == PenguinSpecies.GENTOO:
            uri = self.URI_GENTOO

        response = requests.get(uri)
        with tpf.TemporaryFile() as file:
            file.write(response.content)
            file.seek(0)
            return pd.read_csv(file)
