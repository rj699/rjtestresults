import pandas as pd
import json
import unittest

def create_orders_dataframe(file_path):
    """
    Creates a DataFrame from orders CSV file with order_id and contact_full_name columns.
    
    Args:
        file_path (str): Path to the CSV file
        
    Returns:
        pandas.DataFrame: DataFrame with order_id and contact_full_name columns
    """
    # Read CSV file with semicolon separator
    df = pd.read_csv(file_path, sep=';')
    
    def extract_full_name(contact_data):
        try:
            # Parse JSON string into Python object
            if pd.isna(contact_data):
                return "Fake Person"
            
            # Handle both single dict and list of dict cases
            contact_info = json.loads(contact_data)
            if isinstance(contact_info, list):
                contact_info = contact_info[0]
                
            # Extract and combine name components
            full_name = f"{contact_info['contact_name']} {contact_info['contact_surname']}"
            return full_name
        except (json.JSONDecodeError, KeyError, TypeError):
            return "Fake Person"
    
    # Create new DataFrame with required columns
    df_1 = pd.DataFrame({
        'order_id': df['order_id'],
        'contact_full_name': df['contact_data'].apply(extract_full_name)
    })
    
    return df_1

class TestOrderProcessing(unittest.TestCase):
    def setUp(self):
        # Sample test data
        self.test_data = """order_id;date;company_id;company_name;crate_type;contact_data;salesowners
f47ac10b-1234;29.01.22;1e2b47e6;Company A;Plastic;[{ "contact_name":"John", "contact_surname":"Smith"}];Owner1
f47ac10b-5678;21.02.22;0f05a8f1;Company B;Wood;;Owner2
f47ac10b-9012;03.04.22;1e2b47e6;Company C;Metal;[{ "contact_name":"Jane", "contact_surname":"Doe"}];Owner3"""
        
        # Write test data to temporary file
        with open('test_orders.csv', 'w') as f:
            f.write(self.test_data)
        
        # Create DataFrame
        self.df = create_orders_dataframe('test_orders.csv')
    
    def test_dataframe_columns(self):
        """Test if DataFrame has the correct columns"""
        expected_columns = ['order_id', 'contact_full_name']
        self.assertEqual(list(self.df.columns), expected_columns)
    
    def test_valid_contact_name(self):
        """Test if valid contact data is correctly processed"""
        self.assertEqual(self.df.iloc[0]['contact_full_name'], 'John Smith')
    
    def test_missing_contact_data(self):
        """Test if missing contact data returns 'Fake Person'"""
        self.assertEqual(self.df.iloc[1]['contact_full_name'], 'Fake Person')
    
    def test_no_null_values(self):
        """Test if there are no null values in contact_full_name"""
        self.assertFalse(self.df['contact_full_name'].isnull().any())
    
    def tearDown(self):
        import os
        # Clean up test file
        if os.path.exists('test_orders.csv'):
            os.remove('test_orders.csv')

if __name__ == '__main__':
    # Create the actual DataFrame
    df_1 = create_orders_dataframe('orders.csv')
    print("DataFrame created successfully:")
    print(df_1.head())
    
    # Run unit tests
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
