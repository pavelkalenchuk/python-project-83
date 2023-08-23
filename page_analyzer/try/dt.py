import datetime as dt

a = dt.datetime.now()

print(a)
print(type(a))

b = str(a)
print(b)
print(type(b))

z = a.strftime('%Y-%m-%d')
print(z)
