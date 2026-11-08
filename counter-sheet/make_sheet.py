# Koh Chang counter rate sheet (A4). Fills template.html with today's rates and writes sheet.html.
# Usage: python3 make_sheet.py "28 Oct 2026" "Wednesday 28 October 2026" USD100 USD20 EUR GBP CHF AUD CAD
#   (the seven numbers are column D "Buying ลูกค้า" of Rate_Table, exactly as read from the Google Sheet)
# Rule agreed with Orathai (8 Nov 2026): the POS pays the sheet value rounded half-up to 2 decimals.
# The printed rate sits just under that POS price, by a small amount that differs per currency
# (0.0001-0.0008) so the endings look natural rather than identical.
# The printed rate is NEVER above what the POS pays.
import sys, re, os
from decimal import Decimal, ROUND_HALF_UP
here = os.path.dirname(os.path.abspath(__file__))
date_key, date_long = sys.argv[1], sys.argv[2]
paid = [float(Decimal(x).quantize(Decimal('0.01'), ROUND_HALF_UP)) for x in sys.argv[3:10]]
keys = [('USD','$100 · $50 notes'),('USD','$20 · $5 notes'),('EUR','Euro'),('GBP','British Pound'),('CHF','Swiss Franc'),('AUD','Australian Dollar'),('CAD','Canadian Dollar')]
OFFSET = {'$100 · $50 notes': 1, '$20 · $5 notes': 6, 'Euro': 2, 'British Pound': 8,
          'Swiss Franc': 4, 'Australian Dollar': 3, 'Canadian Dollar': 7}
def shown(v, code, desc):
    # v is already the POS price (2 decimals). Print a little under it, by a small amount
    # that differs per currency so the endings look natural instead of all the same.
    # Never returns a value above v.
    return round(v - OFFSET.get(desc, 5)/10000, 4)
s = open(os.path.join(here, 'template.html'), encoding='utf-8').read()
for (c, d), v in zip(keys, paid):
    s, k = re.subn(r'(<b>%s</b><span>%s</span></div><div class="rt">)[0-9.]+(</div>)' % (re.escape(c), re.escape(d)), r'\g<1>%.4f\g<2>' % shown(v, c, d), s)
    assert k == 1, (c, d)
    print('%s %-18s POS %.2f  sheet %.4f' % (c, d, v, shown(v, c, d)))
s = re.sub(r'Today&rsquo;s rates &middot; [^<]+', 'Today&rsquo;s rates &middot; ' + date_long, s)
open('sheet.html', 'w', encoding='utf-8').write(s)
