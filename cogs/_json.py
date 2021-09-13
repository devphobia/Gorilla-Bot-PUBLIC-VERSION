# imports

import json
from pathlib import Path
from discord.ext import commands

# Pega o caminho da pasta principal do programa
# Self-explanatory

def get_path():
    cwd = Path(__file__).parents[1]
    cwd = str(cwd)
    return cwd

# Lê o arquivo .json
# Self-explanatory

def read_json(filename):
    cwd = get_path()
    with open(f"{cwd}/bot_config/{filename}.json", "r") as file:
        data = json.load(file)
    return data

# Altera o arquivo .json
# Self-explanatory

def write_json(data, filename):
    cwd = get_path()
    with open(f"{cwd}/bot_config/{filename}.json", "w") as file:
        json.dump(data, file, indent=4)
        