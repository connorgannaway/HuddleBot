from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from django.utils import timezone
import os
import requests

class StatusChangeView(APIView):

    #saves a statuschange entry to db
    def post(self, request, format=None):

        #attempt mapping request data to model format
        try:
            data = {
                "jira_issue_key": request.data['issue']['key'],
                "old_status": request.query_params['old_status'],
                "new_status": request.query_params['new_status'],
                "description": request.data['issue']['fields']['summary']
            }
        except:
            print('Improper Formatting')
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = ticket_status_changes_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    
    ''' GET METHOD DISALLOWED
    #returns all statuschange entries
    def get(self, request, format=None):
        objects = ticket_status_changes.objects.all()
        serializer = ticket_status_changes_serializer(objects, many=True)

        return Response(serializer.data)
    '''
  


class AssignmentView(APIView):

    #saves an assignment entry to db
    def post(self, request, format=None):
        assignee = None #assignee will be null if unassigned
        
        #if assignee
        if request.data['issue']['fields']['assignee']:
            try:
                #match assignee to person in db
                assigneeID = request.data['issue']['fields']['assignee']['accountId']
                assigneeObject = Person.objects.get(jira_id=assigneeID)
                assignee = assigneeObject.pk
            except:
                print("Unable to match Person")
        
        #attempt mapping request data to model format
        try:
            data = {
                "jira_issue_key": request.data['issue']['key'],
                "assigned_to": assignee
            }
        except:
            print('Improper Formatting')
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = ticket_assignment_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    '''GET METHOD DISALLOWED
    #returns all assignment entries
    def get(self, request, format=None):
        objects = ticket_assignment.objects.all()
        serializer = ticket_assignment_serializer(objects, many=True)

        return Response(serializer.data)
    '''

class TokenView(APIView):

    def refreshOauthToken(self, refresh_token):
        print("REFRESHING OAUTH TOKEN")
        headers = {'Content_Type': 'application/json'}
        data = {
            'grant_type': 'refresh_token',
            'client_id': os.environ.get('JIRA_CLIENT'),
            'client_secret': os.environ.get('JIRA_SECRET'),
            'refresh_token': refresh_token,
        }

        res = requests.post('https://auth.atlassian.com/oauth/token',
            data=data,
            headers=headers)
        data = {
            'token_type': 'jira',
            'token': res.json()['access_token'],
            'refresh_token': res.json()['refresh_token']
        }
        newtoken = api_token(**data)
        newtoken.save()
        return data['token']

    def get(self, request, format=None):
        try:
            if(request.query_params['type'] == "slack"):
                obj = api_token.objects.filter(token_type="slack").order_by('-updated_at').first()
                data = {
                    "token": obj.token
                }
                return Response(data=data, status=status.HTTP_200_OK)

            elif(request.query_params['type'] == "jira"):
                obj = api_token.objects.filter(token_type="jira").order_by('-updated_at').first()
                token = obj.token
                delta = timezone.now() - obj.updated_at
                if((delta.total_seconds() / 3600) >= 1.0):
                    #refresh token
                    token = self.refreshOauthToken(obj.refresh_token)

                data = {
                    "token": token
                }
                return Response(data=data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
