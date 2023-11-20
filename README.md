# GEM-SPASS coding challenge

## Setup
```
# Clone the repository
git clone https://github.com/flyingbot91/gem-spass.git
# Prepare the virtual environment
cd gem-spass
python3 -m venv env
source env/bin/activate
env/bin/python -m pip install --upgrade pip
env/bin/python -m pip install -r requirements.txt
# Run server
python3 gem/manage.py runserver 0.0.0.0:8888
```

## How to test

I have included a few **JSON** test files in the **./data** folder.

In order to test the application you can use [curl](https://curl.se/docs/manpage.html). For example:

```
curl -v --header "Content-Type: application/json" -d @./data/payload1.json http://localhost:8888/productionplan/
* processing: http://localhost:8888/productionplan/
*   Trying [::1]:8888...
* connect to ::1 port 8888 failed: Conexión rehusada
*   Trying 127.0.0.1:8888...
* Connected to localhost (127.0.0.1) port 8888
> POST /productionplan/ HTTP/1.1
> Host: localhost:8888
> User-Agent: curl/8.2.1
> Accept: */*
> Content-Type: application/json
> Content-Length: 887
> 
< HTTP/1.1 200 OK
< Date: Mon, 20 Nov 2023 00:01:59 GMT
< Server: WSGIServer/0.2 CPython/3.11.6
< Content-Type: application/json
< X-Frame-Options: DENY
< Content-Length: 212
< X-Content-Type-Options: nosniff
< Referrer-Policy: same-origin
< Cross-Origin-Opener-Policy: same-origin
< 
* Connection #0 to host localhost left intact
[{"name": "windpark1", "p": 90.0}, {"name": "windpark2", "p": 21.6}, {"name": "gasfiredbig1", "p": 368.4}, {"name": "gasfiredbig2", "p": 0}, {"name": "gasfiredsomewhatsmaller", "p": 0}, {"name": "tj1", "p": 0.0}]hans@hans-desktop:~/proyectos/github/gem$ 
```

## Logging

Logs can be found at **/tmp/gem.log**.
