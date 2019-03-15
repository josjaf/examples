import os


def lambda_handler(event, context):

    print(str(os.environ))
    print(event)
    return
