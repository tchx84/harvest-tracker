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

from gi.repository import GLib

from jarabe.webservice import account

from tracker.tracker import Tracker


class Account(account.Account):

    def __init__(self):
        self._tracker = None
        GLib.idle_add(self.__start_cb)

    def __start_cb(self):
        self._tracker = Tracker()

    def get_token_state(self):
        return self.STATE_VALID


def get_account():
    return Account()
