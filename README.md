# aws-cloudformation-dev-rest

## Synopsis

Using the AWS Cloudformation template in this repository, a developer can bring up an AWS stack to interact with Senzing's API server.

## Overview

The following diagram illustrates the AWS stack that would be brought up by the cloudformation template.

Using this stack, a developer could view the api documentation via swagger and access Senzing's api server to interact with Senzing.

![overview diagram](assets/overview_diagram.png)

## Contents

1. [Pre-requisites](#pre-requisites)
1. [How to Deploy](#how-to-deploy)
1. [How to generate keystores for SSL client authentication](#how-to-generate-keystores-for-ssl-client-authentication)
1. [How to interact using SSL client authentication](#how-to-interact-using-ssl-client-authentication)

## Pre-requisites

1. Deploy [aws-cloudformation-database-cluster cloudformation stack](https://github.com/Senzing/aws-cloudformation-database-cluster)
1. FIXME: Install `keytool`
    1. FIXME: Make it clear what needs to be installed and why a certain version is needed.
    1. FIXME: Install [adoptopenjdk 11](https://adoptopenjdk.net/archive.html)
    1. FIXME:  If you already have `keytool` installed...
1. Install [git](https://github.com/Senzing/knowledge-base/blob/master/HOWTO/install-git.md)

## How to Deploy?

1. :warning: **Warning:** This Cloudformation deployment will accrue AWS costs.
   With appropriate permissions, the
   [AWS Cost Explorer](https://aws.amazon.com/aws-cost-management/aws-cost-explorer/)
   can help evaluate costs.
1. Visit [AWS Cloudformation with dev-rest template](https://console.aws.amazon.com/cloudformation/home#/stacks/new?stackName=sz-dev&templateURL=https://s3.amazonaws.com/public-read-access/aws-cloudformation-dev-rest/cloudformation.yaml)
1. At lower-right, click on "Next" button.
1. In **Specify stack details**
    1. In **Parameters**
        1. In **Senzing installation**
            1. Accept the End User License Agreement
            1. Adjust the Senzing version, if necessary
            1. If using more than 100k records, input base64 encoded license string
        1. In **Identify existing database stack**
            1. Enter the stack name of the previously deployed
               [aws-cloudformation-database-cluster](https://github.com/Senzing/aws-cloudformation-database-cluster)
               Cloudformation stack
               Example:  `senzing-db`
        1. In **Security**
            1. Enter your email address.
                1. Example: `me@example.com`
            1. Enter the permitted IP address block
            1. Enter a base64 representation of the *server* keystore
                1. Example: Contents of `KEYTOOL_SERVER_STORE_FILE_BASE64` created below.
            1. Enter the server keystore password
                1. Example: Contents of `KEYTOOL_SERVER_PASSWORD` created below.
            1. Enter the server keystore alias
                1. Example: Contents of `KEYTOOL_SERVER_ALIAS` created below.
            1. Enter a base64 representation of the *client* keystore
                1. Example: Contents of `KEYTOOL_CLIENT_STORE_FILE_BASE64` created below.
            1. Enter the client keystore password
                1. Example: Contents of `KEYTOOL_CLIENT_PASSWORD` created below.
        1. In **Security responsibility**
            1. Understand the nature of the security in the deployment.
            1. Once understood, enter "I AGREE".
    1. At lower-right, click "Next" button.
1. In **Configure stack options**
    1. At lower-right, click "Next" button.
1. In **Review senzing-basic**
    1. Near the bottom, in **Capabilities**
        1. Check ":ballot_box_with_check: I acknowledge that AWS CloudFormation might create IAM resources."
    1. At lower-right, click "Create stack" button.

## How to generate keystores for SSL client authentication

The following instructions would typically be done by a **system admin** before bringing up this cloudformation template.

1. :pencil2: Create values for variables.
   Example:

    ```console
    export KEYTOOL_CLIENT_ALIAS=my-senzing-client
    export KEYTOOL_CLIENT_CERTIFICATE_FILE=~/my-senzing-client.cer
    export KEYTOOL_CLIENT_PASSWORD=BadClientPassword
    export KEYTOOL_CLIENT_STORE_FILE=~/my-senzing-client-store.p12
    export KEYTOOL_SERVER_ALIAS=my-senzing-server
    export KEYTOOL_SERVER_PASSWORD=BadServerPassword
    export KEYTOOL_SERVER_STORE_FILE=~/my-senzing-server-store.p12
    ```

1. Synthesize variables.
   Example:

    ```console
    export KEYTOOL_CLIENT_STORE_FILE_BASE64=${KEYTOOL_CLIENT_STORE_FILE}.base64
    export KEYTOOL_SERVER_STORE_FILE_BASE64=${KEYTOOL_SERVER_STORE_FILE}.base64
    ```

1. Create the *server* PKCS12 key store (`sz-api-server-store.p12`).

   **NOTE:** Answer prompts for the 7 fields for the Distinguished Name ("DN") for the certificate being generated.
   Example:

    ```console
    keytool \
        -alias ${KEYTOOL_SERVER_ALIAS} \
        -genkey \
        -keyalg RSA \
        -keysize 2048 \
        -keystore ${KEYTOOL_SERVER_STORE_FILE} \
        -storepass ${KEYTOOL_SERVER_PASSWORD} \
        -storetype PKCS12 \
        -validity 730
    ```

1. Create the *client* PKCS12 key store.
   A single authorized client certificate is assumed for example purposes.
   Create the client key and certificate for the client to use.

   **NOTE:** Answer prompts for the 7 fields for the Distinguished Name ("DN") for the certificate being generated.
   Example:

    ```console
    keytool \
        -alias ${KEYTOOL_CLIENT_ALIAS} \
        -genkey \
        -keyalg RSA \
        -keysize 2048
        -keystore ${KEYTOOL_CLIENT_STORE_FILE} \
        -storepass ${KEYTOOL_CLIENT_PASSWORD} \
        -storetype PKCS12 \
        -validity 730 \
    ```

1. Export the client certificate.
   Example:

    ```console
    keytool \
        -alias ${KEYTOOL_CLIENT_ALIAS} \
        -export \
        -file ${KEYTOOL_CLIENT_CERTIFICATE_FILE} \
        -keystore ${KEYTOOL_CLIENT_STORE_FILE} \
        -storepass ${KEYTOOL_CLIENT_PASSWORD} \
        -storetype PKCS12
    ```

1. Create a trust store containing certificate.
   Example:

    ```console
    keytool \
        -alias ${KEYTOOL_CLIENT_ALIAS} \
        -file ${KEYTOOL_CLIENT_CERTIFICATE_FILE} \
        -import \
        -keystore ${KEYTOOL_CLIENT_STORE_FILE} \
        -storepass ${KEYTOOL_CLIENT_PASSWORD} \
        -storetype PKCS12
    ```

1. Convert server store and client store `.p12` files base64 strings.
   Example:

    ```console
    base64 \
      ${KEYTOOL_CLIENT_STORE_FILE} \
      >> ${KEYTOOL_CLIENT_STORE_FILE_BASE64}

    base64 \
      ${KEYTOOL_SERVER_STORE_FILE} \
      >> ${KEYTOOL_SERVER_STORE_FILE_BASE64}
    ```

1. Insert base64 string into the cloudformation stack.

![cloudformation stack](assets/cft_input.png)

## How to interact using SSL client authentication?

1. Retrieve the senzing api server url from the cloudformation stack that was brought up. It can be found in the output tab, under the key "UrlApiServer".

![api url](assets/cloudformation_output_api.png)

1. To interact directly with the Senzing API server, you can make a curl call with the --cert and --cert-type options to get curl to authenticate itself to the API server.

    ```console
    curl -k https://<senzing-api-server-url>/heartbeat \
        --cert ${KEYTOOL_CLIENT_STORE_FILE}:${KEYTOOL_CLIENT_PASSWORD} \
        --cert-type P12
    ```

To get a more in-depth look on how a sample python application can authenticate with the senzing's api server, refer to [here](examples/demo.py).

1. To run the sample python application, first export the following variables.
   Example:

    ```console
    export CLIENT_STORE_PATH=${KEYTOOL_CLIENT_STORE_FILE}
    export CLIENT_STORE_PASSWORD=${KEYTOOL_CLIENT_PASSWORD}
    export API_HEARTBEAT_URL=<senzing-api-server-url>
    ```

1. Use the following commands to run the sample application.
   Example:

    ```console
    cd examples
    pip install -r requirements.txt
    export FLASK_APP=demo
    flask run
    ```

1. To get the sample python application to interact the Senzing's api server, simply send the following curl command.
   Example:

    ```console
    curl http://127.0.0.1:5000/
    ```

## References

To understand mutual TLS authentication better, refer to the resources here:

- [What is Mutual TLS Authentication?](https://www.cloudflare.com/learning/access-management/what-is-mutual-tls/)
- [Difference between key store and trust store](https://www.baeldung.com/java-keystore-truststore-difference)
