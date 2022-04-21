from sre_parse import State
import requests
import json

import logging
log = logging.getLogger(__name__)

class Hass:
    def __init__(self, url, token):
        self.url = url
        self.token = token

    def get_state(self, sensor):

        headers = {
            "Authorization": "Bearer " + self.token,
            "content-type": "application/json",
        }

        try:
            response = requests.get(self.url+sensor, headers=headers, timeout=1)
        except requests.exceptions.Timeout as e:
            log.error("Request timeout from HomeAssistant. Check your connection: {}".format(e))
            return("Request timeout from HomeAssistant. Check your connection: {}".format(e))
        except requests.exceptions.RequestException as e:
            log.error("Check your connection or config file: {}".format(e))
            return("Check your connection or config file: {}".format(e))

        if response.status_code == 200:
            # Create a json variable
            jdata = json.loads(response.text)
            output = jdata['state'] + " " + jdata['attributes']['unit_of_measurement']
            return(output)
        else:
            log.error("API call to Home Assistant failed with error code {}".format(response.status_code))
            return("API call to Home Assistant failed with error code {}".format(response.status_code))
