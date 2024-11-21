from django.contrib import admin


class StockManagementAdminMixin:
    @admin.action(description='Mark as out of stock')
    def mark_as_out_of_stock(model, request, queryset):
        queryset.update(stock=0)


class PlaceHolderMixin:
    def add_placeholder(self):
        if hasattr(self, 'fields'):
            for field_name, field in self.fields.items():
                help_text = getattr(field, 'help_text', None)
                if help_text:
                    field.widget.attrs.update({
                        'placeholder': help_text,
                    })

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_placeholder()
