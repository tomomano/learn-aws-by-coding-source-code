# Shin-Bahoutter

```
export MY_DOMAIN=<mydomain.com>
export CERTIFICATE_ARN=<your own value!>
```

```
$ cdk deploy --all -c domain=$MY_DOMAIN -c certificate_arn=$CERTIFICATE_ARN
```

```
$ aws s3 sync dist $BUCKET_URI --delete
```

```
$ cdk destroy --all -c domain=$MY_DOMAIN -c certificate_arn=$CERTIFICATE_ARN
```
