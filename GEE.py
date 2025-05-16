import ee
# import geemap

# Force re-authentication by clearing any existing credentials
try:
    ee.Reset()
except:
    pass

# Authenticate Earth Engine
try:
    ee.Authenticate()
    ee.Initialize()
    print("Earth Engine authenticated successfully!")
except Exception as e:
    print(f"Authentication error: {e}")
    print("Please make sure you have:")
    print("1. A Google account with Earth Engine access")
    print("2. The earthengine-api package installed (pip install earthengine-api)")
    print("3. A stable internet connection")
    exit(1)

# Set your project
try:
    ee.Project.setProject('pm2-5-predictor')
    print(f"Project set to: {ee.Project.getProject()}")
except Exception as e:
    print(f"Error setting project: {e}")
    exit(1)

# Test the connection
try:
    # Get a simple dataset to test the connection
    dataset = ee.ImageCollection('COPERNICUS/S5P/OFFL/L3_NO2').first()
    print("Successfully connected to Earth Engine!")
except Exception as e:
    print(f"Error connecting to Earth Engine: {e}")
    exit(1)
