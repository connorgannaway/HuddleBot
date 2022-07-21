from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *


class StatusChange(APIView):
    
    #returns all statuschange entries
    def get(self, request, format=None):
        objects = ticket_status_changes.objects.all()
        serializer = ticket_status_changes_serializer(objects, many=True)

        return Response(serializer.data)

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


class Assignment(APIView):

    #returns all assignment entries
    def get(self, request, format=None):
        objects = ticket_assignment.objects.all()
        serializer = ticket_assignment_serializer(objects, many=True)

        return Response(serializer.data)

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
