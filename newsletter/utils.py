import hashlib
import json
import re
import requests
from django.conf import settings


from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError

import address
from address.models import Address

MAILCHIMP_API_KEY = getattr(settings, "MAILCHIMP_API_KEY", None)
MAILCHIMP_DATA_CENTER = getattr(settings, "MAILCHIMP_DATA_CENTER", None)
MAILCHIMP_EMAIL_LIST_ID = getattr(settings, "MAILCHIMP_EMAIL_LIST_ID", None)

def check_email(email):
    if not re.match(r".+@.+\..+", email):
        raise ValueError('String passed is not a valid email address')
    return email

def get_subscriber_hash(member_email):
    check_email(member_email)
    member_email = member_email.lower().encode()
    m = hashlib.md5(member_email)
    return m.hexdigest()

def get_first_last_name(the_name):
    last_name = ''
    if len(the_name.split()) > 1:
        first_name = the_name.split()[0].capitalize()
        last_name = the_name.split()[1].capitalize()
    else:
        first_name = the_name.capitalize()
    return first_name, last_name

class Mailchimp(object):

    def change_subcription_status(self, mailinglist_object, status='unsubscribed'):
        mailchimp = Client()
        the_response = 'error'
        hashed_email = get_subscriber_hash(mailinglist_object.email)
        mailchimp.set_config({
            "api_key": MAILCHIMP_API_KEY,
            "server": MAILCHIMP_DATA_CENTER,
        })
        address = ''
        phone = ''
        user = mailinglist_object.user
        if user is not None:
            first_name, last_name = get_first_last_name(user.full_name)
            address_object = (user.billingprofile.address_set.filter(
                        address_type=Address.Types.Billing).first() or None)
            if address_object is not None:
                address = {
                    "addr1": address_object.street,
                    "addr2": address_object.apartment or '',
                    "city": address_object.city,
                    "country": address_object.country.capitalize(),
                    "zip": address_object.zipcode,
                }
                phone = address_object.phone or ''
        else:
            first_name, last_name = get_first_last_name(mailinglist_object.name)

        member_info = {
            "email_address": mailinglist_object.email,
            "status_if_new": self.check_valid_status(status),
            "merge_fields": {
                'FNAME': first_name,
                'LNAME': last_name,
                'PHONE': phone,
                "ADDRESS": address
            }
        }
        try:
            response = mailchimp.lists.set_list_member(MAILCHIMP_EMAIL_LIST_ID, hashed_email, member_info)
            the_response = response['status']
        except ApiClientError as error:
            print('oh shit error occured')
            print(error.text)
        return the_response

    def subscribe(self, mailinglist_object):
        return self.change_subcription_status(mailinglist_object, status='subscribed')

    def unsubscribe(self, mailinglist_object):
        return self.change_subcription_status(mailinglist_object, status='unsubscribed')
    
    def transaction(self, mailinglist_object):
        return self.change_subcription_status(mailinglist_object, status='transactional')

    def pending(self, mailinglist_object):
        return self.change_subcription_status(mailinglist_object, status='pending')

    def check_valid_status(self, status):
        choices = ['subscribed', 'unsubscribed', 'cleaned', 'pending', 'transactional']
        if status not in choices:
            raise ValueError("Not a valid choice for email status")
        return status




