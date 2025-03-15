API using Python with Flask and Gunicorn module.

to run with flask:
1. flask --app api run
   
2. python3 api.py

to run with gunicorn
1. gunicorn --config gunicorn_config.py api:app   OR
2. python3 -m gunicorn -w 4 -b 0.0.0.0:8000 api:app

docker had been push to dockerhub

API sample for rds
https://<URL>?country_id=NLD

memcache.py use HR schema from oracle dev 23ai vm
