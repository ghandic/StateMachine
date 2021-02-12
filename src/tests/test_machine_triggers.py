from truth.truth import AssertThat

from ..machine import MachineError
from .videos import GoodVideo


def test_state_initialised():
    vid = GoodVideo()
    assert vid.machine.state == vid.STOPPED


def test_state_change_triggered_on_play_works_when_moving_from_stop():
    vid = GoodVideo()
    assert vid.machine.state == vid.STOPPED
    vid.play()
    assert vid.machine.state == vid.PLAYING


def test_state_change_triggered_on_play_works_when_moving_from_stop_vid_state():
    vid = GoodVideo()
    assert vid.state == vid.STOPPED
    vid.play()
    assert vid.state == vid.PLAYING


def test_state_change_triggered_on_play_works_when_moving_from_stop_vid_state_is_not_added():
    vid = GoodVideo()
    assert not hasattr(vid, "is_stopped")


def test_state_change_triggered_on_play_works_when_moving_from_stop_vid_state_is_added():
    vid = GoodVideo(add_is_state=True)
    assert hasattr(vid, "is_stopped")
    assert hasattr(vid, "is_playing")
    assert hasattr(vid, "is_paused")
    assert vid.is_stopped
    vid.play()
    assert vid.is_playing


def test_state_change_triggered_on_play_errors_when_moving_from_play():
    vid = GoodVideo()
    assert vid.machine.state == vid.STOPPED
    vid.play()
    assert vid.machine.state == vid.PLAYING
    with AssertThat(MachineError).IsRaised():
        vid.play()
