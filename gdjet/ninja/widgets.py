# -*- coding: utf-8 -*-
from dojango.forms.widgets import DojoWidgetMixin, TextInput
from django.utils.safestring import mark_safe

class ColorPickerInput(TextInput):
    dojo_type = 'dijit.ColorPalette'
    alt_require = 'dijit.form.Button'
    extra_dojo_require = [ 'dojo.parser', 'dijit.form.DropDownButton', 'dijit.ColorPalette' ]
    valid_extra_attrs = [
        'palette',
        'onChange',
    ]
    field_attr_map = {
        'palette': 'palette',
        'onChange': 'onChange',
    }
    def render(self, name, value, attrs=None):
        fattrs = self.build_attrs(attrs, name = name )
        cattrs = {} # for passing into html.
        cattrs.update(fattrs)
        cattrs['name'] = name
        cattrs['value'] = value or "''"
        
        hiddenfield = u"<!-- hidden field -->"
        if value:
            hiddenfield = '<input type="hidden" id="%(id)s" name="%(name)s" value="%(value)s" />' % cattrs
        else:
            hiddenfield = '<input type="hidden" id="%(id)s" name="%(name)s" />' % cattrs
        
        colorfield = '<div dojoType="dijit.ColorPalette" onChange="dojo.byId(\'%(id)s\').value = this.value; '\
                     'dojo.byId(\'%(id)s_colorshow\').style.backgroundColor=this.value; '\
                     '" name="%(name)s_colorfield" id="%(id)s_colorfield"></div>' % cattrs 
        colorshow = '<span style="width: 40px; height: 40px; background-color: %(value)s; border-color: black; border-width: 1px;" '\
                    'name="%(name)s_colorshow" id="%(id)s_colorshow">Aktuelle Farbe</span>' % cattrs
        return mark_safe ( hiddenfield + colorfield + colorshow )
    
    def _render_defunct(self, name, value, attrs=None):
        fattrs = self.build_attrs(attrs, name = name )
        
        hiddenfield = u"<!-- hidden field -->"
        if value:
            hiddenfield = '<input type="hidden" id="%s" name="%s" value="%s" />' % (
                            fattrs['id'], name, value )
        else:
            hiddenfield = '<input type="hidden" id="%s" name="%s" />' % (
                            fattrs['id'], name, )
        colorspan = '<div class="django_nowebkit" id="%s_all" style="background-color: %s">'\
                    '<div class="django_nowebkit tundra" id="%s_showcolor" '\
                    'style="width: 150px; height: 20px; backround-image: none !important;" dojoType="dijit.form.DropDownButton" iconClass="noteIcon">'\
                    '<span style="background-color: %s">Farbe</span>\n' % (fattrs['id'], value, fattrs['id'], value)
        colorfield = colorspan + '<div dojoType="dijit.ColorPalette" onChange="dojo.byId(\'%s\').value = this.value; '\
                     'dojo.byId(\'%s_all\').style.backgroundColor=this.value; '\
                     ' dojo.byId(\'%s_showcolor\').style.backgroundColor=this.value; '\
                     ' dojo.byId(\'%s_showcolor_label\').style.backgroundColor=this.value;"'\
                     ' style="display:none;"'\
                     ' id="%s" name="%s"></div>' % ( fattrs['id'], fattrs['id'], fattrs['id'], fattrs['id'],
                                                     fattrs['id'] + '_colorpalette',
                                                    name + '_colorpalette' ) + '</div></div>'
                     
        
        return mark_safe ( hiddenfield + colorfield )
    class Media:
        pass

