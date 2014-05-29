# Copyright (c) 2013 Martin Abente Lahaye. - tch@sugarlabs.org
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

        self._monitor = Gio.File.new_for_path(self.DCON_SLEEP_PATH)\
            .monitor_file(Gio.FileMonitorFlags.NONE, None)
        self._monitor.connect('changed', self.__file_changed_cb)

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
        logging.debug('timetracker _deactivate')
        self._activity = self._model.get_active_activity()
        if self._activity is not None:
            self._activity.set_active(False)

    def _activate(self):
        logging.debug('timetracker _activate')
        if self._activity is not None:
            self._activity.set_active(True)
        self._activity = None

    def get_token_state(self):
        return self.STATE_VALID


def get_account():
    return Account()
