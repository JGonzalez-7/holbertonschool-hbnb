# Sequence Diagrams for API Calls

This document contains four sequence diagrams showing how the HBnB layers interact:
- **Presentation Layer** (API / Services)
- **Business Logic Layer** (Facade / Models)
- **Persistence Layer** (Repositories / Database)

---

## 1) User Registration

```mermaid
sequenceDiagram
autonumber
actor Client
participant API as Presentation: UsersAPI
participant Facade as Business: HBnBFacade
participant Repo as Persistence: UserRepository
participant DB as Database

Client->>API: POST /users (first_name,last_name,email,password)
API->>API: Validate request data
API->>Facade: register_user(user_data)

Facade->>Repo: get_by_email(email)
Repo->>DB: SELECT user WHERE email=...
DB-->>Repo: result (none)
Repo-->>Facade: None

Facade->>Facade: Create User entity + apply rules
Facade->>Repo: save(user)
Repo->>DB: INSERT user
DB-->>Repo: ok + id
Repo-->>Facade: saved user

Facade-->>API: 201 Created (user DTO)
API-->>Client: 201 Created (id, first_name, last_name, email)