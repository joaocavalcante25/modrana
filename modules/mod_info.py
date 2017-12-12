# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# A modRana module providing various kinds of information.
#----------------------------------------------------------------------------
# Copyright 2007, Oliver White
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
from modules.base_module import RanaModule
from core.point import Point
import math
from core import geo
from core.i18n import _

def getModule(*args, **kwargs):
    return Info(*args, **kwargs)


class Info(RanaModule):
    """A modRana information handling module"""

    def __init__(self, *args, **kwargs):
        RanaModule.__init__(self, *args, **kwargs)
        self.versionString = "unknown version"
        currentVersionString = self.modrana.paths.getVersionString()
        if currentVersionString is not None:
            # check version string validity
            self.versionString = currentVersionString


        self._dirPoint = None
        dirPoint = self.get("directionPointLatLon", None)
        if dirPoint:
            lat, lon = dirPoint
            self._dirPoint = Point(lat, lon)

    @property
    def pay_pal_url(self):
        return "https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=martin%2ekolman%40gmail%2ecom&lc=CZ&item_name=The%20modRana%20project&currency_code=EUR&bn=PP%2dDonationsBF%3abtn_donate_LG%2egif%3aNonHosted"

    @property
    def flattr_url(self):
        return "https://flattr.com/thing/678708/modRana-flexible-GPS-navigation-system"

    @property
    def gratipay_url(self):
        return "https://gratipay.com/M4rtinK"

    @property
    def bitcoin_address(self):
        return "14DXzkqqYCfSG5vZNYPnPiZzg3wW2hXsE8"

    @property
    def discussions(self):
        """List of modRana-relevant discussions, with the most relevant discussion on top."""
        return [("http://talk.maemo.org/showthread.php?t=58861", _("talk.maemo.org thread"))]

    @property
    def main_discussion(self):
        """Url for the most relevant modRana discussion."""
        return self.discussions[0]

    @property
    def website_url(self):
        """Url to the modRana homepage."""
        return "http://www.modrana.org"

    @property
    def source_repository_url(self):
        """Link to the modRana source code."""
        return "https://github.com/M4rtinK/modrana"

    @property
    def translation_url(self):
        """Url for the modRana translation project."""
        return "https://www.transifex.com/martink/modrana"

    @property
    def email_address(self):
        """ModRana project email address."""
        return "modrana@gmail.com"

    def drawMenu(self, cr, menuName, args=None):
        if menuName == 'infoAbout':
            menus = self.m.get('menu', None)
            if menus:
                button1 = ('Discussion', 'generic', "ms:menu:openUrl:%s" % self.discussions[0][0])
                button2 = ('Donate', 'generic', "ms:menu:openUrl:%s" % self.pay_pal_url)
                web = " <u>www.modrana.org</u> "
                email = " modrana@gmail.com "
                text = "modRana version:\n\n%s\n\n\n\nFor questions or feedback,\n\ncontact the <b>modRana</b> project:\n\n%s\n\n%s\n\n" % (
                self.versionString, web, email)
                box = (text, "ms:menu:openUrl:http://www.modrana.org")
                menus.drawThreePlusOneMenu(cr, 'infoAbout', 'set:menu:info', button1, button2, box)
        elif menuName == "infoDirection":
            menus = self.m.get('menu', None)
            if menus:
                button1 = ('set point', 'generic', "info:setPoint")
                button2 = ('clear', 'generic', "info:clearPoint")
                boxText = "no point selected"
                if self._dirPoint:
                    lat = self._dirPoint.lat
                    lon = self._dirPoint.lon
                    boxText= "lat: <b>%f</b> lon: <b>%f</b>" % (lat, lon)
                    # if possible, add distance information
                    units = self.m.get("units", None)
                    pos = self.get("pos", None)
                    if pos and units:
                        lat1, lon1 = pos
                        distance = geo.distance(lat, lon, lat1, lon1)*1000
                        distance, shortUnit, longUnit = units.humanRound(distance)
                        boxText+=" %s %s" % (str(distance), shortUnit)
                box = (boxText, "")
                # draw the buttons and main box background
                menus.drawThreePlusOneMenu(cr, 'infoDirection', 'set:menu:info', button1, button2, box)
                # get coordinates for the box
                (e1, e2, e3, e4, alloc) = menus.threePlusOneMenuCoords()
                # upper left corner XY
                (x4, y4) = e4
                # width and height
                (w, h, dx, dy) = alloc
                w4 = w - x4
                h4 = h - y4

                # draw the direction indicator
                axisX = x4 + w4/2.0
                axisY = y4 + h4/2.0
                # shortest side
                shortestSide = min(w4,h4)
                # usable side - 10% border
                side = shortestSide*0.7

                angle = self._getDirectionAngle()

                self._drawDirectionIndicator(cr, axisX, axisY, side, angle)

    def handleMessage(self, message, messageType, args):
        if message == "setPoint":
            # open the coordinates entry dialog
            entry = self.m.get('textEntry', None)
            if entry:
                initialText = ""
                dirPoint = self.get("directionPointLatLon", None)
                if dirPoint:
                    initialText = "%f,%f" % dirPoint
                entry.entryBox(self, 'directionPointCoordinates', 'Coordinates (Example: 1.23,4.56)', initialText=initialText)
        elif message == "clearPoint":
            self._dirPoint = None
            self.set("directionPointLatLon" ,None)

    def handleTextEntryResult(self, key, result):
        if key == 'directionPointCoordinates':
            try:
                lat, lon = result.split(",")
                lat = float(lat)
                lon = float(lon)
                self.log.info("Direction coordinates %f,%f", lat, lon)
                self._dirPoint = Point(lat, lon)
                self.set("directionPointLatLon", (lat, lon))
            except Exception:
                self.log.exception("direction point coordinate parsing failed")

    # from SGTL
    # TODO: move to appropriate place
    def _bearingTo(self, pos, target, currentBearing):

        lat1 = math.radians(pos.lat)
        lat2 = math.radians(target.lat)
        lon1 = math.radians(pos.lon)
        lon2 = math.radians(target.lon)

        dlon = math.radians(target.lon - pos.lon)
        y = math.sin(dlon) * math.cos(lat2)
        x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1)*math.cos(lat2)*math.cos(dlon)
        bearing = math.degrees(math.atan2(y, x))
        bearing = (-180 + currentBearing - bearing) % 360
        return bearing

    def _getDirectionAngle(self):
        angle = 0.0
        pos = self.get("pos", None)
        bearing = self.get("bearing", None)
        if pos and bearing is not None and self._dirPoint:
            lat, lon = pos
            posPoint = Point(lat, lon)
            angle = self._bearingTo(posPoint, self._dirPoint, bearing)
        return angle


    def _drawDirectionIndicator(self, cr, x1, y1, side, angle):
        # looks like some of the menu drawing functions does not
        # call stroke() at the end of drawing
        # TODO: find which one is it and remove stroke() from here
        cr.stroke()

        cr.set_source_rgb(1.0, 1.0, 0.0)
        cr.save()
        cr.translate(x1, y1)
        cr.rotate(math.radians(angle))
        # inside area
        cr.move_to(0, side/2.0) # tip of the arrow
        cr.line_to(-side/3.0, -side/2.0) # left extreme
        cr.line_to(0, -side/5.0) # arrow inset
        cr.line_to(side/3.0, -side/2.0) # right extreme
        cr.fill()
        cr.set_source_rgb(0.0, 0.0, 0.0)
        cr.set_line_width(6)
        cr.move_to(0, side/2.0) # tip of the arrow
        cr.line_to(-side/3.0, -side/2.0) # left extreme
        cr.line_to(0, -side/5.0) # arrow inset
        cr.line_to(side/3.0, -side/2.0) # right extreme
        cr.close_path()
        cr.stroke()

        # draw middle indicator
        cr.set_source_rgb(0.0, 0.0, 0.0)
        cr.arc(0, 0, 16, 0, 2.0 * math.pi)
        cr.fill()


        cr.restore()






        #
        #cr.set_source_rgb(1.0, 1.0, 0.0)
        #cr.save()
        #cr.translate(x1, y1)
        #cr.rotate(math.radians(angle))
        #cr.move_to(-10, 15)
        #cr.line_to(10, 15)
        #cr.line_to(0, -15)
        #cr.fill()
        #cr.set_source_rgb(0.0, 0.0, 0.0)
        #cr.set_line_width(3)
        #cr.move_to(-10, 15)
        #cr.line_to(10, 15)
        #cr.line_to(0, -15)
        #cr.close_path()
        #cr.stroke()
        #cr.restore()