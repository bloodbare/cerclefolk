.. contents::

Introduction
============

- defines portal languages (profiles/default/portal_languages.xml)

- changes language names for language viewlet (browser/__init__.py)

- soft scrolling on internal links with class soft_scroll (browser/javascripts/apuntador.js)

- responsive tabs (browser/javascripts/jquery.responsiveTabs.min.js, browser/stylesheets/responsive-tabs.css)

- faceted navigation:

    - customized widgets (browser/widgets_faceted, browser/overrides.zcml)

    - new html widget (browser/widgets_faceted/html)

    - responsive (browser/stylesheets/faceted_custom.less, cssregistrty.xml, eea.facetednavigation.browser.template.view.pt, eea.facetednavigation.browser.template.widgets.pt)

    - total results number (eea.facetednavigation.views.preview-items.pt)

- registers a diazo theme folder
    - html
    - rules
    - less (includes bootstrap)
    - bootstrap.min.js

- offers a menu viewlet for the header

- offers a menu viewlet for the footer 

- customized register and reset password mails and forms (jbot/pwreset_finish.pt, jbot/pwreset_form.pt, jbot/registered_notify_template.pt)

- catalan translations for dexterity (locales/ca/plone.dexterity.po)
