import cowsay
import random
import argparse
import urllib.request
from typing import Callable, Optional


def bullscows(attempt: str, secret: str) -> tuple[int, int]:
    if len(attempt) != len(secret):
        raise ValueError("Attempt and secret must be of the same length")

    bulls = sum(a == s for a, s in zip(attempt, secret))
    cows = sum(min(attempt.count(x), secret.count(x)) for x in set(attempt)) - bulls

    return bulls, cows


def gameplay(ask: Callable, inform: Callable, words: list[str]) -> int:
    secret = random.choice(words)

    attempts = 0
    while True:
        attempt = ask("Введите слово: ", words)
        attempts += 1

        try:
            bulls, cows = bullscows(attempt, secret)
            inform("Быки: {}, Коровы: {}", bulls, cows)
        except ValueError as e:
            print(e)
            continue

        if bulls == len(secret):
            break

    return attempts


def ask(prompt: str, valid: Optional[list[str]] = None) -> str:
    ans = input(prompt)

    while valid and ans not in valid:
        print("Word not in the dictionary. Please try again.")
        ans = input(prompt)

    return ans


def inform(format_string: str, bulls: int, cows: int) -> None:
    print(format_string.format(bulls, cows))

    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Play the Bulls and Cows game")
    parser.add_argument(
        "dictionary",
        type=str,
        help="Path to the dictionary file or URL",
    )
    parser.add_argument(
        "length",
        type=int,
        nargs="?",
        default=5,
        help="Length of the words to use (default: 5)",
    )
    args = parser.parse_args()

    print("Length of the words to use:", args.length)

    dictionary = []

    if args.dictionary.startswith("http://") or args.dictionary.startswith("https://"):
        with urllib.request.urlopen(args.dictionary) as response:
            content = response.read().decode("utf-8")
            dictionary = content.splitlines()
    else:
        with open(args.dictionary, "r") as file:
            dictionary = file.read().splitlines()

    dictionary = [word for word in dictionary if len(word) == args.length]

    attempts = gameplay(ask, inform, dictionary)
    print(f"Количество попыток: {attempts}")
