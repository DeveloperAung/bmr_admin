from django import forms

from api.events.models import Event, EventDate, EventCategory


class EventForm(forms.ModelForm):
    """Form for creating/updating an event"""
    category = forms.ModelChoiceField(
        queryset=EventCategory.objects.filter(is_active=True),  # Fetch all categories
        empty_label="Select a Category",  # Placeholder text
        widget=forms.Select(attrs={"class": "form-control"})  # Bootstrap styling
    )

    class Meta:
        model = Event
        fields = ["title", "short_description", "description", "category",
                  "location", "feature_image", "cover_image",
                  "is_short_course", "max_seat", "is_publish"]


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

