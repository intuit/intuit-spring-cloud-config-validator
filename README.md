# Intuit Spring Cloud Config Validator

Github Enterprise pre-receive hook implementation for status validations: `Commits` and `Pull Requests` validated by running a python script that performs static validation of configuration repos used by Spring Cloud Config with `.json`, `.yaml`, `.yml` and `.properties` files. It implements the basic Pre-Receive hook steps detailed at https://help.github.com/enterprise/2.6/admin/guides/developer-workflow/creating-a-pre-receive-hook-script/.

<a link="https://github.com/intuit/intuit-spring-cloud-config-validator/wiki"><img width="1022" alt="pushing-error" src="https://user-images.githubusercontent.com/131457/56830365-00e62800-681b-11e9-883c-0a3fdd259b5f.png"></a>

Go to the [Wiki](https://github.com/intuit/intuit-spring-cloud-config-validator/wiki) for more information!

* Spring Cloud Config Validator Docker Image (Python)

[![resolution](http://dockeri.co/image/intuit/intuit-spring-cloud-config-validator "Github Enterprise Pre-Receive Hook Base Image")](https://hub.docker.com/r/intuit/intuit-spring-cloud-config-validator/)

* Golang, Python2 and Python3 images at the following:

[![resolution](http://dockeri.co/image/marcellodesales/github-enterprise-prereceive-hook-base "Github Enterprise Pre-Receive Hook Base Image")](https://hub.docker.com/r/marcellodesales/github-enterprise-prereceive-hook-base/)

# Validations

This is useful for teams using Spring Cloud Config repos and wants to be rest-assured that the configuration changes pushed to the repo won't break anything!

* [Validate Local Commits](https://github.com/intuit/intuit-spring-cloud-config-validator/wiki/Validate-Local-Commits)
* [Validate Online Commits](https://github.com/intuit/intuit-spring-cloud-config-validator/wiki/Validate-Online-Commits)
* [Validate Pull Requests](https://github.com/intuit/intuit-spring-cloud-config-validator/wiki/Validate-Files-In-Pull-Request)

# Setup

* `Docker Engine`: latest is recommended with `multi-stage` support
* `Docker Compose`: latest is recommended

Run the following to setup a local development environment:

1. `setup-github-simulator.sh`: Create a Git server with the pre-receive hook script `validate_config_files.py`
2. `test.sh`: test a given github config repo locally by attempting to push to the test git server

# Package for Github Enterprise

* You can package the latest version of this branch by making sure `.env` file has the following:
* VERSION: The version to apply the action
* ACTION: the action to perform
  * `pacakge` makes a tar.gz by building q docker image of the current files
  * `pull` downloads the given version from the Docker Registry

```sh
ACTION=package
VERSION=1.3.0
```

* Just run

```console
./package.sh
```

[![asciicast](https://asciinema.org/a/mzKWawCw5lZlhxIGOtHv1rJij.svg)](https://asciinema.org/a/mzKWawCw5lZlhxIGOtHv1rJij)



## Create Git Server

* Run the command `./setup-github-simulator.sh`

[![asciicast](https://asciinema.org/a/q8Y735uZ48fktw6rmlDXTY3sP.svg)](https://asciinema.org/a/q8Y735uZ48fktw6rmlDXTY3sP)

* The output shows the full command to run with `test.sh`

## Test Local Config Repo

* Change to the directory of your config repo
* Copy `test.sh` into your config repo
* Execute the command displayed
  * Branch `master` is always pushed
  * If the parameter `BRANCH=` is specified, the script will force `git push`

[![asciicast](https://asciinema.org/a/PhuWp0BZg39Bu60UgixBa7xAM.svg)](https://asciinema.org/a/PhuWp0BZg39Bu60UgixBa7xAM)

## Test Local Config Error

* Making changes and attempting to push errors will fail the push

[![asciicast](https://asciinema.org/a/eqBwPS6Cxsv7RvOMn4dTwZ4u2.svg)](https://asciinema.org/a/eqBwPS6Cxsv7RvOMn4dTwZ4u2)

# Github Enterprise Pre-receive

* Based on the steps from https://help.github.com/enterprise/2.6/admin/guides/developer-workflow/creating-a-pre-receive-hook-script/, we have created a `package.sh` script that creates the `tar.gz` file to Upload in your Github Enterprise installation.
  * This is known as the `Environment` in Github Enterprise Terms
  * Your SRE will also get a clone of this repo to be installed locally, where it will specify the script `validate_config_files.py` as the pre-receive hook to use.

The original base image with Git server with Python is located at https://github.com/marcellodesales/github-prereceive-base-docker.

## Create .tar.gz Package

* Just execute `package.sh` from this repo
* The resulting `tar.gz` file will be displayed

[![asciicast](https://asciinema.org/a/EaVR7aRXfmkgPL3iIt5DPFB1c.svg)](https://asciinema.org/a/EaVR7aRXfmkgPL3iIt5DPFB1c)


## Test in Github Dev

Once the environment has been uploaded to the dev environment, push the current script to it. Github Pre-Receive hook will require your OPS Engineer to specify the scripts to be placed inside the volume of the base Image above.

1. Push the Config Repo to Github
2. Enable the Hook in Settings
3. Attempt to push config with errors

### Github Enteprise Setup

* Push a forked version of this repository to Github Prod Enterprise
* With the Environment, that is, the Docker image in the `tar.gz` format, upload through the Admin setup of Github Enterprise
  * Manage it at `Admin Center -> Pre-receive hooks -> Manage Hooks -> Intuit Spring Cloud Config Validator`
* Select the Github repo where the this repo is pushed, and choose the script `validate_config_files.py`

![github-admin-pre-receive-hook-setup](https://user-images.githubusercontent.com/131457/56842586-8c77ad00-684b-11e9-8dab-796835d185f5.png)

### Enable The Hook in Settings

This is to verify that a Config repo can be validated with the hook.

* After pushing this repo, go to the Settings section of the repo and `Hooks`

<img width="1064" alt="setup-repo" src="https://user-images.githubusercontent.com/131457/56830371-05124580-681b-11e9-9624-b6923d049f44.png">

### Attempt to push Config with Errors

* Just then through the UI try to push errors

<img width="1022" alt="pushing-error" src="https://user-images.githubusercontent.com/131457/56830365-00e62800-681b-11e9-883c-0a3fdd259b5f.png">

### Attempt to push errors from console

* Just clone the repo and try to push errors

[![asciicast](https://asciinema.org/a/fokS3lAgx8O8I1vuVFvxSTqON.svg)](https://asciinema.org/a/fokS3lAgx8O8I1vuVFvxSTqON)

### Change process

* The Environment, or Docker Image in `.tar.gz` format, only needs to be pushed to Github Enterprise if any line on `requirements.txt` changes. That is, if any of the python dependencies has changed.

> **ATTENTION**: The script under to Forked repo MUST be managed by the owners of this fork. Any live updates on this script will reflect on the Validator throughout all Github Repos.

* So, updates on the validator script MUST be coordinated and the suggested way is to first do this change process in a DEV environment and repeat it in PROD after it has been verified!

# Development

Everything you need to develop. Here are some requirements and utilities.

* Python 2.7+: We can use the discover mode for all tests on this version
 * https://docs.python.org/2/library/unittest.html#test-discovery

* The Dockerfile build will automatically execute the tests

## Running tests in Docker

```console
$ docker build --no-cache --target tests -t validator-tests .
Sending build context to Docker daemon  34.97MB
Step 1/7 : FROM marcellodesales/github-enterprise-prereceive-hook-base as tests
 ---> ef045e4c014b
Step 2/7 : RUN apk add --no-cache py-pip &&     pip2 install coverage
 ---> Running in b47bad7e7031
fetch http://alpine.gliderlabs.com/alpine/v3.3/main/x86_64/APKINDEX.tar.gz
fetch http://alpine.gliderlabs.com/alpine/v3.3/community/x86_64/APKINDEX.tar.gz
OK: 82 MiB in 33 packages
Collecting coverage
  Downloading https://files.pythonhosted.org/packages/82/70/2280b5b29a0352519bb95ab0ef1ea942d40466ca71c53a2085bdeff7b0eb/coverage-4.5.3.tar.gz (384kB)
Installing collected packages: coverage
  Running setup.py install for coverage: started
    Running setup.py install for coverage: finished with status 'done'
Successfully installed coverage-4.5.3
You are using pip version 9.0.1, however version 19.1 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.
Removing intermediate container b47bad7e7031
 ---> 7b32fa6f90db
Step 3/7 : COPY requirements.txt /build/requirements.txt
 ---> d20e1f359760
Step 4/7 : RUN pip2 install -r /build/requirements.txt
 ---> Running in ff212a50429f
Collecting pyyaml==5.1 (from -r /build/requirements.txt (line 1))
  Downloading https://files.pythonhosted.org/packages/9f/2c/9417b5c774792634834e730932745bc09a7d36754ca00acf1ccd1ac2594d/PyYAML-5.1.tar.gz (274kB)
Collecting yamllint==1.15.0 (from -r /build/requirements.txt (line 2))
  Downloading https://files.pythonhosted.org/packages/0a/0d/52cbd670156058329321451432dedb02885594c1ae91252574fe8eac61e5/yamllint-1.15.0-py2.py3-none-any.whl (44kB)
Collecting pyjavaproperties==0.7 (from -r /build/requirements.txt (line 3))
  Downloading https://files.pythonhosted.org/packages/0a/5a/af92ac36c3e9b8c684fddfbdcf39ffe7d4b39439bc9b60fd88b2c3bfd244/pyjavaproperties-0.7.tar.gz
Collecting glob2==0.6 (from -r /build/requirements.txt (line 4))
  Downloading https://files.pythonhosted.org/packages/f0/e8/970c7a031b2d7f9a21fefaa8c9d5c38001f8f25055f4ffcb32b3dbecd1ea/glob2-0.6.tar.gz
Collecting pathspec>=0.5.3 (from yamllint==1.15.0->-r /build/requirements.txt (line 2))
  Downloading https://files.pythonhosted.org/packages/84/2a/bfee636b1e2f7d6e30dd74f49201ccfa5c3cf322d44929ecc6c137c486c5/pathspec-0.5.9.tar.gz
Installing collected packages: pyyaml, pathspec, yamllint, pyjavaproperties, glob2
  Running setup.py install for pyyaml: started
    Running setup.py install for pyyaml: finished with status 'done'
  Running setup.py install for pathspec: started
    Running setup.py install for pathspec: finished with status 'done'
  Running setup.py install for pyjavaproperties: started
    Running setup.py install for pyjavaproperties: finished with status 'done'
  Running setup.py install for glob2: started
    Running setup.py install for glob2: finished with status 'done'
Successfully installed glob2-0.6 pathspec-0.5.9 pyjavaproperties-0.7 pyyaml-5.1 yamllint-1.15.0
You are using pip version 9.0.1, however version 19.1 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.
Removing intermediate container ff212a50429f
 ---> 45e483ee306e
Step 5/7 : COPY ./tests /build/tests
 ---> b2e1d253ce75
Step 6/7 : COPY ./validate_config_files.py /build
 ---> 76b91e21c8ae
Step 7/7 : RUN coverage run -m unittest discover -v /build/tests
 ---> Running in 209c14f497a8
Filtering Spring Cloud Config Server's files:  ['**/*.json', '**/*.yaml', '**/*.yml', '**/*.properties']
test_some_yaml_yml_files_are_invalid (test_invalid_yaml_yml_duplicate_keys.InvalidYamlDuplicateKeysTests) ... ok
test_that_validation_index_is_dictionary (test_invalid_yaml_yml_duplicate_keys.InvalidYamlDuplicateKeysTests) ... ok
test_all_matrix_json_files_are_invalid (test_invalid_matrix_json_validation.InvalidMatrixFileTests) ... ok
test_that_validation_index_is_dictionary (test_invalid_matrix_json_validation.InvalidMatrixFileTests) ... ok
test_some_yaml_yml_files_are_invalid (test_invalid_yaml_yml_multi_document_validation.InvalidYamlMultiDocumentFileTests) ... Some Yaml Single documents are invalid
✘ is tests/fixtures/invalid-yaml-configs-duplicate-keys/circle.yml valid? False ERROR: [3:1: duplication of key "machine" in mapping (key-duplicates), 11:1: duplication of key "machine" in mapping (key-duplicates)]
Filtering Spring Cloud Config Server's files:  ['**/*.json', '**/*.yaml', '**/*.yml', '**/*.properties']
Filtering Spring Cloud Config Server's files:  ['**/*.json', '**/*.yaml', '**/*.yml', '**/*.properties']
The android matrix file is invalid
✔ is tests/fixtures/invalid-matrix-json-column/ttu-android.yml valid? True
✔ is tests/fixtures/invalid-matrix-json-column/application.properties valid? True
✔ is tests/fixtures/invalid-matrix-json-column/ttu-ios.yml valid? True
✔ is tests/fixtures/invalid-matrix-json-column/ttu.yaml valid? True
Filtering Spring Cloud Config Server's files:  ['**/*.json', '**/*.yaml', '**/*.yml', '**/*.properties']
Filtering Spring Cloud Config Server's files:  ['**/ok
test_that_validation_index_is_dictionary (test_invalid_yaml_yml_multi_document_validation.InvalidYamlMultiDocumentFileTests) ... ok
test_some_yaml_yml_files_are_invalid (test_invalid_properties_validation.InvalidPropertiesFileTests) ... ok
*.json', '**/*.yaml', '**/*.yml', '**/*.properties']
Some Yaml Multi documents are invalid
✘ is tests/fixtures/invalid-yaml-configs-multiple-documents-per-config/sp_boot_sample-e2e.yml valid? False ERROR: [4:3: syntax error: expected '<document start>', but found '<block mapping start>']
✘ is tests/fixtures/invalid-yaml-configs-multiple-documents-per-config/sp_boot_sample-dev.yml valid? False ERROR: [4:1: syntax error: could not find expected ':']
✔ is tests/fixtures/invalid-yaml-configs-multiple-documents-per-config/application.yml valid? True
Filtering Spring Cloud Config Server's files:  ['**/*.json', '**/*.yaml', '**/*.yml', '**/*.properties']
Filtering Spring Cloud Config Server's files:  ['**/*.json', '**/*.yaml', '**/*.yml', '**/*.properties']
Properties files are invalid without associated values
✔ is tests/fixtures/invalid-properties-files/publisher-onboard_prod.yml valid? True
✔ is tests/fixtures/invalid-properties-files/publisher-onboard_preprod.yml valid? Truetest_that_validation_index_is_dictionary (test_invalid_properties_validation.InvalidPropertiesFileTests) ... ok
test_some_yaml_yml_files_are_invalid (test_invalid_yaml_yml_single_document_validation.InvalidYamlSingleDocumentFileTests) ... ok
test_that_validation_index_is_dictionary (test_invalid_yaml_yml_single_document_validation.InvalidYamlSingleDocumentFileTests) ...
✘ is tests/fixtures/invalid-properties-files/publisher.properties valid? False ERROR: local variable 'wspacere' referenced before assignment
Filtering Spring Cloud Config Server's files:  ['**/*.json', '**/*.yaml', '**/*.yml', '**/*.properties']
Filtering Spring Cloud Config Server's files:  ['**/*.json', '**/*.yaml', '**/*.yml', '**/*.properties']
Some Yaml Single documents are invalid
✔ is tests/fixtures/invalid-yaml-configs-single-documents/publisher-prd.yml valid? True
✘ is tests/fixtures/invalid-yaml-configs-single-documents/publisher-onboard_preprod.yml valid? False ERROR: [5:4: syntax error: mapping values are not allowed here]
✔ is tests/fixtures/invalid-yaml-configs-single-documents/publisher-qal.yml valid? True
✔ is tests/fixtures/invalid-yaml-configs-single-documents/publisher.properties valid? True
Filtering Spring Cloud Config Server's files:  ['**/*.json', '**/*.yaml', '**/*.yml', '**/*.properties']
Filtering Spring Cloud Config Server's files: ok
test_all_properties_are_valid (test_all_valid_config_validation.AllSuccessfulTests) ... ok
test_that_validation_index_is_dictionary (test_all_valid_config_validation.AllSuccessfulTests) ... ok

----------------------------------------------------------------------
Ran 12 tests in 6.315s

OK
 ['**/*.json', '**/*.yaml', '**/*.yml', '**/*.properties']
All config files are valid
✔ is tests/fixtures/all-valid-config/publisher.properties valid? True
✔ is tests/fixtures/all-valid-config/application-multi-documents.yml valid? True
✔ is tests/fixtures/all-valid-config/publisher-onboard_preprod.yml valid? True
Filtering Spring Cloud Config Server's files:  ['**/*.json', '**/*.yaml', '**/*.yml', '**/*.properties']
Removing intermediate container 209c14f497a8
 ---> fb2165f8803e
Successfully built fb2165f8803e
Successfully tagged validator-tests:latest
```

## Running with Python local

Make sure to run all the test cases after making changes to the script.

* Make sure to install the `pip install -r requirements.txt`

```console
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

```console
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
