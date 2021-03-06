from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register
)

from users.models import (
    Review,
    Cart,
    Order,
    ShippingAddress
)



class ReviewAdmin(ModelAdmin):
    """Registers the Review model in the Wagtail admin."""

    model = Review
    menu_label = 'Reviews'
    menu_icon = 'tick'
    add_to_settings_menu = False
    exclude_from_explorer = False
    inspect_view_enabled = True

    list_display = ('item', 'user', 'name', 'rating', 'comment',)
    search_fields = ('item', 'user', 'name', 'rating', 'comment',)
    list_filter = ('item', 'rating')



class CartAdmin(ModelAdmin):
    """Registers the Cart model in the Wagtail admin."""

    model = Cart
    menu_label = 'Carts'
    menu_icon = 'doc-full-inverse'
    add_to_settings_menu = False
    exclude_from_explorer = False
    inspect_view_enabled = True

    list_display = ('id', 'user', 'payment_method', 'cart_items', 'tax_price', 'shipping_price', 'total_price', 'is_paid', 'paid_at', 'shipping_address', 'is_delivered', 'delivered_at', 'created_at',)
    search_fields = ('id', 'user', 'payment_method',)
    list_filter = ('is_paid', 'is_delivered',)

    def cart_items(self, obj):
        order_list = []
        for order in obj.order_set.all():
            try:
                order_details = str(order.quantity) + 'x ' + str(order.item.title)
                order_list.append(order_details)
            except:
                order_details = '-'
                order_list.append(order_details)
        return ', '.join(order_list)

    def shipping_address(self, obj):
        address = ShippingAddress.objects.all().get(cart=obj.id)
        print('address_obj = ', address)

        full_address = address.address + ', ' + address.city + ' ' + address.postal_code + ', ' + address.country
        return full_address

class OrderAdmin(ModelAdmin):
    """Registers the Order model in the Wagtail admin."""
    
    model = Order
    menu_label = 'Orders'
    menu_icon = 'form'
    add_to_settings_menu = False
    exclude_from_explorer = False
    inspect_view_enabled = True

    list_display = ('item', 'cart', 'name', 'quantity', 'price', 'image',)
    search_fields = ('item', 'cart', 'name', 'quantity', 'price',)
    list_filter = ('item',)



class ShippingAddressAdmin(ModelAdmin):
    """Registers the ShippingAddress model in the Wagtail admin."""

    model = ShippingAddress
    menu_label = 'Shipping Addresses'
    menu_icon = 'site'
    add_to_settings_menu = False
    exclude_from_explorer = False
    inspect_view_enabled = True

    list_display = ('id', 'cart', 'address', 'city', 'postal_code', 'country', 'shipping_price',)
    list_filter = ('id', 'cart', 'address', 'city', 'postal_code', 'country', 'shipping_price',)
    list_filter = ('country',)


class CustomerAccountGroup(ModelAdminGroup):
    """Groups all related user models together in a Wagtail admin folder."""

    menu_label = 'Customers'
    menu_icon = 'folder-open-inverse'
    menu_order = 190
    items = (ReviewAdmin, CartAdmin, OrderAdmin, ShippingAddressAdmin)


modeladmin_register(CustomerAccountGroup)