# from apps.bluebottle_salesforce.models import ProjectCountry
from django.db import models
from salesforce.models import SalesforceModel
from djchoices import DjangoChoices, ChoiceItem
from django.utils.translation import ugettext as _

# TODO: remove the DjangoChoices or add it if needed to a Helper file.


class SalesforceOrganization(SalesforceModel):
    """
    Default Salesforce Account model.
    """
    class AccountType(DjangoChoices):
        business = ChoiceItem('Business', label=_("Business"))
        fund = ChoiceItem('Fund', label=_("Fund"))
        international = ChoiceItem('International Cooperation', label=_("International Cooperation"))
        network = ChoiceItem('Network', label=_("Network"))
        supplier = ChoiceItem('Supplier', label=_("Supplier"))
        individual = ChoiceItem('Individual', label=_("Individual"))
        percent_idea = ChoiceItem('1%IDEA', label=_("1%IDEA"))
        government = ChoiceItem('Government & Politics', label=_("Individual"))
        media_pr = ChoiceItem('Media / PR', label=_("Media / PR"))

    Legal_status = models.CharField(max_length=10000, db_column='Legal_status__c')
    Name = models.CharField(max_length=255, db_column='Name')
    Type = models.CharField(max_length=40, db_column="Type", choices=AccountType.choices,
                                         help_text=("Type"))
    external_id = models.CharField(max_length=255, db_column='Organization_External_ID__c')
    BillingCity = models.CharField(max_length=40, db_column='BillingCity')
    BillingStreet = models.CharField(max_length=255, db_column='BillingStreet')
    BillingPostalCode = models.CharField(max_length=20, db_column='BillingPostalCode')
    BillingCountry = models.CharField(max_length=80, db_column='BillingCountry')
    BillingState = models.CharField(max_length=20, db_column='BillingState')
    E_mail_address = models.EmailField(max_length=80, db_column='E_mail_address__c')
    Phone = models.CharField(max_length=40, db_column='Phone')
    Website = models.URLField(max_length=255, db_column='Website')
    Bank_account_address = models.CharField(max_length=255, db_column='Bank_account_address__c')
    Bank_account_name = models.CharField(max_length=255, db_column='Bank_account_name__c')
    Bank_account_number = models.CharField(max_length=40, db_column='Bank_account_number__c')
    Bank_account_IBAN = models.CharField(max_length=255, db_column='Bank_account_IBAN__c')
    Bank_account_postalcode = models.CharField(max_length=20, db_column='Bank_account_postalcode__c')
    Bank_account_city = models.CharField(max_length=255, db_column='Bank_account_city__c')
    Bank_account_country = models.CharField(max_length=60, db_column='Bank_account_country__c')
    Bank_bankname = models.CharField(max_length=255, db_column='Bank_bankname__c')
    Bank_SWIFT = models.CharField(max_length=40, db_column='Bank_SWIFT__c')
    Bank_address = models.CharField(max_length=255, db_column='Bank_address__c')
    Bank_postalcode = models.CharField(max_length=20, db_column='Bank_postalcode__c')
    Bank_city = models.CharField(max_length=255, db_column='Bank_city__c')
    Bank_country = models.CharField(max_length=60, db_column='Bank_country__c')
    Twitter = models.CharField(max_length=255, db_column='Twitter__c')
    Facebook = models.CharField(max_length=255, db_column='Facebook__c')
    Tags = models.CharField(max_length=255, db_column='Tags__c')
    Skype = models.CharField(max_length=255, db_column='Skype__c')
    Organization_created_date = models.DateField(db_column='Organization_created_date__c')
    Deleted = models.DateTimeField(db_column='Deleted__c')

    class Meta:
        db_table = 'Account'
        managed = False


class SalesforceMember(SalesforceModel):
    """
    Default Salesforce Contact model.
    """
    external_id = models.CharField(max_length=255, db_column='Contact_External_ID__c')
    Username = models.CharField(max_length=255, db_column='Username__c')
    Category1 = models.CharField(max_length=255, db_column='Category1__c')
    Email = models.EmailField(max_length=80, db_column='Email')
    Member_1_club = models.BooleanField(db_column='Member_1_club__c', default=True)
    Active = models.BooleanField(db_column='Active__c')
    Has_Activated_Account = models.BooleanField(db_column='Has_Activated_Account__c')
    Deleted = models.DateField(db_column='Deleted__c')
    FirstName = models.CharField(max_length=40, db_column='FirstName')
    LastName = models.CharField(max_length=80, db_column='LastName', null=False, blank=False)
    Member_since = models.DateField(db_column='Member_since__c')
    Why_onepercent_member = models.CharField(max_length=32000, db_column='Why_onepercent_member__c')
    About_me_us = models.CharField(max_length=3200, db_column='About_me_us__c')
    Location = models.CharField(max_length=100, db_column='Location__c')
    Picture_Location = models.CharField(max_length=255, db_column='Picture_Location__c')
    Website = models.CharField(max_length=255, db_column='Website__c')
    Date_Last_Login = models.DateTimeField(db_column='Date_Last_Login__c')
    Date_Joined = models.DateTimeField(db_column='Date_Joined__c')
    Account_number = models.CharField(max_length=30, db_column='Account_number__c')
    Account_holder = models.CharField(max_length=60, db_column='Account_holder__c')
    Account_city = models.CharField(max_length=50, db_column='Account_city__c')
    Account_IBAN = models.CharField(max_length=40, db_column='Account_IBAN__c')
    Account_Active_Recurring_Debit = models.BooleanField(db_column='Account_Active_Recurring_Debit__c')
    Has_n_friends = models.CharField(max_length=255, db_column='Has_n_friends__c')
    Has_given_n_1_VOUCHERS = models.CharField(max_length=255, db_column='Has_given_n_1_VOUCHERS__c')
    Number_of_donations = models.CharField(max_length=255, db_column='Number_of_donations__c')
    Support_n_projects = models.CharField(max_length=255, db_column='Support_n_projects__c')
    Total_amount_of_donations = models.CharField(max_length=255, db_column='Total_amount_of_donations__c')
    Birthdate = models.DateField(db_column='Birthdate')
    Gender = models.CharField(max_length=20, db_column='Gender__c')
    MailingCity = models.CharField(max_length=40, db_column='MailingCity')
    MailingCountry = models.CharField(max_length=40, db_column='MailingCountry')
    MailingPostalCode = models.CharField(max_length=20, db_column='MailingPostalCode')
    MailingStreet = models.CharField(max_length=20, db_column='MailingStreet')
    MailingState = models.CharField(max_length=80, db_column='MailingState')
    Phone = models.CharField(max_length=40, db_column='Phone')
    Facebook = models.CharField(max_length=50, db_column='Facebook__c')
    Twitter = models.CharField(max_length=250, db_column='Twitter__c')
    Skype = models.CharField(max_length=255, db_column='Skype__c')
    Available_time = models.CharField(max_length=255, db_column='Available_time__c')
    Where = models.CharField(max_length=255, db_column='Where__c')
    Availability = models.CharField(max_length=255, db_column='Availability__c')
    Receive_newsletter = models.BooleanField(db_column='Receive_newsletter__c')
    Primary_language = models.CharField(max_length=255, db_column='Primary_language__c')
    Tags = models.CharField(max_length=255, db_column='Tags')

    class Meta:
        db_table = 'Contact'
        managed = False


class SalesforceCountry(SalesforceModel):
    external_id = models.CharField(max_length=255, db_column='External_Id__c')

    class Meta:
        db_table = 'Country__c'
        managed = False


class SalesforceProject(SalesforceModel):
    """
    Custom Salesforce Project__c model. For Onepercentclub the mapping is named 1%CLUB Project(s).
    """
    class ProjectStatus(DjangoChoices):
        closed = ChoiceItem('Closed', label=_("Closed"))
        created = ChoiceItem('Created', label=_("Created"))
        done = ChoiceItem('Done', label=_("Done"))
        validated = ChoiceItem('Validated', label=_("Validated"))

    Amount_at_the_moment = models.CharField(max_length=255, db_column='Amount_at_the_moment__c')
    Amount_requested = models.CharField(max_length=255, db_column='Amount_requested__c')
    Amount_still_needed = models.CharField(max_length=255, db_column='Amount_still_needed__c')
    Amount_extra = models.CharField(max_length=255, db_column='Amount_extra__c')
    Project_name = models.CharField(max_length=80, db_column='Project_name__c')
    Project_Owner = models.ForeignKey(SalesforceMember, db_column='Project_Owner__c')
    Status_project = models.CharField(max_length=255,
                                      db_column='Status_project__c',
                                      choices=ProjectStatus.choices,
                                      help_text=_("Status project"))
    Target_group_s_of_the_project = models.CharField(max_length=20000, db_column='Target_group_s_of_the_project__c')
    Country_in_which_the_project_is_located = models.CharField(max_length=255,
                                                               db_column='Country_in_which_the_project_is_located__c')
    Country = models.ForeignKey(SalesforceCountry, db_column='Country__c', null=True)
    Region = models.CharField(max_length=100, db_column='Region__c')
    Sub_region = models.CharField(max_length=100, db_column='Sub_region__c')
    Describe_the_project_in_one_sentence = models.CharField(max_length=50000,
                                                            db_column='Describe_the_project_in_one_sentence__c')
    Story = models.CharField(max_length=32768, db_column='Story__c')
    third_half_project = models.BooleanField(db_column='third_half_project__c', default=False)
    Organization = models.ForeignKey(SalesforceOrganization, db_column='Organization__c', null=True)
    Comments = models.CharField(max_length=32000, db_column='Comments__c')
    Contribution_project_in_reducing_poverty = models.CharField(max_length=32000,
                                                                db_column='Contribution_project_in_reducing_poverty__c')
    Earth_Charther_project = models.BooleanField(db_column='Earth_Charther_project__c', default=False)
    Skip_Monthly = models.BooleanField(db_column='Skip_Monthly__c', default=False)
    Sustainability = models.CharField(max_length=20000, db_column='Sustainability__c')
    Additional_explanation_of_budget = models.CharField(max_length=32000,
                                                        db_column='Additional_explanation_of_budget__c')
    Tags = models.CharField(max_length=255, db_column='Tags__c')
    Slug = models.CharField(max_length=100, db_column='Slug__c')
    Category = models.CharField(max_length=255, db_column='Category__c')
    Type = models.CharField(max_length=60, db_column='Type__c')
    VideoURL = models.CharField(max_length=255, db_column='VideoURL__c')
    Picture_Location = models.CharField(max_length=255, db_column='Picture_Location__c')
    Date_Started = models.DateField(db_column='Date_Started__c')
    Date_Funded = models.DateField(db_column='Date_Funded__c')
    Date_Ended = models.DateField(db_column='Date_Ended__c')
    Is_Campaign = models.BooleanField(db_column='Is_Campaign__c')
    Allow_Overfunding = models.BooleanField(db_column='Allow_Overfunding__c')
    Name_referral_1 = models.CharField(max_length=255, db_column='Name_referral_1__c')
    Name_referral_2 = models.CharField(max_length=255, db_column='Name_referral_2__c')
    Name_referral_3 = models.CharField(max_length=255, db_column='Name_referral_3__c')
    Description_referral_1 = models.CharField(max_length=32000, db_column='Description_referral_1__c')
    Description_referral_2 = models.CharField(max_length=32000, db_column='Description_referral_2__c')
    Description_referral_3 = models.CharField(max_length=32000, db_column='Description_referral_3__c')
    E_mail_address_referral_1 = models.EmailField(max_length=80, blank=True, null=True,
                                                 db_column='E_mail_address_referral_1__c')
    E_mail_address_referral_2 = models.EmailField(max_length=80, blank=True, null=True,
                                                 db_column='E_mail_address_referral_2__c')
    E_mail_address_referral_3 = models.EmailField(max_length=80, blank=True, null=True,
                                                 db_column='E_mail_address_referral_3__c')
    Relation_referral_1_with_project_org = models.CharField(max_length=32000,
                                                            db_column='Relation_referral_1_with_project_org__c')
    Relation_referral_2_with_project_org = models.CharField(max_length=32000,
                                                            db_column='Relation_referral_2_with_project_org__c')
    Relation_referral_3_with_project_org = models.CharField(max_length=32000,
                                                            db_column='Relation_referral_3_with_project_org__c')
    Date_plan_submitted = models.DateField(db_column='Date_plan_submitted__c')
    Project_created_date = models.DateTimeField(db_column='Project_created_date__c')
    Project_updated_date = models.DateTimeField(db_column='Project_updated_date__c')
    Date_project_deadline = models.DateField(db_column='Date_project_deadline__c')
    external_id = models.CharField(max_length=255, db_column='Project_External_ID__c')
    NumberOfPeopleReachedDirect = models.PositiveIntegerField(db_column='NumberOfPeopleReachedDirect__c')
    NumberOfPeopleReachedIndirect = models.PositiveIntegerField(db_column='NumberOfPeopleReachedIndirect__c')
    Theme = models.CharField(max_length=255, db_column='Theme__c')
    Language = models.CharField(max_length=255, db_column='Language__c')
    Donation_total = models.CharField(max_length=20, db_column='Donation_total__c')
    Supporter_count = models.PositiveIntegerField(db_column='Supporter_count__c')
    Donation_oo_total = models.CharField(max_length=20, db_column='Donation_oo_total__c')
    Supporter_oo_count = models.PositiveIntegerField(db_column='Supporter_oo_count__c')
    Popularity = models.CharField(max_length=200, db_column='Popularity__c')

    class Meta:
        db_table = 'Project__c'
        managed = False


class SalesforceProjectBudgetLine(SalesforceModel):
    """
    Custom Salesforce Project_Budget__c model. For Onepercentclub the mapping is named Project Budget.
    """
    Costs = models.CharField(max_length=255, db_column='Costs__c')
    Description = models.CharField(max_length=32000, db_column='Description__c')
    external_id = models.CharField(max_length=255, db_column='Project_Budget_External_ID__c')
    Project = models.ForeignKey(SalesforceProject, db_column='Project__c')

    class Meta:
        db_table = 'Project_Budget__c'
        managed = False


class SalesforceFundraiser(SalesforceModel):
    """
    Custom Fundraiser__c model.
    """
    Amount = models.CharField(max_length=100, db_column='Amount__c')
    Owner = models.ForeignKey(SalesforceMember, db_column='Owner__c')
    Created = models.DateTimeField(db_column='Created__c')
    Deadline = models.DateField(db_column='Deadline__c')
    Description = models.CharField(max_length=131072, db_column='Description__c')
    external_id = models.CharField(max_length=255, db_column='Fundraiser_External_ID__c')
    Picture_Location = models.CharField(max_length=255, db_column='Picture_Location__c')
    Project = models.ForeignKey(SalesforceProject, db_column='Project__c')
    VideoURL = models.CharField(max_length=255, db_column='VideoURL__c')
    Name = models.CharField(max_length=80, db_column='Name')
    Amount_at_the_moment = models.CharField(max_length=100, db_column='Amount_at_the_moment__c')

    class Meta:
        db_table = 'Fundraiser__c'
        managed = False


class SalesforceOpportunity(SalesforceModel):
    """
    Default abstract Salesforce Opportunity model. Used for Donation(s) / Voucher(s).
    """
    Amount = models.CharField(max_length=255, db_column='Amount')
    CloseDate = models.DateField(db_column='CloseDate')
    Type = models.CharField(max_length=40, db_column='Type')
    Name = models.CharField(max_length=120, db_column='Name')
    Payment_method = models.CharField(max_length=255,
                                      db_column='Payment_method__c',
                                      help_text=_("PaymentMethod"))
    Project = models.ForeignKey(SalesforceProject, db_column='Project__c', null=True)
    StageName = models.CharField(max_length=40,
                                  db_column='StageName')
    RecordTypeId = models.CharField(max_length=255, db_column='RecordTypeId')

    class Meta:
        abstract = True
        managed = False


class SalesforceDonation(SalesforceOpportunity):
    """
    Child of the Opportunity for Onepercentclub the mapping is named Donation(s).
    """

    Donation_created_date = models.DateTimeField(db_column='Donation_created_date__c')
    Donation_updated_date = models.DateTimeField(db_column='Donation_updated_date__c')
    Donation_ready_date = models.DateTimeField(db_column='Donation_ready_date__c')
    external_id = models.CharField(max_length=255, db_column='Donation_External_ID__c')
    Receiver = models.ForeignKey(SalesforceMember, db_column='Receiver__c', null=True)
    Fundraiser = models.ForeignKey(SalesforceFundraiser, db_column='Fundraiser__c', null=True)

    class Meta:
        managed = False
        db_table = 'Opportunity'


class SalesforceVoucher(SalesforceOpportunity):
    """
    Child of the Opportunity for Onepercentclub the mapping is named Voucher(s).
    """
    Purchaser = models.ForeignKey(SalesforceMember, db_column='Purchaser__c', related_name='contact_purchasers')
    Description = models.CharField(max_length=32000, db_column='Description')
    Receiver = models.ForeignKey(SalesforceMember, db_column='Receiver__c', related_name='contact_receivers', null=True)
    external_id = models.CharField(max_length=255, db_column='Voucher_External_ID__c')

    class Meta:
        managed = False
        db_table = 'Opportunity'


class SalesforceTask(SalesforceModel):
    """
    Custom Salesforce Tasks__c model. For Onepercentclub the mapping is named 1%CLUB Task(s).
    """
    class TaskStatus(DjangoChoices):
        open = ChoiceItem('Open', label=_("Open"))
        running = ChoiceItem('Running', label=_("Running"))
        closed = ChoiceItem('Closed', label=_("Closed"))
        realized = ChoiceItem('Realized', label=_("Realized"))

    Project = models.ForeignKey(SalesforceProject, db_column='Project__c')
    Deadline = models.DateField(db_column='Deadline__c')
    Effort = models.CharField(max_length=200, db_column='Effort__c')
    Extended_task_description = models.CharField(max_length=32000, db_column='Extended_task_description__c')
    Location_of_the_task = models.CharField(max_length=200, db_column='Location_of_the_task__c')
    Task_expertise = models.CharField(max_length=100, db_column='Task_expertise__c')
    Task_status = models.CharField(max_length=40, db_column='Task_status__c', choices=TaskStatus.choices, help_text=_("TaskStatus"))
    Title = models.CharField(max_length=100, db_column='Title__c')
    Task_created_date = models.DateField(db_column='Task_created_date__c')
    Tags = models.CharField(max_length=255, db_column='Tags__c')
    Date_realized = models.DateField(db_column='Date_realized__c')
    Author = models.ForeignKey(SalesforceMember, db_column='Author__c')
    People_Needed = models.CharField(max_length=10, db_column='People_Needed__c')
    End_Goal = models.CharField(max_length=5000, db_column='End_Goal__c')

    external_id = models.CharField(max_length=255, db_column='Task_External_ID__c')

    class Meta:
        db_table = 'onepercentclubTasks__c'
        managed = False


class SalesforceTaskMember(SalesforceModel):
    """
    Custom Salesforce Task_Members__c model. For Onepercentclub the mapping is named Task Member(s).
    The table is used as a joined table which relates to Tasks to the Contacts.
    """
    Contacts = models.ForeignKey(SalesforceMember, db_column='Contacts__c')
    X1_CLUB_Task = models.ForeignKey(SalesforceTask, db_column='X1_CLUB_Task__c')
    external_id = models.CharField(max_length=100, db_column='Task_Member_External_ID__c')
    Motivation = models.CharField(max_length=5000, db_column='Motivation__c')
    Status = models.CharField(max_length=255, db_column='Status__c')
    Taskmember_Created_Date = models.DateField(db_column='Taskmember_Created_Date__c')

    class Meta:
        db_table = 'Task_Members__c'
        managed = False


class SalesforceOrganizationMember(SalesforceModel):
    """
    Custom Salesforce Organization_Member__c object.
    The object is used as a junction object that connects Account and Contact.
    """
    Contact = models.ForeignKey(SalesforceMember, db_column='Contact__c')
    Organization = models.ForeignKey(SalesforceOrganization, db_column='Organization__c')
    Role = models.CharField(max_length=20, db_column='Role__c')
    external_id = models.CharField(max_length=100, db_column='Organization_Member_External_Id__c')

    class Meta:
        db_table = 'Organization_Member__c'
        managed = False


class SalesforceLogItem(SalesforceModel):
    """
    Custom Salesforce Log_Item__c object.
    The object is used to store log data from external and internal sources.
    """
    Entered = models.DateTimeField(db_column='Entered__c')
    Errors = models.PositiveIntegerField(db_column='Errors__c')
    Message = models.CharField(max_length=32000, db_column='Message__c')
    Source = models.CharField(max_length=255, db_column='Source__c')
    Source_Extended = models.CharField(max_length=255, db_column='Source_Extended__c')
    Successes = models.PositiveIntegerField(db_column='Successes__c')

    class Meta:
        db_table = 'Log_Item__c'
        managed = False
