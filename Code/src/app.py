import json
import traceback
import logging
from search_pipeline import SearchDescriptionPipeline


logging.basicConfig(level=logging.INFO)
search_module = SearchDescriptionPipeline()

def handler(event, context):

    if event['rawPath'] == '/':
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "Service": "Superhero Guessing API",
                "Status": "Active"
            })
        }

    elif event['rawPath'] == '/ping':
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "Service": "Superhero Guessing API",
                "Status": "Active",
                "Ping": "Success"
            })
        }

    elif event['rawPath'] == '/guess_hero':

        request_body = json.loads(event['body'])
        request_description = str(request_body['description'])

        try:
            superhero_names = search_module.run_pipeline(description_text=request_description)
            superhero_names = ",".join(superhero_names)

            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({
                    "enriched_text": superhero_names,
                })
            }
        except Exception as e:
            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({
                    "Error": str(traceback.format_exc),
                    "Exception": str(e)
                })
            }
    else:
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "Service": "Text Enrichment API",
                "Status": "Active",
                "Message": "API method not allowed"
            })
        }