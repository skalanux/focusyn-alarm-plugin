import time
from datetime import datetime as dt, timedelta
from os.path import dirname, join
from typing import Callable

import pytest
from gi.repository import Gst, Gtk
from wiring import Graph

from focusyn.pomodoro import Bus, Config, Events
from focusyn.ui.testing import Q, run_loop_for

CUSTOM_ALARM = f'file://{join(dirname(__file__), "data", "focusyn", "media", "custom.ogg")}'
SECTION_NAME = "alarm_plugin"
OPTION_NAME = "file_uri"


def wait_until(fn: Callable[[], bool], timeout: int = 1, period: int = 0.25):
    limit = dt.utcnow() + timedelta(seconds=timeout)

    while dt.utcnow() < limit:
        if fn():
            return True
        time.sleep(period)
    return False


@pytest.fixture
def bus() -> Bus:
    return Bus()


@pytest.fixture
def config(bus, tmpdir) -> Config:
    cfg = Config(bus)
    tmp_path = tmpdir.mkdir("focusyn").join("focusyn.config")
    cfg.config_path = lambda: tmp_path.strpath
    return cfg


@pytest.fixture
def graph() -> Graph:
    g = Graph()
    g.register_instance(Graph, g)
    return g


@pytest.fixture
def plugin(bus, config, graph):
    graph.providers.clear()
    graph.register_instance("focusyn.config", config)
    graph.register_instance("focusyn.bus", bus)

    import alarm_plugin

    instance = alarm_plugin.AlarmPlugin()
    instance.configure(bus, graph)
    return instance


def test_plays_alarm_when_session_finish(bus, config, plugin):
    plugin.activate()

    bus.send(Events.SESSION_END)
    assert plugin.player.props.current_uri == config.media_uri("alarm.ogg")

    run_loop_for(1)
    assert wait_until(lambda: plugin.player.current_state == Gst.State.NULL, timeout=1)
    assert plugin.player.props.current_uri is None


def test_plays_custom_alarm(bus, config, plugin):
    config.set(SECTION_NAME, OPTION_NAME, CUSTOM_ALARM)
    plugin.activate()

    bus.send(Events.SESSION_END)

    run_loop_for(1)
    assert wait_until(lambda: plugin.player.current_state == Gst.State.NULL, timeout=1)
    assert plugin.player.props.current_uri is None


def test_not_plays_invalid_custom_alarm(bus, config, plugin):
    config.set(SECTION_NAME, OPTION_NAME, "file://invalid")
    plugin.activate()

    bus.send(Events.SESSION_END)

    run_loop_for(1)
    assert wait_until(lambda: plugin.player.current_state == Gst.State.NULL, timeout=1)
    assert plugin.player.props.current_uri == "file://invalid"


class TestSettingsWindow:
    def test_without_custom_alarm(self, config, plugin):
        config.remove(SECTION_NAME, OPTION_NAME)
        window = plugin.settings_window(Gtk.Window())
        window.run()

        entry = Q.select(window.widget, Q.props("name", "alarm_entry"))
        assert entry.props.text == ""
        assert entry.props.sensitive is False

        switch = Q.select(window.widget, Q.props("name", "alarm_switch"))
        assert switch.props.active is False

    def test_with_custom_alarm(self, plugin, config):
        config.set(SECTION_NAME, OPTION_NAME, CUSTOM_ALARM)

        window = plugin.settings_window(Gtk.Window())
        window.run()

        entry = Q.select(window.widget, Q.props("name", "alarm_entry"))
        assert entry.props.text == CUSTOM_ALARM
        assert entry.props.sensitive is True

        switch = Q.select(window.widget, Q.props("name", "alarm_switch"))
        assert switch.props.active is True

    def test_enable_custom_alarm(self, config, plugin):
        dialog = plugin.settings_window(Gtk.Window())
        dialog.run()

        switch = Q.select(dialog.widget, Q.props("name", "alarm_switch"))
        switch.props.active = True
        switch.notify("activate")

        entry = Q.select(dialog.widget, Q.props("name", "alarm_entry"))
        assert entry.props.sensitive is True
        entry.set_text(CUSTOM_ALARM)

        dialog.widget.emit("response", 0)
        assert config.get(SECTION_NAME, OPTION_NAME) == CUSTOM_ALARM

    def test_disable_custom_alarm(self, config, plugin):
        config.set(SECTION_NAME, OPTION_NAME, CUSTOM_ALARM)

        dialog = plugin.settings_window(Gtk.Window())
        dialog.run()

        switch = Q.select(dialog.widget, Q.props("name", "alarm_switch"))
        switch.props.active = False
        switch.notify("activate")

        entry = Q.select(dialog.widget, Q.props("name", "alarm_entry"))
        assert entry.props.text == ""
        assert entry.props.sensitive is False

        dialog.widget.emit("response", 0)
        assert config.has_option(SECTION_NAME, OPTION_NAME) is False
