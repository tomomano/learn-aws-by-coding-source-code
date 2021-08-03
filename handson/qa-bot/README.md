# Creating a Transformer-based Q&A bot system

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

## Submitting tasks

Submit a single question:

```bash
python run_task.py ask "A giant peach was flowing in the river. She picked it up and brought it home. Later, a healthy baby was born from the peach. She named the baby Momotaro." "What is the name of the baby?"
```

Submit many questions (questions are defined in [problems.json](problems.json)):

```bash
python run_task.py ask_many
```

List the answers to the questions asked before:

```bash
python run_task.py list_answers
```

Clear all the questions asked before (i.e. empty the database):

```bash
python run_task.py clear
```

## Destroy

```bash
cdk destroy
```
