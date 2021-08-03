# AWS Batch Tutorial: Running a ML training in parallel

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

## Build and upload docker image

Once the deployment is complete, go to the AWS console through your browser.
Then, navigate to `ECR` > `Repositories`.
There you will find a repository named `simplebatch-repositoryXXXX` (where XXXX is a random string generated for you).
Open this repository, and on the top right corner hit the button saying `View push commands`.
Execute each command displayed in the window (see picture).
Now your docker image is ready in AWS!

<img src="screenshot_ecr.png" width=400 />

## Submiting a single task

See [notebook/run_single.ipynb](notebook/run_single.ipynb)

## Submitting parallel tasks

See [notebook/run_sweep.ipynb](notebook/run_sweep.ipynb)

## Destroy

```
cdk destroy
```
