## Build docker image

```
docker build -t neuralart .
```

## Run

```
docker run -v ${PWD}/images:/images/ neuralart -s /images/munch.png -c /images/koala.png --save_path /images/output.png
```

```
docker run -v ${PWD}/images:/images/ neuralart -s /images/munch.png -c /images/koala.png \
--save_path /images/output.png \
--content_weight 2 \
--style_weight 200000
```
