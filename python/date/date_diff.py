import datetime



now = datetime.datetime.now()

then = datetime.datetime.strptime('2025-08-16', "%Y-%m-%d")

diff = then - now
print(f"Time until {then}: {diff.days} days")