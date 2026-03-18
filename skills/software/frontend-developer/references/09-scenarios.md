# Scenario Examples

## 9.1 API Design Decision

**User:** "Design an API for user management"

**Expert:**
> **RESTful Design:**
> 
> **Endpoints:**
> ```
> GET    /users          # List users
> POST   /users          # Create user
> GET    /users/{id}     # Get user
> PATCH  /users/{id}      # Update user
> DELETE /users/{id}      # Delete user
> ```
> 
> **Response Format:**
> ```json
> {
>   "data": { "id": 1, "name": "John" },
>   "meta": { "timestamp": "2024-01-01T00:00:00Z" }
> }
> ```
> 
> **Error Handling:**
> - 400: Validation errors
> - 401: Authentication required
> - 403: Permission denied
> - 404: Resource not found
