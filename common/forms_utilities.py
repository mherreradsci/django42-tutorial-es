def save_formset(self, request, form, formset, change):
    instances = formset.save(commit=False)
    for obj in formset.deleted_objects:
        obj.delete()
    for instance in instances:
        if instance.pk:
            instance.updated_by = request.user
        else:
            instance.created_by = request.user
            instance.updated_by = request.user

        instance.save()
    formset.save_m2m()
