from rest_framework import serializers


class CustomFieldsSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        exclude = kwargs.pop('exclude', None)
        super(CustomFieldsSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

        if exclude is not None:
            banned = set(exclude)
            for field_name in banned:
                self.fields.pop(field_name)
