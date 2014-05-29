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

from jarabe.model import shell
from jarabe.webservice import account


class Account(account.Account):

    def __init__(self):
        logging.debug('timetracker __init__')
        self._model = shell.get_model()
        self._activity = None

    def __suspend_cb(self):
        logging.debug('timetracker __suspend_cb')
        self._activity = self._model.get_active_activity()
        if self._activity is not None:
            self._activity.set_active(False)

    def __resume_cb(self):
        logging.debug('timetracker __resume_cb')
        if self._activity is not None:
            self._activity.set_active(True)
        self._activity = None

    def get_token_state(self):
        return self.STATE_VALID


def get_account():
    return Account()
