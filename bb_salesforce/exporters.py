# -*- coding: utf-8 -*-

from bb_salesforce.base import BaseExporter
from bb_salesforce.serializers import DateSerializer, BooleanSerializer
from collections import OrderedDict

class OrganizationExporter(BaseExporter):

    field_mapping = OrderedDict([
        ('Organization_External_Id__c', 'external_id'),
        ('Name', 'name'),
        ('BillingStreet', 'billing_street'),
        ('BillingCity', 'billing_city'),
        ('BillingState', 'billing_state'),
        ('BillingCountry', 'billing_country'),
        ('BillingPostalCode', 'billing_postal_code'),
        ('E_mail_address__c', 'email'),
        ('Phone', 'phone'),
        ('Website', 'website'),
        ('Twitter__c', 'twitter'),
        ('Facebook__c', 'facebook'),
        ('Skype__c', 'skype'),
        ('Tags__c', 'tags'),
        ('Bank_account_name__c', 'bank_account_name'),
        ('Bank_account_address__c', 'bank_account_address'),
        ('Bank_account_postalcode__c', 'bank_account_postalcode'),
        ('Bank_account_city__c', 'bank_account_city'),
        ('Bank_account_country__c', 'bank_account_country'),
        ('Bank_account_IBAN__c', 'bank_account_iban'),
        ('Bank_SWIFT__c', 'bank_bic_swift'),
        ('Bank_account_number__c', 'bank_account_number'),
        ('Bank_bankname__c', 'bank_name'),
        ('Bank_address__c', 'bank_address'),
        ('Bank_postalcode__c', 'bank_postalcode'),
        ('Bank_city__c', 'bank_city'),
        ('Bank_country__c', 'account_bank_country'),
        ('Organization_created_date__c', DateSerializer('created_date')),
        ('Deleted__c', DateSerializer('deleted_date'))
    ])


class MemberExporter(BaseExporter):

    field_mapping = OrderedDict([
        ('Contact_External_Id__c', 'external_id'),
        ('Category1__c', 'contact.category1'),
        ('FirstName', 'first_name'),
        ('LastName', 'last_name'),
        ('Gender__c', 'gender'),
        ('Username__c', 'user_name'),
        ('Active__c', BooleanSerializer('is_active')), # Always true
        ('Deleted__c', DateSerializer('deleted')), # Not used
        ('Member_since__c', DateSerializer('date_joined')),
        ('Location__c', 'location'),
        ('Birthdate', DateSerializer('birth_date')),
        ('Email', 'email'),
        ('Website__c', ''), # Removed
        ('Picture_Location__c', 'picture_location'),
        ('Tags__c', ''), # Removed
        ('MailingCity', 'mailing_city'),
        ('MailingStreet', 'mailing_street'),
        ('MailingCountry', 'mailing_country'),
        ('MailingPostalCode', 'mailing_postal_code'),
        ('MailingState', 'mailing_state'),
        ('Receive_newsletter__c', BooleanSerializer('receive_newsletter')),
        ('Primary_language__c', 'primary_language'),
        ('Available_to_share_time_and_knowledge__c', ''), # Removed
        ('Available_to_donate__c', ''), # Removed
        ('Availability__c', ''), # Removed
        ('Facebook__c', ''), # Removed
        ('Twitter__c', ''), # Removed
        ('Skype__c', ''), # Removed
        ('Has_Activated_Account__c', BooleanSerializer('is_active')), # Duplicate
        ('Date_Joined__c', DateSerializer('date_joined')), # Duplicate
        ('Date_Last_Login__c', DateSerializer('date_joined')), # Duplicate
        ('Account_number__c', ''), # Removed
        ('Account_holder__c', 'bank_account_holder'),
        ('Account_city__c', 'bank_account_city'),
        ('Account_IBAN__c', 'bank_account_iban'),
        ('Account_Active_Recurring_Debit__c', 'bank_account_active_recurring_debit'),
        ('Phone', 'phone')
    ])


class ProjectExporter(BaseExporter):
    
    field_mapping = OrderedDict([
        ('Project_External_ID__c', ''),
        ('Project_name__c', ''),
        ('NumerOfPeopleReachedDirect__c', ''),
        ('VideoURL__c', ''),
        ('Date_project_deadline__c', ''),
        ('Is_Campaign__c', ''),
        ('Amount_requested__c', ''),
        ('Amount_at_the_moment__c', ''),
        ('Amount_still_needed__c', ''),
        ('Allow_Overfunding__c', ''),
        ('Date_plan_submitted', ''),
        ('Date_Started__c', ''),
        ('Date_Ended__c', ''),
        ('Date_Funded__c', ''),
        ('Picture_Location__c', ''),
        ('Project_Owner__c', ''),
        ('Organization__c', ''),
        ('Country_in_which_the_project_is_located__c', ''),
        ('Theme__c', ''),
        ('Status_project__c', ''),
        ('Project_created_date__c', ''),
        ('Project_updated_date__c', ''),
        ('Tags__c', ''),
        ('Partner_Organization__c', ''),
        ('Slug__c', ''),
        ('Region__c', ''),
        ('Sub_region__c', ''),
        ('Donation_total__c', ''),
        ('Donation_oo_total__c', ''),
        ('Supporter_count__c', ''),
        ('Supporter_oo_count__c', '')
    ])


class BudgetLineExporter(BaseExporter):

    field_mapping = OrderedDict([
        ('Project_Budget_External_ID__c', ''),
        ('Project__c', ''),
        ('Costs__c', ''),
        ('Description__c', '')
    ])


class DonationExporter(BaseExporter):

    field_mapping = OrderedDict([
        ('Donation_External_ID__c', ''),
        ('Donor__c', ''),
        ('Project__c', ''),
        ('Amount', ''),
        ('CloseDate', ''),
        ('Name', ''),
        ('StageName', ''),
        ('Type', ''),
        ('Donation_created_date__c', ''),
        ('Donation_updated_date__c', ''),
        ('Donation_ready_date__c', ''),
        ('Payment_method__c', ''),
        ('RecordTypeId', ''),
        ('Fundraiser__c', '')
    ])


class TaskExporter(BaseExporter):

    field_mapping = OrderedDict([
        ('Task_External_ID__c', ''),
        ('Project__c', ''),
        ('Deadline__c', ''),
        ('Location_of_the_task__c', ''),
        ('Task_expertise__c', ''),
        ('Task_status__c', ''),
        ('Title__c', ''),
        ('Task_created_date__c', ''),
        ('Tags__c', ''),
        ('Effort__c', ''),
        ('People_Needed__c', ''),
        ('Author__c', ''),
        ('Date_realized__c', '')
    ])


class TaskMemberExporter(BaseExporter):

    field_mapping = OrderedDict([
        ('Task_Member_External_ID__c', ''),
        ('Contacts__c', ''),
        ('X1_CLUB_Task__c', ''),
        ('Status__c', ''),
        ('Taskmember_Created_Date__c', '')
    ])


class FundraiserExporter(BaseExporter):

    field_mapping = OrderedDict([
        ('Fundraiser_External_ID__c', ''),
        ('Name', ''),
        ('Owner__c', ''),
        ('Project__c', ''),
        ('Picture_Location__c', ''),
        ('VideoURL__c', ''),
        ('Amount__c', ''),
        ('Amount_at_the_moment__c', ''),
        ('Deadline__c', ''),
        ('Created__c', '')
    ])


class OrganizationMemberExporter(BaseExporter):

    field_mapping = OrderedDict([
        ('Organization_Member_External_Id__c', ''),
        ('Contact__c', ''),
        ('Account__c', ''),
        ('Role__c', '')
    ])
