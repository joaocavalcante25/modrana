#!/usr/bin/python
#---------------------------------------------------------------------------
# Calculate speed, time, etc. from position
#---------------------------------------------------------------------------
# Copyright 2007-2008, Oliver White
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#---------------------------------------------------------------------------
from base_module import ranaModule
import geo
from time import *

def getModule(m,d):
  return(stats(m,d))

class stats(ranaModule):
  """Handles messages"""
  def __init__(self, m, d):
    ranaModule.__init__(self, m, d)
    self.lastpos = [0,0]
    self.lastT = None
    self.maxSpeed = 0
    self.avg1 = 0
    self.avg2 = 0
  
  def update(self):
    # Run scheduledUpdate every second
    t = time()
    if(self.lastT == None):
      self.scheduledUpdate(t, 0, True)
      self.lastT = t
    else:
      dt = t - self.lastT
      if(dt > 1):
        self.scheduledUpdate(t, dt)
        self.lastT = t
  
  def scheduledUpdate(self, t, dt, firstTime=False):
    """Called every dt seconds"""
    pos = self.get('pos', None)
    if(pos == None):
      return # TODO: zero any stats

    if(not firstTime):
      distance = geo.distance(
        self.lastpos[0],
        self.lastpos[1],
        pos[0],
        pos[1]) * 1000.0 # metres

# from now on we get bearing from gpsd
#      bearing = geo.bearing(
#        self.lastpos[0],
#        self.lastpos[1],
#        pos[0],
#        pos[1]) # degrees

#      speed = distance / dt # m/sec
      speed = self.get('metersPerSecSpeed', 0)

      unitType = self.get("unitType", "kmh") # which unit do we use ?


#      self.set('bearing', bearing)
      average = 0
      if speed < 4000:
        if(speed > self.maxSpeed):
  #          self.set('maxSpeed', speed) # in m/sec
          self.maxSpeed = speed
        self.avg1 += speed
        self.avg2 += dt
        average = self.avg1/self.avg2

      if unitType == "kmh":
        speedUnitPerHour = speed * 3.6 # kilometers/hour
        maxSpeedUnitPerHour = self.maxSpeed * 3.6
        averageSpeedUnitPerHour = average * 3.6

      else:
        speedUnitPerHour = speed * 2.23693629  # miles/hour
        maxSpeedUnitPerHour = self.maxSpeed * 2.23693629
        averageSpeedUnitPerHour = average * 2.23693629

      self.set('maxSpeed', maxSpeedUnitPerHour)
      self.set('avgSpeed', averageSpeedUnitPerHour)
      self.set('speed', speedUnitPerHour)

    self.lastpos = pos

if(__name__ == '__main__'):
  d = {'pos':[51, -1]}
  a = stats({},d)
  a.update()
  d['pos'] = [52, 0]
  a.update()
  print d.get('speed')
  