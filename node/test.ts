import { writeFile } from 'node:fs/promises';
import {
  getMovementsByAccountFull,
  getMovementsByPartnerWeekly,
  getPositionByAccountAndDate,
} from './src/index.js';

if (false) {
  const response = await getPositionByAccountAndDate('004209281', '2025-11-28');
  await writeFile(
    'get_position_by_account_and_date.json',
    JSON.stringify(response)
  );
}

if (false) {
  await getMovementsByAccountFull('000174168');
}

await getMovementsByPartnerWeekly();
await writeFile('get_movements_by_partner_weekly.json', JSON.stringify(null));
