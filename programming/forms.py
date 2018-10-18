from django import forms
from programming.models import Student_details, Groups, DailyChallenges
from django.db.models.functions import datetime
from django.utils.translation import ugettext_lazy as _

class StudentForm(forms.ModelForm):
    name = forms.CharField(required=False)
    codechef = forms.CharField(required = False)
    codeforces = forms.CharField(required = False)
    year = forms.IntegerField(required = False)

    class Meta:
        model = Student_details
        fields = ('name', 'codechef', 'codeforces', 'year')

    def clean_year(self):
        year = int(self.cleaned_data.get("year"))
        if year > int(datetime.timezone.now().year):
            raise forms.ValidationError(_("The year cannot be greater than the current year"))
        if year < 2000:
            raise forms.ValidationError(_("The year cannot be less than 2000"))
        return year


    def clean_codechef(self):
        """
        check username already exists
        :return: cleaned username
        """
        codechef = self.cleaned_data.get('codechef', None)
        if Student_details.objects.filter(codechef=codechef):
            raise forms.ValidationError(_('That username is already in use, please use a new one!'))
        return codechef

class GroupForm(forms.ModelForm):
    groupname = forms.CharField(required = False)

    class Meta:
        model = Groups
        fields = ('groupname',)

    def clean_name(self):
        name = self.cleaned_data.get('groupname', None)
        if Groups.objects.filter(groupname=name):
            raise forms.ValidationError(_('That username is already in use, please use a new one!'))
        return name

class DailyChallengesForm(forms.ModelForm):
    probname = forms.CharField(required = False)

    class Meta:
        model = DailyChallenges
        fields = ('probname',)

    def clean_name(self):
        """
        check username already exists
        :return: cleaned username
        """
        name = self.cleaned_data.get('probname', None)
        if Groups.objects.filter(probname=probname):
            raise forms.ValidationError(_('Not saving'))
        return name
