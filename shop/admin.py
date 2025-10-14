from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'product_count', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    list_per_page = 20

    def product_count(self, obj):
        """Display number of products in category"""
        count = obj.products.count()
        return format_html('<span style="font-weight: bold;">{}</span>', count)
    product_count.short_description = 'Products'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'npk_ratio', 'price', 'stock', 'stock_status', 'available', 'created_at']
    list_filter = ['available', 'category', 'created_at']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description', 'npk_ratio']
    ordering = ['-created_at']
    list_per_page = 20
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category', 'description')
        }),
        ('NPK & Dosage', {
            'fields': ('npk_ratio', 'dosage_info')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'stock', 'available')
        }),
        ('Media', {
            'fields': ('image',)
        }),
    )

    def stock_status(self, obj):
        """Display stock status with color coding"""
        if obj.stock == 0:
            color = 'red'
            status = 'Out of Stock'
        elif obj.stock < 10:
            color = 'orange'
            status = 'Low Stock'
        else:
            color = 'green'
            status = 'In Stock'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, status
        )
    stock_status.short_description = 'Stock Status'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0
    readonly_fields = ['product', 'quantity', 'price', 'item_total']
    can_delete = False

    def item_total(self, obj):
        """Display item total price"""
        return format_html('<strong>${}</strong>', obj.get_total_price())
    item_total.short_description = 'Total'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number','status', 'customer_name', 'email','phone', 'total_price', 'status_badge', 'created_at']
    list_filter = ['status', 'created_at']
    list_editable = ['status']
    search_fields = ['user__username', 'email', 'first_name', 'last_name', 'id']
    inlines = [OrderItemInline]
    ordering = ['-created_at']
    list_per_page = 20
    
    readonly_fields = ['user', 'created_at', 'updated_at', 'order_summary']
    
    fieldsets = (
        ('Order Information', {
            'fields': ('user', 'status', 'total_price', 'created_at', 'updated_at')
        }),
        ('Customer Details', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Shipping Address', {
            'fields': ('address', 'city', 'postal_code')
        }),
        ('Order Summary', {
            'fields': ('order_summary',),
            'classes': ('collapse',)
        }),
    )

    def order_number(self, obj):
        """Display formatted order number"""
        return format_html('<strong>#{}</strong>', obj.id)
    order_number.short_description = 'Order #'

    def customer_name(self, obj):
        """Display customer full name"""
        return f'{obj.first_name} {obj.last_name}'
    customer_name.short_description = 'Customer'

    def status_badge(self, obj):
        """Display status with color badge"""
        colors = {
            'pending': '#FFA500',
            'processing': '#2196F3',
            'shipped': '#9C27B0',
            'delivered': '#4CAF50',
            'cancelled': '#F44336',
        }
        color = colors.get(obj.status, '#999')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 12px; '
            'border-radius: 12px; font-weight: bold; font-size: 11px;">{}</span>',
            color, obj.get_status_display().upper()
        )
    status_badge.short_description = 'Status'

    def order_summary(self, obj):
        """Display detailed order summary"""
        items_html = '<table style="width: 100%; border-collapse: collapse;">'
        items_html += '<tr style="background-color: #f5f5f5;"><th style="padding: 8px; text-align: left;">Product</th><th style="padding: 8px;">Quantity</th><th style="padding: 8px;">Price</th><th style="padding: 8px;">Total</th></tr>'
        
        for item in obj.items.all():
            items_html += f'<tr style="border-bottom: 1px solid #ddd;"><td style="padding: 8px;">{item.product.name}</td><td style="padding: 8px; text-align: center;">{item.quantity}</td><td style="padding: 8px; text-align: center;">${item.price}</td><td style="padding: 8px; text-align: center;"><strong>${item.get_total_price()}</strong></td></tr>'
        
        items_html += f'<tr style="background-color: #f5f5f5; font-weight: bold;"><td colspan="3" style="padding: 8px; text-align: right;">Total:</td><td style="padding: 8px; text-align: center; color: #2d5016;">${obj.total_price}</td></tr>'
        items_html += '</table>'
        
        return format_html(items_html)
    order_summary.short_description = 'Items'


# Customize admin site header and title
admin.site.site_header = 'AgroBioSmart'
admin.site.site_title = 'AgroBioSmart'
admin.site.index_title = 'Dashboard'
