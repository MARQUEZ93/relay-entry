import csv
from django.http import HttpResponse

def export_to_csv(modeladmin, request, queryset):
    meta = modeladmin.model._meta
    field_names = modeladmin.list_display

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={meta}.csv'
    writer = csv.writer(response)

    writer.writerow(field_names)
    # Write the data rows
    for obj in queryset:
        row = []
        for field in field_names:
            # Use getattr to get the value of the field, handling callable fields
            if hasattr(modeladmin, field):
                field_value = getattr(modeladmin, field)(obj)
            else:
                field_value = getattr(obj, field)
            row.append(field_value)
        writer.writerow(row)

    return response