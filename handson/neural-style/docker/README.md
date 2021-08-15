## Build docker image

```
docker build -t artgenerator .
```

## Run

```
docker run -v ${PWD}/images:/images/ artgenerator -s /images/picasso.png -c /images/dancing.png --save_path /images/output.png
```

```
docker run -v ${PWD}/images:/images/ artgenerator -s /images/picasso.png -c /images/dancing.png \
--save_path /images/output.png \
--content_weight 2 \
--style_weight 200000
```
