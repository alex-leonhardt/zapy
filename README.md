# zapy

Run Zed Attack Proxy from command line

## pre-requisites

* ZAP must be running on the same host you're running this script on
* Java (for ZAP)
* Several python packages, do a ```pip install -r requirements.txt```

## run (show help)

```
./zapy.py -h
```

### run spider only

```
./zapy.py -t http://127.0.0.1 -s
```

### run attack + spider 

```
./zapy.py -t http://127.0.0.1 -s -a 
```

### run attack + spider + create html report 

```
./zapy.py -t http://127.0.0.1 -s -a --html-report /data/scan-report.html 
```

If a report already exists, the script will not generate the report, re-run with:

```
./zapy.py -t http://127.0.0.1 -s -a --html-report /data/scan-report.html --force 
```

### set the api key

```
./zapy.py -t http://127.0.0.1 --spider --active-scan --html-report /data/scan-report.html --force --api-key aaabbbccddeeffgghh332211 
```

## spider

spidering now works, use ```-s``` to run the spider against ```TARGET```

## attack

this is now working, use ```-a``` to launch an attack against ```TARGET```

## basic auth

you're now able to configure basic auth to a target by setting 

```--auth``` 

this will require you to also specify 

```--authuser``` (the user you want to authenticate with) 

and 

```--authpass``` (the password for that user)

*Only for HTTP Basic Authentication is currently working*


## html reports

use ```--html-report /path/to/report.html``` to create a report in /path/to

## docker

#### create your own docker file using OWASP's weekly as base

```
docker build -t me/zap:latest .
```

#### run it

docker run --rm -ti -v `pwd`:/data me/zap python /zapy/zapy.py \
    -t http://172.17.0.10 \
    -s \
    --start \
    -k zap \
    --html-report /data/report.html

## todo

- add ability to install plugins into /opt/zap/plugins (once api supports this)
- add ability to only run a specific scan against a target or url 
- maybe run fuzzer against a specific url (?)

## references 

* https://github.com/zaproxy/zaproxy/wiki/ApiGen_Full

## license

The MIT License (MIT)

Copyright (c) 2015 Alex Leonhardt

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

