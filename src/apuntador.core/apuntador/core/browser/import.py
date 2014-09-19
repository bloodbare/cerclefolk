# -*- encoding: utf-8 -*-
"""
Import JSON data as content.
Can be run as a browser view or command line script.

Crea estructura de carpetes i esdeveniments (tot i que cal repassar les dades
després perque falten les dates i la imatge), i crea també els tags, públics,
cicles i descriptors necessaris (cal repassar-ho, alguns amb accents fallen)
"""

import json
import sys
from Products.Five.browser import BrowserView
from plone.dexterity.utils import createContentInContainer
from Products.CMFPlone.utils import _createObjectByType

import dateutil.parser
from DateTime import DateTime
import csv
from zope.component.hooks import getSite
from Products.CMFCore.utils import getToolByName
from datetime import datetime
import pytz

from collective.geo.behaviour.interfaces import ICoordinates
from plone.app.event.dx.behaviors import IEventBasic, IEventLocation
from plone import namedfile
import urllib
import transaction
from plone.app.textfield.value import RichTextValue


description_dict = {
    'concert': '248765fd5284457f824e03a0097516fa',
    'ajuntament': '58c24e354d494549b00ba49931edb3f8',
    'infantils': '7854d93d73d241c98b20fe1108c7728b',
    'solidaritat': '6484db77578a48b186349514fdaf4141',
    'joventut': 'b00ee1295f504a689deb835685ea3602',
    'ocupacio': 'de91cb4a681b4ede95acf694c06f0167'
}

cicles_dict = {
    'festa-major': '2a4caf04df0849838a0dfeddb6d318c1',
    'aules_cultura': '7e739a77920c4d418e58e7bb2600d4ae',
    'lhora-del-conte': '70f71310c5da4fe4b1ee4f9151d0ffad',
    'enramades': '90674c4756d54e8a91af34438f26ccf3',
    'club_de_lectura': 'a1dc50e3e41b44a9819ed9beed8c7403',
    'els-meus-primers-contes': 'a3fb1ceb2ac844c18713cf25de092002',
    'documental-del-mes': '9eef86fa3f99406cab87a661748532ef',
    'espai-familiar': '539d5b27d5ef43bc84d5cc8192965c44',
    'creixer-amb-tu': 'dda5ca0e900348139983981e3f49b621',
    'penjat-de-lestiu': 'd5c2223c7084441ca4b4996c36287f3b',
    'tocats_lletra': '53befcf52fbd41d2b2d6cef1a5e0ef67',
    'festes-de-la-llum': 'fbb2ee96260f425a951a0f2d70f95678',
    'manresa-solidaria': '1cea26a3822e4a22b69a3dc2eb81b419',
    'temes-del-pou': '1a11f57cb5fe472f9bdb7a3ed9fec150',
    'club-de-lectura-de-novel2022la': 'ce74e39fbb1c4eb4ac3fe17fb2644066',
    'nits-de-joc': '7fe5b154235c4b5383dff691f65dcf8b',
    'toc_teatre': '49fdef55ee184653a78890f77a5c6881',
    'toc-de-classica': '527c2598486f48398acd5760f617fe17',
    'toc-de-musica': '730e9ef4e0ec40fe97f6ef23aeaa83b8',
    'entretoc': 'f89b154738394267a95917632c0dc18d',
    'toc-de-dansa': 'bcc77eaf66084ee1b367d4a07cf30f4b',
    'circ': '2ebcf45ad5ca4f1db3403946c6451ba1',
    'platea-jove': 'fcfb3cf0c1e347a5979304db4966af22',
    'tast-de-classica': '47eac96198c74fe4b48380cb2ab2f42e',
    'petit-kursaal': 'f500fb7d8cac46a890d917a4a880b324',
    'toc-d2019opera': 'dea6bb53148846719abf3f1520ab1d46',
    'petit-kursaal-1': 'f500fb7d8cac46a890d917a4a880b324',
    'imaginat': 'ced3941ad71348538e7708d822d5fa7d',
    'quedem': '5bf2e879626d42299602488ea9e2d013',
    'el-llibre-del-mes': '541343cec3dc40cfa0ae8ad533d30448',
    'aula_de_teatre': '40f9ed4f0d634e09987ce0c9cc6d099c',
    'aprendre_amb_tu': '80d223c30a984c9ebd05a65cc75d3c04',
    'ecoviure': '0a728e55269e478c9c1893442b662378'
}

public_dict = {
    'tothom': '88e3655ee137485d9339382cf48648c0',
    'infantil': '4f6c14f216d44bd2aa541dba407a6cce',
    'adult': '35822059c1a04fc8b2f6bc6c9ab6eddb',
    'familiar': '35822059c1a04fc8b2f6bc6c9ab6eddb',
    'juvenil': '883d02970c674489ab98a44404df233b'
}

etiqueta_dict = {
    'esports': '4b809c32c0ca46eb94210a047b6b4935',
    'música': '3af2c88ea61643f386ffee01589052a0',
    'formació': 'a166718c96574c8ebd09751b61ab4093',
    'cultura popular': 'f3d07bf6b00f4683bcff6b6bce8d78b1',
    'expos': 'e726425a05f84510a8abe7bb3b3e292b',
    'cinema': 'fd3c5b3979ba4f12b7ab69121a900de9',
    'visites': '792efa883c1d4a9bb1a64baeb7c53dbd',
    'xerrades': 'f6d10ac1cc0643bbac25bbec09b1fdf5',
    'escena': 'c184709e6d5545d9b28b2ae55c2f23d8',
    'premis': '755d6731010a4badaa7a22c97bcfc046',
    'TIC': '3e5fc190209c429b9a6c507fc50c0028'
}


class import2Content(BrowserView):
    """
    """

    def __call__(self):
        reader = csv.reader(open('deploy.csv', 'r')) 
        writer = csv.writer(open('problems.csv', 'w'))
        writer2 = csv.writer(open('imported.csv', 'w'))
        etiquetes = []
        publics = []
        cicles = []
        descriptors = []
        portal = getSite()
        member_folders = portal.Members
        count = 0
        for row in reader:
            acl_users = getToolByName(portal, "acl_users")
            if row[0] == 'Ajuntament--Cultura':
                usuari = 'Ajuntament-Cultura'
            elif row[0] == 'vic--remei':
                usuari = 'vic-remei'
            elif row[0] == 'ajuntament--desenvolupament':
                usuari = 'ajuntament-desenvolupament'
            else:
                usuari = row[0]
            user = acl_users.getUserById(usuari)
            print usuari
            if user is not None:
                user = user.__of__(acl_users)
            else:
                writer.writerow(row)
                continue

            if usuari not in member_folders:
                mshipTool = getToolByName(portal, 'portal_membership')
                _createObjectByType("Folder", member_folders, usuari)

                # Get the user object from acl_users

                member_object = mshipTool.getMemberById(usuari)

                ## Modify member folder
                member_folder = member_folders[usuari]
                # Grant Ownership and Owner role to Member
                member_folder.changeOwnership(user)
                member_folder.__ac_local_roles__ = None
                member_folder.manage_setLocalRoles(usuari, ['Owner'])
                # We use ATCT now use the mutators
                fullname = member_object.getProperty('fullname')
                member_folder.setTitle(fullname or usuari)
                member_folder.reindexObject()

            else:
                member_folder = member_folders[usuari]

            if row[5] not in member_folder:
                _createObjectByType("esdeveniment", member_folder, row[5])

            obj = member_folder[row[5]]

            IEventLocation(obj).location = row[1]
            # IEventSummary(obj).text = RichTextValue(raw=row[2], mimeType='text/html', outputMimeType='text/html')
            behavior = IEventBasic(obj)
            import pdb
            start = datetime.strptime(row[8].split('.')[0], '%Y-%m-%d %H:%M:%S') if row[8] != '' else pdb.set_trace()
            end = datetime.strptime(row[9].split('.')[0], '%Y-%m-%d %H:%M:%S') if row[9] != '' else pdb.set_trace()
            behavior.timezone = 'Europe/Andorra'
            tz = pytz.timezone(behavior.timezone)
            obj.start = tz.localize(start)
            obj.end = tz.localize(end)
            obj.title = row[4]
            obj.description = row[3]
            obj.event_url = row[7]
            obj.event_keywords = row[6]
            obj.inscriptions_available = True if row[16] == 'True' else False
            obj.start_inscription = datetime.strptime(row[10].split('.')[0], '%Y-%m-%d %H:%M:%S') if row[10] != '' else datetime.now()
            obj.end_inscription = datetime.strptime(row[11].split('.')[0], '%Y-%m-%d %H:%M:%S') if row[11] != '' else datetime.now()

            obj.destacat = True if row[15] == 'True' else False
            obj.paper = True if row[14] == 'True' else False

            obj.etiquetes = []
            for et in row[17].split(':'):
                if et in etiqueta_dict:
                    uid = etiqueta_dict[et]
                    if uid not in obj.etiquetes:
                        obj.etiquetes.append(uid)

            obj.publics = []
            for et in row[18].split(':'):
                if et in public_dict:
                    uid = public_dict[et]
                    if uid not in obj.publics:
                        obj.publics.append(uid)

            obj.cicles = []
            for et in row[19].split(':'):
                if et in cicles_dict:
                    uid = cicles_dict[et]
                    if uid not in obj.cicles:
                        obj.cicles.append(uid)

            obj.descriptors = []
            for et in row[20].split(':'):
                if et in description_dict:
                    uid = description_dict[et]
                    if uid not in obj.descriptors:
                        obj.descriptors.append(uid)

            transaction.commit()

            ICoordinates(obj).coordinates = 'POINT (%s %s)' % (row[13], row[12])

            url = row[21].replace(':','').replace('http', 'http:').replace('localhost', 'localhost:')
            try:
                if not obj.event_image:
                    urllib.urlretrieve(url, "tmp.jpg")
                    imatge = open('tmp.jpg', 'r')
                    data = imatge.read()
                    imatge.close()
                    nf = namedfile.NamedBlobImage(data)
                    if nf.contentType == 'image/jpeg':
                        obj.event_image = nf
                        obj.event_image.filename = u'foto.jpg'
                    elif nf.contentType == 'image/png':
                        obj.event_image = nf
                        obj.event_image.filename = u'foto.png'
                    elif nf.contentType == 'image/gif':
                        obj.event_image = nf
                        obj.event_image.filename = u'foto.gif'
                    elif nf.contentType == 'image/x-ms-bmp':
                        obj.event_image = nf
                        obj.event_image.filename = u'foto.bmp'
            except:
                pass

            writer2.writerow(row)
            obj.changeOwnership(user)
            obj.__ac_local_roles__ = None
            obj.manage_setLocalRoles(usuari, ['Owner'])

            print "%s %s" % (usuari, row[5])
            # # user
            # writer.writerow([
            #     obj.__parent__.id, 0
            #     obj.getLocation(), 1
            #     obj.getText(), 2
            #     obj.Description(), 3
            #     obj.Title(), 4
            #     obj.getId(), 5
            #     obj.tags, 6
            #     obj.eventUrl, 7

            #     8str(obj.startDate.utcdatetime()) if obj.startDate else '',
            #     9str(obj.endDate.utcdatetime()) if obj.endDate else '',
            #     10str(obj.iniciInscripcio.utcdatetime()) if hasattr(obj, 'iniciInscripcio') and obj.iniciInscripcio else '',
            #     11str(obj.fiInscripcio.utcdatetime()) if hasattr(obj, 'fiInscripcio') and obj.fiInscripcio else '',

            #     12obj.geolocation[0],
            #     13obj.geolocation[1],

            #     14'True' if obj.paper else 'False',
            #     15'True' if obj.destacat else 'False',
            #     16'True' if hasattr(obj, 'Inscripcions') and obj.Inscripcions else 'False',
            #     17':'.join(obj.Subject()),
            #     18':'.join(obj.public),
            #     19':'.join(obj.cicle),
            #     20':'.join(obj.descriptor),
            #     21':'.join(obj.imatge.absolute_url()) if hasattr(obj, 'imatge') else ''
            #     ]
            # )
        missatge = 'Etiquetes\n\n'
        missatge += '\n'.join(etiquetes)
        missatge += 'Publics\n\n'
        missatge += '\n'.join(publics)
        missatge += 'Cicles\n\n'
        missatge += '\n'.join(cicles)
        missatge += 'Descriptors\n\n'
        missatge += '\n'.join(descriptors)

        return missatge

class importContent(BrowserView):
    """
    """

    def str_to_DateTime(self, str_data):
        if str_data:
            return DateTime(dateutil.parser.parse(str_data))
        else:
            return None

    def id_to_uid_dict(self, portal_type):
        root = self.context.portal_url.getPortalObject()
        portal_catalog = root.portal_catalog
        brains = portal_catalog.searchResults(portal_type=portal_type)
        tags_dict = {}
        for brain in brains:
            tags_dict[brain.id] = brain.UID
        return tags_dict

    def tags_id_to_uid_dict(self, tags):
        tags_dict = self.id_to_uid_dict("tag")
        tags_a_crear = [a for a in tags if not a in tags_dict.keys()]
        portal = self.context.portal_url.getPortalObject()
        container = portal.restrictedTraverse("apuntador/tags")
        for tag in tags_a_crear:
            createContentInContainer(container, 'tag', title=tag, id=tag)

        return self.id_to_uid_dict("tag")

    def publics_id_to_uid_dict(self, publics):
        publics_dict = self.id_to_uid_dict("public")
        publics_a_crear = [a for a in publics if not a in publics_dict.keys()]
        portal = self.context.portal_url.getPortalObject()
        container = portal.restrictedTraverse("apuntador/public")
        for public in publics_a_crear:
            createContentInContainer(container, 'public', title=public, id=public)

        return self.id_to_uid_dict("public")

    def cicles_id_to_uid_dict(self, cicles):
        cicles_dict = self.id_to_uid_dict("cicle")
        cicles_a_crear = [a for a in cicles if not a in cicles_dict.keys()]
        portal = self.context.portal_url.getPortalObject()
        container = portal.restrictedTraverse("apuntador/cicles")
        for cicle in cicles_a_crear:
            createContentInContainer(container, 'cicle', title=cicle, id=cicle)

        return self.id_to_uid_dict("cicle")

    def descriptors_id_to_uid_dict(self, descriptors):
        descriptors_dict = self.id_to_uid_dict("descriptor")
        descriptors_a_crear = [a for a in descriptors if not a in descriptors_dict.keys()]
        portal = self.context.portal_url.getPortalObject()
        container = portal.restrictedTraverse("apuntador/descriptors")
        for descriptor in descriptors_a_crear:
            createContentInContainer(container, 'descriptor', title=descriptor, id=descriptor)

        return self.id_to_uid_dict("descriptor")

    def create_esdeveniment_resources(self, container, obj_data):
        """ crea els tags, publics, cicles, decsriptors necessaris pels esdeveniments
        """
        self.tags_id_to_uid_dict(obj_data['subject'])
        self.publics_id_to_uid_dict(obj_data['public'])
        self.cicles_id_to_uid_dict(obj_data['cicle'])
        self.descriptors_id_to_uid_dict(obj_data['descriptor'])
        return

    # def create_esdeveniment(self, container, obj_data):
    #     """ [u'startDate', u'endDate', u'contributors', u'geolocation', u'text', u'Inscripcions', u'eventUrl', u'creation_date', u'paper', u'expirationDate', u'iniciInscripcio', u'id', u'subject', u'modification_date', u'title', u'fiInscripcio', u'cicle', u'relatedItems', u'location', u'excludeFromNav', u'public', u'description', u'tags', u'portal_type', u'effectiveDate', u'language', u'rights', u'descriptor', u'destacat', u'allowDiscussion', u'creators', u'imatge']
    #     """
    #     # dades bàsiques
    #     obj = createContentInContainer(container,
    #                                    'esdeveniment',
    #                                    title=obj_data['title'],
    #                                    contributors=obj_data['contributors'],
    #                                    text=obj_data['text'],
    #                                    eventUrl=obj_data['eventUrl'],
    #                                    paper=obj_data['paper'],
    #                                    id=obj_data['id'],
    #                                    location=obj_data['location'],
    #                                    excludeFromNav=obj_data['excludeFromNav'],
    #                                    language=obj_data['language'],
    #                                    destacat=obj_data['destacat'],
    #                                    description=obj_data['description'],
    #                                    start=None,
    #                                    end=None,
    #                                    event_keywords=obj_data['tags'],
    #                                    creators=tuple(obj_data['creators']))

    #     # etiquetes, públics, cicles, descriptors
    #     tags = obj_data['subject']
    #     tags_dict = self.tags_id_to_uid_dict(tags)
    #     try:
    #         obj.etiquetes = [tags_dict[a] for a in tags]
    #     except:
    #         pass

    #     publics = obj_data['public']
    #     publics_dict = self.publics_id_to_uid_dict(publics)
    #     try:
    #         obj.publics = [publics_dict[a] for a in publics]
    #     except:
    #         pass

    #     cicles = obj_data['cicle']
    #     cicles_dict = self.cicles_id_to_uid_dict(cicles)
    #     try:
    #         obj.cicles = [cicles_dict[a] for a in cicles]
    #     except:
    #         pass

    #     descriptors = obj_data['descriptor']
    #     descriptors_dict = self.descriptors_id_to_uid_dict(descriptors)
    #     try:
    #         obj.descriptors = [descriptors_dict[a] for a in descriptors]
    #     except:
    #         pass

    #     # import pdb; pdb.set_trace()
    #     # geolocation

    #     # start=self.str_to_DateTime(obj_data['startDate']),
    #     # end=self.str_to_DateTime(obj_data['endDate']),
    #     # geolocation=obj_data['geolocation'],
    #     # Inscripcions=obj_data['Inscripcions'],
    #     # creation_date=self.str_to_DateTime(obj_data['creation_date']),
    #     # expirationDate=self.str_to_DateTime(obj_data['expirationDate']),
    #     # iniciInscripcio=self.str_to_DateTime(obj_data['iniciInscripcio']),
    #     # modification_date=self.str_to_DateTime(obj_data['modification_date']),
    #     # fiInscripcio=self.str_to_DateTime(obj_data['fiInscripcio']),

    #     # effectiveDate=self.str_to_DateTime(obj_data['effectiveDate']),
    #     # event_image=obj_data['imatge'])

    #     return obj

    def create_folder(self, container, obj_data):
        """ [u'locallyAllowedTypes', u'contributors', u'creation_date', u'expirationDate', u'immediatelyAddableTypes', u'children', u'subject', u'modification_date', u'title', u'id', u'relatedItems', u'location', u'excludeFromNav', u'constrainTypesMode', u'description', u'portal_type', u'nextPreviousEnabled', u'effectiveDate', u'language', u'rights', u'allowDiscussion', u'creators']
        """
        return createContentInContainer(container,
                                        'Folder',
                                        title=obj_data['title'],
                                        locallyAllowedTypes=obj_data['locallyAllowedTypes'],
                                        contributors=obj_data['contributors'],
                                        creation_date=self.str_to_DateTime(obj_data['creation_date']),
                                        expirationDate=self.str_to_DateTime(obj_data['expirationDate']),
                                        immediatelyAddableTypes=obj_data['immediatelyAddableTypes'],
                                        children=obj_data['children'],
                                        subject=obj_data['subject'],
                                        modification_date=self.str_to_DateTime(obj_data['modification_date']),
                                        id=obj_data['id'],
                                        relatedItems=obj_data['relatedItems'],
                                        location=obj_data['location'],
                                        excludeFromNav=obj_data['excludeFromNav'],
                                        constrainTypesMode=obj_data['constrainTypesMode'],
                                        description=obj_data['description'],
                                        nextPreviousEnabled=obj_data['nextPreviousEnabled'],
                                        effectiveDate=self.str_to_DateTime(obj_data['effectiveDate']),
                                        language=obj_data['language'],
                                        rights=obj_data['rights'],
                                        allowDiscussion=obj_data['allowDiscussion'],
                                        creators=tuple(obj_data['creators']))

    def create_object(self, container, obj_data):
        portal_type = obj_data['portal_type']

        if portal_type == 'Event':
            self.create_esdeveniment_resources(container, obj_data)
            
            # endDate = obj_data['endDate']
            # if endDate:
            #     endDate = self.str_to_DateTime(endDate)
            #     if DateTime.greaterThan(endDate, DateTime()):
            #         new_object = self.create_esdeveniment(container, obj_data)
            #         return new_object

        elif portal_type == 'Folder':
            new_object = self.create_folder(container, obj_data)
            return new_object
        # else:
        #     import pdb; pdb.set_trace()

        return

    def clean_json_file(self, json_file_path):
        """ delete first line, if it is 'running with lxml.etree', so we can
        tranform it to python with json.load
        """
        f = open(json_file_path, 'r')
        lines = f.readlines()
        f.close()

        if lines[0] == 'running with lxml.etree\n':
            f = open(json_file_path, 'w')
            f.write('\n'.join(lines[1:]))
            f.close()

    def get_json_data(self, json_file_path):
        self.clean_json_file(json_file_path)
        json_file = open(json_file_path)
        json_data = json.load(json_file)
        json_file.close()
        return json_data

    def import_json(self, container, json_data):
        """
        """
        # lpmayos: per fer proves restringir aquí
        # for obj_data in json_data[0:100]:
        for obj_data in json_data:
            new_object = self.create_object(container, obj_data)
            if new_object and 'children' in obj_data:
                self.import_json(new_object, obj_data['children'])
        return

    def __call__(self):
        """
        """
        folder = self.context.aq_inner
        json_file_path = "src/apuntador.core/apuntador/core/browser/apuntador_content.json"
        json_data = self.get_json_data(json_file_path)
        self.import_json(folder, json_data)
        return


def spoof_request(app):
    """ http://developer.plone.org/misc/commandline.html
    """
    from AccessControl.SecurityManagement import newSecurityManager
    from AccessControl.SecurityManager import setSecurityPolicy
    from Products.CMFCore.tests.base.security import PermissiveSecurityPolicy, OmnipotentUser
    _policy = PermissiveSecurityPolicy()
    setSecurityPolicy(_policy)
    newSecurityManager(None, OmnipotentUser().__of__(app.acl_users))
    return app


def run_import_as_script(path, json_file_path):
    """ Command line helper function.
    Using from the command line::
        bin/instance run [path-to-file]/import.py yoursiteid/path/to/folder path/to/file
        bin/instance run src/apuntador.core/apuntador/core/browser/import.py /apuntador/Members src/apuntador.core/apuntador/core/browser/nem_all.json
    """

    global app

    secure_aware_app = spoof_request(app)
    folder = secure_aware_app.unrestrictedTraverse(path)
    view = importContent(folder, json_file_path)
    json_data = view.get_json_data(json_file_path)
    view.import_json(folder, json_data)
    return


# Detect if run as a bin/instance run script
if "app" in globals():
    # producció
    # run_import_as_script(sys.argv[1], sys.argv[2])
    # local
    run_import_as_script(sys.argv[3], sys.argv[4])
