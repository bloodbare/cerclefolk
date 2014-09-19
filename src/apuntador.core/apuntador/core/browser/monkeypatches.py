from Products.CMFCore.utils import getToolByName


def DateRangeCatalogIndexesVocabulary__call__(self, context):
    """ See IVocabularyFactory interface
    """
    ctool = getToolByName(context, 'portal_catalog')
    res = []
    for index in ctool.getIndexObjects():
        index_id = index.getId()
        if index.meta_type in ('DateIndex', 'DateRecurringIndex'):
            res.append(index_id)

    return self._create_vocabulary(context, res)


import logging
import DateTime
from types import GeneratorType
from zope.component import queryMultiAdapter
from zope.component import getUtility
from zope.component import queryAdapter

from Products.CMFPlone.utils import safeToInt
from Products.CMFPlone.PloneBatch import Batch

from eea.facetednavigation.caching import ramcache
from eea.facetednavigation.caching import cacheKeyFacetedNavigation
from eea.facetednavigation.interfaces import IFacetedLayout
from eea.facetednavigation.interfaces import IFacetedCatalog
from eea.facetednavigation.interfaces import ICriteria
from eea.facetednavigation.interfaces import ILanguageWidgetAdapter
from eea.facetednavigation.interfaces import IFacetedWrapper
from eea.facetednavigation.interfaces import IWidgetFilterBrains

logger = logging.getLogger('eea.facetednavigation.browser.app.query')

from eea.facetednavigation.browser.app.query import FacetedQueryHandler


def query(self, batch=True, sort=True, **kwargs):
    """ Search using given criteria
    """
    if self.request:
        kwargs.update(self.request.form)
        kwargs.pop('sort[]', None)
        kwargs.pop('sort', None)

    # jQuery >= 1.4 adds type to params keys
    # $.param({ a: [2,3,4] }) // "a[]=2&a[]=3&a[]=4"
    # Let's fix this
    kwargs = dict((key.replace('[]', ''), val)
                  for key, val in kwargs.items())

    query = self.criteria(sort=sort, **kwargs)
    catalog = getUtility(IFacetedCatalog)
    try:
        query['start'] = {
            'query': (DateTime.DateTime(), DateTime.DateTime('2062-05-08 15:16:17')),
            'range': 'min:max'
        }
        query['sort_on'] = 'start'
        query['sort_order'] = 'ascending'
        brains = catalog(self.context, **query)
    except Exception, err:
        logger.exception(err)
        return Batch([], 20, 0)
    if not brains:
        return Batch([], 20, 0)

    # Apply after query (filter) on brains
    num_per_page = 20
    criteria = ICriteria(self.context)
    for cid, criterion in criteria.items():
        widgetclass = criteria.widget(cid=cid)
        widget = widgetclass(self.context, self.request, criterion)

        if widget.widget_type == 'resultsperpage':
            num_per_page = widget.results_per_page(kwargs)

        brains_filter = queryAdapter(widget, IWidgetFilterBrains)
        if brains_filter:
            brains = brains_filter(brains, kwargs)

    if not batch:
        return brains

    b_start = safeToInt(kwargs.get('b_start', 0))

    # orphans = 20% of items per page
    orphans = num_per_page * 20 / 100

    if type(brains) == GeneratorType:
        brains = [brain for brain in brains]

    return Batch(brains, num_per_page, b_start, orphan=orphans)

FacetedQueryHandler.query = query
