import django_filters

class provider_name_filter(django_filters.FilterSet):
    class Meta:
        model = prov_name_master
        fields = ['is_client']
