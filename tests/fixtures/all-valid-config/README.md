# spring-cloud-config-publisher-config

The configuration for the Config Publisher server.

# Onboarding Process

Please provide the following for your service:

* `githubOrgRepo`: The name of the github org/repo of the config repository that will register the webhook.
* `githubAccessToken`: The read-only token to clone the given `githubOrgRepo`. Must be provided with `{ciper}VALUE`.
* `githubWebhookSecret`: Utually wiill be `secret`. Must be provided with `{ciper}VALUE`.
* `awsAccessKey`: The AWS Access Key with write permission to the S3 bucket. Must be provided with `{ciper}VALUE`.
* `awsSecretKey`: The associated AWS Secret Key related to the access key. Must be provided with `{ciper}VALUE`.
* `awsS3Bucket` : The S3 bucket that will receive the configuration files.

Use the process below to encrypt the values required for the onboard (manual for now, using PR).

# Encrypt Values

Make calls to any Spring Cloud Config Server.

```
curl -v http://pdevespap30t.corp.intuit.net:9028/encrypt -d 76a837a2cfa362da69fc6080f7bd2e7db9b7c774
*   Trying 10.137.91.116...
* Connected to pdevespap30t.corp.intuit.net (10.137.91.116) port 9028 (#0)
> POST /encrypt HTTP/1.1
> Host: pdevespap30t.corp.intuit.net:9028
> User-Agent: curl/7.43.0
> Accept: */*
> Content-Length: 40
> Content-Type: application/x-www-form-urlencoded
>
* upload completely sent off: 40 out of 40 bytes
< HTTP/1.1 200 OK
< Server: Apache-Coyote/1.1
< intuit_tid: 9ed3a046-f173-4687-b43c-d6ce62621cb9
< X-Application-Context: spring_cloud_config_service:dev,qydc,onboard_preprod:8888
< Content-Type: text/plain;charset=UTF-8
< Content-Length: 432
< Date: Wed, 14 Sep 2016 17:29:41 GMT
<
* Connection #0 to host pdevespap30t.corp.intuit.net left intact
AQBYahdDXSf3/YTi0ymhmzvBR4t9ZF0PEjFk/8kbt0pbdAFB2uXWupd5IZySJmgUCw45y7JtKZeGduC6NqUhgEWi07Q3TYZ/ZDAWgcpgtaJ4+3M+zBEexJMkz9
pQMWmLnYfZtt04BHTb2muqffmd2QNudTSxtRyjlZBfmnoRO/1niEco5FVAUURRe7d4ed0kc4WeLHSMXdrv9Nf8zSa69FbkYZT/DH6t87pq4uV/PERF5EvQARFE
f+koKFLnyZy9qzRUYHOQ5giW7znDWgFBZVLLMA0cNvC7wKztidoeoDV9TETMHXPvcJixytRg79UgIShCkMgSv/RvM+9fPwFcE/lV/DxIxjF7KVQIQyxiWVZyah
X+Hiwt6N14jFlRJLdI+qwvyzF4Sc+S3CgRP65bfwbsFttJnvWr7bK95dGsXU4W7A==
```

# Decrypt values

Make sure to use a URL-Encoded version of the encrypted value when decoding.

* http://meyerweb.com/eric/tools/dencoder/
* http://stackoverflow.com/questions/296536/how-to-urlencode-data-for-curl-command/2236014#2236014

The example below uses the urllib python library to url encode the given encoded value from the previous step.

```
$ curl -v http://pdevespap30t.corp.intuit.net:9028/decrypt -d $(python -c "import urllib; print urllib.quote('''AQCe8VStE7x/rRfPcXZo3mMEjuNaS4A6TLkuhBXxrSi3f1TMDQyOb7a8wJwN2zHjtMF45K4MGzj7Jv0fUsfaze5SQu0DaAkVu/BJlg/32dtxB
OS6m1HtPQ3h6w/CrU5y4m29tniszjw1E7oQa6KEhgjvjOGeRTpoLg3DtcTZcxtuw5B+BOupoouBEZsc1P6WdozCcs4SHpMszw15F03VPMB41tfiN3Wu8d/jRGB4sP
5+vij+JGhxwcwKC4BPyuQEn2+g86FXflKRIQ58Qa3FfD7HBgQRfLjPiWnlY3D1dtVNBtzrLx1rKjiW8j50riAV43z8Hk0zRnkRC6syi48T0eRPn2xc6UB3W8vWDXZ
lpzediLgCBq1uM6A8cGAvaWBQj6Zz9O3SR7BImlm9/bHVYjQJ5sHZdG9tooq4qpagTkgBjw==''')")
*   Trying 10.137.91.116...
* Connected to pdevespap30t.corp.intuit.net (10.137.91.116) port 9028 (#0)
> POST /decrypt HTTP/1.1
> Host: pdevespap30t.corp.intuit.net:9028
> User-Agent: curl/7.43.0
> Accept: */*
> Content-Length: 444
> Content-Type: application/x-www-form-urlencoded
>
* upload completely sent off: 444 out of 444 bytes
< HTTP/1.1 200 OK
< Server: Apache-Coyote/1.1
< intuit_tid: 4538e4a5-48da-49e1-a895-eb12e7c594d1
< X-Application-Context: spring_cloud_config_service:dev,qydc,onboard_preprod:8888
< Content-Type: text/plain;charset=UTF-8
< Content-Length: 40
< Date: Wed, 14 Sep 2016 18:10:04 GMT
<
* Connection #0 to host pdevespap30t.corp.intuit.net left intact
76a837a2cfa362da69fc6080f7bd2e7db9b7c774
```

# Encrypted Config properties

Use the `'{cipher}VALUE'` value in your properties. An example is as follows:

https://github.intuit.com/servicesplatform-tools/spring-cloud-config-publisher-config/blob/master/publisher-onboard_preprod.yml

```yml
      githubAccessToken: '{cipher}AQAwqMO4JFlolzbvQNNhcV8a5yPFThVS6tP1gNkInrJkaym35b+b3gCP0ZL4gFlKM0u3oIdVEeUh0E3
         dcGh0Md+822l+I1JBOzQ6A2IY4GcmTVzvPjBq3W9SXHycV0/SoLHCTQcWC88U/OvkoJOXnfsRRhA/En/GwcxcU8u+iUitql8JUUVCUsW
         0plC6OXUK7ryFJFIj3cCL+wabpDOlnjMWV7jY6vWhS/5TZqGNIkx9T1jztADZKfmI98a9/OEXDTg0FTuYTGcma5Czkfnzo2pQGrYRx5y
         nmerc//3hdX9g6kyYw2TZT1EjOCuj/njflbvjqr2fjakDwBWflcb+p/1fe9n4nNddCfjv+l10K6DvO5Q9QnARk3F1U+SVSCQxf2UAYih
         +Gvy1+UXGuZ5KwPcSB3+a1Ml4j5Sz+gdfqHvwDg=='
```

# Creating/Rotating Keys

Create a JKS key

```
    $ keytool -genkeypair -alias publisher-key -keyalg RSA \
      -dname "CN=Intuit Config Publisher Server,OU=CTO,O=CTO-Dev,L=San Diego,S=CA,C=US" \
      -keypass Th3P0l1c3 -keystore server.jks -storepass Th3P0l1c3
```

## OPS must setup the properties in the config files of the server and/or client

Full details https://github.com/spring-cloud/spring-cloud-config/issues/453#issue-167727103. The configuration can be set in the application like the Publisher.

```yml
encrypt:
  keyStore:
    location: classpath:/server.jks
    password: Th3P0l1c3
    alias: publisher-key
    secret: Th3P0l1c3
```

Now you consume configurations.

# AWS S3 Bucket Setup

* Create a bucket with a regular name.
* Add the Bucket PUT Policy that requires encryption using `AES256` as described at http://docs.aws.amazon.com/cli/latest/reference/s3api/put-bucket-policy.html.
* You can use the CLI for that, Cloud Formation, Chef, etc.
 * http://docs.aws.amazon.com/cli/latest/topic/config-vars.html

```js
AWS_ACCESS_KEY_ID=AKI**O2A AWS_SECRET_ACCESS_KEY=eB6***Mga 
    aws s3api put-bucket-policy --bucket ttuconfig-preprod --policy file://policy.json

policy.json:
{
   "Policy":{
      "Version":"2012-10-17",
      "Statement":[
         {
            "Sid":"AddPerm",
            "Effect":"Allow",
            "Principal":"*",
            "Action":"s3:GetObject",
            "Resource":"arn:aws:s3:::ttuconfig-preprod/*"
         },
         {
            "Sid":"DenyUnEncryptedObjectUploads",
            "Effect":"Deny",
            "Principal":"*",
            "Action":"s3:PutObject",
            "Resource":"arn:aws:s3:::ttuconfig-preprod/*",
            "Condition":{
               "StringNotEquals":{
                  "s3:x-amz-server-side-encryption":"AES256"
               }
            }
         }
      ]
   }
}
```

* Validate that it is in place.

```js
AWS_ACCESS_KEY_ID=AKI**O2A AWS_SECRET_ACCESS_KEY=eB6***Mga 
    aws s3api get-bucket-policy --bucket ttuconfig-preprod | jq
{
   "Policy":{
      "Version":"2012-10-17",
      "Statement":[
         {
            "Sid":"AddPerm",
            "Effect":"Allow",
            "Principal":"*",
            "Action":"s3:GetObject",
            "Resource":"arn:aws:s3:::ttuconfig-preprod/*"
         },
         {
            "Sid":"DenyUnEncryptedObjectUploads",
            "Effect":"Deny",
            "Principal":"*",
            "Action":"s3:PutObject",
            "Resource":"arn:aws:s3:::ttuconfig-preprod/*",
            "Condition":{
               "StringNotEquals":{
                  "s3:x-amz-server-side-encryption":"AES256"
               }
            }
         }
      ]
   }
}
```
