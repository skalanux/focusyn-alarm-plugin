from __future__ import unicode_literals

import unittest

from mock import Mock, patch


class AlarmPluginTestCase(unittest.TestCase):

    def setUp(self):
        from tomate.profile import ProfileManagerSingleton
        from alarm_plugin import AlarmPlugin

        self.profile = ProfileManagerSingleton.get()
        self.profile.app = ''

        self.plugin = AlarmPlugin()

    @patch('alarm_plugin.Gst.ElementFactory', spec_set=True)
    def test_should_create_playbin(self, mElementFactory):
        from gi.repository import Gst
        from alarm_plugin import AlarmPlugin

        plugin = AlarmPlugin()

        mElementFactory.make.assert_called_once_with('playbin', None)

        plugin.player.set_property.assert_called_once_with('uri', self.profile.get_media_uri('alarm.ogg'))

        plugin.player.set_state.assert_called_once_with(Gst.State.NULL)

    def test_player_should_change_state_to_playing(self):
        from gi.repository import Gst

        self.plugin.player = Mock()

        self.plugin.alarm()

        self.plugin.player.set_state.assert_called_once_with(Gst.State.PLAYING)
        self.assertEqual(1, self.plugin.player.set_state.call_count)

    def test_player_should_change_state_to_null(self):
        from gi.repository import Gst

        self.plugin.player = Mock()

        message = Mock()
        message.type = Gst.MessageType.EOS

        self.plugin.on_message(None, message)

        self.plugin.player.set_state.assert_called_once_with(Gst.State.NULL)
        self.assertEqual(1, self.plugin.player.set_state.call_count)

    def test_player_should_change_state_to_null_when_error(self):
        from gi.repository import Gst

        self.plugin.player = Mock()

        message = Mock()
        message.type = Gst.MessageType.ERROR
        message.parse_error.return_value = ('', '')

        self.plugin.on_message(None, message)

        self.plugin.player.set_state.called_once_with(Gst.State.NULL)
        self.assertEqual(1, self.plugin.player.set_state.call_count)