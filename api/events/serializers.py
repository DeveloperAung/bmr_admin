from rest_framework import serializers
from .models import EventCategory, EventSubCategory, Event, EventDate
from datetime import date


class EventCategoryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventCategory
        fields = ['id', 'uuid', 'title']


class EventCategoryRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = ['id', 'uuid', 'title', 'created_at', 'created_by', 'modified_at', 'modified_by']


class EventCategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = ['title']


class EventSubCategoryListSerializer(serializers.ModelSerializer):
    category_title = serializers.CharField(source="event_category.title", read_only=True)

    class Meta:
        model = EventSubCategory
        fields = ['id', 'uuid', 'title', 'category_title', 'event_category']


class EventSubCategoryRetrieveSerializer(serializers.ModelSerializer):
    category_title = serializers.CharField(source="event_category.title", read_only=True)

    class Meta:
        model = EventSubCategory
        fields = [
            'id', 'uuid', 'title', 'event_category', 'category_title',
                  'created_at', 'created_by', 'modified_at', 'modified_by'
        ]


class EventSubCategoryCreateSerializer(serializers.ModelSerializer):
    # category = serializers.PrimaryKeyRelatedField(queryset=EventCategory.objects.all())

    class Meta:
        model = EventSubCategory
        fields = ['title', 'event_category']


class EventDateSerializer(serializers.ModelSerializer):
    """Serializer for EventDate model with conflict validation"""

    class Meta:
        model = EventDate
        fields = ["id", "event_date", "from_time", "to_time"]

    def validate(self, data):
        """
        Custom validation for event dates:
        - Prevents past dates
        - Ensures `to_time` is after `from_time`
        - Prevents time overlap for the same event
        """
        event = self.context.get("event")  # Get event from serializer context

        # Check if the event date is in the past
        if data.get("event_date") < date.today():
            raise serializers.ValidationError("Event date cannot be in the past.")

        # Check if 'from_time' is before 'to_time'
        if data.get("from_time") and data.get("to_time") and data["from_time"] >= data["to_time"]:
            raise serializers.ValidationError("From time must be before To time.")

        # Check for overlapping times in the same event
        if event:
            overlapping_event = EventDate.objects.filter(
                event=event,
                event_date=data["event_date"],
                from_time__lt=data["to_time"],
                to_time__gt=data["from_time"]
            ).exclude(id=self.instance.id if self.instance else None)

            if overlapping_event.exists():
                raise serializers.ValidationError("Event time overlaps with an existing event for this date.")

        return data


class EventListSerializer(serializers.ModelSerializer):
    """ Event Minimal Serializer """
    category_title = serializers.CharField(source="category.title", read_only=True)

    class Meta:
        model = Event
        fields = ["id", "uuid", "title", "category_title", "is_publish"]


class EventRetrieveSerializer(serializers.ModelSerializer):
    category_title = serializers.CharField(source="category.title", read_only=True)
    event_dates = EventDateSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = [
            "id", "uuid", "title", "category_title", "event_dates", "short_description", "description", "location",
            "feature_image", "cover_image", "is_registered", "is_short_course", "max_seat", "is_publish",
            "published_at", "published_by", "media_sent_at", "media_sent_by", "media_sent_count", "created_at",
            "created_by", "modified_at", "modified_by"
        ]

    # def to_representation(self, instance):
    #     """
    #     Override to ensure all string fields are properly encoded as UTF-8.
    #     """
    #     data = super().to_representation(instance)
    #
    #     # Ensure all string fields are UTF-8 encoded
    #     for key, value in data.items():
    #         if isinstance(value, str):
    #             try:
    #                 data[key] = value.encode("utf-8", "ignore").decode("utf-8")
    #             except UnicodeEncodeError:
    #                 data[key] = value.encode("utf-8", "ignore").decode("utf-8")
    #
    #     return data


class EventCreateSerializer(serializers.ModelSerializer):
    event_dates = EventDateSerializer(many=True, required=False)

    class Meta:
        model = Event
        fields = ["title", "short_description", "description", "category", "location", "is_publish", "event_dates"]

    def create(self, validated_data):
        """
        Custom create method to handle nested event_dates with conflict validation
        """
        event_dates_data = validated_data.pop("event_dates", [])  # Extract event_dates if provided
        event = Event.objects.create(**validated_data)  # Create event instance

        # Validate event dates & create them
        for event_date_data in event_dates_data:
            serializer = EventDateSerializer(data=event_date_data, context={"event": event})
            serializer.is_valid(raise_exception=True)
            serializer.save(event=event)

        return event


class EventUpdateSerializer(serializers.ModelSerializer):
    event_dates = EventDateSerializer(many=True, required=False)

    class Meta:
        model = Event
        fields = ["title", "short_description", "description", "category", "location", "is_publish", "event_dates"]
        extra_kwargs = {"title": {"required": False}}  # Allows partial updates

    def update(self, instance, validated_data):
        """
        Custom update method to handle nested event_dates with validation
        """
        event_dates_data = validated_data.pop("event_dates", [])

        # Update event fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        existing_dates = {date.event_date: d for d in instance.event_dates.all()}  # Existing dates

        for event_date_data in event_dates_data:
            event_date = event_date_data["event_date"]

            if event_date in existing_dates:
                # Update existing event date
                event_date_instance = existing_dates[event_date]
                serializer = EventDateSerializer(event_date_instance, data=event_date_data, context={"event": instance})
                serializer.is_valid(raise_exception=True)
                serializer.save()
            else:
                # Create new event date
                serializer = EventDateSerializer(data=event_date_data, context={"event": instance})
                serializer.is_valid(raise_exception=True)
                serializer.save(event=instance)

        return instance



