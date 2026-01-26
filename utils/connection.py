import os
from supabase import create_client
from dotenv import load_dotenv
load_dotenv()

# Connect to the database
DB_URL = os.getenv("DB_SUPABASE_URL")
DB_KEY = os.getenv("DB_SUPABASE_PUBLISHABLE_DEFAULT_KEY")
consignment_type_options = ["Racket", "Shirt", "Shoes", "Bag", "Others"]
status_type_options = ["New", "Posted", "Sold", "Shipped", "Completed", "Completed Elsewhere"]

def get_complete_data(func, tablename, **kwargs):
    client = create_client(DB_URL, DB_KEY)
    id_name = tablename.lower()[:-1]
    n_count = client.table(tablename).select(f"{id_name}_id", count="exact").execute().count
    n_start, n_end = 0, 999999
    findata = []
    while n_start < n_count:
        findata += func(n_start, n_end, **kwargs)
        n_start += 1000000
        n_end += 1000000
    return findata

def get_complete_consignments(types=None, status=None):
    return get_complete_data(_get_complete_consignments, tablename="CONSIGNMENTS", types=types, status=status)

def get_complete_brands():
    return get_complete_data(_get_complete_brands, tablename="BRANDS")

def get_complete_items(item_type=None, brand_name=None, item_name=None):
    return get_complete_data(_get_complete_items, tablename="ITEMS", item_type=item_type, brand_name=brand_name, item_name=item_name)

def get_complete_shapes():
    return get_complete_data(_get_complete_shapes, tablename="SHAPES")

def get_complete_materials(material_type=None):
    return get_complete_data(_get_complete_materials, tablename="MATERIALS", material_type=material_type)

def get_complete_contacts(contact_wa=None):
    return get_complete_data(_get_complete_contacts, tablename="CONTACTS", contact_wa=contact_wa)

# --- ACTUAL GETERS ---
# ---------------------

def _get_complete_consignments(n_start, n_end, types, status):
    """Fetch all complete consignments from the database."""
    client = create_client(DB_URL, DB_KEY)
    types = types if types else consignment_type_options
    status = status if status else status_type_options
    data = (
        client.table("consignments_vw").select("*")
            .in_("item_type", types)
            .in_("status", status)
            .eq("consignment_status_deleted", False)
            .order("consignment_id", desc=True)
            .range(n_start, n_end)
            .execute()
    ).data
    
    return data

def _get_complete_brands(n_start, n_end):
    client = create_client(DB_URL, DB_KEY)
    data = (
        client.table("BRANDS")
            .select("brand_name")
            .range(n_start, n_end)
            .execute()
    ).data
    
    return data

def _get_complete_shapes(n_start, n_end):
    client = create_client(DB_URL, DB_KEY)
    data = (
        client.table("SHAPES")
            .select("shape_name")
            .range(n_start, n_end)
            .execute()
    ).data
    return data

def _get_complete_materials(n_start, n_end, material_type):
    client = create_client(DB_URL, DB_KEY)
    _data = client.table("MATERIALS").select("material_name")
    if material_type:
        _data = _data.eq("material_type", material_type)
    data = (
        _data
            .range(n_start, n_end)
            .execute()
    ).data
    return data


def _get_complete_contacts(n_start, n_end, contact_wa):
    client = create_client(DB_URL, DB_KEY)
    _data = client.table("CONTACTS").select("*")
    if contact_wa:
        _data = _data.eq("contact_wa", contact_wa)
    data = (
        _data
            .range(n_start, n_end)
            .execute()
    ).data
    return data

def get_distinct_contact_location(n_start=0, n_end=99999):
    client = create_client(DB_URL, DB_KEY)
    data = (
        client.table("distinct_contact_locations")
            .select("contact_location")
            .range(n_start, n_end)
            .execute()
    ).data
    return data

def _get_complete_items(n_start, n_end, item_type, brand_name, item_name):
    client = create_client(DB_URL, DB_KEY)
    _data = client.table("items_vw").select("*")
    if item_type:
        _data = _data.eq("item_type", item_type)
    if brand_name:
        _data = _data.eq("brand_name", brand_name)
    if item_name:
        _data = _data.eq("item_name", item_name)
    
    data = (_data.range(n_start, n_end).execute()).data
    return data