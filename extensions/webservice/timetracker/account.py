# Copyright (c) 2014 Martin Abente Lahaye. - tch@sugarlabs.org
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA

import logging

from gi.repository import Gio

from jarabe.model import shell
from jarabe.webservice import account


class Account(account.Account):

    DCON_SLEEP_PATH = '/sys/devices/platform/dcon/sleep'

    def __init__(self):
        logging.debug('timetracker __init__')
        self._activity = None
        self._state = None

        self._model = shell.get_model()

        self._model.zoom_level_changed.connect(self.__zoom_changed_cb)

        self._monitor = Gio.File.new_for_path(self.DCON_SLEEP_PATH)\
            .monitor_file(Gio.FileMonitorFlags.NONE, None)
        self._monitor.connect('changed', self.__file_changed_cb)

    def __zoom_changed_cb(self, **kwargs):
        old_level = kwargs['old_level']
        new_level = kwargs['new_level']

        # ignore non-useful transitions
        if old_level != self._model.ZOOM_ACTIVITY and \
                new_level != self._model.ZOOM_ACTIVITY:
            return

        logging.debug('timetracker zoom level is  %d', new_level)
        if new_level == self._model.ZOOM_ACTIVITY:
            self._activate()
        else:
            self._deactivate()

    def __file_changed_cb(self, monitor, file, other_file, event):
        if event != Gio.FileMonitorEvent.CHANGED:
            return

        with open(self.DCON_SLEEP_PATH) as _file:
            state = bool(int(_file.read()))

        if state == self._state:
            return

        logging.debug('timetracker state is %r', state)
        if state is True:
            self._deactivate()
        else:
            self._activate()

        self._state = state

    def _deactivate(self):
        activity = self._model.get_active_activity()
        if activity.is_journal():
            return

        logging.debug('timetracker deactivate %s', activity.get_bundle_id())
        activity.set_active(False)

        self._activity = activity

    def _activate(self):
        activity = self._model.get_active_activity()

        if activity == self._activity:
            logging.debug('timetracker activate %s', activity.get_bundle_id())
            self._activity.set_active(True)

        self._activity = None

    def get_token_state(self):
        return self.STATE_VALID


def get_account():
    return Account()
