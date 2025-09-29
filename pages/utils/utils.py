import json

consignment_status =  json.load(open("assets/texts.json")).get("status-effect")
def parse_consignment(head, val):
    if head == "ID":
        return int(val[2:])
    elif head == "Status":
        consignment_stats_num = consignment_status.index(val) if consignment_status.index(val) else "X"
        return f"{consignment_stats_num}. {val}"
    else:
        return val