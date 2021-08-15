import argparse, os, io
import boto3
from PIL import Image
from model import (
    image_loader,
    image_unloader,
    get_style_model_and_losses,
    get_input_optimizer
)

def main(style_name, content_name,
         num_steps=300,
         style_weight=1000000,
         content_weight=1,
         save_path="output.png",
         use_s3=False):
    """Run the style transfer"""

    print("Loading images...")
    if use_s3:
        style_img = load_image_from_s3(style_name)
        content_img = load_image_from_s3(content_name)
    else:
        style_img = Image.open(style_name)
        content_img = Image.open(content_name)
    style_img = image_loader(style_img)
    content_img = image_loader(content_img)
    input_img = content_img.clone()
    assert style_img.size() == content_img.size(), \
    "we need to import style and content images of the same size"
    print("Done.")

    model, style_losses, content_losses = get_style_model_and_losses(style_img, content_img)
    optimizer = get_input_optimizer(input_img)

    print('Optimizing...')
    run = [0]
    while run[0] <= num_steps:

        def closure():
            # correct the values of updated input image
            input_img.data.clamp_(0, 1)

            optimizer.zero_grad()
            model(input_img)
            style_score = 0
            content_score = 0

            for sl in style_losses:
                style_score += sl.loss
            for cl in content_losses:
                content_score += cl.loss

            style_score *= style_weight
            content_score *= content_weight

            loss = style_score + content_score
            loss.backward()

            run[0] += 1
            if run[0] % 50 == 0:
                print("run {}:".format(run))
                print('Style Loss : {:4f} Content Loss: {:4f}'.format(
                    style_score.item(), content_score.item()))
                print()

            return style_score + content_score

        optimizer.step(closure)

    input_img.data.clamp_(0, 1)
    # convert to PIL image
    input_img = image_unloader(input_img)
    # save the generated image
    if use_s3:
        upload_image_to_s3(input_img, save_path)
    else:
        input_img.save(save_path)

def load_image_from_s3(key):
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(os.environ["BUCKET_NAME"])
    stream = bucket.Object(key).get().get("Body")
    return Image.open(stream)

def upload_image_to_s3(image, key):
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(os.environ["BUCKET_NAME"])
    with io.BytesIO() as buffer:
        image.save(buffer, "PNG")
        resp = bucket.put_object(
            Key=key,
            Body=buffer.getvalue()
        )

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--style", type=str,
                        help="Style image")
    parser.add_argument("-c", "--content", type=str,
                        help="Content image")
    parser.add_argument("--use_s3", action="store_true", default=False)
    parser.add_argument("--save_path", type=str, default="output.png")
    parser.add_argument("--style_weight", type=float, default=1000000)
    parser.add_argument("--content_weight", type=float, default=1)
    parser.add_argument("--num_steps", type=int, default=300)
    args = parser.parse_args()

    main(args.style, args.content, num_steps=args.num_steps, style_weight=args.style_weight, content_weight=args.content_weight,
         save_path=args.save_path, use_s3=args.use_s3)
