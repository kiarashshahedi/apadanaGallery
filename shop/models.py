from django.db import models

class Product(models.Model):
    """
    مدل محصول برای ذخیره اطلاعات محصولات فروشگاه.
    """
    acc_detail_guid = models.CharField(max_length=36)
    alias = models.CharField(max_length=100)
    parent_guid = models.CharField(max_length=36, null=True, blank=True)
    code = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    alias_formula = models.CharField(max_length=100, null=True, blank=True)
    child_digits = models.IntegerField()
    has_children = models.BooleanField(default=False)
    is_item = models.BooleanField(default=True)
    not_absolute_ratio = models.BooleanField(default=False)
    status = models.CharField(max_length=10)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    buy_price = models.DecimalField(max_digits=10, decimal_places=2)
    has_serial = models.BooleanField(default=False)
    barcode = models.CharField(max_length=50, null=True, blank=True)
    brand_code = models.CharField(max_length=50, null=True, blank=True)
    old_code = models.CharField(max_length=50, null=True, blank=True)
    model_no = models.CharField(max_length=50, null=True, blank=True)
    secondary_group = models.CharField(max_length=50, null=True, blank=True)
    technical_code = models.CharField(max_length=50, null=True, blank=True)
    woocommerce_category_id = models.IntegerField(null=True, blank=True)
    unit1_guid = models.CharField(max_length=36)
    unit2_guid = models.CharField(max_length=36, null=True, blank=True)
    quantity1 = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_inventory = models.DecimalField(max_digits=10, decimal_places=2)
    woocommerce_product_id = models.IntegerField(null=True, blank=True)
    woocommerce_variable_id = models.IntegerField(null=True, blank=True)

    # ارتباط با مدل Depot
    depots = models.ManyToManyField('Depot', through='DepotIoDetail')

    def __str__(self):
        return self.title


# مدل های مربوط به انبار ------------------------------------------------------------------------
class Depot(models.Model):
    """
    مدل انبار برای ذخیره اطلاعات انبارها.
    """
    code = models.CharField(max_length=50)
    check_inventory = models.BooleanField(default=False)
    default_depot_api = models.BooleanField(default=False)
    pre_sell_invoice_check_inventory = models.BooleanField(default=False)
    inventory_valuation = models.IntegerField()
    item_gender = models.IntegerField()
    remarks = models.TextField(null=True, blank=True)
    depot_type = models.CharField(max_length=50)
    status = models.CharField(max_length=10)
    title = models.CharField(max_length=100)
    user_groups = models.JSONField(null=True, blank=True)  # ذخیره اطلاعات گروه‌های کاربری به صورت JSON
    item_groups = models.JSONField(null=True, blank=True)  # ذخیره اطلاعات گروه‌های کالایی به صورت JSON

    def __str__(self):
        return self.title
    
# مدل‌های مربوط به ورودی/خروجی انبار ----------------------------------------------------------------------------

class DepotIoDetail(models.Model):
    """
    مدل جزئیات ورودی/خروجی انبار.
    """
    item_code = models.CharField(max_length=50)
    item_description = models.TextField()
    item_guid = models.CharField(max_length=36)
    depot_io_guid = models.CharField(max_length=36)
    reference_guid = models.CharField(max_length=36)
    unit1 = models.CharField(max_length=50)
    unit1_guid = models.CharField(max_length=36)
    unit1_value = models.DecimalField(max_digits=10, decimal_places=2)
    unit2 = models.CharField(max_length=50, null=True, blank=True)
    unit2_guid = models.CharField(max_length=36, null=True, blank=True)
    unit2_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity1 = models.DecimalField(max_digits=10, decimal_places=2)
    quantity2 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity_value = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)

    # ارتباط با مدل Product
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    # ارتباط با مدل Depot
    depot = models.ForeignKey('Depot', on_delete=models.CASCADE)

    def __str__(self):
        return self.item_description

    
    
    
class DepotIo(models.Model):
    """
    مدل ورودی/خروجی انبار.
    """
    acc_doc_no = models.CharField(max_length=50)
    official = models.CharField(max_length=50)
    no = models.CharField(max_length=50)
    date = models.DateField()
    depot1_description = models.TextField()
    depot1_code = models.CharField(max_length=50)
    account_debit_guid = models.CharField(max_length=36)
    account_credit_guid = models.CharField(max_length=36)
    driver_guid = models.CharField(max_length=36, null=True, blank=True)
    driver_description = models.TextField(null=True, blank=True)
    driver_code = models.CharField(max_length=50, null=True, blank=True)
    depot2_guid = models.CharField(max_length=36, null=True, blank=True)
    depot2_description = models.TextField(null=True, blank=True)
    depot2_code = models.CharField(max_length=50, null=True, blank=True)
    depot1_guid = models.CharField(max_length=36)
    expert_guid = models.CharField(max_length=36, null=True, blank=True)
    expert_description = models.TextField(null=True, blank=True)
    expert_code = models.CharField(max_length=50, null=True, blank=True)
    person_code = models.CharField(max_length=50, null=True, blank=True)
    cargo_no = models.CharField(max_length=50, null=True, blank=True)
    person_description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=10)
    person_guid = models.CharField(max_length=36, null=True, blank=True)
    kind = models.IntegerField()
    portage_cost = models.DecimalField(max_digits=10, decimal_places=2)
    price_list_guid = models.CharField(max_length=36, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=50)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    details = models.ManyToManyField(DepotIoDetail)
    post_status = models.CharField(max_length=10)

    def __str__(self):
        return self.no
