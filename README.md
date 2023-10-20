# zlo-2023-homework1-tests

There are two groups of tests, namely, `correctTests` and `moveOutOfTapeTests`.
Depending on how you handle moving out of tape the latter might not work for
you.

`run()` has a hardcoded run length limit. Depending on your solution you might
need to increase this. For me 400 was anough.

## Running (Jupyter)

Add this code cell somewhere below your code:
```py
%run tests.py
correctTests(run, eliminateInputTape)
moveOutOfTapeTests(run, eliminateInputTape)
```
and run it. Or even better, use "Restart the kernel and run all cells" button,
to make sure your solution works with clean global state.

## Runing (Python)

I haven't tested, but this should work:
```py
from tests import correctTests, moveOutOfTapeTests
correctTests(run, eliminateInputTape)
moveOutOfTapeTests(run, eliminateInputTape)
```
You will need to copy `run()` from the homework notebook.
