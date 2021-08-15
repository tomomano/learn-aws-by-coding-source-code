Ref => https://aws.amazon.com/premiumsupport/knowledge-center/lambda-layer-simulated-docker/

```
docker run -v "$PWD":/var/task "public.ecr.aws/sam/build-python3.7" /bin/sh -c "pip install -r requirements.txt -t python/lib/python3.7/site-packages/; exit"
```

```
zip -r layer.zip python > /dev/null
```
