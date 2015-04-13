# Slashproc_parsers #

pip install git+git://github.com/niallobyrnes/slashproc_parsers.git

### What is this repository for? ###

* Scraping the /proc directory and returning a python dictionary
* Version 0.1
* There will be no dependencies for this repo

### Contact ###

* nobyrnes@icloud.com

### Examples ###

curl -X POST http://localhost:8848 -d '{"method": "get_parsers", "id":"1"}}'
curl -X POST http://localhost:8848 -d '{"method": "get_groups", "id":"2", "params":{"path":"/proc/uptime"}}'
curl -X POST http://localhost:8848 -d '{"method": "get_vars", "id":"3", "params":{"path":"/proc/uptime"}}'
curl -X POST http://localhost:8848 -d '{"method": "get_data", "id":"4", "params":{"path":"/proc/uptime/total"}}'
curl -X POST http://localhost:8848 -d '{"method": "get_data", "id":"5", "params":{"parser":"uptime", "get":"total"}}'


import requests
addr = "http://localhost:8848"

requests.post(addr, data='{"method": "get_parsers", "id":10}').json()

requests.post(addr, data='{"method": "get_groups", "params":{"parser": "cpuinfo"}, "id":11}').json()

requests.post(addr, data='{"method": "get_vars", "params":{"path": "cpuinfo/xtopology"}, "id":13}').json()

requests.post(addr, data='{"method": "get_data", "params":{"parser": "cpuinfo", "get": "model_name"}, "id":10}').json()

requests.post(addr, data='{"method": "get_data", "params":{"parser": "cpuinfo", "get":"bogomips, core_id"}, "id":12}').json()













