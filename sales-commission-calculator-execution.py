import json
from decimal import Decimal
import csv
from io import StringIO

def load_data_from_documents(invoices_json, orders_csv):
    # Parse invoices JSON
    invoices_data = json.loads(invoices_json)

    # Parse orders CSV
    orders_data = {}
    csv_reader = csv.DictReader(StringIO(orders_csv), delimiter=';')
    for row in csv_reader:
        orders_data[row['order_id']] = row

    return invoices_data, orders_data

class SalesCommissionCalculator:
    COMMISSION_RATES = {
        0: Decimal('0.06'),    # Main owner: 6%
        1: Decimal('0.025'),   # First co-owner: 2.5%
        2: Decimal('0.0095'),  # Second co-owner: 0.95%
    }

    def __init__(self, invoices_data, orders_data):
        self.invoices = self._parse_invoices(invoices_data)
        self.orders = orders_data

    def _parse_invoices(self, invoices_data):
        return {inv['orderId']: inv for inv in invoices_data['data']['invoices']}

    def _calculate_net_value(self, gross_value, vat):
        """Calculate net value from gross value and VAT percentage"""
        gross = Decimal(gross_value) / 100  # Convert cents to euros
        vat_rate = Decimal(vat) / 100
        net_value = gross / (1 + vat_rate) if vat_rate > 0 else gross
        return net_value

    def calculate_commission(self, net_value, position):
        """Calculate commission for a given position and net value"""
        if position not in self.COMMISSION_RATES:
            return Decimal('0')
        return net_value * self.COMMISSION_RATES[position]

    def calculate_all_commissions(self):
        """Calculate commissions for all sales owners"""
        commissions = {}
        order_details = {}  # To store details for validation

        # Process each order
        for order_id, order in self.orders.items():
            if order_id in self.invoices:
                invoice = self.invoices[order_id]

                # Calculate net value
                net_value = self._calculate_net_value(
                    invoice['grossValue'],
                    invoice['vat']
                )

                # Split salesowners and calculate commissions
                salesowners = [s.strip() for s in order['salesowners'].split(',')]
                for position, owner in enumerate(salesowners):
                    commission = self.calculate_commission(net_value, position)
                    if owner not in commissions:
                        commissions[owner] = Decimal('0')
                        order_details[owner] = []
                    commissions[owner] += commission

                    # Store order details for validation
                    order_details[owner].append({
                        'order_id': order_id,
                        'position': position,
                        'net_value': float(net_value),
                        'commission': float(commission)
                    })

        # Sort by commission amount in descending order
        sorted_commissions = sorted(
            [(owner, float(amount), order_details[owner])
             for owner, amount in commissions.items()],
            key=lambda x: x[1],
            reverse=True
        )

        return sorted_commissions

# Load your actual data
invoices_json = '''
{
  "data": {
    "invoices": [
      {
        "id": "e1e1e1e1-e1e1-e1e1-e1e1-e1e1e1e1e1e1",
        "orderId": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
        "companyId": "1e2b47e6-499e-41c6-91d3-09d12dddfbbd",
        "grossValue": "324222",
        "vat": "0"
      },
      # ... (rest of your invoice data)
    ]
  }
}
'''

# Calculate commissions
calculator = SalesCommissionCalculator(json.loads(invoices_json), orders_data)
results = calculator.calculate_all_commissions()

# Print detailed results
print("\nSales Commission Report")
print("="*50)
print(f"{'Sales Owner':<30} {'Total Commission':>15}")
print("-"*50)
