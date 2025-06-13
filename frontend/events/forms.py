from django import forms
from django_summernote.widgets import SummernoteWidget

from api.events.models import Event, EventDate, EventCategory


class EventForm(forms.ModelForm):
    """Form for creating/updating an event"""
    category = forms.ModelChoiceField(
        queryset=EventCategory.objects.filter(is_active=True),  # Fetch all categories
        empty_label="Select a Category",  # Placeholder text
        widget=forms.Select(attrs={"class": "form-control"})  # Bootstrap styling
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={'id': 'summernote'})
    )

    is_registered = forms.BooleanField(
        required=False,
        label="Require Registration",
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input switch-input',
            'id': 'id_is_registered'
        })
    )

    is_publish = forms.BooleanField(
        required=False,
        label="Is Publish",
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input switch-input',
            'id': 'id_is_publish'
        })
    )

    class Meta:
        model = Event
        fields = ["title", "short_description", "description", "category",
                  "location", "feature_image", "cover_image", "is_registered",
                  "is_short_course", "max_seat", "is_publish"]
        widgets = {
            "description": SummernoteWidget(),
            "event_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "from_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "to_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        require_registration = cleaned_data.get('require_registration')
        max_seat = cleaned_data.get('max_seat')

        if require_registration and not max_seat:
            self.add_error('max_seat', 'Max seat is required if registration is required.')

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            if field not in ['description']:
                self.fields[field].widget.attrs['class'] = 'form-control'

        self.fields['description'].widget.attrs['required'] = 'required'

        # Set max_seat initially optional
        self.fields['max_seat'].required = False
        self.fields['max_seat'].widget.attrs.update({'id': 'id_max_seat', 'placeholder': 'max seat', 'max': '1500'})
        self.fields['is_publish'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['is_registered'].widget.attrs.update({'class': 'form-check-input icsm'})

        if not (self.data.get('is_registered') or getattr(self.instance, 'is_registered', False)):
            self.fields['max_seat'].widget.attrs['disabled'] = True


class EventDateForm(forms.ModelForm):
    """Form for managing event dates"""
    class Meta:
        model = EventDate
        fields = ["event_date", "from_time", "to_time"]
        widgets = {
            "event_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "from_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "to_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
        }


class EventCategoryForm(forms.ModelForm):
    class Meta:
        model = EventCategory
        fields = ["title"]

