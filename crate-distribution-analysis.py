import pandas as pd
from collections import defaultdict
import unittest
import io

def calculate_crate_distribution(data_str):
    """
    Calculate the distribution of crate types per company from CSV data.
    
    Args:
        data_str (str): CSV data as a string
        
    Returns:
        dict: Nested dictionary with company names as keys and crate type counts as values
    """
    # Read CSV data
    df = pd.read_csv(io.StringIO(data_str), sep=';')
    
    # Create a nested dictionary to store the results
    distribution = defaultdict(lambda: defaultdict(int))
    
    # Calculate distribution
    for _, row in df.iterrows():
        company_name = row['company_name'].strip()
        crate_type = row['crate_type'].strip()
        distribution[company_name][crate_type] += 1
    
    return dict(distribution)

class TestCrateDistribution(unittest.TestCase):
    def setUp(self):
        # Sample test data
        self.test_data = """order_id;date;company_id;company_name;crate_type;contact_data;salesowners
1;01.01.22;1;Test Company 1;Plastic;;Owner1
2;02.01.22;1;Test Company 1;Wood;;Owner1
3;03.01.22;1;Test Company 1;Plastic;;Owner1
4;04.01.22;2;Test Company 2;Metal;;Owner2
5;05.01.22;2;Test Company 2;Metal;;Owner2"""

    def test_basic_distribution(self):
        result = calculate_crate_distribution(self.test_data)
        
        expected = {
            'Test Company 1': {'Plastic': 2, 'Wood': 1},
            'Test Company 2': {'Metal': 2}
        }
        
        self.assertEqual(result, expected)
    
    def test_empty_data(self):
        empty_data = "order_id;date;company_id;company_name;crate_type;contact_data;salesowners"
        result = calculate_crate_distribution(empty_data)
        self.assertEqual(result, {})
    
    def test_with_actual_data(self):
        # Test with a snippet of the actual data
        actual_data = """order_id;date;company_id;company_name;crate_type;contact_data;salesowners
f47ac10b-58cc-4372-a567-0e02b2c3d479;29.01.22;1e2b47e6-499e-41c6-91d3-09d12dddfbbd;Fresh Fruits Co;Plastic;;Leonard Cohen
f47ac10b-58cc-4372-a567-0e02b2c3d480;21.02.22;0f05a8f1-2bdf-4be7-8c82-4c9b58f04898;Veggies Inc;Wood;;Luke Skywalker
f47ac10b-58cc-4372-a567-0e02b2c3d481;03.04.22;1e2b47e6-499e-41c6-91d3-09d12dddfbbd;Fresh Fruits Co;Metal;;Luke Skywalker"""
        
        result = calculate_crate_distribution(actual_data)
        
        expected = {
            'Fresh Fruits Co': {'Plastic': 1, 'Metal': 1},
            'Veggies Inc': {'Wood': 1}
        }
        
        self.assertEqual(result, expected)

def main():
    # Run the tests
    unittest.main(argv=[''], exit=False)
    
    # Process the actual data
    with open('orders.csv', 'r') as f:
        data = f.read()
    
    distribution = calculate_crate_distribution(data)
    
    # Print results
    print("\nCrate Type Distribution per Company:")
    print("=====================================")
    for company, crates in sorted(distribution.items()):
        print(f"\n{company}:")
        for crate_type, count in sorted(crates.items()):
            print(f"  {crate_type}: {count}")

if __name__ == '__main__':
    main()
