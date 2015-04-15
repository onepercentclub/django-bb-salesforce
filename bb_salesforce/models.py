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

    Legal_status__c = models.CharField(max_length=10000, db_column='Legal_status__c')
    Name = models.CharField(max_length=255, db_column='Name')
    Type = models.CharField(max_length=40, db_column="Type", choices=AccountType.choices,
                                         help_text=("Type"))
    Organization_External_ID__c = models.CharField(max_length=255, db_column='Organization_External_ID__c')
    BillingCity = models.CharField(max_length=40, db_column='BillingCity')
    BillingStreet = models.CharField(max_length=255, db_column='BillingStreet')
    BillingPostalCode = models.CharField(max_length=20, db_column='BillingPostalCode')
    BillingCountry = models.CharField(max_length=80, db_column='BillingCountry')
    BillingState = models.CharField(max_length=20, db_column='BillingState')
    E_mail_address__c = models.EmailField(max_length=80, db_column='E_mail_address__c')
    Phone = models.CharField(max_length=40, db_column='Phone')
    Website = models.URLField(max_length=255, db_column='Website')
    Bank_account_address__c = models.CharField(max_length=255, db_column='Bank_account_address__c')
    Bank_account_name__c = models.CharField(max_length=255, db_column='Bank_account_name__c')
    Bank_account_number__c = models.CharField(max_length=40, db_column='Bank_account_number__c')
    Bank_account_IBAN__c = models.CharField(max_length=255, db_column='Bank_account_IBAN__c')
    Bank_account_postalcode__c = models.CharField(max_length=20, db_column='Bank_account_postalcode__c')
    Bank_account_city__c = models.CharField(max_length=255, db_column='Bank_account_city__c')
    Bank_account_country__c = models.CharField(max_length=60, db_column='Bank_account_country__c')
    Bank_bankname__c = models.CharField(max_length=255, db_column='Bank_bankname__c')
    Bank_SWIFT__c = models.CharField(max_length=40, db_column='Bank_SWIFT__c')
    Bank_address__c = models.CharField(max_length=255, db_column='Bank_address__c')
    Bank_postalcode__c = models.CharField(max_length=20, db_column='Bank_postalcode__c')
    Bank_city__c = models.CharField(max_length=255, db_column='Bank_city__c')
    Bank_country__c = models.CharField(max_length=60, db_column='Bank_country__c')
    Twitter__c = models.CharField(max_length=255, db_column='Twitter__c')
    Facebook__c = models.CharField(max_length=255, db_column='Facebook__c')
    Tags__c = models.CharField(max_length=255, db_column='Tags__c')
    Skype__c = models.CharField(max_length=255, db_column='Skype__c')
    Organization_created_date__c = models.DateField(db_column='Organization_created_date__c')
    Deleted__c = models.DateTimeField(db_column='Deleted__c')

    class Meta:
        db_table = 'Account'
        managed = False


class SalesforceMember(SalesforceModel):
    """
    Default Salesforce Contact model.
    """
    Contact_External_ID__c = models.CharField(max_length=255, db_column='Contact_External_ID__c')
    Username__c = models.CharField(max_length=255, db_column='Username__c')
    Category1__c = models.CharField(max_length=255, db_column='Category1__c')
    Email = models.EmailField(max_length=80, db_column='Email')
    Member_1_club__c = models.BooleanField(db_column='Member_1_club__c', default=True)
    Active__c = models.BooleanField(db_column='Active__c')
    Has_Activated_Account__c = models.BooleanField(db_column='Has_Activated_Account__c')
    Deleted__c = models.DateField(db_column='Deleted__c')
    FirstName = models.CharField(max_length=40, db_column='FirstName')
    LastName = models.CharField(max_length=80, db_column='LastName', null=False, blank=False)
    Member_since__c = models.DateField(db_column='Member_since__c')
    Why_onepercent_member__c = models.CharField(max_length=32000, db_column='Why_onepercent_member__c')
    About_me_us__c = models.CharField(max_length=3200, db_column='About_me_us__c')
    Location__c = models.CharField(max_length=100, db_column='Location__c')
    Picture_Location__c = models.CharField(max_length=255, db_column='Picture_Location__c')
    Website__c = models.CharField(max_length=255, db_column='Website__c')
    Date_Last_Login__c = models.DateTimeField(db_column='Date_Last_Login__c')
    Date_Joined__c = models.DateTimeField(db_column='Date_Joined__c')
    Account_number__c = models.CharField(max_length=30, db_column='Account_number__c')
    Account_holder__c = models.CharField(max_length=60, db_column='Account_holder__c')
    Account_city__c = models.CharField(max_length=50, db_column='Account_city__c')
    Account_IBAN__c = models.CharField(max_length=40, db_column='Account_IBAN__c')
    Account_Active_Recurring_Debit__c = models.BooleanField(db_column='Account_Active_Recurring_Debit__c')
    Has_n_friends__c = models.CharField(max_length=255, db_column='Has_n_friends__c')
    Has_given_n_1_VOUCHERS__c = models.CharField(max_length=255, db_column='Has_given_n_1_VOUCHERS__c')
    Number_of_donations__c = models.CharField(max_length=255, db_column='Number_of_donations__c')
    Support_n_projects__c = models.CharField(max_length=255, db_column='Support_n_projects__c')
    Total_amount_of_donations__c = models.CharField(max_length=255, db_column='Total_amount_of_donations__c')
    Birthdate = models.DateField(db_column='Birthdate')
    Gender__c = models.CharField(max_length=20, db_column='Gender__c')
    MailingCity = models.CharField(max_length=40, db_column='MailingCity')
    MailingCountry = models.CharField(max_length=40, db_column='MailingCountry')
    MailingPostalCode = models.CharField(max_length=20, db_column='MailingPostalCode')
    MailingStreet = models.CharField(max_length=20, db_column='MailingStreet')
    MailingState = models.CharField(max_length=80, db_column='MailingState')
    Phone = models.CharField(max_length=40, db_column='Phone')
    Facebook__c = models.CharField(max_length=50, db_column='Facebook__c')
    Twitter__c = models.CharField(max_length=250, db_column='Twitter__c')
    Skype__c = models.CharField(max_length=255, db_column='Skype__c')
    Available_time__c = models.CharField(max_length=255, db_column='Available_time__c')
    Where__c = models.CharField(max_length=255, db_column='Where__c')
    Availability__c = models.CharField(max_length=255, db_column='Availability__c')
    Receive_newsletter__c = models.BooleanField(db_column='Receive_newsletter__c')
    Primary_language__c = models.CharField(max_length=255, db_column='Primary_language__c')
    Tags__c = models.CharField(max_length=255, db_column='Tags__c')

    class Meta:
        db_table = 'Contact'
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

    Amount_at_the_moment__c = models.CharField(max_length=255, db_column='Amount_at_the_moment__c')
    Amount_requested__c = models.CharField(max_length=255, db_column='Amount_requested__c')
    Amount_still_needed__c = models.CharField(max_length=255, db_column='Amount_still_needed__c')
    Project_name__c = models.CharField(max_length=80, db_column='Project_name__c')
    Project_Owner__c = models.ForeignKey(SalesforceMember, db_column='Project_Owner__c')
    Status_project__c = models.CharField(max_length=255,
                                      db_column='Status_project__c',
                                      choices=ProjectStatus.choices,
                                      help_text=_("Status project"))
    Target_group_s_of_the_project__c = models.CharField(max_length=20000, db_column='Target_group_s_of_the_project__c')
    Country_in_which_the_project_is_located__c = models.CharField(max_length=255,
                                                               db_column='Country_in_which_the_project_is_located__c')
    Region__c = models.CharField(max_length=100, db_column='Region__c')
    Sub_region__c = models.CharField(max_length=100, db_column='Sub_region__c')
    Describe_the_project_in_one_sentence__c = models.CharField(max_length=50000,
                                                            db_column='Describe_the_project_in_one_sentence__c')
    Story__c = models.CharField(max_length=32768, db_column='Story__c')
    third_half_project__c = models.BooleanField(db_column='third_half_project__c', default=False)
    Organization__c = models.ForeignKey(SalesforceOrganization, db_column='Organization__c', null=True)
    Comments__c = models.CharField(max_length=32000, db_column='Comments__c')
    Contribution_project_in_reducing_poverty__c = models.CharField(max_length=32000,
                                                                db_column='Contribution_project_in_reducing_poverty__c')
    Earth_Charther_project__c = models.BooleanField(db_column='Earth_Charther_project__c', default=False)
    Sustainability__c = models.CharField(max_length=20000, db_column='Sustainability__c')
    Additional_explanation_of_budget__c = models.CharField(max_length=32000,
                                                        db_column='Additional_explanation_of_budget__c')
    Tags__c = models.CharField(max_length=255, db_column='Tags__c')
    Slug__c = models.CharField(max_length=100, db_column='Slug__c')
    Partner_Organization__c = models.CharField(max_length=255, db_column='Partner_Organization__c')
    VideoURL__c = models.CharField(max_length=255, db_column='VideoURL__c')
    Picture_Location__c = models.CharField(max_length=255, db_column='Picture_Location__c')
    Date_Started__c = models.DateField(db_column='Date_Started__c')
    Date_Funded__c = models.DateField(db_column='Date_Funded__c')
    Date_Ended__c = models.DateField(db_column='Date_Ended__c')
    Is_Campaign__c = models.BooleanField(db_column='Is_Campaign__c')
    Allow_Overfunding__c = models.BooleanField(db_column='Allow_Overfunding__c')
    Name_referral_1__c = models.CharField(max_length=255, db_column='Name_referral_1__c')
    Name_referral_2__c = models.CharField(max_length=255, db_column='Name_referral_2__c')
    Name_referral_3__c = models.CharField(max_length=255, db_column='Name_referral_3__c')
    Description_referral_1__c = models.CharField(max_length=32000, db_column='Description_referral_1__c')
    Description_referral_2__c = models.CharField(max_length=32000, db_column='Description_referral_2__c')
    Description_referral_3__c = models.CharField(max_length=32000, db_column='Description_referral_3__c')
    E_mail_address_referral_1__c = models.EmailField(max_length=80, blank=True, null=True,
                                                 db_column='E_mail_address_referral_1__c')
    E_mail_address_referral_2__c = models.EmailField(max_length=80, blank=True, null=True,
                                                 db_column='E_mail_address_referral_2__c')
    E_mail_address_referral_3__c = models.EmailField(max_length=80, blank=True, null=True,
                                                 db_column='E_mail_address_referral_3__c')
    Relation_referral_1_with_project_org__c = models.CharField(max_length=32000,
                                                            db_column='Relation_referral_1_with_project_org__c')
    Relation_referral_2_with_project_org__c = models.CharField(max_length=32000,
                                                            db_column='Relation_referral_2_with_project_org__c')
    Relation_referral_3_with_project_org__c = models.CharField(max_length=32000,
                                                            db_column='Relation_referral_3_with_project_org__c')
    Date_plan_submitted__c = models.DateField(db_column='Date_plan_submitted__c')
    Project_created_date__c = models.DateTimeField(db_column='Project_created_date__c')
    Project_updated_date__c = models.DateTimeField(db_column='Project_updated_date__c')
    Date_project_deadline__c = models.DateField(db_column='Date_project_deadline__c')
    Project_External_ID__c = models.CharField(max_length=255, db_column='Project_External_ID__c')
    NumberOfPeopleReachedDirect__c = models.PositiveIntegerField(max_length=18,
                                                                  db_column='NumberOfPeopleReachedDirect__c')
    NumberOfPeopleReachedIndirect__c = models.PositiveIntegerField(max_length=18,
                                                                  db_column='NumberOfPeopleReachedIndirect__c')
    Theme__c = models.CharField(max_length=255, db_column='Theme__c')
    Donation_total__c = models.CharField(max_length=20, db_column='Donation_total__c')
    Supporter_count__c = models.PositiveIntegerField(max_length=8, db_column='Supporter_count__c')
    Donation_oo_total__c = models.CharField(max_length=20, db_column='Donation_oo_total__c')
    Supporter_oo_count__c = models.PositiveIntegerField(max_length=8, db_column='Supporter_oo_count__c')

    class Meta:
        db_table = 'Project__c'
        managed = False


class SalesforceProjectBudgetLine(SalesforceModel):
    """
    Custom Salesforce Project_Budget__c model. For Onepercentclub the mapping is named Project Budget.
    """
    Costs__c = models.CharField(max_length=255, db_column='Costs__c')
    Description__c = models.CharField(max_length=32000, db_column='Description__c')
    Project_Budget_External_ID__c = models.CharField(max_length=255, db_column='Project_Budget_External_ID__c')
    Project__c = models.ForeignKey(SalesforceProject, db_column='Project__c')

    class Meta:
        db_table = 'Project_Budget__c'
        managed = False


class SalesforceFundraiser(SalesforceModel):
    """
    Custom Fundraiser__c model.
    """
    Amount__c = models.CharField(max_length=100, db_column='Amount__c')
    Owner__c = models.ForeignKey(SalesforceMember, db_column='Owner__c')
    Created__c = models.DateTimeField(db_column='Created__c')
    Deadline__c = models.DateField(db_column='Deadline__c')
    Description__c = models.CharField(max_length=131072, db_column='Description__c')
    Fundraiser_External_ID__c = models.CharField(max_length=255, db_column='Fundraiser_External_ID__c')
    Picture_Location__c = models.CharField(max_length=255, db_column='Picture_Location__c')
    Project__c = models.ForeignKey(SalesforceProject, db_column='Project__c')
    VideoURL__c = models.CharField(max_length=255, db_column='VideoURL__c')
    Name = models.CharField(max_length=80, db_column='Name')
    Amount_at_the_moment__c = models.CharField(max_length=100, db_column='Amount_at_the_moment__c')

    class Meta:
        db_table = 'Fundraiser__c'
        managed = False


class SalesforceOpportunity(SalesforceModel):
    """
    Default abstract Salesforce Opportunity model. Used for Donation(s) / Voucher(s).
    """
    amount = models.CharField(max_length=255, db_column='Amount')
    close_date = models.DateField(db_column='CloseDate')
    type = models.CharField(max_length=40, db_column='Type')
    name = models.CharField(max_length=120, db_column='Name')
    payment_method = models.CharField(max_length=255,
                                      db_column='Payment_method__c',
                                      help_text=_("PaymentMethod"))
    project = models.ForeignKey(SalesforceProject, db_column='Project__c', null=True)
    stage_name = models.CharField(max_length=40,
                                  db_column='StageName')
    record_type = models.CharField(max_length=255, db_column='RecordTypeId')

    class Meta:
        abstract = True
        managed = False


class SalesforceDonation(SalesforceOpportunity):
    """
    Child of the Opportunity for Onepercentclub the mapping is named Donation(s).
    """

    donation_created_date = models.DateTimeField(db_column='Donation_created_date__c')
    donation_updated_date = models.DateTimeField(db_column='Donation_updated_date__c')
    donation_ready_date = models.DateTimeField(db_column='Donation_ready_date__c')
    external_id_donation = models.CharField(max_length=255, db_column='Donation_External_ID__c')
    donor = models.ForeignKey(SalesforceMember, db_column='Receiver__c', null=True)
    fundraiser = models.ForeignKey(SalesforceFundraiser, db_column='Fundraiser__c', null=True)

    class Meta:
        managed = False
        db_table = 'Opportunity'


class SalesforceVoucher(SalesforceOpportunity):
    """
    Child of the Opportunity for Onepercentclub the mapping is named Voucher(s).
    """
    purchaser = models.ForeignKey(SalesforceMember, db_column='Purchaser__c', related_name='contact_purchasers')
    description = models.CharField(max_length=32000, db_column='Description')
    receiver = models.ForeignKey(SalesforceMember, db_column='Receiver__c', related_name='contact_receivers', null=True)
    external_id_voucher = models.CharField(max_length=255, db_column='Voucher_External_ID__c')

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

    project = models.ForeignKey(SalesforceProject, db_column='Project__c')
    deadline = models.DateField(db_column='Deadline__c')
    effort = models.CharField(max_length=200, db_column='Effort__c')
    extended_task_description = models.CharField(max_length=32000, db_column='Extended_task_description__c')
    location_of_the_task = models.CharField(max_length=200, db_column='Location_of_the_task__c')
    task_expertise = models.CharField(max_length=100, db_column='Task_expertise__c')
    task_status = models.CharField(max_length=40, db_column='Task_status__c', choices=TaskStatus.choices, help_text=_("TaskStatus"))
    title = models.CharField(max_length=100, db_column='Title__c')
    task_created_date = models.DateField(db_column='Task_created_date__c')
    tags = models.CharField(max_length=255, db_column='Tags__c')
    date_realized = models.DateField(db_column='Date_realized__c')
    author = models.ForeignKey(SalesforceMember, db_column='Author__c')
    people_needed = models.CharField(max_length=10, db_column='People_Needed__c')
    end_goal = models.CharField(max_length=5000, db_column='End_Goal__c')

    external_id = models.CharField(max_length=255, db_column='Task_External_ID__c')

    class Meta:
        db_table = 'onepercentclubTasks__c'
        managed = False


class SalesforceTaskMember(SalesforceModel):
    """
    Custom Salesforce Task_Members__c model. For Onepercentclub the mapping is named Task Member(s).
    The table is used as a joined table which relates to Tasks to the Contacts.
    """
    contacts = models.ForeignKey(SalesforceMember, db_column='Contacts__c')
    x1_club_task = models.ForeignKey(SalesforceTask, db_column='X1_CLUB_Task__c')
    external_id = models.CharField(max_length=100, db_column='Task_Member_External_ID__c')
    motivation = models.CharField(max_length=5000, db_column='Motivation__c')
    status = models.CharField(max_length=255, db_column='Status__c')
    taskmember_created_date = models.DateField(db_column='Taskmember_Created_Date__c')

    class Meta:
        db_table = 'Task_Members__c'
        managed = False


class SalesforceOrganizationMember(SalesforceModel):
    """
    Custom Salesforce Organization_Member__c object.
    The object is used as a junction object that connects Account and Contact.
    """
    Contact__c = models.ForeignKey(SalesforceMember, db_column='Contact__c')
    Organization__c = models.ForeignKey(SalesforceOrganization, db_column='Organization__c')
    Role__c = models.CharField(max_length=20, db_column='Role__c')
    Organization_Member_External_Id__c = models.CharField(max_length=100, db_column='Organization_Member_External_Id__c')

    class Meta:
        db_table = 'Organization_Member__c'
        managed = False


class SalesforceLogItem(SalesforceModel):
    """
    Custom Salesforce Log_Item__c object.
    The object is used to store log data from external and internal sources.
    """
    entered = models.DateTimeField(db_column='Entered__c')
    errors = models.PositiveIntegerField(max_length=18, db_column='Errors__c')
    message = models.CharField(max_length=32000, db_column='Message__c')
    source = models.CharField(max_length=255, db_column='Source__c')
    source_extended = models.CharField(max_length=255, db_column='Source_Extended__c')
    successes = models.PositiveIntegerField(max_length=18, db_column='Successes__c')

    class Meta:
        db_table = 'Log_Item__c'
        managed = False


class SalesforceLoginHistory(SalesforceModel):
    """
    Custom Login_History__c model. For Onepercentclub the mapping is named 1%CLUB Login History.
    New mapping to be added later on.
    """

    bounce_rate_from_first_page = models.CharField(max_length=6, db_column='Bounce_rate_from_first_page__c')
    contacts = models.ForeignKey(SalesforceMember, db_column='Contacts__c')
    engagement_on_facebook = models.PositiveIntegerField(max_length=8, db_column='Engagement_on_Facebook__c')
    engagement_on_twitter = models.PositiveIntegerField(max_length=8, db_column='Engagement_on_Twitter__c')
    number_of_pageviews = models.PositiveIntegerField(max_length=8, db_column='Number_of_pageviews__c')
    online_engagement_blogs = models.PositiveIntegerField(max_length=8, db_column='Online_engagement_blogs__c')
    online_engagement_projects = models.PositiveIntegerField(max_length=8, db_column='Online_engagement_projects__c')
    online_engagement_reactions_to_members = models.PositiveIntegerField(max_length=8, db_column='Online_engagement_'
                                                                                                 'reactions_to_'
                                                                                                 'members__c')
    online_engagement_tasks = models.PositiveIntegerField(max_length=8, db_column='Online_engagement_tasks__c')
    preferred_navigation_path = models.PositiveIntegerField(max_length=255, db_column='Preferred_navigation_path__c')
    shares_via_social_media = models.PositiveIntegerField(max_length=8, db_column='Shares_via_social_media__c')
    size_of_basket = models.PositiveIntegerField(max_length=8, db_column='Size_of_basket__c')
    time_on_website = models.PositiveIntegerField(max_length=6, db_column='Time_on_website__c')

    class Meta:
        db_table = 'X1_CLUB_Login_History__c'
        managed = False
