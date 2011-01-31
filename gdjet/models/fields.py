# -*- coding: utf-8 -*-
"""
    Various Fields for your pleasure.
    
    @author: g4b

Copyright (C) 2010 by  Gabor Guzmics, <gab(at)g4b(dot)org>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

"""

# JSONFIELD
# @author Jasber
# @author g4b
# after http://djangosnippets.org/snippets/1478/
# modified to be serializable.
# modified to understand other formats

from django.db import models
from django.utils import simplejson as json, datetime_safe
import datetime
import decimal
from time import mktime, struct_time
from gdjet.utils.json import GdjetJSONEncoder


class JSONField(models.TextField):
    """JSONField is a generic textfield that neatly serializes/unserializes
    JSON objects seamlessly"""

    # Used so to_python() is called
    __metaclass__ = models.SubfieldBase
    def __init__(self, *args, **kwargs):
        if 'json_encoder' in kwargs.keys():
            self.json_encoder = kwargs['json_encoder']
            del kwargs['json_encoder']
        else:
            self.json_encoder = GdjetJSONEncoder
        super(JSONField, self).__init__(*args, **kwargs)
        
    def to_python(self, value):
        """Convert our string value to JSON after we load it from the DB"""

        if value == "":
            return None

        try:
            if isinstance(value, basestring):
                return json.loads(value)
        except ValueError:
            pass

        return value

    def get_prep_value(self, value):
        """Convert our JSON object to a string before we save"""
        if value == "":
            return None
        if isinstance(value, dict) or isinstance(value, list):
            value = json.dumps(value, cls=self.json_encoder)
        return super(JSONField, self).get_prep_value(value)
    
    def value_to_string(self, obj):
        """ called by the serializer.
        """
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)
    
    