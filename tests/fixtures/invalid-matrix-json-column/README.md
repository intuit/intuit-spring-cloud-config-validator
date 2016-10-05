# ctg-config

Configuration repository for the TTU server application family, from TTU Android, iOS, etc.

## Server

* PROD: http://builder-1.hub.docker.intuit.net:81
* DEV: http://config-server.ttu.corp.intuit.net

Note that the DEV server cannot be reached by Publisher.

## Config URLS

* application.properties
 * Metadata: http://config-server.ttu.corp.intuit.net/application/default
 * JSON: http://config-server.ttu.corp.intuit.net/application-default.json

* ttu/ttu.yml
 * Metadata: http://config-server.ttu.corp.intuit.net/ttu/default
 * JSON: http://config-server.ttu.corp.intuit.net/ttu-default.json

* ttu/ttu-android.yml
 * Metadata: http://config-server.ttu.corp.intuit.net/ttu/android
 * JSON: http://config-server.ttu.corp.intuit.net/ttu-android.json

* ttu/ios.yml, ttu/ttu-2.7.yml, ttu/ttu-ios_8.0.yml
 * Metadata: http://config-server.ttu.corp.intuit.net/ttu/ios,2.7,ios_8.0
 * JSON: http://config-server.ttu.corp.intuit.net/ttu-ios,2.7,ios_8.0.json
