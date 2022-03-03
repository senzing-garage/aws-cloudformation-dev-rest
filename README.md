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
1. [Expectations](#expectations)

## Pre-requisites

1. Deploy [aws-cloudformation-database-cluster cloudformation stack](https://github.com/Senzing/aws-cloudformation-database-cluster) 
1. Install [adoptopenjdk 11](https://adoptopenjdk.net/archive.html)
1. Install [git](https://github.com/Senzing/knowledge-base/blob/master/HOWTO/install-git.md)

## How to Deploy?



## How to setup SSL client authentication?

The following instructions would typically be done by a **system admin**.

1. Install [adoptopenjdk 11](https://adoptopenjdk.net/archive.html)

2. Generate a key store, certificate and trust store going through [step 1 & 2 in this guide](https://github.com/Senzing/senzing-api-server#ssl-client-authentication)

3. Convert key store and trust store into base64

```
base64 <path to key store>
base64 <path to trust store>
```
4. Put base64 output into cloudformation stack

![cloudformation stack](assets/cft_input.png)

## Developers Guide: How to authenticate using SSL client authentication?

As a developer you can make a curl call by going through [step 4 & 5 in this guide](https://github.com/Senzing/senzing-api-server#ssl-client-authentication)

To get a more in-depth look on how an application can authenticate with the senzing's api server, refer to [here](examples/demo.py)

## References

To understand mutual TLS authentication better, refer to the resources here
- [What is Mutual TLS Authentication?](https://www.cloudflare.com/learning/access-management/what-is-mutual-tls/)
- [Difference between key store and trust store](https://www.baeldung.com/java-keystore-truststore-difference)