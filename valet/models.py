from django.db import models

from valet import constants


class WhatsappRequest(models.Model):

    HANDLER_OPTIONS = (
        (constants.NO_ONE, 'No one'),
        (constants.KINGSTON, 'Kingston'),
        (constants.FALK, 'Falk'),
        (constants.GERALD, 'Gerald'),
    )

    wap_number = models.CharField(
        'WhatsApp Number',
        max_length=23,
        help_text='WhatsApp number sent as a request'
    )

    handler = models.CharField(
        'Handler',
        max_length=1,
        help_text='Beam Crew member handling the request',
        default=constants.NO_ONE,
        choices=HANDLER_OPTIONS
    )

    def __unicode__(self):
        return '{} - {}'.format(self.wap_number, self.get_handler_display())
