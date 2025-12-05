# Data Model: Physical AI & Humanoid Robotics — User Personalization

## Entity: UserProfile

This entity stores information about a user for content personalization and authentication with Better Auth. It will be stored in a Neon Postgres database.

### Attributes:

*   **`id`**: (Primary Key) Unique identifier for the user. (UUID)
*   **`email`**: User's email address. (String, Unique, Required)
*   **`username`**: User's chosen username. (String, Unique, Optional)
*   **`password_hash`**: Hashed password for authentication. (String, Required)
*   **`skill_level`**: User's declared skill level (e.g., "beginner", "intermediate", "advanced"). Used for personalizing content depth. (String, Enum, Optional)
*   **`preferred_language`**: User's preferred language for content (e.g., "en", "ur"). Used for the translation toggle. (String, Optional, Default: "en")
*   **`learning_preferences`**: JSONB field to store more granular learning preferences (e.g., preferred topics, learning style). (JSONB, Optional)
*   **`created_at`**: Timestamp of user creation. (DateTime, Required)
*   **`updated_at`**: Timestamp of last profile update. (DateTime, Required)

### Relationships:

*   No direct relationships to other entities are defined at this stage, as content is static (generated). Future enhancements could link to user progress or bookmark data.

### Validation Rules:

*   `email` must be a valid email format.
*   `password_hash` must be present for authenticated users.
*   `skill_level` must be one of the predefined enum values.

