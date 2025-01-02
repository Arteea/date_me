from django.shortcuts import render,redirect
from rest_framework import viewsets
from rest_framework.response import Response


from users.models import User,UserInfo
from users.serializers import UserSerializer,UserInfoSerializer

from compatability.models import Compatability,Swipes

from compatability.utils import get_candidates

from .serializers import SwipeActionSerializer,CandidateSerializer

from rest_framework.decorators import action

from django.db.models import Q

from dialogs.models import Pair,Dialog


class CompatabilityView(viewsets.ViewSet):

    serializer_class=SwipeActionSerializer

    def _get_userinfo(self,user_id):
        try:
            return UserInfo.objects.get(user_id=user_id)
        except UserInfo.DoesNotExist:
            return None  

    def _get_candidates(self,userinfo):
        candidate_zodiac = get_candidates(userinfo)
 
        swipe_history=Swipes.objects.filter(swiper_id=userinfo.user.id).select_related('candidate_id')
        swiped_user_ids = [swipe.candidate_id_id for swipe in swipe_history]

        candidates = UserInfo.objects.filter(zodiac__in=candidate_zodiac)

        valid_candidates=candidates.exclude(user_id__in=swiped_user_ids)

        return valid_candidates


    @action(methods=['get'], detail=False)
    def get_candidate(self, request):
        
        user_id = request.session.get('user_id')
        if not user_id:
            return Response({"error": "User ID not found in session."}, status=400)

        userinfo = self._get_userinfo(user_id)
        if not userinfo:
            return Response({"error": "User not found."}, status=404)

        candidates=self._get_candidates(userinfo)
        if not candidates:
            return Response({"No more candidates available"}, status=404)

        candidate=candidates[0]

        candidate_response=CandidateSerializer(candidate)
        return Response(candidate_response.data, status=200)
        

    
    @action(methods=['post'], detail=False)
    def swipe_candidate(self, request):

        user_id = request.session.get('user_id')
        if not user_id:
            return Response({"error": "User ID not found in session."}, status=400)

        userinfo = self._get_userinfo(user_id)
        if not userinfo:
            return Response({"error": "User not found."}, status=404)

        candidates=self._get_candidates(userinfo)
        if not candidates:
            return Response({"No more candidates available"}, status=404)
        
        candidate=candidates[0]
        
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            action = serializer.validated_data['action']
            Swipes.objects.create(
                swiper_id=userinfo.user,
                candidate_id=candidate.user,
                action=(action == 'Yes'),
            )


            ### Pair creation logic
            if action == 'Yes':
                mutual_swipe = Swipes.objects.filter(
                swiper_id=candidate.user,
                candidate_id=userinfo.user,
                action=True,
            ).exists()
                if mutual_swipe:
                    ### Object creation
                    Pair.objects.create(first_participant=userinfo.user,second_participant=candidate.user,)
                    

            redirect_url='http://127.0.0.1:8000/pairs/'
            return Response({"message":f'Pair with {candidate.user.first_name} created','redirect_url':redirect_url,}, status=200)
        else:
            return Response(serializer.errors, status=400)

    
    
    
    
    

        

        

