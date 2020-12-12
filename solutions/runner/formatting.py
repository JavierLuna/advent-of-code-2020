class Color:
    CLEAR = "\033[0m"
    BOLD = "\033[1m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BGREEN = BOLD+GREEN
    BYELLOW = BOLD+YELLOW


def print_sol(part: int, solution):
    phrase = "⭐" * part
    if isinstance(solution, int):
        phrase += f"\t\t{Color.BYELLOW}{solution}{Color.CLEAR}"
    else:
        phrase += f"\n{Color.BOLD}{solution}{Color.CLEAR}\n"
    print(phrase)