# spring-cloud-config-validator

Python script that validates Spring Cloud Config configuration repos by analyzing `.json`, `.yaml`, `.yml` and `.properties`.

* Manual Validations
* Github Pre-receive Hook Status Validations: Commits and Pull Requests  

![Validation with errors](https://jira.intuit.com/secure/attachment/643347/643347_execute-from-curl.png)

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
  https://github.intuit.com/raw/servicesplatform-tools/spring-cloud-config-validator/master/requirements.txt >
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

> $ curl --user "mdesales:******" https://github.intuit.com/raw/servicesplatform-tools/spring-cloud-config-properties-verification/master/validate-config-files.py | python

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
✘ File /home/mdesales/dev/github/intuit/servicesplatform-tools/spring-cloud-config-properties-verification/ttu-ios_8.0.yml is NOT valid: expected '<document start>', but found '<scalar>'
  in "/home/mdesales/dev/github/intuit/servicesplatform-tools/spring-cloud-config-properties-verification/ttu-ios_8.0.yml", line 1, column 5
✔ File /home/mdesales/dev/github/intuit/servicesplatform-tools/spring-cloud-config-properties-verification/ttu-ios.yml is valid!
✘ File /home/mdesales/dev/github/intuit/servicesplatform-tools/spring-cloud-config-properties-verification/.matrix-android.json is NOT valid: No JSON object could be decoded
✔ File /home/mdesales/dev/github/intuit/servicesplatform-tools/spring-cloud-config-properties-verification/ttu-android_N.yml is valid!
✔ File /home/mdesales/dev/github/intuit/servicesplatform-tools/spring-cloud-config-properties-verification/ttu-2.7.yml is valid!
✔ File /home/mdesales/dev/github/intuit/servicesplatform-tools/spring-cloud-config-properties-verification/.matrix-ios.json is valid!
✔ File /home/mdesales/dev/github/intuit/servicesplatform-tools/spring-cloud-config-properties-verification/ttu-android.yml is valid!
✔ File /home/mdesales/dev/github/intuit/servicesplatform-tools/spring-cloud-config-properties-verification/ttu-android_6.0.yml is valid!
✔ File /home/mdesales/dev/github/intuit/servicesplatform-tools/spring-cloud-config-properties-verification/ttu.yaml is valid!
✘ File /home/mdesales/dev/github/intuit/servicesplatform-tools/spring-cloud-config-properties-verification/application.properties is NOT valid: local variable 'wspacere' referenced before assignment
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
