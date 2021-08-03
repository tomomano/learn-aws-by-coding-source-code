# Creating SNS for haiku (Bashoutter)

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

```bash
cdk deploy
```

## Testing API

```bash
python -m unittest
```

## Destroy

```
cdk destroy
```
