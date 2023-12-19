import random
import json
import math


class Problem:
    def __init__(self) -> None:
        with open("./save/settings.json", "r") as f:
            self.settings = json.load(f)
        self.formula = []  # [1, "+", 2, "*", 3, "-", 4, "/", 5]
        self.answer = 0
        self.problem_rule = [self.settings["problem"]["value"]["min"],
                             self.settings["problem"]["value"]["max"]]
        problem_type = self.settings["problem"]["type"]
        self.all_problem_type = [
            char for char in "+-*/" if char in problem_type]

    def create(self):
        self.formula = []
        for _ in range(1):
            self.formula.append(random.randint(
                self.problem_rule[0], self.problem_rule[1]))
            self.formula.append(random.choice(self.all_problem_type))
        self.formula.append(random.randint(
            self.problem_rule[0], self.problem_rule[1]))
        return self.formula

    def check(self):
        if self.formula[1] == "+":
            self.answer = self.formula[0] + self.formula[2]
        elif self.formula[1] == "-":
            self.answer = self.formula[0] - self.formula[2]
        elif self.formula[1] == "*":
            self.answer = self.formula[0] * self.formula[2]
        elif self.formula[1] == "/":
            self.answer = self.formula[0] / self.formula[2]
        # decimalPlaces以降を切り捨て
        self.answer = round(
            self.answer, self.settings["problem"]["decimalPlaces"])
        return self.answer


if __name__ == "__main__":
    problem = Problem()
    problem.create()
    print(problem.formula)
    if problem.check(5) == problem.answer:
        print("Correct")
    else:
        print("In Correct")
    print(problem.check(5))
    # print(problem.answer)
