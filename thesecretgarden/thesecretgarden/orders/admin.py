from django.contrib import admin, messages
from django.contrib.auth.models import Group
from django.contrib.admin import TabularInline
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html

from thesecretgarden.orders.models import Order, OrderItem


class OrderItemInline(TabularInline):
    """
    Items cannot be edited in canceled & completed orders
    """
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'price_per_unit', 'total_price')
    fields = ('product_name', 'quantity', 'price_per_unit', 'total_price')

    def product_name(self, obj):
        if obj.content_type.model == 'plant':
            product_admin_url = reverse(
                'admin:flowers_plant_change', args=[obj.object_id]
            )
            return format_html('<a href="{}">{}</a>', product_admin_url, obj.product.name)
        elif obj.content_type.model == 'gift':
            product_admin_url = reverse(
                'admin:gifts_gift_change', args=[obj.object_id]
            )
            return format_html('<a href="{}">{} {}</a>', product_admin_url, obj.product.brand_name, obj.product.short_name)
        return "Unknown Product Type"

    product_name.short_description = "Product Name"

    def get_readonly_fields(self, request, obj=None):
        """
        Dynamically sets readonly fields based on the order's status.
        """
        if obj and obj.status in ['canceled', 'completed']:
            return self.fields
        return super().get_readonly_fields(request, obj)

    def get_formset(self, request, obj=None, **kwargs):
        """
        Customizes the formset to disable the delete checkbox for canceled & completed orders.
        """
        formset = super().get_formset(request, obj, **kwargs)

        if obj and not obj.user.profile.address:
            messages.error(
                request,
                f"The user for this order has not provided an address. OrderItem fields are readonly."
            )

        if obj and (obj.status in ['canceled', 'completed'] or not obj.user.profile.address):
            formset.can_delete = False

        return formset

    def has_add_permission(self, request, obj=None):
        """
        Disabled for the time being
        """
        return False

    def has_change_permission(self, request, obj=None):
        if obj and (obj.status == ['canceled', 'completed'] or not obj.user.profile.address):
            return False
        return super().has_change_permission(request, obj)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    - On order creation, only users from 'Customer' group can be selected.
    - Stock is restored when order status changes from completed to canceled.
    - Items are deduced from stock when order status changes from pending to completed.
    - Manipulating canceled orders is not allowed.
    - Adding an order without an associated user is not allowed.
    - Changing order status from pending to completed is not allowed for users with no address.
    """
    inlines = [OrderItemInline]
    list_display = ('id', 'user', 'status', 'total_price', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('user', 'status', 'total_price')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        """
        Sets readonly field conditions:
        - For existing orders, the user field cannot be edited.
        - Canceled order fields cannot be edited.
        """
        readonly_fields = set(super().get_readonly_fields(request, obj))
        if obj:
            readonly_fields.add('user')
            if obj.status == 'canceled':
                readonly_fields.update(
                    field.name for field in self.model._meta.fields)
        return tuple(readonly_fields)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        For the related user field, retrieves only users that are in the 'Customer' group
        """
        if db_field.name == 'user':
            customer_group = Group.objects.filter(name='Customer').first()
            if customer_group:
                kwargs['queryset'] = customer_group.user_set.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        """
        Customizes the change form behavior: Prevents editing canceled orders.
        """
        obj = self.model.objects.filter(pk=object_id).first()
        if obj and obj.status == 'canceled':
            messages.info(request, "This is a canceled order. Fields are read-only and cannot be modified.")
        return super().changeform_view(request, object_id, form_url, extra_context)

    def response_change(self, request, obj):
        """
        Customize the response after an object is changed.
        Suppresses the default success message for invalid status transitions.
        """

        previous_instance = self.model.objects.get(pk=obj.pk)

        if previous_instance.status == 'completed' and obj.status == 'pending':
            self.message_user(
                request,
                f"Changing the status of a completed order (Order #{obj.id}) back to 'pending' is not allowed.",
                level=messages.ERROR
            )

            return HttpResponseRedirect(
                reverse(f'admin:{self.model._meta.app_label}_{self.model._meta.model_name}_change', args=[obj.pk])
            )

        if previous_instance.status == 'pending' and obj.status == 'completed' and not obj.user.profile.address:
            self.message_user(
                request,
                f"Order #{obj.id} cannot be completed because the user has not provided an address.",
                level=messages.ERROR
            )
            return HttpResponseRedirect(
                reverse(f'admin:{self.model._meta.app_label}_{self.model._meta.model_name}_change', args=[obj.pk])
            )

        return super().response_change(request, obj)

    def save_model(self, request, obj, form, change):
        """
           Enforces logical status transitions:
           - Prevents 'completed' → 'pending' transitions.
           - Restores stock on 'completed' → 'canceled'.
           - Deducts stock on 'pending' → 'completed',
           - Prevents completing orders of users without address in profile.
        """
        if not change:
            if not obj.user:
                messages.error(request, "The 'user' field is required for creating an order.")
                return
            super().save_model(request, obj, form, change)
            return

        previous_instance = self.model.objects.get(pk=obj.pk)

        if previous_instance.status == 'completed' and obj.status == 'pending':
            return

        if previous_instance.status == 'completed' and obj.status == 'canceled':
            for item in obj.order_items.all():
                product = item.product
                product.stock += item.quantity
                product.save()

        elif previous_instance.status == 'pending' and obj.status == 'completed':
            if not obj.user.profile.address:
                return

            for item in obj.order_items.all():
                product = item.product
                if product.get_available_stock() < item.quantity:
                    messages.error(request, f"Not enough stock for {product}.")
                    return
                product.stock -= item.quantity
                product.save()

        super().save_model(request, obj, form, change)
