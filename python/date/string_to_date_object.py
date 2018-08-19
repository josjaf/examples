import datetime

# string to date time object
date_string = "2018-08-18 15:41:51.970478".rsplit(":", 1)[0]
date_object =  datetime.datetime.strptime(date_string, "%Y-%m-%d %H:%M")

# strip off the seconds
created_time = datetime.datetime.strptime('2018-08-16T20:11:20.6724986Z'.rsplit(".", 1)[0], "%Y-%m-%dT%H:%M:%S")



dt = datetime.datetime.strptime("21/11/06 16:30", "%d/%m/%y %H:%M")

