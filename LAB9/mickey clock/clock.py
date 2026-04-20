import datetime



class Clock:

    def currently_time(self):

        now = datetime.datetime.now()

        seconds_angles = now.second * 6

        minutes_angles = now.minute * 6

        return minutes_angles, seconds_angles