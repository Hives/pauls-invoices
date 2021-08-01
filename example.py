from paulsInvoices import Invoice, InvoiceTable
from datetime import date

hourly_rate = 66

output_table = InvoiceTable()

output_table.addHourlyItem(["Clean the toilet", 0.16, hourly_rate])
output_table.addHourlyItem(["Scrub the floor", 9.40, hourly_rate])
output_table.addHourlyItem(["Take out the rubbish", 19.79, hourly_rate])
output_table.addSubtotal("Cleaning subtotal")
output_table.addFixedItem(["This is a one off task with no hourly rate", 101.20])
output_table.addHourlyItem(["Darn your socks", 20, hourly_rate])

inv = Invoice()

# your personal details (use <br> for multiple lines):
inv.name = "Joe Bloggs"
inv.address = """56 Avenue Street<br>
                 Townsville<br>
                 123 ABC"""
inv.phone = "01223 334444"
inv.email = "joe.bloggs@joebloggs.com"

# invoice details
inv.invoice_id = "INVOICE01"
inv.period = "September 2018"  # the period to which the invoice refers - optional
inv.date = date(2018, 10, 4)  # year, month, day

# client details
inv.client = "Janet Colgate"
inv.client_address = """99 Boulevard Road<br>
                        Cityborough<br>
                        789 XYZ"""

# how you accept payment
inv.payment_details = """Please make cheques payable to Joe Bloggs,<br>
                         or bank transfer to Joe Bloggs, Frank's Bank, 12345678 12-34-56"""

# the actual details
inv.invoice_table = output_table

inv.render()
