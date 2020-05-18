import time


# local_t = time.localtime()
# print(f"Local time: {local_t}")

# ctime = time.ctime()
# print(f"Ctime is: {ctime}")

time_stamp = time.time()
print(f"Time stamp: {time_stamp}")

str = '1689441934.089837'
time_stamp_new = time.time(str)
print(time_stamp_new)

# strf_time = time.strftime("%Y-%m-%d", local_t)
# print(f"Strftime is: {strf_time}")

# strftime = '2020-05-14 10:00:01'
# strp_time = time.strptime(strftime, '%Y-%m-%d %H:%M:%S')
# print(f"The strfp time is: {strp_time}")

# import datetime

# curr_time = datetime.datetime.now()
# print("Current time: ", curr_time)
# print("seconds:      ", curr_time + datetime.timedelta(seconds=1))
# print("minutes:      ", curr_time + datetime.timedelta(minutes=1))
# print("hours:        ", curr_time + datetime.timedelta(hours=1))
# print("days:         ", curr_time + datetime.timedelta(days=1))
# print("weeks:        ", curr_time + datetime.timedelta(weeks=1))

# from datetime import date
# today = date.today()
# print("Today: ", today)
# print("Ctime: ", today.ctime())
# print("Struct_time: ", today.timetuple())
# print("Year: ", today.year)
# print("Month: ", today.month)
# print("Day: ", today.day)


# import datetime
 
# print('Now    :', datetime.datetime.now())
# print('Today  :', datetime.datetime.today())
# print('UTC Now:', datetime.datetime.utcnow())
 
# d = datetime.datetime.now()
# for attr in [ 'year', 'month', 'day', 'hour', 'minute', 'second', 'microsecond']:
#     print(attr, ":", getattr(d, attr))


