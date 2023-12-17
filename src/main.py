import problem
import stats
from rich import print
import sys
from concurrent.futures import ThreadPoolExecutor
from rich.prompt import Prompt
from rich.console import Console


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


class GameMode:
    def __init__(self) -> None:
        self.loop = Loop()
        self.stats = stats.Statistics()
        self.console = Console()

    def start(self, round: int) -> None:
        # ラウンド数分ループ
        for i in range(round):
            # print(f"Round {i+1}")
            self.console.rule(f"[bold cyan]Round {i+1}")
            self.loop.run()

        self.console.rule(f"[bold red] Result")
        # 終了処理
        self.end(self.loop.score / round)  # 平均スコア

    def end(self, avg_score: int) -> None:
        # 結果表示
        print(f"Total Score: {self.loop.score}")
        print(f"Average Score: {avg_score}")

        # ユーザー情報更新
        name = self.stats.ask_name()
        self.stats.set(name, "lastScore", self.loop.score)
        self.stats.set(name, "totalGames",
                       self.stats.save_data["users"][name]["totalGames"] + 1)

        # 全体統計更新
        self.stats.save_data["statistic"]["totalGames"] += 1
        self.stats.set(
            name, "totalScore", self.stats.save_data["users"][name]["totalScore"] + self.loop.score)

        # ユーザーハイスコア(Avg)
        if avg_score > self.stats.save_data["users"][name]["highScore"]:
            self.console.rule(f"[bold italic red] High Score!!")
            self.stats.set(name, "highScore", avg_score)
            print("[blue bold italic]New High Score![/blue bold italic]")

            # 全体ハイスコア(Avg)
            if avg_score > self.stats.save_data["statistic"]["totalHighScore"]:
                self.stats.save_data["statistic"]["totalHighScore"] = avg_score
                print("[red bold italic]New Total High Score![/red bold italic]")

        # 更新データを保存
        self.stats.save()
        print(self.stats.save_data["users"][name])


class MainMenu:
    def __init__(self) -> None:
        self.stats = stats.Statistics()
        self.mode = GameMode()

    def menu(self):
        print("[bold cyan]Welcome to Math Game[/bold cyan]")
        mode = Prompt.ask("1. Start Game\n2. Statistics\n3. Exit\n",
                          choices=["1", "2", "3"])
        if mode == "1":
            round = Prompt.ask("Enter the rounds", default="10")
            self.mode.start(int(round))

        elif mode == "2":
            name = self.stats.ask_name()
            print(self.stats.save_data["users"][name])
            print(self.stats.save_data["statistic"])


if __name__ == "__main__":
    menu = MainMenu()
    menu.menu()
