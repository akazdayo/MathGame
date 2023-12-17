import json
import time
from rich.prompt import Prompt


class Scores:
    def __init__(self) -> None:
        with open("./save/settings.json", "r") as f:
            self.settings = json.load(f)
        self.end_flag = False

    def timer(self):
        self.end_flag = False
        score = self.settings["score"]["firstScore"]
        while not self.end_flag:
            time.sleep(self.settings["score"]["interval"])
            score -= self.settings["score"]["decrease"]
        return score


class Statistics:
    def __init__(self) -> None:
        with open("./save/scores.json", "r") as f:
            self.save_data = json.load(f)

    def get(self):
        pass

    def ask_name(self):
        users = list(self.save_data["users"].keys())
        users.append("+")
        name = Prompt.ask("What your name?", choices=users)
        if name == "+":
            name = Prompt.ask("Enter your name")
            self.save_data["users"][name] = {
                "level": 1,
                "highScore": 0,
                "lastScore": 0,
                "totalGames": 0,
                "totalScore": 0
            }
        return name

    def set(self, name, key, value,):
        self.save_data["users"][name][key] = value

    def save(self):
        with open("./save/scores.json", "w") as f:
            json.dump(self.save_data, f)


if __name__ == "__main__":
    stats = Statistics()
    name = stats.ask_name()
    stats.set(name, "level", 2)
    stats.save()
