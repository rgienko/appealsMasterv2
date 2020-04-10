from django.db import models
from django.urls import reverse
import uuid
from datetime import date

# Create your models here.


# FORIEGN KEY TABLES

class action_master(models.Model):
    id = models.CharField(primary_key=True, max_length=25)
    note = models.TextField(blank=True, null=True)
    description = models.TextField(max_length=3000, blank=True, null=True)
    lead_time = models.IntegerField(db_column='lead time', blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return(self.id)

class charge_master(models.Model):
    charge_id = models.IntegerField(primary_key=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return(str(self.charge_id))

class fi_master(models.Model):
    fi_id = models.IntegerField(primary_key=True)
    fi_name = models.CharField(max_length=255, blank=True, null=True)
    fi_abbr = models.CharField(max_length=25, blank=True, null=True)
    fi_juris = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return '{0}-{1}'.format(self.fi_abbr, self.fi_juris)

class issue_master(models.Model):
    issue_id = models.IntegerField(primary_key=True)
    old_id = models.IntegerField(blank=True, null=True)
    issue = models.CharField(max_length=255)
    realization_weight = models.FloatField()
    rep_id = models.IntegerField()
    category_id = models.IntegerField()
    abbreviation = models.CharField(max_length=255, blank=True, null=True)
    short_description = models.TextField(blank=True, null=True)
    long_description = models.TextField(blank=True, null=True)
    is_groupable = models.BooleanField()

    def __str__(self):
        return '{0} - {1}'.format(str(self.issue_id), self.issue)

class state_name_master(models.Model):
    state_id = models.CharField(primary_key=True, max_length=2)
    state_name = models.CharField(max_length=25, blank=True, null=True)

class parent_master(models.Model):
    parent_id = models.CharField(primary_key=True, max_length=255)
    parent_full_name = models.CharField(max_length=255, blank=True, null=True)
    corp_contact_first_name = models.CharField(max_length=255, blank=True, null=True)
    corp_contact_last_name = models.CharField(max_length=255, blank=True, null=True)
    corp_contact_street = models.CharField(max_length=255, blank=True, null=True)
    corp_contact_city = models.CharField(max_length=255, blank=True, null=True)
    corp_contact_state_id = models.ForeignKey(state_name_master, on_delete = models.CASCADE)
    corp_contact_zip = models.CharField(max_length=255, blank=True, null=True)
    corp_contact_phone = models.CharField(max_length=255, blank=True, null=True)
    corp_contact_fax = models.CharField(max_length=255, blank=True, null=True)
    corp_contact_email = models.EmailField(max_length=255, blank=True, null=True)

    def __str__(self):
        return(self.parent_id)

class prov_name_master(models.Model):
    provider_number = models.CharField(primary_key=True, max_length=7, verbose_name="Proivider Number")
    provider_name = models.CharField(max_length=255, blank=True, null=True)
    fye = models.CharField(max_length=5, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    county = models.CharField(max_length=255, blank=True, null=True)
    state_id = models.ForeignKey(state_name_master, on_delete = models.CASCADE, verbose_name="State") # FK
    parent_id = models.ForeignKey(parent_master, on_delete=models.CASCADE) #FK
    fi_number = models.CharField(max_length=25, blank=True, null=True)
    is_client = models.BooleanField()

    def __str__(self):
        return(self.provider_number)

    def get_system_name(self):
        return (self.parent_id.parent_full_name)

class prrb_contacts(models.Model):
    prrb_contact_id = models.IntegerField(primary_key=True)
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    email_address = models.CharField(max_length=255)
    appeals_general_email = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=255)
    street_1 = models.CharField(max_length=255, blank=True, null=True)
    street_2_suite_dept = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state_id = models.ForeignKey(state_name_master, on_delete=models.CASCADE)
    zip = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return '{0} - {1}'.format(str(self.prrb_contact_id), self.last_name)

class rep_master(models.Model):
    rep_id = models.IntegerField(primary_key=True)
    rep = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return '{0} - {1}'.format(str(self.rep_id), self.last_name)

class srg_staff_master(models.Model):
    sri_staff_id = models.IntegerField(primary_key=True)
    employee = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return(str(self.sri_staff_id))




class status_master(models.Model):
    status_id = models.IntegerField(primary_key=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return '{0} - {1}'.format(str(self.status_id), self.status)

class appeal_master(models.Model): # my person model related to example
    case_number = models.CharField(primary_key=True, max_length=255)
    rep_id = models.ForeignKey(rep_master, on_delete=models.CASCADE,) # FK
    fi_id = models.ForeignKey(fi_master, on_delete=models.CASCADE)
    prrb_contact_id = models.ForeignKey(prrb_contacts, on_delete=models.CASCADE) # FK
    status_id = models.ForeignKey(status_master, on_delete=models.CASCADE) # FK
    appeal_name = models.CharField(max_length=255, blank=True, null=True)
    structure_choices = [
        ('INDIVIDUAL', 'Individual'),
        ('CIRP', 'CIRP'),
        ('OPTIONAL', 'Optional')
        ]
    structure = models.CharField(max_length=10, choices = structure_choices)
    general_info_and_notes = models.TextField(blank=True, null=True)
    stamp = models.DateTimeField(blank=True, null=True)
    prrb_trk_num = models.CharField(max_length=255, blank=True, null=True)
    mac_trk_num = models.CharField(max_length=255, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    request_date = models.DateTimeField(blank=True, null=True)
    acknowledged = models.BooleanField()

    def __str__(self):
        return (self.case_number)

    def get_rep(self):
        return (self.rep_id.rep)

    def get_prrb(self):
        return (self.prrb_contact_id.last_name)

    def get_status(self):
        return(self.status_id.status)

    def is_individual(self):
        return (self.structure in {self.INDIVIDUAL})

    def is_group(self):
        return (self.structure in {self.CIRP, self.OPTIONAL})

    def is_cirp_group(self):
        return (self.structure in {self.CIRP})

    def is_opt_group(self):
        return (self.structure in {self.OPTIONAL})

    def is_ack(self):
        return (self.acknowledged)

    def get_fi(self):
        return (self.fi_id.fi_name)



class provider_master(models.Model):
    id = models.UUIDField(primary_key=True, default = uuid.uuid4())
    case_number = models.ManyToManyField(appeal_master, through='case_master')
    provider_number = models.ForeignKey(prov_name_master, on_delete=models.CASCADE) #FK
    fiscal_year = models.IntegerField(blank=True, null=True)
    npr_date = models.DateField(blank=True, null=True)
    receipt_date = models.DateTimeField(blank=True, null=True) # Remove field, already in AppealMaster
    was_added = models.BooleanField(blank=True, null=True)
    issue_id = models.ForeignKey(issue_master, on_delete=models.CASCADE)  # FK
    charge_id = models.ForeignKey(charge_master,on_delete=models.CASCADE) # FK
    amount = models.DecimalField(decimal_places = 2, max_digits = 16, blank=True, null=True)
    audit_adjustments = models.CharField(max_length=255, blank=True, null=True)
    realization_weight = models.FloatField(blank=True, null=True)
    sri_staff_id = models.ForeignKey(srg_staff_master, on_delete=models.CASCADE) # FK
    hospcontactid = models.IntegerField(blank=True, null=True) # FK?
    active_in_appeal_field = models.BooleanField(blank=True, null=True, default=True)
    to = models.CharField(max_length=7, blank=True, null=True)
    to_date = models.DateField(blank=True, null=True)
    transmactrack = models.CharField(max_length=255, blank=True, null=True)
    from_field = models.CharField(max_length=7, blank=True, null=True)
    agreement = models.CharField(max_length=255, blank=True, null=True)
    agree_note = models.TextField(blank=True, null=True)
    provider_specific_note = models.TextField(blank=True, null=True)

class case_master(models.Model):
    case_number = models.ForeignKey(appeal_master, on_delete=models.CASCADE)
    provider_master_id = models.ForeignKey(provider_master, on_delete=models.CASCADE)
