import pytest
from truth.truth import AssertThat

from ..machine import InvalidMachine
from .videos import BadVideo, ExtraGoodVideo, GenericVideo, GoodVideo


def test_state_machine_without_triggers_as_methods_raises_invalid_machine_error():
    with AssertThat(InvalidMachine).IsRaised():
        BadVideo()


def test_state_machine_with_all_triggers_as_methods_doesnt_error():
    GoodVideo()


def test_state_machine_with_all_triggers_as_methods_plus_extra_methods_doesnt_error():
    ExtraGoodVideo()


@pytest.mark.parametrize(
    "transitions,initial_state,expected_error",
    [
        (
            [
                {"trigger": "play", "source": GenericVideo.PAUSED, "dest": GenericVideo.PLAYING},
                {"trigger": "play", "source": GenericVideo.STOPPED, "dest": GenericVideo.PLAYING},
                {"trigger": "pause", "source": GenericVideo.PLAYING, "dest": GenericVideo.PAUSED},
                {"trigger": "stop", "source": GenericVideo.PLAYING, "dest": GenericVideo.STOPPED},
                {"trigger": "stop", "source": GenericVideo.PAUSED, "dest": GenericVideo.STOPPED},
            ],
            GenericVideo.STOPPED,
            None,
        ),
        (
            [
                "",
                {"trigger": "play", "source": GenericVideo.PAUSED, "dest": GenericVideo.PLAYING},
                {"trigger": "play", "source": GenericVideo.STOPPED, "dest": GenericVideo.PLAYING},
                {"trigger": "pause", "source": GenericVideo.PLAYING, "dest": GenericVideo.PAUSED},
                {"trigger": "stop", "source": GenericVideo.PLAYING, "dest": GenericVideo.STOPPED},
                {"trigger": "stop", "source": GenericVideo.PAUSED, "dest": GenericVideo.STOPPED},
            ],
            GenericVideo.STOPPED,
            InvalidMachine,
        ),
        (
            [
                {"trigger": "play", "source": GenericVideo.PAUSED},
                {"trigger": "play", "source": GenericVideo.STOPPED, "dest": GenericVideo.PLAYING},
                {"trigger": "pause", "source": GenericVideo.PLAYING, "dest": GenericVideo.PAUSED},
                {"trigger": "stop", "source": GenericVideo.PLAYING, "dest": GenericVideo.STOPPED},
                {"trigger": "stop", "source": GenericVideo.PAUSED, "dest": GenericVideo.STOPPED},
            ],
            GenericVideo.STOPPED,
            InvalidMachine,
        ),
        (
            [
                {"trigger": "play", "dest": GenericVideo.PLAYING},
                {"trigger": "play", "source": GenericVideo.STOPPED, "dest": GenericVideo.PLAYING},
                {"trigger": "pause", "source": GenericVideo.PLAYING, "dest": GenericVideo.PAUSED},
                {"trigger": "stop", "source": GenericVideo.PLAYING, "dest": GenericVideo.STOPPED},
                {"trigger": "stop", "source": GenericVideo.PAUSED, "dest": GenericVideo.STOPPED},
            ],
            GenericVideo.STOPPED,
            InvalidMachine,
        ),
        (
            [
                {"source": GenericVideo.PAUSED, "dest": GenericVideo.PLAYING},
                {"trigger": "play", "source": GenericVideo.STOPPED, "dest": GenericVideo.PLAYING},
                {"trigger": "pause", "source": GenericVideo.PLAYING, "dest": GenericVideo.PAUSED},
                {"trigger": "stop", "source": GenericVideo.PLAYING, "dest": GenericVideo.STOPPED},
                {"trigger": "stop", "source": GenericVideo.PAUSED, "dest": GenericVideo.STOPPED},
            ],
            GenericVideo.STOPPED,
            InvalidMachine,
        ),
        (
            [
                {"trigger": "pause", "source": GenericVideo.PLAYING, "dest": GenericVideo.PAUSED},
                {"trigger": "stop", "source": GenericVideo.PLAYING, "dest": GenericVideo.STOPPED},
                {"trigger": "stop", "source": GenericVideo.PAUSED, "dest": GenericVideo.STOPPED},
            ],
            GenericVideo.STOPPED,
            InvalidMachine,
        ),
        (
            [
                {"trigger": "play", "source": GenericVideo.PAUSED, "dest": GenericVideo.PLAYING},
                {"trigger": "play", "source": GenericVideo.STOPPED, "dest": GenericVideo.PLAYING},
                {"trigger": "pause", "source": GenericVideo.PLAYING, "dest": GenericVideo.PAUSED},
                {"trigger": "stop", "source": GenericVideo.PLAYING, "dest": GenericVideo.STOPPED},
                {"trigger": "stop", "source": GenericVideo.PAUSED, "dest": GenericVideo.STOPPED},
                {"trigger": "stop", "source": GenericVideo.PAUSED, "dest": GenericVideo.PAUSED},
            ],
            GenericVideo.STOPPED,
            InvalidMachine,
        ),
    ],
)
def test_state_machine_transition_invalid_raises_invalid_machine_error(transitions, initial_state, expected_error):
    vid = GenericVideo()
    if expected_error is None:
        vid.set_machine(transitions, initial_state)
    else:
        with AssertThat(expected_error).IsRaised():
            vid.set_machine(transitions, initial_state)


@pytest.mark.parametrize(
    "transitions,initial_state,expected_error",
    [
        (
            [
                {"trigger": "play", "source": GenericVideo.PAUSED, "dest": GenericVideo.PLAYING},
                {"trigger": "play", "source": GenericVideo.STOPPED, "dest": GenericVideo.PLAYING},
                {"trigger": "pause", "source": GenericVideo.PLAYING, "dest": GenericVideo.PAUSED},
                {"trigger": "stop", "source": GenericVideo.PLAYING, "dest": GenericVideo.STOPPED},
                {"trigger": "stop", "source": GenericVideo.PAUSED, "dest": GenericVideo.STOPPED},
            ],
            GenericVideo.STOPPED,
            None,
        ),
        (
            [
                {"trigger": "play", "source": GenericVideo.PAUSED, "dest": GenericVideo.PLAYING},
                {"trigger": "play", "source": GenericVideo.STOPPED, "dest": GenericVideo.PLAYING},
                {"trigger": "pause", "source": GenericVideo.PLAYING, "dest": GenericVideo.PAUSED},
                {"trigger": "stop", "source": GenericVideo.PLAYING, "dest": GenericVideo.STOPPED},
                {"trigger": "stop", "source": GenericVideo.PAUSED, "dest": GenericVideo.STOPPED},
                {"trigger": "stop", "source": GenericVideo.PAUSED, "dest": GenericVideo.PAUSED},
            ],
            GenericVideo.STOPPED,
            InvalidMachine,
        ),
        (
            [{"trigger": "play", "source": GenericVideo.STOPPED, "dest": GenericVideo.PLAYING},],
            GenericVideo.STOPPED,
            InvalidMachine,
        ),
    ],
)
def test_state_machine_transition_invalid_raises_invalid_machine_error_optionals(
    transitions, initial_state, expected_error
):

    vid = GenericVideo(skip_optional_validation=False)
    if expected_error is None:
        vid.set_machine(transitions, initial_state)
    else:
        with AssertThat(expected_error).IsRaised():
            vid.set_machine(transitions, initial_state)
