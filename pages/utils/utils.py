import json

consignment_status =  json.load(open("assets/texts.json")).get("status-effect")
def parse_consignment(head, val):
    if head == "ID":
        return int(val[2:])
    if head in ("Price Posted", "Price Seller", "Price - Sold", "Profit"):
        return price_to_value(val)
    else:
        return val
    
def price_to_value(price):
    if isinstance(price, str):
        if price=="":
            return price
        elif "(" in price:
            return float(price.replace("Rp. ", "").replace(",","").replace(")","").replace("(","-"))
        else:
            return float(price.replace("Rp. ", "").replace(",",""))
    else:
        return price