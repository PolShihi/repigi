from django.contrib import admin
from .models import *

class MedicationInline(admin.StackedInline):
    model = Medication

class MedicationCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('name',)
    
class MedicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name', 'cost', 'get_total_revenue')
    list_display_links = ('id', 'code', 'name')
    search_fields = ('name', 'code')
    list_filter = ('name', 'cost')
    
    @admin.display(description='Total revenue')
    def get_total_revenue(self, obj):
        return f"{obj.get_total_revenue()}"
    
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('id', 'company_name', 'phone', 'address')
    list_display_links = ('id', 'company_name')
    search_fields = ('company_name',)
    list_filter = ('company_name',)
    inlines = [MedicationInline]
    
class PharmacyDepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'address', 'get_total_revenue')
    list_display_links = ('id', 'address')
    
    @admin.display(description='Total revenue')
    def get_total_revenue(self, obj):
        return f"{obj.get_total_revenue()}"

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_of_birth', 'date_of_birth', 'phone')
    list_display_links = ('id',)
    list_filter = ('date_of_birth',)

class EmployeeAddAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone')
    list_display_links = ('id',)
    
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'date_of_birth', 'phone')
    list_display_links = ('id', 'user')
    list_filter = ('date_of_birth',)
    
class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'date_added')
    list_display_links = ('id', 'question')
    list_filter = ('date_added',)
    
class PromoAdmin(admin.ModelAdmin):
    list_display = ('id', 'promo', 'is_active', 'discount')
    list_display_links = ('id', 'promo')
    search_fields = ('promo',)
    list_filter = ('is_active',)
    list_editable = ('is_active', 'discount')
    
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'mark', 'date_added')
    list_display_links = ('id', 'full_name')
    search_fields = ('full_name',)
    list_filter = ('mark', 'date_added')
    
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('id', 'position', 'salary', 'posted_date')
    list_display_links = ('id', 'position')
    search_fields = ('position',)
    list_filter = ('salary', 'posted_date')
    
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'medication', 'client', 'quantity', 'department', 'get_total_cost', 'date_of_order')
    list_display_links = ('id', 'medication')
    search_fields = ('medication',)
    list_filter = ('quantity', 'date_of_order')
    
    @admin.display(description='Total cost')
    def get_total_cost(self, obj):
        return f"{obj.get_total_cost()}"
    
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'summary', 'posted_date')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'posted_date')
    
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'registration_number')
    list_display_links = ('id',)
    search_fields = ('name',)  
    list_filter = ('registration_number',)
    ordering = ('name',)  

class CompanyHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'year', 'event')
    list_display_links = ('id',)
    search_fields = ('event',)  
    ordering = ('year',)  

class AddBannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'text',)
    list_display_links = ('id',)
    search_fields = ('text',)  

class PartnerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'official_site')
    list_display_links = ('id',)
    search_fields = ('name',) 
    ordering = ('name',) 

admin.site.register(MedicationCategory, MedicationCategoryAdmin)
admin.site.register(Medication, MedicationAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(PharmacyDepartment, PharmacyDepartmentAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(EmployeeAdd, EmployeeAddAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(CompanyInfo, CompanyInfoAdmin)
admin.site.register(QuestionAnswer, QuestionAnswerAdmin)
admin.site.register(Promo, PromoAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Vacancy, VacancyAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(CompanyHistory, CompanyHistoryAdmin)
admin.site.register(AddBanner, AddBannerAdmin)
admin.site.register(Partner, PartnerAdmin)
