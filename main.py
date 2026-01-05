import time
import random
from prometheus_client import start_http_server, Gauge, Counter


#--------------------------------------(METRICS)--------------------------------------
# Gauge can go up & down. It represents current state.
# Use it for things like...
# Active users, Memory usage, Queue depth, CPU temp, Current sessions
active_users = Gauge(
    "active_users",
    "Number of active users"
)

# Counter only ever goes up. It resets when process restarts.
# Use it for things like...
# Total requests, Total logins, Total errors, Total bytes sent
# You never graph a counter directly, you use things like ex:
# rate(requests_total[10s]) or increase(requests_total[1m])
requests_total = Counter(
    "requests_total",
    "Total number of requests"
)
#-------------------------------------------------------------------------------------


#--------------------------------------(MAIN)-----------------------------------------
if __name__ == "__main__":
    # Expose metrics on http://localhost:9090
    # In there type ex a command like...
    # up, active_users or rate(requests_total[10s]) or requests_total
    # Note tha rate function does not show the raw counter value in the ex above
    # it shows the average requests per second over 10 secs, because rate calculates the slope
    start_http_server(8000)

    while True:
        # Simulated data
        active_users.set(random.randint(10, 100))
        requests_total.inc(random.randint(1, 5))

        time.sleep(1)
#-------------------------------------------------------------------------------------
