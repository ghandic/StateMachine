from ..machine import Machine


class GenericVideo(object):
    PAUSED = "paused"
    PLAYING = "playing"
    STOPPED = "stopped"

    def __init__(self, skip_optional_validation=True):
        self.skip_optional_validation = skip_optional_validation

    def set_machine(self, transitions, initial_state):
        self.machine = Machine(self, transitions, initial_state, skip_optional_validation=self.skip_optional_validation)

    def play(self):
        ...

    def pause(self):
        ...

    def stop(self):
        ...


class BadVideo(object):

    PAUSED = "paused"
    PLAYING = "playing"
    STOPPED = "stopped"

    def __init__(self, skip_optional_validation=True, add_is_state=False):

        transitions = [
            {"trigger": "play", "source": self.PAUSED, "dest": self.PLAYING},
            {"trigger": "play", "source": self.STOPPED, "dest": self.PLAYING},
            {"trigger": "pause", "source": self.PLAYING, "dest": self.PAUSED},
            {"trigger": "stop", "source": self.PLAYING, "dest": self.STOPPED},
            {"trigger": "stop", "source": self.PAUSED, "dest": self.STOPPED},
        ]

        self.machine = Machine(self, transitions, self.STOPPED, skip_optional_validation, add_is_state)

    @property
    def state(self):
        return self.machine.state

    def play(self):
        ...


class GoodVideo(BadVideo):
    def pause(self):
        ...

    def stop(self):
        ...


class ExtraGoodVideo(GoodVideo):
    def extra(self):
        ...
