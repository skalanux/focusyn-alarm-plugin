from __future__ import unicode_literals

import logging

import gi

gi.require_version('Gst', '1.0')

from gi.repository import Gst

import tomate.plugin
from tomate.constant import State
from tomate.event import Events, on
from tomate.graph import graph
from tomate.utils import suppress_errors

logger = logging.getLogger(__name__)


class AlarmPlugin(tomate.plugin.Plugin):
    @suppress_errors
    def __init__(self):
        super(AlarmPlugin, self).__init__()
        self.config = graph.get('tomate.config')

        Gst.init(None)

        self.player = Gst.ElementFactory.make('playbin', None)
        self.player.set_property('uri', self.audio_path)
        self.player.set_state(Gst.State.NULL)

        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.connect('message', self.on_message)

    @suppress_errors
    @on(Events['Session'], [State.finished])
    def ring(self, *args, **kwargs):
        self.player.set_state(Gst.State.PLAYING)

        logger.debug('play ')

    @suppress_errors
    def on_message(self, bus, message):
        if message.type == Gst.MessageType.EOS:
            self.player.set_state(Gst.State.NULL)

            logger.debug('alarm end')

        elif message.type == Gst.MessageType.ERROR:
            self.player.set_state(Gst.State.NULL)

            logger.error('alarm error %s - %s', *message.parse_error())

    @property
    def audio_path(self):
        return self.config.get_media_uri('alarm.ogg')
