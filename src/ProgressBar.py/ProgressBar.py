from time import time


class ProgressBar:
    COMPLETED: str = "█"
    UNCOMPLETED: str = "░"
    COLORS = {'black': 30,
              'red': 31,
              'green': 32,
              'yellow': 33,
              'blue': 34,
              'magenta': 35,
              'cyan': 36,
              'white': 37,
              None: 0}

    def __init__(self, color: str = None, bright: bool = False, length: int = 40,
                 print_progress: bool = True, estimate_time: bool = False):
        # progress value between 0 and 1
        self.progress = 0
        # color of progress bar
        try:
            if color is not None:
                self.color = ProgressBar.COLORS[color.lower()]
            else:
                self.color = 0
        except KeyError:
            raise KeyError(f"Unknown color key! Possible keys are: {ProgressBar.COLORS.keys()}")
        # determine if color should be bright
        if bright:
            self.color += 60
        # intervals of the progress bar, should be a divisor of 100
        if type(length) != int:
            raise TypeError(f'progress_resolution must be an int, but {type(length)} was given!')
        self.length = length
        # Decides if the current progress in percent should be displayed
        self.print_progress = print_progress
        # Decides if the remaining should be calculated
        self.estimate_time = estimate_time
        self.last_time = time()
        self.diff = 0

    def __str__(self):
        completed = int(self.progress * self.length)
        bar = f"\033[{self.color}m" + ProgressBar.COMPLETED * completed \
              + ProgressBar.UNCOMPLETED * (self.length - completed)
        if self.print_progress:
            bar += f" {self.progress:.0%}"
        if self.estimate_time:
            dt = time() - self.last_time
            self.last_time = time()
            try:
                speed = self.diff / dt
                remaining = (1 - self.progress) / speed
                bar += f" ({remaining:.1f}s)"
            except ZeroDivisionError:
                pass
        return bar + "\033[0m"

    def _print(self):
        print('\r' + str(self), end='')

    def update(self, progress):
        if self.estimate_time:
            self.diff = progress - self.progress
        self.progress = progress
        self._print()

    def __enter__(self):
        self.update(0)
        if self.estimate_time:
            self.last_time = time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("")


def framed(s: str):
    return f"\033[51m{s}\033[54m"


def main():
    from time import sleep
    from itertools import cycle
    with ProgressBar(estimate_time=True) as progress:
        N = 10
        for i in range(N):
            sleep(.1)
            progress.update((i + 1) / N)
    print(framed('End Test'))
    test = cycle(['—', '\\', '|', '/'])
    for i in test:
        print('\r' + i, end="")
        sleep(.5)


if __name__ == '__main__':
    main()
