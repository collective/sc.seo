# -*- coding: utf-8 -*-
from plone.app.layout.viewlets import common
from sc.seo.behaviors.metarobots import IMetaRobots


class MetaRobotsViewlet(common.ViewletBase):
    """Renders the  <meta name="robots"> tag if the IMetaRobots is applied
       to the context
    """

    def update(self):
        super(MetaRobotsViewlet, self).update()
        try:
            self.behavior = IMetaRobots(self.context)
        except TypeError:
            self.behavior = None

    def available(self):
        return True if self.behavior else False

    def content(self):
        content = self.behavior.robots
        # If there is no restriction, we explicity allow indexing
        if not content:
            return 'all'
        content = list(content)
        # For unavailable_after we need to inform the expiration date
        if 'unavailable_after' in content:
            content.remove('unavailable_after')
            expiration = self.context.expires
            if expiration:
                content.append(
                    'unavailable_after: {:%d %b %Y %H:%M:%S %Z}'.format(expiration)
                )
        return u', '.join(content)
