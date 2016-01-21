# FlipClock
# Copyright (c) .:TBX:. 2016
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
from Renderer import Renderer
from enigma import ePixmap, eTimer
from Components.config import config

class SevenHDFlipClock(Renderer):

    def __init__(self):
        Renderer.__init__(self)
        self.timer = eTimer()
        self.timer.callback.append(self.pollme)

    GUI_WIDGET = ePixmap

    def changed(self, what):
        if not self.suspended:
            value = self.source.text
            self.debug(str(value))
            
            if 'H1' in value:
               value = value[3:4]
            elif 'H2' in value:
               value = value[4:5]
            elif 'M1' in value:
               value = value[3:4]
            elif 'M2' in value:
               value = value[4:5]   
            else:
               value = 0
            self.instance.setPixmapFromFile('/usr/share/enigma2/SevenHD/clock/' + str(value) + '.png')

    def pollme(self):
        self.changed(None)
        return

    def onShow(self):
        self.suspended = False
        self.timer.start(200)

    def onHide(self):
        self.suspended = True
        self.timer.stop()
        
    def debug(self, what):
        if config.plugins.SevenHD.debug.value:
               f = open('/tmp/kraven_debug.txt', 'a+')
               f.write('[SevenHD_FlipClock_Render] ' + str(what) + '\n')
               f.close() 