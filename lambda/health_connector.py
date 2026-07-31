import json, uuid

import boto3

from mod_medicaid.ViaConnection import ViaConnection
from mod_medicaid.AWS_Data_Operations import dd_new_trip


def api_handler(event, context):
    # Obtain header information
    ep = event['requestContext']['resourcePath']
    try:
        payload = json.loads(event['body'])
    except:
        print(f'[{ep}] No Payload / failed to parse body:', event.get('body'))
        payload = ''
    status_code = 200
    print(f'[{ep}] payload:', payload)
    output = event

    # Legacy Lyft TAPI code
    if ep == '/v1/tapi/trips/{trip_id}/cancel':
        output = 'Not Available'
        status_code = 404
    elif ep == '/v1/tapi/trips/{trip_id}':
        output = 'Not Available'
        status_code = 404
    elif ep == '/v1/tapi/trips':
        output = 'Not Available'
        status_code = 404
    elif ep == '/kiosk_status' or ep == '/connector_status':
        try:
            vc = ViaConnection()
            output = vc.via_kiosk_trip_status(payload)
            print(f'[{ep}] success - output:', output)
        except ValueError as e:
            print(f'[{ep}] ValueError:', e)
            output = str(e)
            status_code = 200
        except SystemError as e:
            print(f'[{ep}] SystemError:', e)
            output = str(e)
            status_code = 400
    # NOTE: Kiosk request was broken into two separate calls to keep the
    #           API calls under 30 seconds per API Gateway limits
    elif ep == '/kiosk_request' or ep == '/connector':
        try:
            vc = ViaConnection()
            print(f'[{ep}] requesting trip')
            output = vc.via_request_book_trip(payload)
            print(f'[{ep}] success - trip booked, output:', output)
            dd_new_trip(via_response=output)
        except ValueError as e:
            print(f'[{ep}] ValueError:', e)
            output = str(e), 200
        except SystemError as e:
            print(f'[{ep}] SystemError:', e)
            output = str(e), 500
            # TODO: need to let front end accept this error code
            # status_code = 500
    elif ep == '/kiosk_request_detail':
        try:
            vc = ViaConnection()
            trip_id = payload.get('trip_id') if isinstance(payload, dict) else None
            if not trip_id:
                print(f'[{ep}] missing trip_id - payload was:', payload)
                raise SystemError('Error: Missing trip_id')
            print(f'[{ep}] requesting details for trip_id:', trip_id)
            output = vc.via_trip_details(trip_id)
            print(f'[{ep}] success - output:', output)
        except SystemError as e:
            print(f'[{ep}] SystemError:', e)
            output = str(e), 500

    # Legacy Code
    elif ep == '/via_webhook':
        try:
            # Legacy code here for future use for MOD-Medicaid
            output = ''
        except Exception as e:
            print(f'[{ep}] Exception:', e)
            output = ''
    elif ep == '/v1/tapi/providers':
        output = 'Not Available'
        status_code = 404

    print(f'[{ep}] response - status_code: {status_code}, output:', output)
    return {
        'isBase64Encoded': False,
        'statusCode': status_code,
        'body': json.dumps(output),
        'headers': {
            'content-type': 'application/json',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        }
    }

# Legacy code
def lambda_kiosk(event, context):
    return api_handler(event, context)

def lambda_kiosk_status(event, context):
    return api_handler(event, context)