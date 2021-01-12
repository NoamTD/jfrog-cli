# jfrog-cli

## Summary

This project provides a cli called 'jfrog-saas' allowing you to manage a jfrog saas instance.

## Installation

To install the cli, run the following command:

```bash
pip3 install --index https://noamdolovich.jfrog.io/artifactory/api/pypi/jfrog/simple jfrog
```

After installation, you should be able to access the cli by running the following command:

```bash
jfrog-saas --help
```

## Configuration

Every command uses a host/username/password in order to authenticate with the jfrog instance. There are two ways to configure these options.

1. Using flags:

   ```bash
       jfrog --host HOSTNAME --jfrog-username USERNAME --jfrog-password PASSWORD COMMAND...
   ```

2. Using environment variables:
   It is possible to configure the authentication values using environment variables. for example:

   ```bash
   export JFROG_HOST='https://hostname.jfrog.io'
   export JFROG_USERNAME='jfrog_user'
   export JFROG_PASSWORD='jfrog_password'
   ```

## Commands

The following commands are available:

```bash
jfrog storage info - get a summary of the storage consumed by the instance
jfrog system ping - ping the jfrog instance to ensure it is up
jfrog system version - get version of the jfrog instance
jfrog user create - create a new user
jfrog user delete - delete an existing user
```

You can obtain additional help from the cli by using the '--help' flag with each command. for example:

```bash
$ jfrog-saas system ping --help


Usage: jfrog-saas system ping [OPTIONS]

  Ping system, ensuring saas instance is up

Options:
  --help  Show this message and exit.
```
