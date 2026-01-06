import time
import random
from prometheus_client import start_http_server, Gauge, Counter


#--------------------------------------(METRICS)--------------------------------------
# Gauge can go up & down. It represents current state.
# Use it for things like...
# Active users, Memory usage, Queue depth, CPU temp, Current sessions
active_users = Gauge(
    "active_users",
    "Number of active users",
    ["app", "env", "region"]
)

# Counter only ever goes up. It resets when process restarts.
# Use it for things like...
# Total requests, Total logins, Total errors, Total bytes sent
# You never graph a counter directly, you use things like ex:
# rate(requests_total[10s]) or increase(requests_total[1m])
requests_total = Counter(
    "requests_total",
    "Total number of requests",
    ["app", "env", "endpoint", "method", "status_class"]
)
#-------------------------------------------------------------------------------------


#--------------------------------------(MAIN)-----------------------------------------
if __name__ == "__main__":
    # Expose metrics on http://localhost:9090
    # In there type ex a command like...
    # up, active_users or rate(requests_total[10s]) or requests_total
    # Note tha rate function does not show the raw counter value in the ex above
    # it shows the average requests per second over 10 secs, because rate calculates the slope
    # ==================================================

    #This is the target for this python program to be called from prometheus
    start_http_server(8000)
    #Prometheus groups targets into jobs ex from the yaml job_name: "prometheus"
    #So this python script is A Target inside A Job exposing Metrics

    while True:
        # Know that in these scraped endpoints even if they are time series or just metrics
        # prometheus auto adds a label called an "instance" so if prometheus
        # auto added instance="localhost:8000 " then if you ran 5 copies the instances generated would be
        #instance="10.0.1:8000" and instance="10.0.0.2:8000" and so on
        #these 5 copies can either be 5 different scraped endpoints in one script, like here we have 3 scraped enpoints
        #or it can mean 1 scraped endpoints but having 5 of this python script ran at the same time.

        #==================================================
        # Below are examples of (metric_name) and we call this just metrics or more generic a "scraped endpoint"
        # Simulated data WITHOUT rich meta-data
        #active_users.set(random.randint(10, 100))
        #requests_total.inc(random.randint(1, 5))


        # ==================================================
        #Below are examples of (metric_name + label sets) and we call "time series" or more generic a "scraped endpoint"
        # Simulated active users with rich meta-data (state)
        active_users.labels(
            app="prometheus notes",
            env="BAD Anaconda environment",
            region="us-east-1"
        ).set(random.randint(40,90))

        # ==================================================
        # Simulated requests (events) with rich meta-data
        requests_total.labels(
            app="prometheus notes",
            env="BAD Anaconda environment",
            endpoint="/login",
            method="POST",
            status_class="2xx"
        ).inc(random.randint(1,5))

        requests_total.labels(
            app="prometheus notes",
            env="BAD Anaconda environment",
            endpoint="/login",
            method="POST",
            status_class="4xx"
        ).inc(random.randint(0,2))
        # ==================================================



        time.sleep(1) #Every N sec.
#-------------------------------------------------------------------------------------
