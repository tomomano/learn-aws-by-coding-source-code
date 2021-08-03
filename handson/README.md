## Prerequisites

- Python (>= 3.7)
- AWS Account
- [AWS CLI](https://aws.amazon.com/cli/)
  - See [this link](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-linux.html) to install
  - Once installed, run `aws configure`. For more information, see [this link](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html).
- [AWS CDK](https://github.com/aws/aws-cdk)
  - See [this link](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html) to install
    * To install CDK, you need `Node.js` and `npm`.
       * [Installation instruction](https://github.com/nodesource/distributions/blob/master/README.md)
       * `Node.js` version must be >=10.0
    * Once Node.js and npm is installed, then you can install `cdk` with this command:

       `sudo npm install -g aws-cdk`

    * To start using CDK, you must run

        `cdk bootstrap`

## Docker

Docker image which contains libraries/softwares to run the hands-on programs is available.

Pull and run the image by

```bash
docker run -it tomomano/labc:latest
```
