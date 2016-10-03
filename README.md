# spring-cloud-config-properties-verification

Verification of Spring Cloud Config configuration repos by analyzing `.json`, `.yaml`, `.yml` and `.properties`.

# Usage

Download the script `validate-config-files.py` and execute it. The script returns 0 for success or 1 for errors.

## Execute current Directory

```
$ validate-config-files.py
```

## Execute for another Directory

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

* Github Change on a local workspace

![git change](https://jira.intuit.com/secure/attachment/643248/git-show-commit.png)

* Git push fails when errors are in the files

![Github Pre-receive Failure](https://jira.intuit.com/secure/attachment/643249/pre-receive-hook-docker.png)
