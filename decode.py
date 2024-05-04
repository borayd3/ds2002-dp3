import boto3
from botocore.exceptions import ClientError
import requests
import json

url = "https://sqs.us-east-1.amazonaws.com/440848399208/ngx3fy"
sqs = boto3.client('sqs')

dict1 = {}
del_message = []

def get_message():
    try:
        for m in range (10):
            response = sqs.receive_message(
                QueueUrl=url,
                AttributeNames=[
                    'All'
                ],
                MaxNumberOfMessages=1,
                MessageAttributeNames=[
                    'All'
                ]
            )
        if "Messages" in response:
            order = response['Messages'][0]['MessageAttributes']['order']['StringValue']
            word = response['Messages'][0]['MessageAttributes']['word']['StringValue']
            handle = response['Messages'][0]['ReceiptHandle']

            #print(f"Order: {order}")
            #print(f"Word: {word}")
            unorder_message = {order: word}
            dict1.update(unorder_message)
            del_message.append(handle)

        else:
            print("No message in the queue")
            exit(1)
        for d in del_message:
            sqs.delete_message(
                QueueUrl=url,
                ReceiptHandle=handle
            )
        print("The message has been deleted")
    except ClientError as e:
        print(e.response['Error']['Message'])

ordered_message = sorted(dict1, key=lambda x: x['order'])
print(ordered_message)

if __name__ == "__main__":
    get_message()

            