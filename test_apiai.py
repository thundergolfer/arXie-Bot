
from private_settings import apiai_access_token

import apiai
import json

API_ACCESS_TOKEN = apiai_access_token

api_ai = apiai.ApiAI(API_ACCESS_TOKEN)

request = api_ai.text_request()
print(dir(request))
request.query = "Get most recent"

resp = request.getresponse().read().decode('utf-8')
json_obj = json.loads(resp)
