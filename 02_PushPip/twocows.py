from cowsay import cowsay
import argparse


"""
Написать программу twocows.py, которая работает аналогично cowsay, входящей в состав пакета, только представляет реплики двух персонажей

    Допустимо не писать программу с нуля, а скопировать часть модуля с разбором командной строки и показом монолога, и потом его модифицировать

    Дополнительно появляются ключи -E, -F и -N, задающие параметры второй коровы, и второй свободный параметр командной строки — второе сообщение
    Коровы расположены строго друг за другом и выровнены по «земле» 
    
python twocows.py -f moose -E "^^" -F sheep "Hi there" "Ahoy!"
"""

"""
original module
cowsay --help 
usage: cowsay [-h] [-e eye_string] [-f cowfile] [-l] [-n] [-T tongue_string]
↪ [-W column] [-b] [-d] [-g] [-p] [-s] [-t] [-w] [-y] [--random] [message]

Generates an ASCII image of a cow saying the given text

positional arguments:
  message           The message to include in the speech bubble. If not given, 
                    stdin is used instead.

options:
  -h, --help        show this help message and exit
  -e eye_string     An eye string. This is ignored if a preset mode is given
  -f cowfile        Either the name of a cow specified in the COWPATH, or a 
                    path to a cowfile (if provided as a path, the path must 
                    contain at least one path separator)
  -l                Lists all cows in the cow path and exits
  -n                If given, text in the speech bubble will not be wrapped
  -T tongue_string  A tongue string. This is ignored if a preset mode is given
  -W column         Width in characters to wrap the speech bubble (default 40)
  --random          If provided, picks a random cow from the COWPATH.
                    Is superseded by the -f option

Mode:
  There are several out of the box modes which change the appearance of the cow.
  If multiple modes are given, the one furthest down this list is selected

  -b                Borg
  -d                dead
  -g                greedy
  -p                paranoid
  -s                stoned
  -t                tired
  -w                wired
  -y                young
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("message1")
    parser.add_argument("message2")
    parser.add_argument("-e", dest="e", default="oo")
    parser.add_argument("-f", dest="f", default="default")
    parser.add_argument("-n", dest="n", action="store_true")
    parser.add_argument("-T", dest="T", default="  ")
    parser.add_argument("-W", dest="W", type=int, default=40)
    parser.add_argument("-E", dest="E", default="oo")
    parser.add_argument("-F", dest="F", default="default")
    parser.add_argument("-N", dest="N", action="store_true")
    for flag, name in [
        ("-b", "borg"),
        ("-d", "dead"),
        ("-g", "greedy"),
        ("-p", "paranoid"),
        ("-s", "stoned"),
        ("-t", "tired"),
        ("-w", "wired"),
        ("-y", "young"),
    ]:
        parser.add_argument(flag, dest=name, action="store_true")
    args = parser.parse_args()

    preset = None
    for name in [
        "borg",
        "dead",
        "greedy",
        "paranoid",
        "stoned",
        "tired",
        "wired",
        "young",
    ]:
        if getattr(args, name):
            preset = name

    first = cowsay(
        args.message1,
        cow=args.f,
        eyes=args.e,
        tongue=args.T,
        width=args.W,
        wrap_text=not args.n,
        preset=preset,
    )
    second = cowsay(
        args.message2,
        cow=args.F,
        eyes=args.E,
        wrap_text=not args.N,
        preset=preset,
    )

    first = first.splitlines()
    second = second.splitlines()

    h = max(len(first), len(second))

    left_padded = [""] * (h - len(first)) + first
    right_padded = [""] * (h - len(second)) + second
    left_width = max((len(s) for s in left_padded), default=0)

    result = []
    for l, r in zip(left_padded, right_padded):
        result.append(f"{l:<{left_width}}{r}")

    print("\n".join(result))
