# scripts for 

```
export USER_POOL_ID=ap-northeast-1_trU9ZOpQM
export APP_CLIENT_ID=5vsfkkp1jt4c0p3bihclpa39km
```

```
python3 cognito_client.py create_user bob EBYKn2RYU5hGfrjA
```

```
python3 cognito_client.py login bob EBYKn2RYU5hGfrjA
```

## API call examples

```
$ export ENDPOINT_URL="https://api.bashoutter.com"
$ AUTH=`python3 cognito_client.py login bob EBYKn2RYU5hGfrjA`

$ http POST "${ENDPOINT_URL}/haiku" \
"Authorization:${AUTH}" \
username="松尾芭蕉" \
first="閑さや" \
second="岩にしみ入る" \
third="蝉の声"

$ http GET "${ENDPOINT_URL}/haiku" "Authorization:${AUTH}"
```