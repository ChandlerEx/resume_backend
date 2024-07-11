import boto3

dynamodb = boto3.resource('dynamodb').Table('site_hits')

def lambda_handler(event, context):
    try:
        response = dynamodb.update_item(
            Key={'id': 'total_hits'},
            UpdateExpression='ADD hits :inc',
            ExpressionAttributeValues={':inc': 1},
            ReturnValues="UPDATED_NEW"
        )
        new_count = str(response['Attributes']['hits'])
    except Exception as e:
        print(f"Error: {str(e)}")
        new_count = '0'

    return {
        'statusCode': 200 if new_count != '0' else 500,
        'headers': {
            'Content-Type': 'text/plain',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,GET'
        },
        'body': new_count
    }