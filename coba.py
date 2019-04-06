from datetime import datetime, date, timedelta


f = 13.949999999999999
a= float("{0:.2f}".format(f))
print(a)
d=datetime.now() + timedelta(hours=1.5)
# d=datetime.now().hour
print(d)
print(type(d))