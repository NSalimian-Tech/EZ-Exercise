import folium
import webbrowser
import math

class Place:
    def __init__(self, name, latitude, longitude):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
    
    def get_info(self):
        return f"{self.name} ({self.latitude}, {self.longitude})"
    
    def distance_to(self, other_place):
        lat_diff = self.latitude - other_place.latitude
        lon_diff = self.longitude - other_place.longitude
        distance_km = math.sqrt(lat_diff**2 + lon_diff**2) * 111
        return round(distance_km, 2)
    
    def get_marker_color(self):
        return "blue"
    
    def get_popup_text(self):
        return f"<b>{self.name}</b><br>Click for more info!"

class Restaurant(Place):
    def __init__(self, name, latitude, longitude, food_type):
        super().__init__(name, latitude, longitude)
        self.food_type = food_type
    
    def get_popup_text(self):
        return f"<b>RESTAURANT: {self.name}</b><br>Food: {self.food_type}"
    
    def get_marker_color(self):
        return "red"

class Park(Place):
    def __init__(self, name, latitude, longitude, has_playground):
        super().__init__(name, latitude, longitude)
        self.has_playground = has_playground
    
    def get_popup_text(self):
        status = "Yes" if self.has_playground else "No"
        return f"<b>PARK: {self.name}</b><br>Playground: {status}"
    
    def get_marker_color(self):
        return "green"

class Museum(Place):
    def __init__(self, name, latitude, longitude, entry_fee):
        super().__init__(name, latitude, longitude)
        self.entry_fee = entry_fee
    
    def get_popup_text(self):
        return f"<b>MUSEUM: {self.name}</b><br>Entry: €{self.entry_fee}"
    
    def get_marker_color(self):
        return "purple"

class MyMap:
    def __init__(self, city, zoom=12):
        self.city = city
        self.places = []
        centers = {
            "Paris": [48.8566, 2.3522],
            "London": [51.5074, -0.1278],
            "New York": [40.7128, -74.0060],
            "Tokyo": [35.6762, 139.6503]
        }
        center = centers.get(city, [0, 0])
        self.map = folium.Map(location=center, zoom_start=zoom)
    
    def add_place(self, place):
        self.places.append(place)
        folium.Marker(
            location=[place.latitude, place.longitude],
            popup=place.get_popup_text(),
            tooltip=place.name,
            icon=folium.Icon(color=place.get_marker_color())
        ).add_to(self.map)
    
    def show_distances(self):
        if len(self.places) < 2: return
        print(f"\n📏 Distances in {self.city}:")
        for i in range(len(self.places)):
            for j in range(i+1, len(self.places)):
                dist = self.places[i].distance_to(self.places[j])
                print(f"  {self.places[i].name} -> {self.places[j].name}: {dist} km")

    def save(self, filename="my_map.html"):
        self.map.save(filename)
        return filename

def main():
    my_city = "Paris" 
    mymap = MyMap(my_city)
    
    places = [
        Museum("Louvre Museum", 48.8606, 2.3376, 17),
        Restaurant("Cafe Paris", 48.8566, 2.3522, "French"),
        Park("Luxembourg Garden", 48.8462, 2.3372, True),
        Place("Eiffel Tower", 48.8584, 2.2945)
    ]
    
    for p in places:
        mymap.add_place(p)
    
    mymap.show_distances()
    filename = mymap.save("my_favorite_places.html")
    webbrowser.open(filename)

if __name__ == "__main__":
    main()