import random
import json


class Problem:
    def __init__(self) -> None:
        with open("./save/settings.json", "r") as f:
            self.settings = json.load(f)
        self.answer = 0
        self.problem_rule = [self.settings["problem"]["value"]["min"],
                             self.settings["problem"]["value"]["max"]]
        problem_type = self.settings["problem"]["type"]
        self.all_problem_type = [
            char for char in "+-*/" if char in problem_type]

    def create(self):
        formula = []
        operator = random.choice(self.all_problem_type)

        match operator:
            case "+" | "-" | "*":
                formula.append(random.randint(
                    self.problem_rule[0], self.problem_rule[1]))
                formula.append(operator)
                formula.append(random.randint(
                    self.problem_rule[0], self.problem_rule[1]))
            case "/":
                while True:
                    formula = [random.randint(
                        1, 9), operator, random.randint(1, 9)]
                    formula[0] = formula[0] * formula[2]
                    if formula[0] != formula[2]:
                        break
            case _:
                raise ValueError("Invalid Operator")

        return formula

    def check(self, formula):
        if formula[1] == "+":
            self.answer = formula[0] + formula[2]
        elif formula[1] == "-":
            self.answer = formula[0] - formula[2]
        elif formula[1] == "*":
            self.answer = formula[0] * formula[2]
        elif formula[1] == "/":
            self.answer = formula[0] / formula[2]
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
