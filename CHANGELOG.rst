1.9.0 2020-04-30
----------------
- Add support for attribute removing #500
- Add support for groups in checkbox select multiple #436
- Add basic support for ordering custom fields in list view #224
- Change to lazy evaluation {{ modules }} context variable


1.7.4 2020-12-31
----------------
- Fix perfect scrollbar init

1.7.3 2020-11-20
----------------
- Update pre-generated themes and theme generator code


1.7.2 2020-11-18
----------------
- Bump material-design-icons DX to 6.1.0


1.7.0 2020-08-07
----------------
- Django 3.1 support


1.6.7 2020-05-13
----------------
- Switch icon font to `Material Design Icon DX <https://jossef.github.io/material-design-icons-iconfont/>`_
- [PRO] collapsable filter panel on mobile


1.6.3 2020-02-25
----------------
- Fix NullBooleanField for django>2.2


1.6.0 2019-11-19
----------------
- Django 3.0 compatibility
- Fix textarea autoresize on init
- Send clicked button name within <dmc-form>


1.5.3 2019-04-11
----------------

- Fix forms js inclusion template
- Fix delete view user message


1.5.2 2019-03-21
----------------

- Add collapse sidebar button on desktop-sized screen


1.5.1 2019-03-07
----------------

- Fix js injection vulnerability in a list view


1.5.0 2019-02-13
----------------

- Added portuguese translation
- Added default page print styles
- [PRO] WYSIWYG medium editor widget


1.4.0 2018-10-25
----------------

- New WebComponents based Javascript code
- Upgrade to Materialize 1.0.0


1.3.0 2018-08-23
----------------

- Django 2.1 compatibility
- Conform select multiple attribute rendering
- Fix multiple and clearable file inputs
- Support for field.disabled
- [PRO] Improve custom columns ordering handing
- [PRO] Allow to select object from different pages in a list view


1.2.5 2018-05-07
----------------

- Fix pre-build themes


1.2.4 2018-05-02
----------------

- Upgrade to Materialize 1.0.0.rc.1


1.2.3 2018-04-19
----------------

- Upgrade to Materialize 1.0.0.beta
- [PRO] do not show clear label for ajax fields
- [PRO] trigger js change events on autocomplete


1.2.2 2017-01-11
----------------

- Materialize 1.0.0.alpha3
- [PRO] Fix ajax multi-select widget


1.2.0 2017-12-20
----------------

- Materialize 1.0.0.alpha2
- Django 2.0 support
- Drop compatibility with Django 1.8/1.9/1.10
- Drop Material Admin


1.1.0 2017-10-27
----------------

- Update MaterializeCSS to 0.100.2
- Forms - Localize DateTime picker
- Forms - Add clear button on ajax autocomplete fields
- Frontend - Allow to set ordering in the list view from viewset
- Frontend - Fix permission check for the create view
- Admin - Fix inline formset errors
- Admin - Add file download link on the file fields

1.0.0 2017-05-29
----------------

- Django 1.11 support
- Update MaterializeCSS to 0.98.2
- Fix missing badges in shipped MaterializeCSS build
- Localization added: German/French/Spainish/Korean/Chinese
- Forms - Fix allows to use html in a `help_text` of widgets
- Frontend - Improved Login/Logout/403/404/500 service screen templates
- Admin - fix application list layout

0.13.0 2017-03-16 - Beta
------------------------

- Forms - Update MaterializeCSS to 0.98.0
- Forms - `model autocomplete<http://docs.viewflow.io/forms_widgets.html>`_ widgets added (PRO)
- Frontend - Fix viewset customization for update view form.
- Frontend - Fix permission validation to add items in detail template
- Frontend - Icons for boolean variables in the list view
- Frontend - Destroy select and toast to fix issue with turbolinks cache
- Frontend - Allow using non-object level permission in the frontend
- Frontend - Allow specifying custom form widgets in the viewset
- Frontend - Redirect to detail view after object create
- Admin - Improve content page layout
- Admin - Add {% block main_content %}
- Admin - Improve object tools list
- Admin - django-guardian support (PRO)


0.12.0 2017-01-24 - Beta
------------------------

* Forms - Fix select rendering
* Forms - Fix date and datetime fields rendering
* Frontend - Refactor datatables list view
* Frontend - Fix viewset incompatibility under python 2.7
* Frontend - Natural default theme color
* Frontend - Prebuild theme set
* Frontend - Custom theme builder management command (PRO)
* Frontend - Generic views templates now extends base module template
* Frontend - Improve base 2 columns layout
* Admin - Add "Save as New" change form action
* Admin - Fix redirect after login


0.11.0 2016-12-13 - Beta
------------------------

* Forms - Default theme secondary color changed to green
* Frontend - Added `startmodule` management command
* Frontend - Added list view actions (PRO)
* Frontend - Integration with django-filters (PRO)
* Frontend - Active page highlight fixed under IE/Safari
* Admin - Fix ManyToMany field height
* Admin - Fix change form markup


0.10.1 2016-11-10 - Beta
------------------------

- Fix admin raw_id select on django 1.10


0.10.0 2016-10-31 - Beta
------------------------

- Forms - Upgrade to Materialize CSS 0.97.8
- Frontend, Admin - New sidebar with user photo
- Frontend, Admin - Massive CSS/JS/HTML cleanup
- Frontend, Admin - Serve minfied js/css in the production mode
- Frontend - Switch from unsupported PJAX to Turbolinks!
- Admin - Use `model_admin.has_module_permission()` permission check


0.9.2 2016-10-27 - Beta
-----------------------

- Fix admin read-only field for simple values


0.9.1 2016-10-18 - Beta
-----------------------

- Fix duplicate error message for admin non field error.


0.9.0 2016-10-17 - Beta
-----------------------

- Forms - Add Formset and Inlines Form fields (PRO)
- Forms - Add input[type=range] support
- Forms - Fix initial label position for datetime field with value
- Forms - Fix initial label position for number field with zero as initial value
- Forms - Fix XSS vulnerability in input fields.
- Forms - Fix CSS inclusion default template
- Frontend - Fix module delete
- Frontend - Add CRUD views and viewset
- Frontend - Remove LOGIN_REDIRECT_URL override on frontend autoregister
- Admin - User `user.get_username` instead of `user.username`
- Admin - Django 1.9/1.10 compatibility
- Admin - Readonly field support in inlines
- Admin - Use `AdminSite.site_url` as back link


0.8.0 2016-06-14 - Beta
-----------------------

First beta release.

* Forms - Fix 0 as initial value for number input
* Forms - Remove Roboto font fix hack on windows
* Frontend - module heareds fixed
* Admin - list sorting support
* Admin - fixedHeader fixed
* Admin - fix pagination display bug under dj19
* Admin - lost actions support
* Admin - added datetime today shortcut links
* Admin - added filter for select multiple field
* Admin - readonly fields support for inlines
* Admin - mansory layout for index page
* Admin - added app and model icons support


0.7.0 2016-03-13 - Alpha
------------------------

The last alpha release.

* Forms - Fix controls in new forms in formsets
* Forms - New way to append or override widget attrs in template
* Forms - Removed `group_class`, `add_group_class`, `add_label_class` redefinable parts
* Admin - Match table styles to google guidelines.
* Admin - Start to work on admin widget support improvements http://forms.viewflow.io/demo/widget/admin/
* Admin - Fix scrollbar
* Frontend - Switch from fontawesome to material-design-iconic font
* Frontend - Fix broken links on user navigation menu
* Frontend - Modules are refactored to AppConfig mixins


0.6.0 2015-11-19 - Alpha
------------------------

* First release with full django standard widgets support
* Forms - New per-widget demos on http://forms.viewflow.io/demo/widget/
* Forms - Many widget behaviour fixes (DecimalInput, Select, MultiSelect, RadioInput)
* Forms - Disable change datetime on mouse wheel
* Admin - Style fixes and improvements
* Admin - Custom form layouts support (ex: http://forms.viewflow.io/admin/sales/shipment/add/)
* Admin - Admin css/js files modded to separate templates. Fix static files issue with CDN
* Admin - Move All js/css dependencies inside the package. Make it intranet app friendly.
* Frontend - Style fixes and improvements
* Frontend - Fix load indicator on pjax back


0.5.0 2015-11-19 - Alpha
------------------------

* Django 1.9 support
* Forms - Add latest materializecss
* Admin - Support for Readonly widget
* Admin - Custom admin site support
* Admin - Proper lang_code for html
* Admin - Tabular inlines formset support
* Admin - Fk and Many2Many fields support
* Frontend - Integrate django-easy-pjax into the app
* Frontend - Cancel animation as soon as page loaded


0.4.0 2015-05-29 - Alpha
------------------------

* Forms - CheckboxSelectMultiple widgets with multi-column layout support
* Forms - TimeInput widget support (thnks @Morozzzko)
* Forms - Dynamic formsets support
* Admin - fix user change password form
* Frontend - support for smooth navigation back to initial page


0.3.0 2015-05-11 - Alpha
------------------------

* Migrated to new version of materializecss framework
* List all applications in admin navigation menu
* Added breadcrumbs in admin
* Custom material css and js cleanup
* New Frontend template
* Various widget rendering fixes (splitdatetime, empty selects)


0.2.1 2015-04-20 - Alpha
------------------------

* Fixed SplitDateTime widget rendering with empty value
* More consistent parts/variables names over widgets templates
* Fixed file field submission and validation
* Compact html output
* Added ellipses on long labels overflow


0.2.0 2015-04-03 - Alpha
------------------------
* Switched to material design
* Initial admin interface support


0.1.0 2014-11-05 - Alpha
------------------------

* First alpha version extracted from `Viewflow <http://viewflow.io>`_ library
* Basic django widgets support
