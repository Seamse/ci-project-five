from django.contrib import admin
from .models import NewOrder, OrderLineItem


class OrderItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemAdminInline,)

    readonly_fields = ('order_number', 'date',
                       'delivery_cost', 'order_total',
                       'total_cost',)

    fields = ('order_number', 'user_account', 'date', 'first_name',
              'last_name', 'email', 'country',
              'postcode', 'town_or_city', 'street_address1',
              'street_address2', 'delivery_cost',
              'order_total', 'total_cost',)

    list_display = ('order_number', 'date', 'first_name',
                    'last_name', 'order_total', 'delivery_cost',
                    'total_cost',)

    ordering = ('-date',)


admin.site.register(NewOrder, OrderAdmin)
