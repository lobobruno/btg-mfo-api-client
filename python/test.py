from btg_api_position import get_position_by_account_and_date
from btg_api_operation import get_movements_by_account_full, get_movements_by_partner_weekly
import json

if False:
    response = get_position_by_account_and_date("001234567", "2025-11-28")

    # save the response to json file
    with open('get_position_by_account_and_date.json', 'w') as f:
        json.dump(response, f)


if False:
    response = get_movements_by_account_full("001234567")

    with open('get_movements_by_account_full.json', 'w') as f:
        json.dump(response, f)


reponse = get_movements_by_partner_weekly()

with open('get_movements_by_partner_weekly.json', 'w') as f:
    json.dump(reponse, f)
