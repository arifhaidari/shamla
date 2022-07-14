from django.core.serializers import serialize
from django.db.models.query import QuerySet
# ValuesListQuerySet
from django.template import Library

import json

register = Library()

# @register.filter( is_safe=True )
@register.filter
def jsonify(object):
     # if isinstance(object, ValuesListQuerySet):
     #      return json.dumps(list(object))
     if isinstance(object, QuerySet):
          return serialize('json', object)
     return json.dumps(object)