from users.models import UserInfo
from compatability.models import Compatability,Swipes


def get_candidates(userinfo):
    if userinfo.gender=='male':
        zodiac_selection=Compatability.objects.filter(zodiac_male=userinfo.zodiac)
    elif userinfo.gender=='female':
        zodiac_selection=Compatability.objects.filter(zodiac_female=userinfo.zodiac)
        


    candidate_zodiac=[]

    for variant in zodiac_selection:
        if variant.compatability>=userinfo.compatability_preferences:
            if userinfo.gender=='male':
                candidate=variant.zodiac_female
            elif userinfo.gender=='female':
                candidate=variant.zodiac_male
            candidate_zodiac.append(candidate)
    
    return candidate_zodiac