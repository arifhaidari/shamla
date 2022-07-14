from django.contrib import admin

from .models import Slider, Brand, NewArrival, Recommendation

# class MarketingPreferenceAdmin(admin.ModelAdmin):
#      list_display  = ['__str__', 'subscribed', 'updated']
#      readonly_fields = ['mailchimp_msg', 'mailchimp_subscribed', 'timestamp', 'updated']
#      class Meta:
#           model = MarketingPreference
#           fields = [
#                          'user', 
#                          'subscribed', 
#                          'mailchimp_msg',
#                          'mailchimp_subscribed', 
#                          'timestamp', 
#                          'updated'
#                     ]

# admin.site.register(MarketingPreference, MarketingPreferenceAdmin)
admin.site.register(Slider)
admin.site.register(Brand)
admin.site.register(NewArrival)
admin.site.register(Recommendation)