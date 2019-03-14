"""
python subscribe.py EMAIL FILTER
"""
import sys
import boto3


def main():
    EMAIL = sys.argv[1]
    FILTER = sys.argv[2]

    sns = boto3.client('sns')
    topics = []

    response = sns.list_topics()
    for topic in response['Topics']:
        topics.append(topic)
    while 'NextToken' in response:
        response = sns.list_topics(NextToken=response['NextToken'])
        for topic in response['Topics']:
            topics.append(topic)
    print(topics)

    topic_arn = [t['TopicArn'] for t in topics if FILTER in t['TopicArn']]
    assert len(topic_arn) == 1, f"Filter: {FILTER} needs to be more specific"
    topic_arn = topic_arn[0]
    response = sns.subscribe(
        TopicArn=topic_arn,
        Protocol='email',
        Endpoint=EMAIL,
    )
    print(response)
    return


if __name__ == '__main__':
    main()
