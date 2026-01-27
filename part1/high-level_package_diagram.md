```mermaid
classDiagram
direction TB

class PresentationLayer {
  <<Interface>>
  +UsersAPI()
  +PlacesAPI()
  +ReviewsAPI()
  +AmenitiesAPI()
}

class HBnBFacade {
  <<Facade>>
  +create_user()
  +update_user()
  +create_place()
  +create_review()
  +add_amenity_to_place()
}

class BusinessLogicLayer {
  +User
  +Place
  +Review
  +Amenity
}

class PersistenceLayer {
  +UserRepository
  +PlaceRepository
  +ReviewRepository
  +AmenityRepository
  +DatabaseAccess
}

PresentationLayer --> HBnBFacade : Facade Pattern
HBnBFacade --> BusinessLogicLayer : Business Rules
BusinessLogicLayer --> PersistenceLayer : Database Operations