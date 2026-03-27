import json
import boto3

ssm = boto3.client('ssm', region_name='ap-southeast-2')

KFC_KEY = '/myinvoices/kfc_rental_amount'
SUBWAY_KEY = '/myinvoices/subway_rental_amount'

CORS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type,x-api-key',
    'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
}


def lambda_handler(event, context):
    method = event.get('httpMethod', '')

    if method == 'OPTIONS':
        return {'statusCode': 200, 'headers': CORS, 'body': ''}

    if method == 'GET':
        try:
            result = ssm.get_parameters(Names=[KFC_KEY, SUBWAY_KEY], WithDecryption=False)
            values = {p['Name'].split('/')[-1]: p['Value'] for p in result['Parameters']}
            return {
                'statusCode': 200,
                'headers': CORS,
                'body': json.dumps(values)
            }
        except Exception as e:
            return {'statusCode': 500, 'headers': CORS, 'body': json.dumps({'error': str(e)})}

    if method == 'POST':
        try:
            body = json.loads(event.get('body') or '{}')
            ssm.put_parameter(Name=KFC_KEY, Value=str(body['kfc_rental_amount']), Type='String', Overwrite=True)
            ssm.put_parameter(Name=SUBWAY_KEY, Value=str(body['subway_rental_amount']), Type='String', Overwrite=True)
            return {
                'statusCode': 200,
                'headers': CORS,
                'body': json.dumps({'ok': True})
            }
        except Exception as e:
            return {'statusCode': 500, 'headers': CORS, 'body': json.dumps({'error': str(e)})}

    return {'statusCode': 405, 'headers': CORS, 'body': json.dumps({'error': 'Method not allowed'})}
