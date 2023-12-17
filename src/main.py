import problem
import stats
from rich import print
import sys
from concurrent.futures import ThreadPoolExecutor
from rich.prompt import Prompt


class Loop:
    def __init__(self) -> None:
        self.problem = problem.Problem()
        self.scores = stats.Scores()
        self.score = 0

    def run(self):
        formula = self.problem.create()
        print(
            f"[italic][red]{formula[0]}[/red] [green]{formula[1]}[/green] [red]{formula[2]}[/red] [cyan]=[/cyan][/italic]")
        with ThreadPoolExecutor() as executor:
            timer_task = executor.submit(self.scores.timer)
            ans_task = executor.submit(self.async_input)

            score = timer_task.result()
            ans_input = ans_task.result()
        ans = self.problem.check()
        if float(ans_input) == float(ans):
            print("[italic green]Correct[/italic green]")
        else:
            print(
                f"[italic red]In Correct[/italic red]\n[green]The correct answer is[/green] {ans}")
            score = self.scores.settings["inCorrectScore"]
        print(f"Score: {score}")
        self.score += score

    def async_input(self):
        ans = input()
        if ans == "exit" or ans == "quit" or ans == "q":
            self.scores.end_flag = True
            sys.exit()
        try:
            ans = float(ans)
        except ValueError:
            self.scores.end_flag = True
            return 999999999999
        self.scores.end_flag = True
        return ans


class MainMenu:
    def __init__(self) -> None:
        self.problem = problem.Problem()
        self.scores = stats.Scores()
        self.stats = stats.Statistics()
        self.loop = Loop()

    def menu(self):
        print("[bold cyan]Welcome to Math Game[/bold cyan]")
        mode = Prompt.ask("1. Start Game\n2. Statistics\n3. Exit\n",
                          choices=["1", "2", "3"])
        if mode == "1":
            Prompt.ask("Enter the rounds", default="10")
            for i in range(10):
                print(f"Round {i+1}")
                self.loop.run()
            print(f"Total Score: {self.loop.score}")
            name = self.stats.ask_name()
            self.stats.set(name, "lastScore", self.loop.score)
            self.stats.set(name, "totalGames",
                           self.stats.save_data["users"][name]["totalGames"] + 1)
            self.stats.save_data["statistic"]["totalGames"] += 1
            self.stats.set(
                name, "totalScore", self.stats.save_data["users"][name]["totalScore"] + self.loop.score)

            if self.loop.score > self.stats.save_data["users"][name]["highScore"]:
                self.stats.set(name, "highScore", self.loop.score)
                print("[blue bold italic]New High Score![/blue bold italic]")
                if self.loop.score > self.stats.save_data["statistic"]["totalHighScore"]:
                    self.stats.save_data["statistic"]["totalHighScore"] = self.loop.score
                    print("[red bold italic]New Total High Score![/red bold italic]")
        elif mode == "2":
            name = self.stats.ask_name()
            print(self.stats.save_data["users"][name])
            print(self.stats.save_data["statistic"])
        self.stats.save()


if __name__ == "__main__":
    menu = MainMenu()
    menu.menu()
