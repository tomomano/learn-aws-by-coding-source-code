import requests
import os, argparse

ENDPOINT_URL = os.environ['ENDPOINT_URL']

def post_job(style_image_name, content_image_name):
    resp = requests.post(
        ENDPOINT_URL + '/job',
    ).json()

    resp2 = requests.post(
        resp["style_image_url"]["url"],
        data=resp["style_image_url"]["fields"],
        files={"file": open(style_image_name, "rb")}
    )

    resp3 = requests.post(
        resp["content_image_url"]["url"],
        data=resp["content_image_url"]["fields"],
        files={"file": open(content_image_name, "rb")}
    )

    print("Job ID:", resp["job_id"])
    print("Upload style image success?", resp2.status_code == 204)
    print("Upload content image success?", resp3.status_code == 204)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--style", type=str,
                        help="Style image")
    parser.add_argument("-c", "--content", type=str,
                        help="Content image")
    subparsers = parser.add_subparsers(dest="command")

    sp1 = subparsers.add_parser("many")
    sp1.add_argument("num", type=int, default=10)

    sp2 = subparsers.add_parser("single")

    args = parser.parse_args()

    if args.command == "many":
        for i in range(int(args.num)):
            post_job(args.style, args.content)
    elif args.command == "single":
        post_job(args.style, args.content)
    else:
        raise ValueError("Invalid command")
