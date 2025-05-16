import ee

# Trigger the authentication flow (you might need to do this again if it wasn't fully completed)
try:
    ee.Initialize()
except ee.EEException as e:
    if "no project found" in str(e):
        print("It seems you need to authenticate and/or provide a project.")
        print("Let's try the authentication again.")
        ee.Authenticate()
        # After successful authentication, you should be able to initialize,
        # but it's still good practice to include the project ID.

# Replace 'YOUR_CLOUD_PROJECT_ID' with your actual Google Cloud Project ID
project_id = 'YOUR_CLOUD_PROJECT_ID'

try:
    ee.Initialize(project=project_id)
    print(f"Earth Engine API initialized successfully with project: {project_id}")
except ee.EEException as e:
    print(f"Error initializing Earth Engine with project: {e}")