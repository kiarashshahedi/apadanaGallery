from django.shortcuts import render, redirect
from .click_api import create_product, edit_product, view_product, list_products, list_product_count
from .models import Product
from django.contrib.auth.decorators import login_required

@login_required
def create_product_view(request):
    """
    ویو ایجاد محصول. اگر درخواست POST باشد، تلاش می‌کند محصول را با استفاده از API کلید ایجاد کند.
    در غیر این صورت، فرم ایجاد محصول را نمایش می‌دهد.
    """
    if request.method == 'POST':
        user_guid = request.user.user_guid
        product_data = {
            "AccDetailGuid": request.POST['acc_detail_guid'],
            "Alias": request.POST['alias'],
            "ParentGuid": request.POST.get('parent_guid', None),
            "Code": request.POST['code'],
            "Title": request.POST['title'],
            "AliasFormula": request.POST.get('alias_formula', ''),
            "ChildDigits": request.POST['child_digits'],
            "HasChildren": request.POST.get('has_children', False),
            "IsItem": request.POST.get('is_item', True),
            "NotAbsoluteRatio": request.POST.get('not_absolute_ratio', False),
            "Status": request.POST['status'],
            "SalePrice": request.POST['sale_price'],
            "BuyPrice": request.POST['buy_price'],
            "HasSerial": request.POST.get('has_serial', False),
            "Barcode": request.POST.get('barcode', ''),
            "BrandCode": request.POST.get('brand_code', ''),
            "OldCode": request.POST.get('old_code', ''),
            "ModelNo": request.POST.get('model_no', ''),
            "SecondaryGroup": request.POST.get('secondary_group', ''),
            "TechnicalCode": request.POST.get('technical_code', ''),
            "WooCommerceCategoryId": request.POST.get('woocommerce_category_id', None),
            "Unit1Guid": request.POST['unit1_guid'],
            "Unit2Guid": request.POST.get('unit2_guid', None),
            "Quantity1": request.POST['quantity1'],
            "MinimumInventory": request.POST['minimum_inventory'],
            "WooCommerceProductId": request.POST.get('woocommerce_product_id', None),
            "WooCommerceVariableId": request.POST.get('woocommerce_variable_id', None)
        }
        response = create_product(user_guid, product_data)
        if response.get('success'):
            return redirect('product_list')
    return render(request, 'shop/create_product.html')

@login_required
def edit_product_view(request, item_guid):
    """
    ویو ویرایش محصول. اگر درخواست POST باشد، تلاش می‌کند محصول را با استفاده از API کلید ویرایش کند.
    در غیر این صورت، فرم ویرایش محصول را نمایش می‌دهد.
    """
    if request.method == 'POST':
        product_data = {
            "AccDetailGuid": request.POST['acc_detail_guid'],
            "Status": request.POST['status'],
            "Quantity1": request.POST['quantity1'],
            "Unit2Guid": request.POST.get('unit2_guid', None),
            "Unit1Guid": request.POST['unit1_guid'],
            "TechnicalCode": request.POST.get('technical_code', ''),
            "SecondaryGroup": request.POST.get('secondary_group', ''),
            "ModelNo": request.POST.get('model_no', ''),
            "OldCode": request.POST.get('old_code', ''),
            "BrandCode": request.POST.get('brand_code', ''),
            "Barcode": request.POST.get('barcode', ''),
            "NotAbsoluteRatio": request.POST.get('not_absolute_ratio', False),
            "IsItem": request.POST.get('is_item', True),
            "HasSerial": request.POST.get('has_serial', False),
            "HasChildren": request.POST.get('has_children', False),
            "ChildDigits": request.POST['child_digits'],
            "AliasFormula": request.POST.get('alias_formula', ''),
            "Alias": request.POST['alias'],
            "Title": request.POST['title'],
            "Code": request.POST['code'],
            "ParentGuid": request.POST.get('parent_guid', None),
            "MaximumInventory": request.POST.get('maximum_inventory', None),
            "MinimumInventory": request.POST['minimum_inventory'],
            "WooCommerceCategoryId": request.POST.get('woocommerce_category_id', None),
            "WooCommerceProductId": request.POST.get('woocommerce_product_id', None),
            "WooCommerceVariableId": request.POST.get('woocommerce_variable_id', None),
            "SalePrice": request.POST['sale_price'],
            "BuyPrice": request.POST['buy_price'],
            "Discount": request.POST.get('discount', 0)
        }
        response = edit_product(item_guid, product_data)
        if response.get('success'):
            return redirect('product_list')
    product = view_product(request.user.user_guid, item_guid)
    return render(request, 'shop/edit_product.html', {'product': product})

@login_required
def view_product_view(request, item_guid):
    """
    ویو مشاهده محصول. اطلاعات محصول را با استفاده از API کلید دریافت کرده و نمایش می‌دهد.
    """
    product = view_product(request.user.user_guid, item_guid)
    return render(request, 'shop/view_product.html', {'product': product})

@login_required
def list_product_view(request):
    """
    ویو لیست محصولات. لیست محصولات را با استفاده از API کلید دریافت کرده و نمایش می‌دهد.
    """
    user_guid = request.user.user_guid
    page_number = request.GET.get('page_number', 1)
    step = request.GET.get('step', 10)
    search = request.GET.get('search', '')
    products = list_products(user_guid, page_number, step, search)
    return render(request, 'shop/list_products.html', {'products': products})

@login_required
def list_product_count_view(request):
    """
    ویو تعداد لیست محصولات. تعداد محصولات را با استفاده از API کلید دریافت کرده و نمایش می‌دهد.
    """
    user_guid = request.user.user_guid
    step = request.GET.get('step', 10)
    search = request.GET.get('search', '')
    count = list_product_count(user_guid, step, search)
    return render(request, 'shop/list_product_count.html', {'count': count})


import requests
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required

API_BASE_URL = settings.CLICK_API_BASE_URL

# تابع برای دریافت درخت کالاها
@login_required
def items_tree_view(request):
    user_guid = request.user.user_guid
    parent_guid = request.GET.get('parent_guid', '')
    response = requests.get(f'{API_BASE_URL}/api/Item/ItemsTree', params={'userGuid': user_guid, 'parentGuid': parent_guid})
    items_tree = response.json()
    return render(request, 'shop/items_tree.html', {'items_tree': items_tree})

# تابع برای دریافت لیست پدرهای کالاها
@login_required
def item_parents_view(request):
    user_guid = request.user.user_guid
    response = requests.get(f'{API_BASE_URL}/api/Item/ItemParentList', params={'userGuid': user_guid})
    item_parents = response.json()
    return render(request, 'shop/item_parents.html', {'item_parents': item_parents})

# تابع برای دریافت لیست واحدهای شمارش
@login_required
def unit_list_view(request):
    user_guid = request.user.user_guid
    response = requests.get(f'{API_BASE_URL}/api/Item/UnitList', params={'userGuid': user_guid})
    unit_list = response.json()
    return render(request, 'shop/unit_list.html', {'unit_list': unit_list})

#---------------------------------------------------------------------------------------------------------------------
# تابع برای ایجاد انبار
@login_required
def create_depot_view(request):
    if request.method == 'POST':
        data = {
            "Code": request.POST['code'],
            "CheckInventory": request.POST.get('check_inventory', False),
            "DefultDepotAPI": request.POST.get('default_depot_api', False),
            "PreSellInvoiceCheckInventory": request.POST.get('pre_sell_invoice_check_inventory', False),
            "InventoryValuation": request.POST['inventory_valuation'],
            "ItemGender": request.POST['item_gender'],
            "Remarks": request.POST['remarks'],
            "DepotType": request.POST['depot_type'],
            "Status": request.POST['status'],
            "Title": request.POST['title'],
            "UserGroups": [],  # Add user group data if needed
            "ItemGroups": []  # Add item group data if needed
        }
        user_guid = request.user.user_guid
        response = requests.post(f'{API_BASE_URL}/api/Depot/Create', params={'userGuid': user_guid}, json=data)
        if response.status_code == 200:
            return redirect('depot_list')
    return render(request, 'shop/create_depot.html')

# تابع برای مشاهده انبار
@login_required
def view_depot_view(request, depot_guid):
    user_guid = request.user.user_guid
    response = requests.get(f'{API_BASE_URL}/api/Depot/View', params={'userGuid': user_guid, 'depotGuid': depot_guid})
    depot = response.json()
    return render(request, 'shop/view_depot.html', {'depot': depot})

# تابع برای ویرایش انبار
@login_required
def edit_depot_view(request, depot_guid):
    if request.method == 'POST':
        data = {
            "Code": request.POST['code'],
            "CheckInventory": request.POST.get('check_inventory', False),
            "DefultDepotAPI": request.POST.get('default_depot_api', False),
            "PreSellInvoiceCheckInventory": request.POST.get('pre_sell_invoice_check_inventory', False),
            "InventoryValuation": request.POST['inventory_valuation'],
            "ItemGender": request.POST['item_gender'],
            "Remarks": request.POST['remarks'],
            "DepotType": request.POST['depot_type'],
            "Status": request.POST['status'],
            "Title": request.POST['title'],
            "UserGroups": [],  # Add user group data if needed
            "ItemGroups": []  # Add item group data if needed
        }
        response = requests.put(f'{API_BASE_URL}/api/Depot/Edit', params={'depotGuid': depot_guid}, json=data)
        if response.status_code == 200:
            return redirect('depot_list')
    user_guid = request.user.user_guid
    response = requests.get(f'{API_BASE_URL}/api/Depot/View', params={'userGuid': user_guid, 'depotGuid': depot_guid})
    depot = response.json()
    return render(request, 'shop/edit_depot.html', {'depot': depot})

# تابع برای لیست انبارها
@login_required
def list_depot_view(request):
    user_guid = request.user.user_guid
    page_number = request.GET.get('pageNumber', 1)
    step = request.GET.get('step', 10)
    search = request.GET.get('search', '')
    response = requests.get(f'{API_BASE_URL}/api/Depot/List', params={'userGuid': user_guid, 'pageNumber': page_number, 'step': step, 'search': search})
    depots = response.json()
    return render(request, 'shop/depot_list.html', {'depots': depots})

# تابع برای شمارش لیست انبارها
@login_required
def list_depot_count_view(request):
    user_guid = request.user.user_guid
    step = request.GET.get('step', 10)
    search = request.GET.get('search', '')
    response = requests.get(f'{API_BASE_URL}/api/Depot/ListCount', params={'userGuid': user_guid, 'step': step, 'search': search})
    count = response.json()
    return render(request, 'shop/depot_list_count.html', {'count': count})

# تابع برای ایجاد ورودی/خروجی انبار
@login_required
def create_depot_io_view(request):
    if request.method == 'POST':
        data = {
            "AccDocNo": request.POST['acc_doc_no'],
            "Official": request.POST['official'],
            "No": request.POST['no'],
            "Date": request.POST['date'],
            "Depot1Description": request.POST['depot1_description'],
            "Depot1Code": request.POST['depot1_code'],
            "AccountDebitGuid": request.POST['account_debit_guid'],
            "AccountCreditGuid": request.POST['account_credit_guid'],
            "DriverGuid": request.POST['driver_guid'],
            "DriverDescription": request.POST['driver_description'],
            "DriverCode": request.POST['driver_code'],
            "Depot2Guid": request.POST['depot2_guid'],
            "Depot2Description": request.POST['depot2_description'],
            "Depot2Code": request.POST['depot2_code'],
            "Depot1Guid": request.POST['depot1_guid'],
            "ExpertGuid": request.POST['expert_guid'],
            "ExpertDescription": request.POST['expert_description'],
            "ExpertCode": request.POST['expert_code'],
            "PersonCode": request.POST['person_code'],
            "CargoNo": request.POST['cargo_no'],
            "PersonDescription": request.POST['person_description'],
            "Status": request.POST['status'],
            "PersonGuid": request.POST['person_guid'],
            "Kind": request.POST['kind'],
            "PortageCost": request.POST['portage_cost'],
            "PriceListGuid": request.POST['price_list_guid'],
            "Remarks": request.POST['remarks'],
            "Type": request.POST['type'],
            "Value": request.POST['value'],
            "Details": request.POST.get('details', []),
            "PostStatus": request.POST['post_status']
        }
        user_guid = request.user.user_guid
        response = requests.post(f'{API_BASE_URL}/api/DepotIo/Create', params={'userGuid': user_guid}, json=data)
        if response.status_code == 200:
            return redirect('depot_io_list')
    return render(request, 'shop/create_depot_io.html')

# تابع برای ویرایش ورودی/خروجی انبار
@login_required
def edit_depot_io_view(request, depot_io_guid):
    if request.method == 'POST':
        data = {
            "AccDocNo": request.POST['acc_doc_no'],
            "AccountCreditGuid": request.POST['account_credit_guid'],
            "AccountDebitGuid": request.POST['account_debit_guid'],
            "No": request.POST['no'],
            "Date": request.POST['date'],
            "Depot1Code": request.POST['depot1_code'],
            "Depot1Description": request.POST['depot1_description'],
            "Depot1Guid": request.POST['depot1_guid'],
            "Depot2Code": request.POST['depot2_code'],
            "Depot2Description": request.POST['depot2_description'],
            "Depot2Guid": request.POST['depot2_guid'],
            "DriverCode": request.POST['driver_code'],
            "DriverDescription": request.POST['driver_description'],
            "DriverGuid": request.POST['driver_guid'],
            "ExpertCode": request.POST['expert_code'],
            "ExpertDescription": request.POST['expert_description'],
            "ExpertGuid": request.POST['expert_guid'],
            "PersonDescription": request.POST['person_description'],
            "PersonCode": request.POST['person_code'],
            "PersonGuid": request.POST['person_guid'],
            "CargoNo": request.POST['cargo_no'],
            "Official": request.POST['official'],
            "Kind": request.POST['kind'],
            "PriceListGuid": request.POST['price_list_guid'],
            "PortageCost": request.POST['portage_cost'],
            "Remarks": request.POST['remarks'],
            "Value": request.POST['value'],
            "Status": request.POST['status'],
            "PostStatus": request.POST['post_status'],
            "Type": request.POST['type'],
            "Details": request.POST.get('details', [])
        }
        response = requests.put(f'{API_BASE_URL}/api/DepotIo/Edit', params={'depotIoGuid': depot_io_guid}, json=data)
        if response.status_code == 200:
            return redirect('depot_io_list')
    user_guid = request.user.user_guid
    response = requests.get(f'{API_BASE_URL}/api/DepotIo/View', params={'userGuid': user_guid, 'depotIoGuid': depot_io_guid})
    depot_io = response.json()
    return render(request, 'shop/edit_depot_io.html', {'depot_io': depot_io})

# تابع برای مشاهده ورودی/خروجی انبار
@login_required
def view_depot_io_view(request, depot_io_guid):
    user_guid = request.user.user_guid
    response = requests.get(f'{API_BASE_URL}/api/DepotIo/View', params={'userGuid': user_guid, 'depotIoGuid': depot_io_guid})
    depot_io = response.json()
    return render(request, 'shop/view_depot_io.html', {'depot_io': depot_io})

# تابع برای لیست ورودی/خروجی انبار
@login_required
def list_depot_io_view(request):
    user_guid = request.user.user_guid
    depot_guid = request.GET.get('depot_guid', '')
    depot_io_type = request.GET.get('depot_io_type', '')
    price_list_guid = request.GET.get('price_list_guid', '')
    response = requests.get(f'{API_BASE_URL}/api/DepotIo/ItemList', params={'userGuid': user_guid, 'depotGuid': depot_guid, 'depotIoType': depot_io_type, 'priceListGuid': price_list_guid})
    depot_ios = response.json()
    return render(request, 'shop/depot_io_list.html', {'depot_ios': depot_ios})

# تابع برای مشاهده موجودی کالا در انبار
@login_required
def depot_holding_view(request):
    user_guid = request.user.user_guid
    response = requests.get(f'{API_BASE_URL}/api/DepotIo/DepotHolding', params={'userGuid': user_guid})
    depot_holding = response.json()
    return render(request, 'shop/depot_holding.html', {'depot_holding': depot_holding})
