import ee
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim

def check_dataset_exists(dataset_id):
    """Check if a dataset exists in Earth Engine"""
    try:
        ee.ImageCollection(dataset_id).first().getInfo()
        return True
    except Exception as e:
        print(f"Dataset {dataset_id} not found or not accessible: {e}")
        return False

def initialize_earth_engine():
    """Initialize and authenticate Earth Engine"""
    try:
        # Initialize with project name
        ee.Initialize(project='pm2-5-predictor')
        print("Earth Engine already authenticated!")
    except Exception as e:
        if "no project found" in str(e):
            print("Authenticating Earth Engine...")
            ee.Authenticate()
            ee.Initialize(project='pm2-5-predictor')
            print("Earth Engine authenticated successfully!")
        else:
            print(f"Error during initialization: {e}")
            raise

def extract_data(lat, lon):
    """Extract data from multiple datasets for a specific location"""
    point = ee.Geometry.Point([lon, lat])
    
    # Define dataset IDs
    datasets = {
        'MODIS': 'MODIS/061/MOD08_M3'  # Updated to version 6.1
    }
    
    print("\nChecking dataset availability:")
    for name, dataset_id in datasets.items():
        exists = check_dataset_exists(dataset_id)
        print(f"{name}: {'Available' if exists else 'Not available'} ({dataset_id})")
    
    try:
        # MODIS Terra Monthly Global Product
        modis = ee.ImageCollection('MODIS/061/MOD08_M3')
        
        # Filter for specific date (2020-06-01)
        start_date = '2020-06-01'
        end_date = '2020-06-03'  # Using a 3-day window to ensure we get data
        modis = modis.filterDate(start_date, end_date)
        modis_img = modis.first()  # Get the first image in this date range
        
        if modis_img is None:
            print(f"No data available for Mumbai on {start_date}")
            return
            
        # Get the date of the data
        modis_date = ee.Date(modis_img.get('system:time_start')).format('YYYY-MM-dd').getInfo()
        print(f"\nData for Mumbai ({lat}°N, {lon}°E) on {modis_date}:")
        
        # Get only the three specific bands we need using correct band names
        modis_bands = [
            'Aerosol_Optical_Depth_Land_Ocean_Mean_Mean',  # AOD
            'Atmospheric_Water_Vapor_Mean_Mean',  # Water Vapor
            'Retrieved_Temperature_Profile_Mean_Mean_1000'  # Surface temperature
        ]
        
        # Sample the data with a larger scale to ensure we get values
        modis_data = modis_img.select(modis_bands).sample(
            region=point,
            scale=100000,  # 100km scale
            dropNulls=True  # Drop null values
        ).first()
        
        if modis_data is None:
            print("No data available for this location. Try a different location or time period.")
            return
            
        modis_info = modis_data.getInfo()
        if not modis_info or 'properties' not in modis_info:
            print("No valid data properties found for this location.")
            return
            
        properties = modis_info['properties']
        
        # Print values with error checking
        aod = properties.get('Aerosol_Optical_Depth_Land_Ocean_Mean_Mean', 'No data')
        temp = properties.get('Retrieved_Temperature_Profile_Mean_Mean_1000', 'No data')
        water_vapor = properties.get('Atmospheric_Water_Vapor_Mean_Mean', 'No data')
        
        print(f"AOD: {aod}")
        print(f"Air Temperature: {temp} Kelvin")
        print(f"Water Vapor: {water_vapor} cm")
        
    except Exception as e:
        print(f"Error during data extraction: {str(e)}")
        print("This might be due to:")
        print("1. No data available for this location")
        print("2. Cloud cover in the area")
        print("3. Data processing issues")
        print("\nTry:")
        print("- Using a different location")
        print("- Using a different time period")
        print("- Increasing the scale parameter")

if __name__ == "__main__":
    initialize_earth_engine()
    
    geolocator = Nominatim(user_agent="city_modis_lookup")
    city = input("Enter the city name: ").strip()
    location = geolocator.geocode(city)
    if not location:
        print(f"Could not find coordinates for '{city}'. Please check the city name and try again.")
    else:
        lat, lon = location.latitude, location.longitude
        print(f"\nExtracting data for {city} coordinates: {lat}°N, {lon}°E")
        print("Please wait while data is being extracted...")
        try:
            extract_data(lat, lon)
        except Exception as e:
            print(f"Error extracting data for {city}: {e}")
