# Class Diagram for Business Logic Layer

```mermaid
classDiagram
direction TB

class BaseModel {
  +UUID id
  +datetime created_at
  +datetime updated_at
  +save()
  +update(data)
}

class User {
  +string first_name
  +string last_name
  +string email
  +string password
  +bool is_admin
  +update_profile(first_name, last_name, email, password)
  +add_place(place)
  +add_review(review)
}

class Place {
  +string name
  +string description
  +float price
  +float latitude
  +float longitude
  +UUID owner_id
  +add_amenity(amenity)
  +remove_amenity(amenity)
  +add_review(review)
  +average_rating() float
}

class Review {
  +int rating
  +string comment
  +UUID user_id
  +UUID place_id
  +edit(rating, comment)
}

class Amenity {
  +string name
  +rename(name)
}

%% Inheritance (common base fields)
BaseModel <|-- User
BaseModel <|-- Place
BaseModel <|-- Review
BaseModel <|-- Amenity

%% Relationships + multiplicity
User "1" --> "0..*" Place : owns
Place "1" --> "0..*" Review : has
User "1" --> "0..*" Review : writes

%% Many-to-many (place amenities)
Place "0..*" -- "0..*" Amenity : includes