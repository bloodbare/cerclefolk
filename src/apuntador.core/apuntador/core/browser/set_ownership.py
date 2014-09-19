# -*- encoding: utf-8 -*-
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
import json


class setOwnership(BrowserView):

    def __call__(self):

        resultat = []

        # # Netejem els propietaris
        # # Posem les dates a lloc
        pc = getToolByName(self.context, 'portal_catalog')
        brains = pc.searchResults(portal_type='esdeveniment')

        pm = self.context.portal_membership
        total = len(brains)
        print "TOTAL : %d" % total
        count = 0
        for brain in brains:
            count += 1
            resultat.append({
                'url': brain.getURL(),
                'creator': brain.Creator
            })
            new_member = brain.getURL().split('/')[-2]
            obj = brain.getObject()
            parent = obj.__parent__
            if '-40' in new_member:
                new_member = new_member.replace('-40', '@')
            elif '--' in new_member:
                new_member = new_member.replace('--', '-')

            member = pm.getMemberById(new_member)
            if member:
                parent.changeOwnership(member, recursive=True)
                obj.manage_setLocalRoles(new_member, ["Owner",])
                parent.manage_setLocalRoles(new_member, ["Owner",])
                parent.reindexObjectSecurity()
                obj.reindexObjectSecurity()
                print "FET : %s (%d/%d)" % (brain.getURL(), count, total)
            else:
                print "NO te member %s" % brain.getURL()

        # Mirem els usuaris
        aclusers = getToolByName(self.context, 'acl_users')

        mt = getToolByName(self, 'portal_membership')
        mt_users = mt.listMembers()
        fake_users = []
        for user in mt_users:
            if 'Authenticated' not in user.getRoles():
                # aclusers.source_users.removeUser(user.getId())
                print "Fake user No MEMBER: %s" % (user.getId())
                fake_users.append(user.getId())

        mt_users_ids = mt.listMemberIds()
        for user in mt_users_ids:
            folder = mt.getHomeFolder(user)
            if folder is not None:
                print "User %s : %d at %s" % (user, len(folder.items()), folder)
            if folder is None:
                if user not in fake_users:
                    print "Fake Member user without HOME: %s" % (user)
                    aclusers.source_users.removeUser(user)


        # Mirem les carpetes
        llistat_usuaris_carpetes = []
        memberfolder = mt.getMembersFolder()
        for carpeta in memberfolder.values():
            if len(carpeta.items()) == 0:
                print "Carpeta Builda %s" % (carpeta.getId())
            else:
                try:
                    llistat_usuaris_carpetes.append(carpeta.getOwnerTuple()[1])
                    print "Carpeta amb elements %s %s" % (carpeta.getId(), carpeta.getOwnerTyple()[1])
                except:
                    print "Carpeta error %s " % carpeta.getId()

        for user in mt_users_ids:
            if user not in llistat_usuaris_carpetes:
                print "PER BORRAR: %s" % user


        for user in llistat_usuaris_carpetes:
            if user not in mt_users_ids:
                print "AMB CARPETA PERÒ SENSE USUARI: %s" % user

        return json.dumps(resultat)
