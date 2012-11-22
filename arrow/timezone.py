from datetime import datetime, timedelta, tzinfo
from dateutil import tz

import re

class TimeZone(object):

    tz_re = re.compile(r'(\+|\-)([0-9]{1,2}):([0-9]{1,2})')

    def __init__(self, time_zone=None):

        if time_zone is None or time_zone == 'UTC':
            time_zone = tz.tzutc()

        self._tzinfo, self._name = self._parse(time_zone)

    def __str__(self):

        minutes = self.utcoffset.total_seconds() / 60.0
        hours = int(minutes / 60)
        minutes = minutes - hours * 60

        offset_str = '{0:+03g}:{1:02g}'.format(hours, abs(minutes))

        return '{0} ({1})'.format(offset_str, self.name)

    def __repr__(self):
        return '{0}({1})'.format(self.__class__.__name__, self.__str__())

    @staticmethod
    def _parse(tz_expr):

        _tzinfo = None
        name = None

        if isinstance(tz_expr, TimeZone):
            _tzinfo = tz_expr.tzinfo
            name = tz_expr.name

        elif isinstance(tz_expr, str):
            _tzinfo, name = TimeZone._parse_str(tz_expr)

        elif isinstance(tz_expr, tzinfo):
            _tzinfo = tz_expr
            name = tz_expr.tzname(tz_expr) # correct?

        elif isinstance(tz_expr, timedelta):
            _tzinfo = tz.tzoffset(None, tz_expr.total_seconds())
            name = None

        if _tzinfo is None:
            raise ValueError('Could not recognize time zone')

        return _tzinfo, name

    @staticmethod
    def _parse_str(tz_expr):

        _tzinfo = None
        name = None

        if tz_expr == 'local':
            _tzinfo = tz.gettz()
            name = tz_expr

        else:

            iso_match = TimeZone.tz_re.match(tz_expr)

            if iso_match:
                sign, hours, minutes = iso_match.groups()
                seconds = int(hours) * 3600 + int(minutes) * 60

                if sign == '-':
                    seconds *= -1

                _tzinfo = tz.tzoffset(None, seconds)

            else:
                _tzinfo = tz.gettz(tz_expr)
                name = tz_expr

        return _tzinfo, name

    @property
    def name(self):
        return self._name

    @property
    def utcoffset(self):
        dt = datetime.now(self._tzinfo)
        return self._tzinfo.utcoffset(dt)

    @property
    def utc(self):
        return self.utcoffset.total_seconds() == 0.0

    @property
    def tzinfo(self):
        return self._tzinfo
