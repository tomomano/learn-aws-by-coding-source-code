# Shin-Bahoutter

## Installation

```bash
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
```

## Set AWS credentials

Use either `~/.aws/credentials` or environmental variables.

```bash
export AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
export AWS_SECRET_ACCESS_KEY=ABCDEFGHIJK
export AWS_DEFAULT_REGION=ap-northeast-1
```

## Deploy

First set environmental variables.
```
export MY_DOMAIN=<mydomain.com>
export CERTIFICATE_ARN=<your own value!>
```

Then run deploy:

```
$ cdk deploy --all -c domain=$MY_DOMAIN -c certificate_arn=$CERTIFICATE_ARN
```

## Build and upload GUI

Build Vue app:

```
$ cd gui/
$ npm install
$ npm run build
```

Upload the build files to S3:

```
$ aws s3 sync dist $BUCKET_URI --delete
```

## Destroy

```
$ cdk destroy --all -c domain=$MY_DOMAIN -c certificate_arn=$CERTIFICATE_ARN
```
