import boto3
import argparse, os

def create_user(username: str, password: str, 
                user_pool_id: str, app_client_id: str) -> None:
    """
    creates a user in the specified user pool using specified app client
    """
    print("Creating a new user...")

    client = boto3.client('cognito-idp')

    # initial sign up
    resp = client.sign_up(
        ClientId=app_client_id,
        Username=username,
        Password=password
    )
    user_sub = resp["UserSub"]
    
    # then confirm signup
    resp = client.admin_confirm_sign_up(
        UserPoolId=user_pool_id,
        Username=username
    )

    print("User successfully created.")
    return user_sub

def login(username: str, password: str, 
          app_client_id: str) -> str:
    """
    log in to the cognito user pool and returns access token
    """
    client = boto3.client('cognito-idp')

    try:
        resp = client.initiate_auth(
            ClientId=app_client_id,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                "USERNAME": username,
                "PASSWORD": password
            }
        )
    except:
        raise ("Log in failed!")
    
    print(resp['AuthenticationResult']['IdToken'])
    return resp['AuthenticationResult']['IdToken']

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    sp1 = subparsers.add_parser("create_user")
    sp1.add_argument("username", type=str)
    sp1.add_argument("password", type=str)

    sp2 = subparsers.add_parser("login")
    sp2.add_argument("username", type=str)
    sp2.add_argument("password", type=str)

    args = parser.parse_args()

    user_pool_id = os.environ["USER_POOL_ID"]
    app_client_id = os.environ["APP_CLIENT_ID"]

    if args.command == "create_user":
        create_user(args.username, args.password, user_pool_id, app_client_id)
    elif args.command == "login":
        login(args.username, args.password, app_client_id)
    else:
        raise ValueError("Invalid command!")
