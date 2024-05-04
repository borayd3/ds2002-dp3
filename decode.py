import boto3
from botocore.exceptions import ClientError
import requests
import json

url = "https://sqs.us-east-1.amazonaws.com/440848399208/ngx3fy"
sqs = boto3.client('sqs')
list1 = []
del_message = []

def get_message():
    try:
        for m in range (1, 10):
            response = sqs.receive_message(
                QueueUrl=url,
                AttributeNames=[
                    'All'
                ],
                MaxNumberOfMessages=10,
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
            list1.append(("Order: {order}","Word: {word}" ))
            del_message.append(handle)
        else:
            print("No message in the queue")
            exit(1)
        for d in del_message:
            sqs.delete_message(
                QueueUrl=url,
                ReceiptHandle=handle
            )
        print("The messages have been deleted")
    except ClientError as e:
        print(e.response['Error']['Message'])

ordered_message = list1.sort(key = lambda x: x[0])
print(ordered_message)


if __name__ == "__main__":
    get_message()

            