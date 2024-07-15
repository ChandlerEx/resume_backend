import boto3
import json
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb').Table('site_hits')

def lambda_handler(event, context):
    logger.info(f"Received event: {json.dumps(event)}")
    
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
        'Access-Control-Allow-Methods': 'GET,OPTIONS'
    }

    if event['httpMethod'] == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps('Success')
        }

    try:
        # Try to update the item
        logger.info("Attempting to update DynamoDB item")
        response = dynamodb.update_item(
            Key={'id': 'total_hits'},
            UpdateExpression='ADD hits :inc',
            ExpressionAttributeValues={':inc': 1},
            ReturnValues="UPDATED_NEW"
        )
        new_count = int(response['Attributes']['hits'])
        logger.info(f"Successfully updated count to {new_count}")
    except ClientError as e:
        if e.response['Error']['Code'] == 'ValidationException':
            logger.info("Item doesn't exist, creating new item")
            response = dynamodb.put_item(
                Item={'id': 'total_hits', 'hits': 1}
            )
            new_count = 1
        else:
            logger.error(f"Unexpected DynamoDB error: {str(e)}")
            return {
                'statusCode': 500,
                'headers': headers,
                'body': json.dumps({'error': str(e)})
            }
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }

    return {
        'statusCode': 200,
        'headers': headers,
        'body': json.dumps({'count': new_count})
    }