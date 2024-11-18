import pandas as pd
import pytest

def create_company_salesowners_df(orders_data):
    """
    Creates a DataFrame with unique companies and their associated salesowners.
    
    Args:
        orders_data (pd.DataFrame): DataFrame containing order information with
            company_id, company_name, and salesowners columns
    
    Returns:
        pd.DataFrame: DataFrame with company_id, company_name, and list_salesowners columns
    """
    # Create a copy to avoid modifying the original data
    df = orders_data.copy()
    
    # Split salesowners string into list and explode to create separate rows
    df['salesowners'] = df['salesowners'].fillna('').str.split(',')
    df = df.explode('salesowners')
    
    # Clean up salesowner names by stripping whitespace
    df['salesowners'] = df['salesowners'].str.strip()
    
    # Group by company and aggregate data
    df_grouped = df.groupby(['company_id', 'company_name'])['salesowners'].agg(
        lambda x: ','.join(sorted(set(filter(None, x))))
    ).reset_index()
    
    # Rename the column to match requirements
    df_grouped = df_grouped.rename(columns={'salesowners': 'list_salesowners'})
    
    return df_grouped

def test_create_company_salesowners_df():
    """Unit tests for create_company_salesowners_df function"""
    
    # Test case 1: Basic functionality with single company
    test_data_1 = pd.DataFrame({
        'company_id': ['123'],
        'company_name': ['Test Co'],
        'salesowners': ['John Smith, Alice Brown']
    })
    result_1 = create_company_salesowners_df(test_data_1)
    assert result_1['list_salesowners'].iloc[0] == 'Alice Brown,John Smith'
    
    # Test case 2: Handling duplicate salesowners
    test_data_2 = pd.DataFrame({
        'company_id': ['123', '123'],
        'company_name': ['Test Co', 'Test Co'],
        'salesowners': ['John Smith, Alice Brown', 'John Smith, Bob Carter']
    })
    result_2 = create_company_salesowners_df(test_data_2)
    assert result_2['list_salesowners'].iloc[0] == 'Alice Brown,Bob Carter,John Smith'
    
    # Test case 3: Handling empty salesowners
    test_data_3 = pd.DataFrame({
        'company_id': ['123'],
        'company_name': ['Test Co'],
        'salesowners': ['']
    })
    result_3 = create_company_salesowners_df(test_data_3)
    assert result_3['list_salesowners'].iloc[0] == ''
    
    # Test case 4: Multiple companies with overlapping salesowners
    test_data_4 = pd.DataFrame({
        'company_id': ['123', '456'],
        'company_name': ['Test Co 1', 'Test Co 2'],
        'salesowners': ['John Smith, Alice Brown', 'Alice Brown, Bob Carter']
    })
    result_4 = create_company_salesowners_df(test_data_4)
    assert len(result_4) == 2
    assert result_4.loc[result_4['company_id'] == '123', 'list_salesowners'].iloc[0] == 'Alice Brown,John Smith'
    assert result_4.loc[result_4['company_id'] == '456', 'list_salesowners'].iloc[0] == 'Alice Brown,Bob Carter'

# Process the actual data
def process_orders_data(orders_csv):
    """
    Process the orders CSV data into the required DataFrame format.
    
    Args:
        orders_csv (str): CSV string containing orders data
    
    Returns:
        pd.DataFrame: Processed DataFrame with required columns
    """
    # Read the CSV data
    df = pd.read_csv(orders_csv, sep=';')
    
    # Create the final DataFrame
    df_3 = create_company_salesowners_df(df)
    
    return df_3

if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__])
    
    # Read the orders CSV data
    orders_df = pd.read_csv('orders.csv', sep=';')
    
    # Create the final DataFrame
    df_3 = create_company_salesowners_df(orders_df)
    
    # Display the results
    print("\nFinal DataFrame (df_3):")
    print(df_3)
    
    # Display some basic statistics
    print("\nDataFrame Statistics:")
    print(f"Total number of unique companies: {len(df_3)}")
    print("\nSample of the data:")
    print(df_3.head())
