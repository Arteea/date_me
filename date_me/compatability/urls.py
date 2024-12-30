from django.urls import include, path
from compatability.views import CompatabilityView


app_name='compatability'

urlpatterns = [
    path('pairs/',CompatabilityView.as_view({'get':'get_candidate','post':'swipe_candidate',})),
    
]
