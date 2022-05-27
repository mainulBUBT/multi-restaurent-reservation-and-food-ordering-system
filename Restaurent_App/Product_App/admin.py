
from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum

from Product_App.models import History, Order, Product, Reservation, Restaurent

# Register your models here.


class RestaurentAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'name','total_seat', 'calculate', 'opening', 'closed',)
    list_filter = ('name',)

    # Image show function
    def image_tag(self, obj):
        return format_html('<img src="{}" width="30px"/>'.format(obj.restaurent_pics.url))

    image_tag.short_description = 'Image'

    def calculate(self, obj):
        from .models import Reservation
        res= Reservation.objects.filter(status='Accepted', restaurents = obj).aggregate(Sum('person'))

        if res['person__sum'] is None:
            res['person__sum'] = 0
        return obj.total_seat - res['person__sum']      

    calculate.short_description = 'Seat Left'


admin.site.register(Restaurent, RestaurentAdmin)


class ReservationAdmin(admin.ModelAdmin):
    list_display = ('get_user','image_tag', 'get_restaurents', 'person',
                    'booking_date', 'booking_time', 'status', 'url')
    list_filter = ('status','restaurents', 'booking_date','booking_time',)

    # Restaurent name function

    def get_restaurents(self, obj):
        return obj.restaurents.name
    get_restaurents.short_description = 'Restaurent'
    
    # User name function
    def get_user(self, obj):
        return obj.user.username
    get_user.short_description = 'User'

     # Image show function
    def image_tag(self, obj):
        return format_html('<img src="{}" width="30px"/>'.format(obj.restaurents.restaurent_pics.url))
    image_tag.short_description = 'Image'

    def url(self, obj):
        from .models import Reservation
        Reservation.objects.filter(status = "Restore").delete()
        

    url.short_description = 'ID'

admin.site.register(Reservation, ReservationAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_tag', 'price', 'get_restaurents', 'date',)
    list_filter = ('name', 'restaurents', 'date',)

    # Restaurent name function
    def get_restaurents(self, obj):
        return obj.restaurents.name
    get_restaurents.short_description = 'Restaurent'

    # Image show function
    def image_tag(self, obj):
        return format_html('<img src="{}" width="30px"/>'.format(obj.image.url))

    image_tag.short_description = 'Image'


admin.site.register(Product, ProductAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('image_tag','get_restaurents','get_user','tran_id','method','service_type', 'date',)

    fieldsets = [(None, {'fields':()}),]

    def __init__(self, *args, **kwargs):
        super(OrderAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = ()

    # User name function
    def get_user(self, obj):
        return obj.user.username
    get_user.short_description = 'User'

    # Image show function
    def image_tag(self, obj):
        return format_html('<img src="{}" width="30px"/>'.format(obj.image.url))

    image_tag.short_description = 'Image'

    # Restaurent name function

    def get_restaurents(self, obj):
        return obj.restaurents.name
    get_restaurents.short_description = 'Restaurent'
    


admin.site.register(Order, OrderAdmin)

class HistoryAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'product_name', 'image_tag','restaurent_name', 'price', 'quantity','service_type','get_user', 'date','get_id',)
    actions = None

    fieldsets = [(None, {'fields':()}),]

    def __init__(self, *args, **kwargs):
        super(HistoryAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = ()

    # User name function
    def get_user(self, obj):
        return obj.user.username
    get_user.short_description = 'User'

    def get_id(self,obj):
        return format_html("<a class='btn btn-outline-danger' href='http://127.0.0.1:8000/product/pdf/{url}' target='_blank'>{url}</a>", url=obj.order_id)
    get_id.short_description = 'PDF'

    # Image show function
    def image_tag(self, obj):
        return format_html('<img src="{}" width="30px"/>'.format(obj.product_img.url))

    image_tag.short_description = 'Image'

admin.site.register(History, HistoryAdmin)
