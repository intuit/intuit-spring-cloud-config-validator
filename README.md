# spring-cloud-config-validator

Python script that validates Spring Cloud Config configuration repos by analyzing `.json`, `.yaml`, `.yml` and `.properties`.

* Manual Validations
* Github Pre-receive Hook Status Validations: Commits and Pull Requests  

![Validation with errors](https://jira.intuit.com/secure/attachment/643347/643347_execute-from-curl.png)

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

![Validation without errors](https://jira.intuit.com/secure/attachment/639030/validation-no-errors.png)

## Validation with errors

The execution of the script fails and returns 1.

![Validation with errors](https://jira.intuit.com/secure/attachment/639031/validation-with-errors.png)

# Github Enterprise Pre-receive

You can follow the steps at https://help.github.com/enterprise/2.6/admin/guides/developer-workflow/creating-a-pre-receive-hook-script/ to include this script as a Pre-receive hook.

## Github Pre-receive failure

The execution of a pre-receive hook in Github prevents users from pushing code with errors. The validate script developed here can prevent users from publishing changes in Spring Cloud Config repos that can break the server. The example below shows the validation. 

* Github Change on a local workspace

![git change](https://jira.intuit.com/secure/attachment/643248/git-show-commit.png)

* Git push fails when errors are in the files

![Github Pre-receive Failure](https://jira.intuit.com/secure/attachment/643249/pre-receive-hook-docker.png)

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
remote: ###### Spring Cloud Config Validator 0.1.3 #######
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
