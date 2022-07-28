from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from django.utils import timezone
from webhooks.serializers import *
from datetime import timedelta

#/api/person/
class PersonView(APIView):

    #create person in database
    def post(self, request, format=None):
        serializer = Person_Serializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

#/api/check-in/uuid/
class UUIDView(APIView):
    
    #get list of check-in uuids/user pairs based on date
    def get(self, request, format=None):
        try:
            date = request.query_params['date']
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        objs = check_in.objects.filter(date=date)
        uuids = [{"check_in_uuid": obj.uuid, "user": obj.user.pk} for obj in objs]
        
        return Response(data=uuids, status=status.HTTP_200_OK)

    #create check-in objects for today and return uuids/user pair
    def post(self, request, format=None):
        try:
            create = request.data['create']
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if(create != True):
            return Response(status=status.HTTP_200_OK)
        
        persons = Person.objects.all()
        uuids = []
        for person in persons:
            if(person.is_active == False):
                continue
            data = {
                'user': person,
            }
            obj = check_in(**data)
            obj.save()
            uuids.append({
                "user": person.pk,
                "check_in_uuid": obj.uuid
            })

        return Response(data=uuids, status=status.HTTP_201_CREATED)

#/api/check-in/<str:uuid>/
class CheckInView(APIView):
    
    def get(self, request, uuid, format=None):
        try:
            obj = check_in.objects.get(uuid=uuid)
            data = check_in_serializer(obj).data
            return Response(data=data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, uuid, format=None):
        try:
            obj = check_in.objects.get(uuid=uuid)
            serializer = check_in_serializer(obj, data=request.data, partial=True)
            if(serializer.is_valid()):
                serializer.validated_data['submitted_at'] = timezone.now()
                serializer.save()
                return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

#/api/check-in/<str:uuid/ticketdata/
class CheckInJiraDataView(APIView):
    
    def get(self, request, uuid, format=None):
        try:
            checkInObject = check_in.objects.get(uuid=uuid)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        uid = checkInObject.user

        doneIssueTimeframeIDs = []
        doneIssueIDs = []
        testingIssueIDs = []
        inProgressIssueIDs = []

        #DONE
        tickets = ticket_status_changes.objects.filter(new_status='done')
        delta = timezone.now() - timedelta(days=1)
        for ticket in tickets:
            assignment = ticket_assignment.objects.filter(jira_issue_key=ticket.jira_issue_key).earliest('assigned_at')
            if(assignment.assigned_to == uid):
                doneIssueIDs.append(ticket.jira_issue_key)
                
        tickets = tickets.filter(updated_at__gt=delta)
        for ticket in tickets:
            if(ticket.jira_issue_key in doneIssueIDs):
                doneIssueTimeframeIDs.append(ticket.jira_issue_key)

        #TESTING
        tickets = ticket_status_changes.objects.filter(new_status='testing')
            
        for ticket in tickets:
            assignment = ticket_assignment.objects.filter(jira_issue_key=ticket.jira_issue_key).earliest('assigned_at')
            if(assignment.assigned_to == uid and not ticket.jira_issue_key in doneIssueIDs):
                testingIssueIDs.append(ticket.jira_issue_key)

        #IN PROGRESS
        tickets = ticket_status_changes.objects.filter(new_status='in_progress')
            
        for ticket in tickets:
            assignment = ticket_assignment.objects.filter(jira_issue_key=ticket.jira_issue_key).earliest('assigned_at')
            if(assignment.assigned_to == uid and not ticket.jira_issue_key in doneIssueIDs and not ticket.jira_issue_key in testingIssueIDs):
                inProgressIssueIDs.append(ticket.jira_issue_key)

        data = {
            'in_progress': inProgressIssueIDs,
            'testing': testingIssueIDs,
            'done': doneIssueTimeframeIDs
        }

        return Response(data=data, status=status.HTTP_200_OK)