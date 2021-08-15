# Deep Art Generator

```
export MY_DOMAIN=<mydomain.com>
export CERTIFICATE_ARN=<your own value!>
```

```
$ cdk deploy --all --require-approval never -c domain=$MY_DOMAIN -c certificate_arn=$CERTIFICATE_ARN
```

```
$ aws s3 sync dist $BUCKET_URI --delete
```

```
$ cdk destroy --all -c domain=$MY_DOMAIN -c certificate_arn=$CERTIFICATE_ARN
```

## Testing APIs

```
$ export ENDPOINT_URL="https://api.deepartgenerator.org"
```

```
$ http POST "${ENDPOINT_URL}/job"
$ http GET "${ENDPOINT_URL}/job/d513d9df1a184e9aa3ed1b405f970096"
$ http DELETE "${ENDPOINT_URL}/job/d513d9df1a184e9aa3ed1b405f970096"
```
