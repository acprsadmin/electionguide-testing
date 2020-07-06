import requests
from django.conf import settings
import json
import urllib

class Mailgun():
    
    api = settings.MAILGUN_API_KEY
    domain = settings.MAILGUN_DOMAIN
    mailing_list = settings.MAILGUN_MAILINGLIST

    def _api_request(self, path, data=None, method=None, domain=True):
        response_json = None
        success = False
        reason = None

        if not method:
            if data:
                method = "POST"
            else:
                method = "GET"

        query_string = ""
        if method.lower() == "get" and data:
            query_string = urllib.urlencode(data)
            data = None

        try:
            http_func = getattr(requests, method.lower())
            if domain:
                response = http_func(
                    "https://api.mailgun.net/v2/%s/%s?%s" % (
                        self.domain, path, query_string),
                    auth=("api", self.api),
                    data=data,
                )
            else:
                response = http_func(
                    "https://api.mailgun.net/v2/%s?%s" % (
                        path, query_string),
                    auth=("api", self.api),
                    data=data,
                )

#             if response.ok:
            response_json = json.loads(response.content)
            success = response.ok
            reason = response_json.get('message')

        except BaseException as error:
            reason = error

        if not success and reason:
            raise reason

        return response_json
    
    def send_mail(self, subject, plaintext, html, campaign=None, images=None, to_address=None, ):
        if not to_address:
            to_address = self.mailing_list 
            
        data={
             "from": 'info@electionguide.org',
             "to": to_address,
             "subject": subject,
             "text": plaintext,
             "html": html,
             "inline": images,
             "o:campaign": campaign
             }
        
        return self._api_request("messages", data)
        
    
    def create_update_campaign(self, name, campaign_id, method='post'):
        data={
              "name": name,
              "id": campaign_id
              }
        path = 'campaigns/%s' % (campaign_id) if method == 'put' else 'campaigns'
        return self._api_request(path, data, method)
    
    def delete_campaign(self, campaign_id):
        path = 'campaigns/%s' % (campaign_id)
        return self._api_request(path, method='delete')
    
    def get_campaign_stats(self, campaign_id):
        path = 'campaigns/%s/stats' % (campaign_id)
        return self._api_request(path, method='get')
    
    def add_member_mailinglist(self, address, name=None, options=None, subscribed=True):
        path = 'lists/%s/members' % self.mailing_list
        data={
            "address": address,
            "name": name,
            "vars": options,
            "subscribed": 'yes',
            "upsert": 'yes',
            }
        return self._api_request(path, data, method='POST', domain=False)
    
    def delete_member_mailinglist(self, address, name=None, options=None, subscribed=True):
        path = 'lists/%s/members/%s' % (self.mailing_list, address)       
        return self._api_request(path, method='DELETE', domain=False)
        
        
