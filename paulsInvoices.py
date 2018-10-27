from datetime import date

class Invoice:
    """Paul's invoices"""
    template = "invoice-template.html"

    def __init__(self):
        self.name = False
        self.address = False
        self.phone = False
        self.email = False
        self.invoice_id = False
        self.period = False
        self.date = False
        self.client = False
        self.client_address = False
        self.payment_details = False
        self.invoice_table = False

    def render(self):
        if self.invoice_id:
            output_file = self.invoice_id + ".html"
        else:
            output_file = "output.html"

        with open(self.template) as t, open(output_file, "w") as o:
            for line in t:

                # mandatory items in simple string format
                for item in ['name', 'address', 'phone', 'email', 'invoice_id', 'client', 'payment_details']:
                    searchstring = "{+%s+}" % item
                    if searchstring in line:
                        if getattr(self, item):
                            line = line.replace(searchstring, getattr(self, item))
                        else:
                            line = line.replace(searchstring, "<span class='whoops'>No " + item +"?!</span>")

                # optional items - deletes whole line if not entered
                for item in ['period', 'client_address']:
                    searchstring = "{+%s+}" % item
                    if searchstring in line:
                        if getattr(self, item):
                            line = line.replace(searchstring, getattr(self, item))
                        else:
                            line = ""

                # items with formatting requirements
                if "{+date+}" in line:
                    if self.date:
                        line = line.replace("{+date+}", format_date(self.date))
                    else:
                        line = line.replace("{+date+}", "<span class='whoops'>No date?!</span>")

                if "{+invoice_table+}" in line:
                    if self.invoice_table:
                        line = line.replace("{+invoice_table+}", self.invoice_table.render())
                    else:
                        line = line.replace(searchstring, "<span class='whoops'>No invoice_table?!</span>")


                o.write(line)

class InvoiceTable:
    """Paul's output table class with hourly calculations"""

    def __init__ (self):
        self.header = []
        self.rows = []
        self.columns = 3

    def addHeader(self, fields):
        self.header.append(fields)

    def addHourlyItem(self, fields):
        self.rows.append(["hourly", fields])

    def addFixedItem(self, fields):
        self.rows.append(["fixed", fields])

    def addSubtotal(self, text):
        self.rows.append(["subtotal", text])

    def render(self):
        output = "<table>"
        count_hours = 0
        count_money = 0
        sub_count_hours = 0
        sub_count_money = 0

        # table header
        output += "<thead><tr>"
        output += "<th class='task'>Task</th>"
        output += "<th class='hours'>Hours</th>"
        output += "<th class='money'>Amount</th>"
        output += "</tr></thead>"
        
        output += "<tbody>"

        for row in self.rows:
            type = row[0]
            
            if type == "hourly":
                fields = row[1]

                description = fields [0]
                hours = fields[1]
                money = fields[1]*fields[2]

                count_hours += hours
                count_money += money
                sub_count_hours += hours
                sub_count_money += money
               
                output += "<tr>"
                output += "<td class='task'>" + description + "</td>"
                output += "<td class='hours'>" + format_hours(hours) + "</td>"
                output += "<td class='money'>" + format_money(money) + "</td>"
                output += "<tr>"

            if type == "fixed":
                fields = row[1]

                description = fields[0]
                money = fields[1]

                count_money += money
                sub_count_money += money
               
                output += "<tr>"
                output += "<td class='task'>" + description + "</td>"
                output += "<td></td>"
                output += "<td class='money'>" + format_money(money) + "</td>"
                output += "<tr>"

            if type == "subtotal":
                output += "<tr class='subtotal'>"
                output += "<td>" + row[1] + ":</td>"
                output += "<td class='hours'>" + format_hours(sub_count_hours) + "</td>"
                output += "<td class='money'>" + format_money(sub_count_money) + "</td>"
                output += "<tr>"

                sub_count_hours = 0
                sub_count_money = 0

        output += "</tbody>"

        output += "<tfoot>"
        output += "<tr>"
        output += "<td colspan=2>Balance due:</td>"
        output += "<td class='money'>" + format_money(count_money) + "</td>"
        output += "<tr>"
        output += "</tfoot>"

        output += "</table>"

        return output

class CASInvoiceTable:
    """Paul's output table class for CAS invoices"""

    def __init__ (self):
        self.header = []
        self.rows = []
        self.columns = 3

    def addHeader(self, fields):
        self.header.append(fields)

    def addGig(self, fields):
        self.rows.append(["gig", fields])

    def render(self):
        output = "<table>"
        count_hours = 0
        count_money = 0
        sub_count_hours = 0
        sub_count_money = 0

        # table header
        output += "<thead><tr>"
        output += "<th class='reference'>Reference</th>"
        output += "<th class='date'>Date</th>"
        output += "<th class='task'>Description</th>"
        output += "<th class='money'>Amount</th>"
        output += "</tr></thead>"
        
        output += "<tbody>"

        for row in self.rows:
            type = row[0]
            
            if type == "gig":
                fields = row[1]

                reference = fields[0]
                date = fields[1]
                description = fields[2]
                money = fields[3]

                count_money += money
                sub_count_money += money
               
                output += "<tr>"
                output += "<td class='reference'>" + reference + "</td>"
                output += "<td class='date'>" + format_date(date) + "</td>"
                output += "<td class='task'>" + description + "</td>"
                output += "<td class='money'>" + format_money(money) + "</td>"
                output += "<tr>"

        output += "</tbody>"

        output += "<tfoot>"
        output += "<tr>"
        output += "<td colspan=3>Balance due:</td>"
        output += "<td class='money'>" + format_money(count_money) + "</td>"
        output += "<tr>"
        output += "</tfoot>"

        output += "</table>"

        return output

def format_hours(h):
    return '{0:.2f}'.format(h)

def format_money(m):
    return "<span class='pound-sign'>&pound;</span>" + '{0:,.2f}'.format(m)

def format_date(d):
    date_format = "%d %b %Y"
    return d.strftime(date_format)
