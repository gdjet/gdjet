# -*- coding: utf-8 -*-

from django.forms import CheckboxSelectMultiple, CheckboxInput, ModelMultipleChoiceField
from django.utils.encoding import force_unicode
from django.utils.html import escape, conditional_escape
from django.utils.safestring import mark_safe
from itertools import chain

class CheckboxSelectMultipleIndent( CheckboxSelectMultiple ):
    split_char = '|'
    
    def render(self, name, value, attrs=None, choices=()):
        """
            renders the widget.
        """
        def update_dictionary( d, item_label, checkbox, label_for, motherlist = [] ):
                b = d
                # item_label = item_label.strip()
                for mother in motherlist:
                    mother = mother.strip()
                    if mother in b.keys():
                        b = b[mother]['children']
                    else:
                        m = { 'label': u'', 'checkbox': u'', 'label_for': u'', 'children': {} }
                        b[mother] = m
                        b = m['children']
                if item_label in b.keys():
                    b[item_label]['label'] = conditional_escape(force_unicode( item_label ))
                    b[item_label]['checkbox'] = checkbox
                    b[item_label]['label_for'] = label_for
                else:
                    i = { 'label': conditional_escape(force_unicode( item_label )) , 
                          'checkbox': checkbox, 
                          'label_for': label_for,
                          'children': {} }
                    b[item_label] = i
                return d
        def write_output_old( out, item, depth = 0 ):
            if depth:
                out.append(u'<li>%s <label%s>%s %s</label></li>' % (
                                '.' * depth * 3,
                                item['label_for'], item['checkbox'], item['label']) )
            else:
                out.append(u'<li><label%s>%s %s</label></li>' % (
                                item['label_for'], item['checkbox'], item['label']) )
            
            for i in item['children'].keys():
                write_output_old( out, item['children'][i], depth+1)
        def write_output( out, item, depth = 0 ):
            out.append(u'<tr><td style="padding: 5px 0 5px %spx;">%s %s</label></td></tr>' % (
                                str(5 + depth * 20),
                                item['checkbox'], item['label']) )
            
            for i in item['children'].keys():
                write_output( out, item['children'][i], depth+1)
                        
        
        if value is None: value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        # output = [u'<ul>']
        output = ['<table><tbody>']
        output_inner = {}
        # output_debug = "DEBUG: "
        # Normalize to strings
        str_values = set([force_unicode(v) for v in value])
        for i, (option_value, option_label) in enumerate(chain(self.choices, choices)):
            # If an ID attribute was given, add a numeric index as a suffix,
            # so that the checkboxes don't all have the same ID attribute.
            if has_id:
                final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
                label_for = u' for="%s"' % final_attrs['id']
            else:
                label_for = ''

            cb = CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
            
            option_value = force_unicode(option_value)
            rendered_cb = cb.render(name, option_value)
            
            option_label = force_unicode(option_label)
            temp = option_label.split( self.split_char )
            mothers = []
            if len(temp) > 1:
                mothers = temp[:-1]
            actual_name = temp[-1].strip()
            # now we search the node we insert this checkbox.
            # entry = { 'checkbox': cb, 'label': escaped..., children: {} }
            update_dictionary( output_inner, actual_name, rendered_cb, label_for, mothers )
            
        for i in output_inner.keys():
            write_output(output, output_inner[i], 0)
        
        output.append(u'</tbody></table>')
        return mark_safe(u'\n'.join(output))

class ModelMultipleChoiceFieldCheckboxes(ModelMultipleChoiceField):
    widget = CheckboxSelectMultipleIndent
    