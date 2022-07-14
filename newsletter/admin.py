from django.contrib import admin

from .models import NewsLetter, NewsLetterType, MailingList, CustomerMessage


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

admin.site.register(NewsLetter)
admin.site.register(NewsLetterType)
admin.site.register(MailingList)
admin.site.register(CustomerMessage)



# Register your models here.
