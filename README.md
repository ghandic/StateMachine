# Python State Machine

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![made-with-Markdown](https://img.shields.io/badge/Made%20with-Markdown-1f425f.svg)](http://commonmark.org)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)
[![Open Source? Yes!](https://badgen.net/badge/Open%20Source%20%3F/Yes%21/blue?icon=github)](https://github.com/ghandic/PyCap-TODO-CRUD)
![coverage](https://img.shields.io/badge/coverage-100%25-green)

Pure Python implementation of a state machine that can be initialized with the transitions it can take and an initial state.
It can also add convenience methods to your class based on the states you have defined such as `is_stopped` for a state of `"stopped"`.

## Concepts covered

- Object Oriented Programming
- Decorators
- Introspection
- Unit testing
- Error handling
- Advanced control flow
- Advanced Python syntax

## Example usage

```python
from machine import Machine

class Video(object):
    PAUSED = "paused"
    PLAYING = "playing"
    STOPPED = "stopped"

    def __init__(self, skip_optional_validation=True):
        self.skip_optional_validation = skip_optional_validation
        transitions = [
            {"trigger": "play", "source": self.PAUSED, "dest": self.PLAYING},
            {"trigger": "play", "source": self.STOPPED, "dest": self.PLAYING},
            {"trigger": "pause", "source": self.PLAYING, "dest": self.PAUSED},
            {"trigger": "stop", "source": self.PLAYING, "dest": self.STOPPED},
            {"trigger": "stop", "source": self.PAUSED, "dest": self.STOPPED},
        ]

        self.machine = Machine(self, transitions, self.STOPPED, skip_optional_validation=True)

    def play(self):
        ...

    def pause(self):
        ...

    def stop(self):
        ...

```

Now when you call `play()`, the machine's state will be updated to `"playing"`, if you run `pause()`,
the machine's state will be updated to `"stopped"`, if you try to stop it again in this state it will raise
a `MachineError` as you cannot transition from stopped to stopped.

## License

This project is licensed under the terms of the MIT license.

- This repo is based off a [Youtube video on "When Booleans Are Not Enough... State Machines?"](https://www.youtube.com/watch?v=I1Mzx_tSpew&list=WL&index=4)
