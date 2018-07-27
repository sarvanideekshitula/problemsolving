from django import forms
from programming.models import Student_details, Groups
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


    def clean_name(self):
        """
        check username already exists
        :return: cleaned username
        """
        username = self.cleaned_data.get('name', None)
        if Student_details.objects.filter(name=username):
            raise forms.ValidationError(_('That username is already in use, please use a new one!'))
        return username

class GroupForm(forms.ModelForm):
    groupname = forms.CharField(required = False)

    class Meta:
        model = Groups
        fields = ('groupname',)

    def clean_name(self):
        """
        check username already exists
        :return: cleaned username
        """
        name = self.cleaned_data.get('groupname', None)
        if Groups.objects.filter(groupname=name):
            raise forms.ValidationError(_('That username is already in use, please use a new one!'))
        return name
