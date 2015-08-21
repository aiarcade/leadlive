from itertools import chain
from django import forms
from django.conf import settings
from django.contrib.admin import widgets
from django.utils.encoding import smart_unicode, force_unicode
from django.utils.safestring import mark_safe
from django.utils.html import escape, conditional_escape

class MultiSelectWidget(forms.SelectMultiple):
   
    def __init__(self, language=None, attrs=None):
        self.language = language or settings.LANGUAGE_CODE[:2]
        super(MultiSelectWidget, self).__init__(attrs=attrs)

    def render(self, name, value, attrs=None):
        rendered = super(MultiSelectWidget, self).render(name, value, attrs)
        print value
        return rendered + mark_safe(u'''<script type="text/javascript">
            $(document).ready(function afterReady() {
                var elem = $('#id_%(name)s');
                elem.bootstrapDualListbox({nonSelectedListLabel: 'Admitted Students',
                selectedListLabel: 'Students in the Division',moveOnSelect:false});
            });
            </script>''' % {'name':name})
