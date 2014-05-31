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

import time
import logging

from gi.repository import Gio

from jarabe.model import shell


class Time(object):

    def __init__(self, bundle_id):
        self.bundle_id = bundle_id
        self.launch = int(time.time())
        self.active = None
        self.time = 0

    def deactivate(self):
        if self.active is not None:
            self.time += int(time.time()) - self.active
            self.active = None
            logging.debug('TimeTracker %s increated to %d',
                          self.bundle_id, self.time)

    def activate(self):
        if self.active is None:
            self.active = int(time.time())


class TimeTracker(object):

    DCON_SLEEP_PATH = '/sys/devices/platform/dcon/sleep'

    def __init__(self):
        logging.debug('TimeTracker __init__')

        self._times = {}
        self._active = None

        self._model = shell.get_model()
        self._model.connect('activity-removed', self.__removed_cb)
        self._model.connect('active-activity-changed', self.__changed_cb)

        self._state = None

        self._monitor = Gio.File.new_for_path(self.DCON_SLEEP_PATH)\
            .monitor_file(Gio.FileMonitorFlags.NONE, None)
        self._monitor.connect('changed', self.__file_changed_cb)

    def __removed_cb(self, model, activity):
        _time = self._times[activity]
        logging.debug('TimeTracker for %s is %d', _time.bundle_id, _time.time)
        del self._times[activity]

    def __changed_cb(self, model, activity):
        if self._active is not None:
            self._active.deactivate()

        if activity not in self._times:
            self._times[activity] = Time(activity.get_bundle_id())

        self._active = self._times[activity]
        self._active.activate()
        logging.debug('TimeTracker changed to %s', self._active.bundle_id)

    def __file_changed_cb(self, monitor, file, other_file, event):
        if event != Gio.FileMonitorEvent.CHANGED:
            return

        with open(self.DCON_SLEEP_PATH) as _file:
            state = bool(int(_file.read()))

        if state == self._state:
            return

        logging.debug('TimeTracker state %r with %s',
                      state, self._active.bundle_id)

        if state is True:
            self._active.deactivate()
        else:
            self._active.activate()

        self._state = state
