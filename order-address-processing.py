import pandas as pd
import json
import unittest

def create_address_dataframe(file_path):
    """
    Creates a DataFrame from orders CSV file with order_id and contact_address columns.
    
    Args:
        file_path (str): Path to the CSV file
        
    Returns:
        pandas.DataFrame: DataFrame with order_id and contact_address columns
    """
    # Read CSV file with semicolon separator
    df = pd.read_csv(file_path, sep=';')
    
    def format_address(contact_data):
        try:
            if pd.isna(contact_data):
                return "Unknown, UNK00"
            
            # Parse JSON string into Python object
            contact_info = json.loads(contact_data)
            if isinstance(contact_info, list):
                contact_info = contact_info[0]
            
            # Extract city and postal code
            city = contact_info.get('city', 'Unknown')
            postal_code = contact_info.get('cp', 'UNK00')
            
            # Format postal code to string if it's a number
            if isinstance(postal_code, (int, float)):
                postal_code = str(postal_code)
            
            # Create formatted address
            return f"{city}, {postal_code}"
            
        except (json.JSONDecodeError, KeyError, TypeError):
            return "Unknown, UNK00"
    
    # Create new DataFrame with required columns
    df_2 = pd.DataFrame({
        'order_id': df['order_id'],
        'contact_address': df['contact_data'].apply(format_address)
    })
    
    return df_2

class TestAddressProcessing(unittest.TestCase):
    def setUp(self):
        # Sample test data with various scenarios
        self.test_data = """order_id;date;company_id;company_name;crate_type;contact_data;salesowners
id1;29.01.22;1e2b47e6;Company A;Plastic;[{ "contact_name":"John", "contact_surname":"Smith", "city":"New York", "cp":"10001"}];Owner1
id2;21.02.22;0f05a8f1;Company B;Wood;;Owner2
id3;03.04.22;1e2b47e6;Company C;Metal;[{ "contact_name":"Jane", "contact_surname":"Doe", "city":"Chicago"}];Owner3
id4;04.04.22;1e2b47e6;Company D;Metal;[{ "contact_name":"Bob", "contact_surname":"Jones", "cp":"12345"}];Owner4
id5;05.04.22;1e2b47e6;Company E;Metal;[{ "contact_name":"Alice", "contact_surname":"Brown", "city":"London", "cp":2000}];Owner5"""
        
        # Write test data to temporary file
        with open('test_orders.csv', 'w') as f:
            f.write(self.test_data)
        
        # Create DataFrame
        self.df = create_address_dataframe('test_orders.csv')
    
    def test_dataframe_columns(self):
        """Test if DataFrame has the correct columns"""
        expected_columns = ['order_id', 'contact_address']
        self.assertEqual(list(self.df.columns), expected_columns)
    
    def test_complete_address(self):
        """Test if complete address data is correctly formatted"""
        self.assertEqual(self.df.iloc[0]['contact_address'], 'New York, 10001')
    
    def test_missing_all_contact_data(self):
        """Test if missing contact data returns default values"""
        self.assertEqual(self.df.iloc[1]['contact_address'], 'Unknown, UNK00')
    
    def test_missing_postal_code(self):
        """Test if missing postal code is replaced with UNK00"""
        self.assertEqual(self.df.iloc[2]['contact_address'], 'Chicago, UNK00')
    
    def test_missing_city(self):
        """Test if missing city is replaced with Unknown"""
        self.assertEqual(self.df.iloc[3]['contact_address'], 'Unknown, 12345')
    
    def test_numeric_postal_code(self):
        """Test if numeric postal code is handled correctly"""
        self.assertEqual(self.df.iloc[4]['contact_address'], 'London, 2000')
    
    def test_no_null_values(self):
        """Test if there are no null values in contact_address"""
        self.assertFalse(self.df['contact_address'].isnull().any())
    
    def tearDown(self):
        import os
        # Clean up test file
        if os.path.exists('test_orders.csv'):
            os.remove('test_orders.csv')

if __name__ == '__main__':
    # Create the actual DataFrame
    df_2 = create_address_dataframe('orders.csv')
    print("DataFrame created successfully:")
    print(df_2.head())
    print("\nSample addresses:")
    print(df_2['contact_address'].head())
    
    # Run unit tests
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
