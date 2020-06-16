# Webinar Introduction to Hawkbit

## Start Hawkbit Server

See Documentation here: https://hub.docker.com/r/hawkbit/hawkbit-update-server

or simply run

```docker
docker run -d -p 8080:8080 hawkbit/hawkbit-update-server
```

## Create a Device in UI

* Create a Device with `{device-name}`
* Go to the Device and look for the secret token
* Enter Both in the top of the python script

## Prepare a Distribution (App!)

* Upload a File
* Create a Software Module (App)
* Add File to Software Module
* Create a Distribution (App)
* Add Software Module to Distribution

## Schedule an Update

* Drag Software Module onto Device
