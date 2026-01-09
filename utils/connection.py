import os
from supabase import create_client, Client
from dotenv import load_dotenv
load_dotenv()

# Connect to the database
DB_URL = os.getenv("DB_SUPABASE_URL")
DB_KEY = os.getenv("DB_SUPABASE_PUBLISHABLE_DEFAULT_KEY")
CLIENT = create_client(DB_URL, DB_KEY)
consignment_type_options = ["Racket", "Shirt", "Shoes", "Bag", "Others"]
status_type_options = ["New", "Posted", "Sold", "Shipped", "Completed", "Completed Elsewhere"]

def get_complete_consignments(types=None, status=None):
    n_count = get_total_consignments_count()
    n_start, n_end = 0, 999999
    findata = []
    while n_start < n_count:
        findata += _get_complete_consignments(n_start, n_end, types, status)
        n_start += 1000000
        n_end += 1000000
    return findata

def _get_complete_consignments(n_start, n_end, types, status):
    """Fetch all complete consignments from the database."""
    types = types if types else consignment_type_options
    status = status if status else status_type_options
    data = (
        CLIENT.table("CONSIGNMENTS")
            .select("*")
            .in_("item_type", types)
            .in_("status", status)
            .eq("consignment_status_deleted", False)
            .order("consignment_id", desc=True)
            .range(n_start, n_end)
            .execute()
    ).data
    data_seller = (
        CLIENT.table("CONSIGNMENTS")
            .select("consignment_id, CONTACTS!CONSIGNMENTS_seller_id_fkey(contact_wa, contact_name, contact_location)")
            .in_("item_type", types)
            .in_("status", status)
            .eq("consignment_status_deleted", False)
            .order("consignment_id", desc=True)
            .range(n_start, n_end)
            .execute()
    ).data
    data_buyers = (
        CLIENT.table("CONSIGNMENTS")
            .select("consignment_id, CONTACTS!CONSIGNMENTS_buyer_id_fkey(contact_wa, contact_name, contact_location)")
            .in_("item_type", types)
            .in_("status", status)
            .eq("consignment_status_deleted", False)
            .order("consignment_id", desc=True)
            .range(n_start, n_end)
            .execute()
    ).data

    findata = []
    for d, ds, db in zip(data, data_seller, data_buyers):
        record = d.copy()
        record.update({
            "seller_wa": ds["CONTACTS"]["contact_wa"] if ds["CONTACTS"] else None,
            "seller_name": ds["CONTACTS"]["contact_name"] if ds["CONTACTS"] else None,
            "seller_location": ds["CONTACTS"]["contact_location"] if ds["CONTACTS"] else None,
            "buyer_wa": db["CONTACTS"]["contact_wa"] if db["CONTACTS"] else None,
            "buyer_name": db["CONTACTS"]["contact_name"] if db["CONTACTS"] else None,
            "buyer_location": db["CONTACTS"]["contact_location"] if db["CONTACTS"] else None,
        })
        findata.append(record)
    
    return findata

def get_total_consignments_count():
    """Get the total count of consignments in the database."""
    count = CLIENT.table("CONSIGNMENTS").select("consignment_id", count="exact").execute().count
    return count