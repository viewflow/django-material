==============================
The Django Material Admin site
==============================

Unsupported django admin options
================================

.. attribute:: ModelAdmin.actions_on_top
.. attribute:: ModelAdmin.actions_on_bottom
   
Options have no effect

.. attribute:: ModelAdmin.filter_horizontal
.. attribute:: ModelAdmin.filter_vertical

No difference between options/ If there is enought width, the
horizontal layout is used. Vertical layout with the box of unselected
options appearing above the box of selected options used on the small
screens.

.. attribute:: ModelAdmin.list_editable

No support for editable lists is implemented

.. attribute:: ModelAdmin.preserve_filters

No support for preserve filters is implemented.
               
.. attribute:: InlineModelAdmin.min_num

 But default inlines have no forms, only `plus` button that allows to
 add new.

.. attribute:: InlineModelAdmin.template

Option is ignored


.. attribute:: AdminSite.site_header

Option is ignored, material admin have no site header.

.. attribute:: AdminSite.site_url

Option is ignored

.. attribute:: AdminSite.index_title

Option is ignored


