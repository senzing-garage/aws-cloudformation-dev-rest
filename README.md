# aws-cloudformation-dev-rest

## Synopsis
Using the AWS Cloudformation template in this repository, a developer can bring up an AWS stack to interact with Senzing's API server.

## Overview

The following diagram illustrates the AWS stack that would be brought up by the cloudformation template.

Using this stack, a developer could view the api documentation via swagger and access Senzing's api server to interact with Senzing.

![overview diagram](assets/overview_diagram.png)

## Contents

1. [Pre-requisites](#Pre-requisites)
1. [How to Deploy?](#how-to-deploy)
1. [How to generate keystores for SSL client authentication?](#how-to-generate-keystores-for-SSL-client-authentication)

## Pre-requisites

1. Deploy [aws-cloudformation-database-cluster cloudformation stack](https://github.com/Senzing/aws-cloudformation-database-cluster) 
1. Install [adoptopenjdk 11](https://adoptopenjdk.net/archive.html)
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
            1. Enter your email address.  Example: `me@example.com`
            1. Enter the permitted IP address block
            1. Enter a base64 representation of the server keystore with the relevant certificates loaded in
            1. Enter the server keystore password
            1. Enter the server keystore alias
            1. Enter a base64 representation of the client keystore with the relevant certificates loaded in
            1. Enter the client keystore password
        1. In **Security responsibility**
            1. Understand the nature of the security in the deployment.
            1. Once understood, enter "I AGREE".
    2. At lower-right, click "Next" button.
2. In **Configure stack options**
    1. At lower-right, click "Next" button.
3. In **Review senzing-basic**
    1. Near the bottom, in **Capabilities**
        1. Check ":ballot_box_with_check: I acknowledge that AWS CloudFormation might create IAM resources."
    2. At lower-right, click "Create stack" button.

## How to generate keystores for SSL client authentication?

The following instructions would typically be done by a **system admin**.

1. Generate a key store, certificate and trust store going through [step 1 & 2 in this guide](https://github.com/Senzing/senzing-api-server#ssl-client-authentication)

1. Convert key store and trust store into base64

1. Put base64 output into cloudformation stack

![cloudformation stack](assets/cft_input.png)

## Developers Guide: How to authenticate using SSL client authentication?

As a developer you can make a curl call by going through [step 4 & 5 in this guide](https://github.com/Senzing/senzing-api-server#ssl-client-authentication)

To get a more in-depth look on how an application can authenticate with the senzing's api server, refer to [here](examples/demo.py)

## References

To understand mutual TLS authentication better, refer to the resources here
- [What is Mutual TLS Authentication?](https://www.cloudflare.com/learning/access-management/what-is-mutual-tls/)
- [Difference between key store and trust store](https://www.baeldung.com/java-keystore-truststore-difference)