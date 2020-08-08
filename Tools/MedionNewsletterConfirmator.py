import json
import re
import time

import graphene
import requests


class Query(graphene.ObjectType):
    headers = {"Authorization": "Bearer 25ad9e51-ce4d-4bcb-b15f-b8dbd2779ca0"}

    def run_query(self, query):
        request = requests.post('https://api.testmail.app/api/graphql', json={'query': query},
                                headers=self.headers)
        if request.status_code == 200:
            return request.json()
        else:
            raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

    def email_counter(self):
        query = """
        {
          inbox (
            namespace:"ui38k"
          ) 
          {
            count
          }
        }
        """
        return self.run_query(query)

    def view_raw_emails(self):
        query = """
        {
          inbox (
            namespace:"ui38k"
          ) {
            emails{
              html
            }
          }
        }
        """
        return self.run_query(query)

    def email_filtering(self, email_field, email_filter):
        """
        Scheme Details: Tools/emailscheme.json
        scheiß michi

        :param email_field: sorting field
        :param email_filter:
        :return:
        """

        query = """
        {
          inbox(
            namespace:"ui38k"
            limit: 50
            advanced_filters : 
            [
                {
                field: %s
                match:exact
                action:include
                value: "%s"
              }
            ]
          )
          {
            emails{
              from
              html
            }
          }
        }
        """ % (email_field, email_filter)


        return self.run_query(query)

    def dic_to_json(self, dictionary):
        """
        :param dictionary:
        :return a pretty printed dictionary with 3 indents:
        """

        return json.dumps(dictionary, indent=3)

    def extract_confirmation_link(self, dictionary):
        """
        :param dictionary:
        :return returns the confirmation from medion:
        """

        a = dictionary.get('data')
        b = a.get('inbox')
        c = b.get('emails')
        d = [x for x in c]

        confirmation_reg = 'https:\\/\\/link.newsletter.medion.com\\/u\\/nrd.*?(?=" target="_blank" class="cta1a")'
        links = [re.findall(confirmation_reg, x.get('html')) for x in d]
        print('emails to confirm:', len(links))
        return links

    def Confirm(self):
        for x in self.extract_confirmation_link(
                self.email_filtering(email_field='subject', email_filter='Deine Anmeldung zum MEDION-Newsletter')):
            try:
                another_reg = 'http://.*?(?=">here)'
                html = requests.get(*x).text
                link = re.findall(another_reg, html)
                redirect_link = str(link[0]).replace('&amp;', '&')
                confirm_page = requests.get(redirect_link)
                print(x, 'confirmed')

            except Exception as ex:
                print(x, 'threw:', ex)




