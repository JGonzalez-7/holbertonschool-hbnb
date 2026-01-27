# HBnB – Technical Documentation

## 1. Introduction

This document provides a comprehensive technical overview of the **HBnB** application.
It compiles the architectural diagrams and explanatory notes created in previous tasks
and serves as a **blueprint for implementation**.

The purpose of this document is to:
- Describe the overall system architecture
- Explain the responsibilities of each layer
- Clarify how core entities interact
- Illustrate how API requests flow through the system

This documentation will be used as a reference throughout development to ensure
consistency, correctness, and alignment with the intended design.

---

## 2. High-Level Architecture

### Purpose
This section presents the **three-layer architecture** of the HBnB application and
illustrates how layers communicate using the **Facade pattern**.

### Diagram – High-Level Package Diagram

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