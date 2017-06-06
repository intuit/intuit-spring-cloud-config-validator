# spring-cloud-config-validator

Python script that validates Spring Cloud Config configuration repos by analyzing `.json`, `.yaml`, `.yml` and `.properties`.

* Manual Validations
* Github Pre-receive Hook Status Validations: Commits and Pull Requests  

> *USER REFERENCE DOCUMENTATION*: For user reference and how-to, please go to the `Wiki page` of this repo clicking in the icon above. 

![Validation with errors](https://github.intuit.com/storage/user/42/files/91ffb398-3702-11e7-944c-813b1072db5e)

![GIthubValidator](https://github.intuit.com/services-configuration/spring-cloud-config-validator/wiki/images/enabled-spring-cloud-config-validator.png)

# Requirements

* Install Python 2.6+
* Install Pip https://pip.pypa.io/en/stable/installing/
 * Mac `sudo easy_install pip` 

```
$ curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | sudo python
```

Make sure you have the required versions:

```
$ python --version
Python 2.7.10

$ pip --version
pip 7.0.3 from /usr/local/lib/python2.7/dist-packages (python 2.7)
```

## Script Dependencies

You MUST install the required dependencies if you are running the script locally:

```
$ curl --user "mdesales:******" \       
 https://github.intuit.com/raw/servicesplatform-tools/spring-cloud-config-validator/master/requirements.txt > \
 requirements.txt && pip install --user -r requirements.txt
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100    24  100    24    0     0     30      0 --:--:-- --:--:-- --:--:--    30
Collecting pyyaml (from -r requirements.txt (line 1))
Collecting pyjavaproperties (from -r requirements.txt (line 2))
Installing collected packages: pyyaml, pyjavaproperties
Successfully installed pyjavaproperties pyyaml
```

At this point, you are ready to execute the script manually.

# Usage

* **Current Directory Validation**: Download and execute for a given directory using `curl`.
* **Multiple Directory Validation**: Download the script `validate-config-files.py` and execute it for a given directory path.
* **Exit Values**: The script returns `0 for success` or `1 for errors`.
* **Report**: Gives hints about the errors

## Execute current Directory

You can execute the script directly in the current directory by using your LDAP credentials to the script.

> $ curl --user "mdesales:******" \
  https://github.intuit.com/raw/servicesplatform-tools/spring-cloud-config-properties-verification/master/validate-config-files.py \
  | python

* Change `--user "mdesales:*****"` with your `LDAP` credentials. 

```
$ pwd
/home/mdesales/dev/github/intuit/servicesplatform-tools/spring-cloud-config-properties-verification

$ curl --user "mdesales:******" https://github.intuit.com/raw/servicesplatform-tools/spring-cloud-config\
                                              -properties-verification/master/validate-config-files.py | python
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  7946  100  7946    0     0  23442      0 --:--:-- --:--:-- --:--:-- 23439
##################################################
###### Intuit Spring Cloud Config Validator ######
##################################################
=> Validating directory /home/mdesales/dev/github/intuit/servicesplatform-tools/spring-cloud-config-properties-verification
✘ File /home/mdesales/dev/github/intuit/servicesplatform-tools/spring-cloud-config-properties-verification/ttu-ios_8.0.yml 
    is NOT valid: expected '<document start>', but found '<scalar>' 
    in "/home/mdesales/dev/github/intuit/servicesplatform-tools/spring-cloud-config-properties-verification/ttu-ios_8.0.yml", line 1, column 5
✔ File /home/mdesales/dev/github/intuit/servicesplatform-tools/spring-cloud-config-properties-verification/ttu-ios.yml is valid!
✘ File /home/mdesales/dev/github/intuit/servicesplatform-tools/spring-cloud-config-properties-verification/.matrix-android.json 
    is NOT valid: No JSON object could be decoded
✔ File /home/mdesales/dev/github/intuit/servicesplatform-tools/spring-cloud-config-properties-verification/ttu-android_N.yml is valid!
✔ File /home/mdesales/dev/github/intuit/servicesplatform-tools/spring-cloud-config-properties-verification/ttu-2.7.yml is valid!
✔ File /home/mdesales/dev/github/intuit/servicesplatform-tools/spring-cloud-config-properties-verification/.matrix-ios.json is valid!
✔ File /home/mdesales/dev/github/intuit/servicesplatform-tools/spring-cloud-config-properties-verification/ttu-android.yml is valid!
✔ File /home/mdesales/dev/github/intuit/servicesplatform-tools/spring-cloud-config-properties-verification/ttu-android_6.0.yml is valid!
✔ File /home/mdesales/dev/github/intuit/servicesplatform-tools/spring-cloud-config-properties-verification/ttu.yaml is valid!
✘ File /home/mdesales/dev/github/intuit/servicesplatform-tools/spring-cloud-config-properties-verification/application.properties 
    is NOT valid: local variable 'wspacere' referenced before assignment
```

## Execute for another Directory

You need to download the script and execute it, passing the parameter.

```
$ validate-config-files.py /another/springcloud/config/directory
```

# Examples

## Validation without errors

The execution of the script succeeds and returns 0.

![Validation without errors](https://github.intuit.com/storage/user/42/files/9701d376-3702-11e7-968b-a69ffb809b8b)

## Validation with errors

The execution of the script fails and returns 1.

![Validation with errors](https://github.intuit.com/storage/user/42/files/8df40bbe-3702-11e7-9d76-47c63599250e)

# Github Enterprise Pre-receive

You can follow the steps at https://help.github.com/enterprise/2.6/admin/guides/developer-workflow/creating-a-pre-receive-hook-script/ to include this script as a Pre-receive hook.

## Github Pre-receive failure

The execution of a pre-receive hook in Github prevents users from pushing code with errors. The validate script developed here can prevent users from publishing changes in Spring Cloud Config repos that can break the server. The example below shows the validation. 

* Github Change on a local workspace

![git change](https://github.intuit.com/storage/user/42/files/8afc1ac8-3702-11e7-9f7a-e8f8349616db)

* Git push fails when errors are in the files

![Github Pre-receive Failure](https://github.intuit.com/storage/user/42/files/21edf618-3703-11e7-86e6-bbc4f4e22555)

# Development

Everything you need to develop. Here are some requirements and utilities.

* Python 2.7+: We can use the discover mode for all tests on this version
 * https://docs.python.org/2/library/unittest.html#test-discovery


## Running all test cases suite

Make sure to run all the test cases after making changes to the script.

```
$ python -m unittest discover -v tests
test_all_matrix_json_files_are_invalid (test_invalid_matrix_json_validation.InvalidMatrixFileTests) ... The android matrix file is invalid
is tests/fixtures/invalid-matrix-json-column/ttu-android.yml valid? True
is tests/fixtures/invalid-matrix-json-column/.matrix-android.json valid? False ERROR: Extra data: line 2 column 11 - line 29 column 1 (char 11 - 394)
is tests/fixtures/invalid-matrix-json-column/ttu.yaml valid? True
is tests/fixtures/invalid-matrix-json-column/application.properties valid? True
is tests/fixtures/invalid-matrix-json-column/.matrix-ios.json valid? True
is tests/fixtures/invalid-matrix-json-column/ttu-ios.yml valid? True
ok
test_that_validation_index_is_dictionary (test_invalid_matrix_json_validation.InvalidMatrixFileTests) ... ok
test_all_properties_are_valid (test_all_valid_config_validation.AllSuccessfulTests) ... All config files are valid
is tests/fixtures/all-valid-config/.matrix.json valid? True
is tests/fixtures/all-valid-config/publisher-e2e.yml valid? True
is tests/fixtures/all-valid-config/publisher-onboard_prod.yml valid? True
is tests/fixtures/all-valid-config/publisher-prf.yml valid? True
is tests/fixtures/all-valid-config/publisher-qal.yml valid? True
is tests/fixtures/all-valid-config/publisher.properties valid? True
is tests/fixtures/all-valid-config/publisher-prd.yml valid? True
is tests/fixtures/all-valid-config/publisher-onboard_preprod.yml valid? True
is tests/fixtures/all-valid-config/publisher-dev.yml valid? True
ok
test_that_validation_index_is_dictionary (test_all_valid_config_validation.AllSuccessfulTests) ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.049s

OK
```

## Running individual test cases

Just use python with the `-m` switch to indicate the test module to be executed.

```
$ python -m tests.test_invalid_matrix_json_validation
test_all_matrix_json_files_are_invalid (__main__.InvalidMatrixFileTests) ... The android matrix file is invalid
is tests/fixtures/invalid-matrix-json-column/ttu-android.yml valid? True
is tests/fixtures/invalid-matrix-json-column/.matrix-android.json valid? False ERROR: Extra data: line 2 column 11 - line 29 column 1 (char 11 - 394)
is tests/fixtures/invalid-matrix-json-column/ttu.yaml valid? True
is tests/fixtures/invalid-matrix-json-column/application.properties valid? True
is tests/fixtures/invalid-matrix-json-column/.matrix-ios.json valid? True
is tests/fixtures/invalid-matrix-json-column/ttu-ios.yml valid? True
ok
test_that_validation_index_is_dictionary (__main__.InvalidMatrixFileTests) ... ok

----------------------------------------------------------------------
Ran 2 tests in 0.026s

OK
```

## Validating Pull Request execution.

Just update the data docker container with the new value.

```
~/dev/github/intuit/servicesplatform-tools/spring-cloud-config-validator on  feature/make-validator-oop! ⌚ 14:25:46
$ docker cp validate_config_files.py data:/home/git/test.git/hooks/pre-receive
```

Then, execute the command to push new commits to the test origin server.

```
~/dev/github/intuit/servicesplatform-tools/spring-cloud-config-validator/ttu-config on  master ⌚ 14:25:55
$ GIT_SSH_COMMAND="ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -p 52311 -i ../id_rsa" git push -u test master
Warning: Permanently added '[192.168.154.132]:52311' (ECDSA) to the list of known hosts.
Counting objects: 214, done.
Delta compression using up to 2 threads.
Compressing objects: 100% (100/100), done.
Writing objects: 100% (214/214), 21.50 KiB | 0 bytes/s, done.
Total 214 (delta 127), reused 184 (delta 109)
remote: ##################################################
remote: ###### Spring Cloud Config Validator 1.0.0 #######
remote: ##################################################
remote: Processing base=0000000000000000000000000000000000000000 commit=6ff408ac89564c994925c46847d775fff940caa3 ref=refs/heads/master
remote: => Validating SHA 6ff408ac89564c994925c46847d775fff940caa3
remote: ✘ File .matrix-android.json is NOT valid: Extra data: line 2 column 11 - line 29 column 1 (char 11 - 394)
remote: ✔ File .matrix-ios.json is valid!
To git@192.168.154.132:test.git
 ! [remote rejected] master -> master (pre-receive hook declined)
error: failed to push some refs to 'git@192.168.154.132:test.git'
```

## Code Coverage

> Based on the following: 
> * https://coverage.readthedocs.io/en/coverage-4.2/source.html#source
> * https://coverage.readthedocs.io/en/coverage-4.2/
> * https://github.com/audreyr/how-to/blob/master/python/use_coverage_with_unittest.rst
> * http://stackoverflow.com/questions/3312451/how-can-you-get-unittest2-and-coverage-py-working-together

You can generate the code coverage by running the following:

```
$ coverage run -m unittest discover -v tests         
test_some_yaml_yml_files_are_invalid (test_invalid_yaml_yml_multi_document_validation.InvalidYamlMultiDocumentFileTests) ... Some Yaml Multi documents are invalid
✔ is tests/fixtures/invalid-yaml-configs-multiple-documents-per-config/sp_boot_sample-prf.yml valid? True
✔ is tests/fixtures/invalid-yaml-configs-multiple-documents-per-config/sp_boot_sample-dev.yml valid? True
✘ is tests/fixtures/invalid-yaml-configs-multiple-documents-per-config/sp_boot_sample-e2e.yml valid? False ERROR: expected '<document start>', but found '<block mapping start>'
...
...
✔ is tests/fixtures/all-valid-config/publisher-onboard_preprod.yml valid? True
✔ is tests/fixtures/all-valid-config/application-multi-documents.yml valid? True
✔ is tests/fixtures/all-valid-config/publisher-dev.yml valid? True
ok
test_that_validation_index_is_dictionary (test_all_valid_config_validation.AllSuccessfulTests) ... ok

----------------------------------------------------------------------
Ran 10 tests in 0.258s

OK
```

You can view the Code Coverage reports in the terminal as follows:

```
$ coverage report
Name                       Stmts   Miss  Cover
----------------------------------------------
validate_config_files.py     144     63    56%
```

Or you can view the HTML reports, just like the following:

```
coverage html
open html_cov/index.html
```

# Production Deployment

You need to generate a Docker image with the environment of the Validator using
the repo https://github.intuit.com/docker/github, along with the Dockerfile in 
this repo.

* Base the image following: https://help.github.com/enterprise/2.6/admin/guides/developer-workflow/creating-a-pre-receive-hook-environment/#creating-a-pre-receive-hook-environment-using-docker.
  * Build the base Image
  * Build the Validator Image
* Export the Docker environment as `tar.gz`
* Test it locally.
* Test it in https://github-dev.intuit.com
* Open a ticket at the `GIT` Jira project for integration with PROD.

## Build the Base Image

```
$ docker build -f Dockerfile.pre-receive -t github-enterprise-pre-receive-hook-base .
Sending build context to Docker daemon  66.56kB
Step 1/6 : FROM gliderlabs/alpine:3.3
3.3: Pulling from gliderlabs/alpine
ebf4d2c9f0ef: Pull complete
a3ed95caeb02: Pull complete
Digest: sha256:144c17928bb34f18179403d70384414ab25a289c0793af6620b67d3ee21cbcb5
Status: Downloaded newer image for gliderlabs/alpine:3.3
 ---> eb784592c2f8
Step 2/6 : MAINTAINER Marcello_deSales@intuit.com
 ---> Running in 87b33d48a18e
 ---> a07b3d5f70d9
Removing intermediate container 87b33d48a18e
Step 3/6 : RUN apk add --no-cache git openssh bash python py-pip &&   pip install --upgrade pip &&   ssh-keygen -A &&   sed -i "s/#AuthorizedKeysFile/AuthorizedKeysFile/g" /etc/ssh/sshd_config &&   adduser git -D -G root -h /home/git -s /bin/bash &&   passwd -d git &&   su git -c "mkdir /home/git/.ssh &&   ssh-keygen -t rsa -b 4096 -f /home/git/.ssh/id_rsa -P '' &&   mv /home/git/.ssh/id_rsa.pub /home/git/.ssh/authorized_keys &&   mkdir /home/git/test.git &&   git --bare init /home/git/test.git"
 ---> Running in 6538221061d0
fetch http://alpine.gliderlabs.com/alpine/v3.3/main/x86_64/APKINDEX.tar.gz
fetch http://alpine.gliderlabs.com/alpine/v3.3/community/x86_64/APKINDEX.tar.gz
(1/22) Installing ncurses-terminfo-base (6.0-r6)
(2/22) Installing ncurses-terminfo (6.0-r6)
(3/22) Installing ncurses-libs (6.0-r6)
(4/22) Installing readline (6.3.008-r4)
(5/22) Installing bash (4.3.42-r6)
Executing bash-4.3.42-r6.post-install
(6/22) Installing openssl (1.0.2k-r0)
(7/22) Installing ca-certificates (20161130-r0)
(8/22) Installing libssh2 (1.6.0-r1)
(9/22) Installing curl (7.52.1-r1)
(10/22) Installing expat (2.1.1-r1)
(11/22) Installing pcre (8.38-r1)
(12/22) Installing git (2.6.6-r0)
(13/22) Installing openssh-client (7.2_p2-r3)
(14/22) Installing openssh-sftp-server (7.2_p2-r3)
(15/22) Installing openssh (7.2_p2-r3)
(16/22) Installing libbz2 (1.0.6-r4)
(17/22) Installing libffi (3.2.1-r2)
(18/22) Installing gdbm (1.11-r1)
(19/22) Installing sqlite-libs (3.9.2-r0)
(20/22) Installing python (2.7.12-r0)
(21/22) Installing py-setuptools (18.8-r0)
(22/22) Installing py-pip (7.1.2-r0)
Executing busybox-1.24.2-r1.trigger
Executing ca-certificates-20161130-r0.trigger
OK: 81 MiB in 33 packages
Collecting pip
  Downloading pip-9.0.1-py2.py3-none-any.whl (1.3MB)
Installing collected packages: pip
  Found existing installation: pip 7.1.2
    Uninstalling pip-7.1.2:
      Successfully uninstalled pip-7.1.2
Successfully installed pip-9.0.1
ssh-keygen: generating new host keys: RSA DSA ECDSA ED25519
Password for git changed by root
Generating public/private rsa key pair.
Your identification has been saved in /home/git/.ssh/id_rsa.
Your public key has been saved in /home/git/.ssh/id_rsa.pub.
The key fingerprint is:
SHA256:bdkjJt2tMpsAQpnTSTggtJLydoGxTXF5PONj9Hte1iM git@03c849f93444
The key's randomart image is:
+---[RSA 4096]----+
|o.o.oooo         |
| o.*o*..*        |
|+.o B.o+ +       |
|o. . o  +o.+ .   |
|  o o ..S.B.+ .. |
| . . . . +...Eo..|
|        . oo.o. .|
|         . =.    |
|          o      |
+----[SHA256]-----+
Initialized empty Git repository in /home/git/test.git/
 ---> ec5d5e5dffbf
Removing intermediate container 6538221061d0
Step 4/6 : VOLUME /home/git/.ssh /home/git/test.git/hooks
 ---> Running in 444b3582ba16
 ---> dabecc6b117c
Removing intermediate container 444b3582ba16
Step 5/6 : WORKDIR /home/git
 ---> 0bb6afae2a22
Removing intermediate container e563010c2cac
Step 6/6 : CMD /usr/sbin/sshd -D
 ---> Running in 8ea4e5cde242
 ---> c47928816175
Removing intermediate container 8ea4e5cde242
Successfully built c47928816175
Successfully tagged github-enterprise-pre-receive-hook-base:latest
```

## Build the Validator Image

```
$ docker build -f Dockerfile.spring-cloud-config-validation -t springboot-config-verification .
Sending build context to Docker daemon  594.4kB
Step 1/4 : FROM github-enterprise-pre-receive-hook-base
 ---> c47928816175
Step 2/4 : MAINTAINER Marcello_deSales@intuit.com
 ---> Using cache
 ---> 5fdcf852ec6d
Step 3/4 : RUN apk add --no-cache py-pip &&   pip install yamllint pyyaml pyjavaproperties
 ---> Using cache
 ---> a9336ec4e702
Step 4/4 : ADD ./validate_config_files.py /home/git/test.git/hooks/pre-receive
 ---> b69fb82ef455
Removing intermediate container d3a1d2d5e3ae
Successfully built b69fb82ef455
Successfully tagged springboot-config-verification:latest
```

## Export the Docker Environment as tar.gz

* Run a container

```
$ docker create --name springboot-config-verification springboot-config-verification /bin/true
d7e0a13505b4d01c91ce30b408d35910bcbd872a5ed24b0b2b8857769e591929
```

* Export the image as tar.gz

```
$ docker export springboot-config-verification | gzip > spring-cloud-config-validator-v1.1.0.tar.gz
$ ls -lah spring-cloud-config-validator-v1.1.0.tar.gz
-rw-r--r--  1 mdesales  CORP\Domain Users    27M Jun  5 18:25 spring-cloud-config-validator-v1.1.0.tar.gz
```

## Open GIT jira ticket

* Open a ticket like the following, attaching the environment to the ticket: https://jira.intuit.com/browse/GIT-778.
* Talk to Eric Castle in Slack for the procedure.


## Test in Github Dev

Once the environment has been uploaded to the dev environment, push the current script to it.

```
$ git remote add dev git@github-dev.intuit.com:services-configuration/spring-cloud-config-validator.git

$ git fetch dev
remote: Counting objects: 51, done.
remote: Compressing objects: 100% (19/19), done.
remote: Total 51 (delta 34), reused 49 (delta 32), pack-reused 0
Unpacking objects: 100% (51/51), done.
From github-dev.intuit.com:services-configuration/spring-cloud-config-validator
 * [new branch]      master     -> dev/master

$ git fetch dev
remote: Counting objects: 51, done.
remote: Compressing objects: 100% (19/19), done.
remote: Total 51 (delta 34), reused 49 (delta 32), pack-reused 0
Unpacking objects: 100% (51/51), done.
From github-dev.intuit.com:services-configuration/spring-cloud-config-validator
 * [new branch]      master     -> dev/master
```

From now on, you can make changes to the validator and verify it using the
test repos specified below.

## Test repos for validation

Now you can test the configuration in the Config Repos:

* https://github-dev.intuit.com/MDESALES/config-repo
* https://github-dev.intuit.com/MDESALES/spring-cloud-config-publisher-config

> NOTE: Make sure the validator is enabled in those repos.

## Prod environment

Once you have verified that it works, ask Eric Castle to update the PROD environment
with the new Docker image.
