from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable

def get_city_coordinates(city_name):
    try:
        geolocator = Nominatim(user_agent="my_geocoder")
        location = geolocator.geocode(city_name)
        
        if location:
            return (location.latitude, location.longitude)
        else:
            print(f"Could not find coordinates for {city_name}")
            return None
            
    except (GeocoderTimedOut, GeocoderUnavailable) as e:
        print(f"Error occurred while geocoding: {str(e)}")
        return None

def main():
    city_name = input("Enter a city name: ")
    coordinates = get_city_coordinates(city_name)
    
    if coordinates:
        latitude, longitude = coordinates
        print(f"\nCoordinates for {city_name}:")
        print(f"Latitude: {latitude}")
        print(f"Longitude: {longitude}")



if __name__ == "__main__":
    main()
