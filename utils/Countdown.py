from datetime import datetime, timedelta


class Countdown:

    date = None
    errorMessage = ''

    def __init__(self, _format: str):
        self.date = datetime.now()
        second = 0
        minute = 0
        hour = 0
        day = 0
        week = 0
        month = 0
        year = 0
        currentCharacters = ''
        for fc in _format:
            if self.is_number(s=fc):
                currentCharacters = currentCharacters + fc
                continue
            if fc == 's':
                if currentCharacters == '':
                    self.error('Please enter a valid time format.')
                    break
                if int(currentCharacters) <= 0:
                    self.error('0 and negative values are not allowed in time format.')
                    break
                second = int(currentCharacters)
                currentCharacters = ''
            if fc == 'o':
                if currentCharacters == '':
                    self.error('Please enter a valid time format.')
                    break
                if int(currentCharacters) <= 0:
                    self.error('0 and negative values are not allowed in time format.')
                    break
                minute = int(currentCharacters)
                currentCharacters = ''
            if fc == 'm':
                if currentCharacters == '':
                    self.error('Please enter a valid time format.')
                    break
                if int(currentCharacters) <= 0:
                    self.error('0 and negative values are not allowed in time format.')
                    break
                month = int(currentCharacters)
                currentCharacters = ''
            if fc == 'h':
                if currentCharacters == '':
                    self.error('Please enter a valid time format.')
                    break
                if int(currentCharacters) <= 0:
                    self.error('0 and negative values are not allowed in time format.')
                    break
                hour = int(currentCharacters)
                currentCharacters = ''
            if fc == 'd':
                if currentCharacters == '':
                    self.error('Please enter a valid time format.')
                    break
                if int(currentCharacters) <= 0:
                    self.error('0 and negative values are not allowed in time format.')
                    break
                day = int(currentCharacters)
                currentCharacters = ''
            if fc == 'w':
                if currentCharacters == '':
                    self.error('Please enter a valid time format.')
                    break
                if int(currentCharacters) <= 0:
                    self.error('0 and negative values are not allowed in time format.')
                    break
                week = int(currentCharacters)
                currentCharacters = ''
            if fc == 'y':
                if currentCharacters == '':
                    self.error('Please enter a valid time format.')
                    break
                if int(currentCharacters) <= 0:
                    self.error('0 and negative values are not allowed in time format.')
                    break
                year = int(currentCharacters)
                currentCharacters = ''
        while year >= 1:
            month += 12
            year -= 1
        while month >= 1:
            day += 30
            month -= 1

        timedelta_ = timedelta(seconds=second, minutes=minute, hours=hour, days=day)
        newDate = self.date + timedelta_
        self.date = newDate
            
    def getDate(self):
        return self.date

    def error(self, msg: str):
        self.errorMessage = msg
    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False

def timeToNow(time: str):
    ts = time_to_now_in_seconds(time)

    if ts <= 0:
        return  "unknow time"
    msg = ''
    second = ts
    minute = 0
    hour = 0
    day = 0
    week = 0
    month = 0
    year = 0
    while second >= 60:
        minute += 1
        second -= 60
    while minute >= 60:
        hour += 1
        minute -= 60
    while hour >= 24:
        day += 1
        hour -= 24
    while week >= 1:
        day += 7
        week -= 1
    while day >= 30:
        month += 1
        day -= 30
    while month >= 12:
        year += 1
        month -= 12
    if year != 0:
        msg = msg+str(year)+' year '
    if month != 0:
        msg = msg+str(month)+' month '
    if day != 0:
        msg = msg+str(day)+' day '
    if hour != 0:
        msg = msg+str(hour)+' hour '
    if minute != 0:
        msg = msg+str(minute)+' minute '
    if second != 0:
        msg = msg+str(second)+' second '
    
    return msg

def time_to_now_in_seconds(time: str):
    y = int(time[0:4])
    m = int(time[5:7])
    d = int(time[8:10])
    h = int(time[11:13])
    o = int(time[14:16])
    s = int(time[17:19])
    now = datetime.now()
    date = datetime(y, m, d, h, o, s)
    x = date - now

    ts = int(x.total_seconds())

    return ts
