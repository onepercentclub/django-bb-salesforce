import logging
import sys
import bb_salesforce
import os
import collections
from optparse import make_option
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
from django.db import connection
from bb_salesforce.synchronize import export_all
from ...synchronize import sync_all, send_log
from bluebottle.clients.models import Client

#
# Run with (example):
# ./manage.py sync_salesforce -t onepercent -x -v2
# ./manage.py sync_salesforce -t onepercent -s -u 120 -v2 --log-to-salesforce
#


class Command(BaseCommand):
    help = 'Synchronize data to Salesforce.'
    requires_model_validation = True

    verbosity_log_level = {
        '0': logging.ERROR,    # 0 means no output.
        '1': logging.WARNING,  # 1 means normal output (default).
        '2': logging.INFO,     # 2 means verbose output.
        '3': logging.DEBUG     # 3 means very verbose output.
    }

    option_list = BaseCommand.option_list + (
        make_option('--log-to-salesforce', action='store_true', default=False, dest='log_to_salesforce',
                    help='Send the execution log to Salesforce'),

        make_option('--tenant', '-t', action='store', type='string', dest='tenant',
                    help='Tenant to sync or export'),

        make_option('--dry-run', action='store_true', dest='dry_run', default=False,
                    help='Execute a Salesforce sync without saving to Salesforce.'),

        make_option('--updated', '-u', action='store', dest='updated', type='int', metavar='MINUTES',
                    help="Only sync/export records that have been updated in the last MINUTES minutes."),

        make_option('--sync-new', action='store_true', dest='sync_new',
                    help="Sync only new records."),

        make_option('--synchronize', '-s', action='store_true', dest='synchronize',
                    help="Sync all records."),

        make_option('--csv-export', '-x', action='store_true', dest='csv_export', default=False,
                    help="Generate CSV files instead of syncing data with the Salesforce REST API.")
    )

    def handle(self, *args, **options):
        # Setup the log level for root logger.
        if options['log_to_salesforce']:
            logger = logging.getLogger('salesforce')
            fhndl = logging.handlers.RotatingFileHandler(
                os.path.join(settings.PROJECT_ROOT, "export", "salesforce", "last.log"),
                backupCount=5)
            formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
            fhndl.setFormatter(formatter)
            fhndl.doRollover()
            logger.addHandler(fhndl)
        else:
            logger = logging.getLogger('console')

        log_level = self.verbosity_log_level.get(options['verbosity'])

        logger.setLevel(log_level)
        tenant_list = Client.objects.values_list('client_name', flat=True)
        if not options['tenant']:
            logger.error("You must specify a tenant with '--tenant' or '-t'.")
            logger.info("Valid tenants are: {0}".format(tenant_list))
            sys.exit(1)
        elif options['tenant'] not in tenant_list:
            logger.error("Tenant does not exists: '{0}'".format(options['tenant']))
            logger.info("Valid tenants are: {0}".format(tenant_list))
            sys.exit(1)
        else:
            tenant = Client.objects.get(client_name=options['tenant'])
            connection.set_tenant(tenant)

        if not options['csv_export'] and not options['synchronize']:
            logger.error("You must specify an action [--csv-export or --synchronize]")
            sys.exit(1)

        sync_from_datetime = None
        sync_counter = collections.Counter()

        if options['updated']:
            delta = timedelta(minutes=options['updated'])
            sync_from_datetime = timezone.now() - delta
            logger.info("Filtering only updated records from {0}".format(timezone.localtime(sync_from_datetime)))

        logger.info("Salesforce Sync Settings [timeout: {0}s] [retries: {1}x] [version: {2}]".
                     format(getattr(settings, 'SALESFORCE_QUERY_TIMEOUT', '(def) '),
                            getattr(settings, 'REQUESTS_MAX_RETRIES', '(def) '),
                            bb_salesforce.__version__))

        logger.info("Process starting at {0}".format(timezone.localtime(timezone.now())))

        if options['synchronize']:
            try:
                sync_all(sync_counter, logger, sync_from_datetime, only_new=options['sync_new'])
                logger.info("Process finished at {2} with {0} successes and {1} errors.".
                            format(sync_counter['s'],
                                   sync_counter['e'],
                                   timezone.localtime(timezone.now())))
            except Exception as e:
                sync_counter.update('e')
                logger.error("Error - stopping: {0}".format(e))
        elif options['csv_export']:
            try:
                export_all(logger, sync_from_datetime)
                logger.info("Process finished at {0}".format(timezone.localtime(timezone.now())))
            except Exception as e:
                sync_counter.update('e')
                logger.error("Error - stopping: {0}".format(e))

        if options['log_to_salesforce']:
            send_log(os.path.join(settings.PROJECT_ROOT, "export", "salesforce", "last.log"),
                     sync_counter['e'], sync_counter['s'], "export" if options['csv_export'] else "sync",
                     options, logger)