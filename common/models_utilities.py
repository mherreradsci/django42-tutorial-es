def save_model(self, request, obj, form, change):
    """
    Given a model instance save it to the database adding the
    request user to audit info
    """

    if not obj.pk:
        obj.created_by = request.user
        obj.updated_by = request.user
    elif change:
        obj.updated_by = request.user
    obj.save()
