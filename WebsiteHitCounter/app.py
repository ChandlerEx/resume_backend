import boto3
import json
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb').Table('site_hits')

def lambda_handler(event, context):
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'OPTIONS,GET'
    }

    try:
        # Try to update the item
        response = dynamodb.update_item(
            Key={'id': 'total_hits'},
            UpdateExpression='ADD hits :inc',
            ExpressionAttributeValues={':inc': 1},
            ReturnValues="UPDATED_NEW"
        )
        new_count = int(response['Attributes']['hits'])
    except ClientError as e:
        # If the item doesn't exist, create it
        if e.response['Error']['Code'] == 'ValidationException':
            response = dynamodb.put_item(
                Item={'id': 'total_hits', 'hits': 1}
            )
            new_count = 1
        else:
            print(f"Unexpected error: {e.response['Error']['Message']}")
            raise
    except Exception as e:
        print(f"Error: {str(e)}")
        raise

    return {
        'statusCode': 200,
        'headers': headers,
        'body': json.dumps({'count': new_count})
    }