import logging
import sys
import os
from optparse import make_option
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
from django.db import connection
from ...synchronize import sync_all
from ...export import generate_donations_csv_file, generate_organizations_csv_file, generate_users_csv_file, \
    generate_projects_csv_file, generate_projectbudgetlines_csv_file, \
    generate_tasks_csv_file, generate_taskmembers_csv_file, generate_fundraisers_csv_file, \
    generate_organizationmember_csv_file
from ...sync import sync_organizations, sync_users, sync_projects, sync_projectbudgetlines, sync_tasks, \
    sync_taskmembers, sync_donations, sync_fundraisers, send_log, sync_organizationmembers
from bluebottle.clients.models import Client

#
# Run with:
# ./manage.py sync_to_salesforce -v 2 --settings=bluebottle.settings.salesforcesync
#


class Command(BaseCommand):
    help = 'Synchronize data to Salesforce.'
    requires_model_validation = True

    error_count = 0
    success_count = 0

    verbosity_log_level = {
        '0': logging.ERROR,    # 0 means no output.
        '1': logging.WARNING,  # 1 means normal output (default).
        '2': logging.INFO,     # 2 means verbose output.
        '3': logging.DEBUG     # 3 means very verbose output.
    }

    option_list = BaseCommand.option_list + (
        make_option('--log-to-salesforce', action='store_true', default=False, dest='log_to_salesforce',
                    help='Tenant to sync or export'),

        make_option('--tenant', '-t', action='store', type='string', dest='tenant',
                    help='Tenant to sync or export'),

        make_option('--dry-run', action='store_true', dest='dry_run', default=False,
                    help='Execute a Salesforce sync without saving to Salesforce.'),

        make_option('--sync-updated', action='store', dest='sync_updated', type='int', metavar='MINUTES',
                    help="Only sync records that have been updated in the last MINUTES minutes."),

        make_option('--sync-all', action='store_true', dest='sync_all',
                    help="Sync all records."),

        make_option('--csv-export', action='store_true', dest='csv_export', default=False,
                    help="Generate CSV files instead of syncing data with the Salesforce REST API.")
    )

    def handle(self, *args, **options):
        # Setup the log level for root logger.
        if options['log_to_salesforce']:
            logger = logging.getLogger('salesforce')
            fhndl = logging.handlers.RotatingFileHandler(os.path.join(settings.PROJECT_ROOT, "salesforce", "log", "last.log"),
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
            logger.error("You must specify a ternant with '--tenant' or '-t'.")
            logger.info("Valid tenants are: {0}".format(tenant_list))
            sys.exit(1)
        elif options['tenant'] not in tenant_list:
            logger.error("Tenant does not exists: '{0}'".format(options['tenant']))
            logger.info("Valid tenants are: {0}".format(tenant_list))
            sys.exit(1)
        else:
            tenant = Client.objects.get(client_name=options['tenant'])
            connection.set_tenant(tenant)

        if options['sync_updated'] and options['sync_all']:
            logger.error("You cannot set both '--sync-all' and '--sync-updated'.")
            sys.exit(1)
        elif not options['csv_export'] and not options['sync_updated'] and not options['sync_all']:
            logger.error("You must set either '--csv-export', '--sync-all' or '--sync-updated MINUTES'. "
                         "See help for more information.")
            sys.exit(1)

        sync_from_datetime = None
        if options['sync_updated']:
            delta = timedelta(minutes=options['sync_updated'])
            sync_from_datetime = timezone.now() - delta
            logger.info("Filtering only updated records from {0}".format(timezone.localtime(sync_from_datetime)))

        logger.info("Process starting at {0}.".format(timezone.localtime(timezone.now())))

        try:
            sync_all()

        except Exception as e:
            self.error_count += 1
            logger.error("Error - stopping: {0}".format(e))

        logger.info("Process finished at {2} with {0} successes and {1} errors.".format(self.success_count,
                                                                                        self.error_count,
                                                                                        timezone.localtime(
                                                                                            timezone.now())))
        send_log(os.path.join(settings.PROJECT_ROOT, "salesforce", "log", "last.log"),
                 self.error_count, self.success_count, "export" if options['csv_export'] else "sync",
                 options, options['dry_run'], logger)

    def run_with_count_update(self, function, *args, **kwargs):
        cur_success_count, cur_error_count = function(*args, **kwargs)
        self.success_count += cur_success_count
        self.error_count += cur_error_count