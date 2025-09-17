import pandas as pd
import os
import numpy as np
from pathlib import Path

def validate_dataset(file_path, dataset_name):
    """Validate a single dataset and return validation results"""
    print(f"\n{'='*60}")
    print(f"VALIDATING: {dataset_name}")
    print(f"{'='*60}")
    
    try:
        # Read the dataset
        df = pd.read_csv(file_path)
        
        # Basic info
        print(f"✓ File loaded successfully")
        print(f"✓ Shape: {df.shape[0]} rows, {df.shape[1]} columns")
        print(f"✓ Columns: {list(df.columns)}")
        
        # Check for missing values
        missing_data = df.isnull().sum()
        if missing_data.sum() > 0:
            print(f"⚠️  Missing values found:")
            for col, missing in missing_data.items():
                if missing > 0:
                    print(f"   - {col}: {missing} missing values")
        else:
            print(f"✓ No missing values found")
        
        # Check for duplicates
        duplicates = df.duplicated().sum()
        if duplicates > 0:
            print(f"⚠️  {duplicates} duplicate rows found")
        else:
            print(f"✓ No duplicate rows found")
        
        # Check coordinate columns if they exist
        coord_cols = [col for col in df.columns if 'lat' in col.lower() or 'lon' in col.lower() or 'x_coord' in col.lower() or 'y_coord' in col.lower()]
        if coord_cols:
            print(f"✓ Coordinate columns found: {coord_cols}")
            
            # Validate coordinate ranges (Dubai is roughly 24.7°N to 25.4°N and 55.1°E to 55.6°E)
            for col in coord_cols:
                if 'lat' in col.lower() or 'y_coord' in col.lower():
                    min_val, max_val = df[col].min(), df[col].max()
                    if 24.0 <= min_val <= 26.0 and 24.0 <= max_val <= 26.0:
                        print(f"   ✓ {col}: Valid latitude range ({min_val:.6f} to {max_val:.6f})")
                    else:
                        print(f"   ⚠️  {col}: Unusual latitude range ({min_val:.6f} to {max_val:.6f})")
                
                if 'lon' in col.lower() or 'x_coord' in col.lower():
                    min_val, max_val = df[col].min(), df[col].max()
                    if 55.0 <= min_val <= 56.0 and 55.0 <= max_val <= 56.0:
                        print(f"   ✓ {col}: Valid longitude range ({min_val:.6f} to {max_val:.6f})")
                    else:
                        print(f"   ⚠️  {col}: Unusual longitude range ({min_val:.6f} to {max_val:.6f})")
        
        # Data type info
        print(f"✓ Data types:")
        for col, dtype in df.dtypes.items():
            print(f"   - {col}: {dtype}")
        
        return True, df
        
    except Exception as e:
        print(f"❌ Error loading {dataset_name}: {str(e)}")
        return False, None

def main():
    """Main validation function"""
    print("🔍 DATA VALIDATION FOR GIS INTEGRATION")
    print("="*60)
    
    # Define datasets to validate
    datasets = {
        "Private Schools": "preprocessed_datasets/Private-Schools_Database_-(English)_cleaned.csv",
        "Community Population": "preprocessed_datasets/dubai_pop_2019_cleaned.csv", 
        "Metro Venues": "preprocessed_datasets/metro_venues_total_cleaned.csv",
        "Healthcare Facilities": "preprocessed_datasets/Sheryan_Facility_Detail_cleaned.csv"
    }
    
    validation_results = {}
    
    # Validate each dataset
    for name, path in datasets.items():
        if os.path.exists(path):
            success, df = validate_dataset(path, name)
            validation_results[name] = {"success": success, "dataframe": df}
        else:
            print(f"\n❌ Dataset not found: {path}")
            validation_results[name] = {"success": False, "dataframe": None}
    
    # Summary report
    print(f"\n{'='*60}")
    print("VALIDATION SUMMARY")
    print(f"{'='*60}")
    
    successful = sum(1 for result in validation_results.values() if result["success"])
    total = len(datasets)
    
    print(f"✓ Successfully validated: {successful}/{total} datasets")
    
    if successful == total:
        print("🎉 All datasets are ready for GIS integration!")
    else:
        print("⚠️  Some datasets need attention before proceeding")
    
    return validation_results

if __name__ == "__main__":
    validation_results = main()
