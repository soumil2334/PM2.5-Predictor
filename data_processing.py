"""
Data processing utilities for PM2.5 prediction model.
"""
import pandas as pd
import numpy as np
import xarray as xr
import os
from typing import Optional, List, Dict, Any, Tuple

def load_netcdf_to_dataframe(netcdf_file: str, output_csv: Optional[str] = None) -> pd.DataFrame:
    """
    Load NetCDF file to pandas DataFrame and optionally save to CSV.
    
    Args:
        netcdf_file: Path to the NetCDF file
        output_csv: Optional path to save as CSV
        
    Returns:
        DataFrame with the NetCDF data
    """
    try:
        # Open the NetCDF file
        ds = xr.open_dataset(netcdf_file, engine="netcdf4")
        
        # Convert to DataFrame
        df = ds.to_dataframe().reset_index()
        
        # Save as CSV if output_csv is provided
        if output_csv:
            df.to_csv(output_csv, index=False)
            print(f"Saved data to {output_csv}")
        
        return df
    except Exception as e:
        print(f"Error processing NetCDF file: {e}")
        raise

def merge_dataframes(df_list: List[pd.DataFrame], 
                     on: List[str],
                     how: str = 'inner') -> pd.DataFrame:
    """
    Merge multiple DataFrames on common columns.
    
    Args:
        df_list: List of DataFrames to merge
        on: Columns to merge on
        how: Type of merge (inner, outer, left, right)
        
    Returns:
        Merged DataFrame
    """
    if not df_list:
        raise ValueError("No DataFrames provided for merging")
    
    result = df_list[0]
    for df in df_list[1:]:
        result = result.merge(df, on=on, how=how)
    
    return result

def preprocess_features(df: pd.DataFrame, 
                       features: List[str], 
                       target: Optional[str] = None) -> Tuple[pd.DataFrame, Optional[pd.Series]]:
    """
    Preprocess features for model training or prediction.
    
    Args:
        df: DataFrame with raw data
        features: List of feature column names to include
        target: Optional target column name
        
    Returns:
        Tuple of (feature_df, target_series) where target_series may be None if no target provided
    """
    # Select features
    X = df[features].copy()
    
    # Handle missing values
    X = X.fillna(X.mean())
    
    # Select target if provided
    y = df[target] if target else None
    
    return X, y

def create_train_test_split(X: pd.DataFrame, 
                           y: pd.Series,
                           test_size: float = 0.2,
                           random_state: int = 42) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Split data into training and testing sets.
    
    Args:
        X: Feature DataFrame
        y: Target Series
        test_size: Fraction of data to use for testing
        random_state: Random seed for reproducibility
        
    Returns:
        Tuple of (X_train, X_test, y_train, y_test)
    """
    from sklearn.model_selection import train_test_split
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    
    return X_train, X_test, y_train, y_test 