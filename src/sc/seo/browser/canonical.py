# -*- coding: utf-8 -*-
from plone.app.layout.links import viewlets
from sc.seo.behaviors.canonical import ICanonicalURL


class CanonicalURLViewlet(viewlets.CanonicalURL):

    def update(self):
        super(CanonicalURLViewlet, self).update()
        try:
            self.behavior = ICanonicalURL(self.context)
        except TypeError:
            self.behavior = None

    def render(self):
        canonical_url = self.behavior.canonical_url
        if not canonical_url:
            return super(CanonicalURLViewlet, self).render()
        return u'    <link rel="canonical" href="{0}" />'.format(canonical_url)
