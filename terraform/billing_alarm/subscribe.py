import boto3
import sys
import os


def main():
    EMAIL = os.environ.get('EMAIL')
    TOPIC_ARN = os.environ.get('TOPIC_ARN')

    sns = boto3.client('sns')
    print(EMAIL)
    print(TOPIC_ARN)
    response = sns.subscribe(
        TopicArn=TOPIC_ARN,
        Protocol='email',
        Endpoint=EMAIL,
    )
    print(response)
    return


if __name__ == '__main__':
    main()
