import redis

r = redis.Redis(host='localhost',port=6379)
r.config_set("notify-keyspace-events", "AKE")
