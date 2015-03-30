from bb_salesforce.base import BaseExporter


class OrganizationExporter(BaseExporter):

    field_mappings = {
        'Organization_External_Id__c': 'external_id',
        'Name': 'name',
        'BillingStreet': 'billing_street',
        'BillingCity': 'billing_city',
        'BillingState': 'billing_state',
        'BillingCountry': 'billing_country',
        'BillingPostalCode': 'billing_postal_code',
        'E_mail_address__c': 'email',
        'Phone': 'phone',
        'Website': 'website',
        'Twitter__c': 'twitter',
        'Facebook__c': 'facebook',
        'Skype__c': 'skype',
        'Tags__c': 'tags',
        'Bank_account_name__c': 'bank_account_name',
        'Bank_account_address__c': 'bank_account_address',
        'Bank_account_postalcode__c': 'bank_account_postalcode',
        'Bank_account_city__c': 'bank_account_city',
        'Bank_account_country__c': 'bank_account_country',
        'Bank_account_IBAN__c': 'bank_account_iban',
        'Bank_SWIFT__c': 'bank_bic_swift',
        'Bank_account_number__c': 'bank_account_number',
        'Bank_bankname__c': 'bank_name',
        'Bank_address__c': 'bank_address',
        'Bank_postalcode__c': 'bank_postalcode',
        'Bank_city__c': 'account_bank_city',
        'Bank_country__c': 'account_bank_country',
        'Organization_created_date__c': DateField('created_date'),
        'Deleted__c': DateSerializer('deleted_date')
    }
