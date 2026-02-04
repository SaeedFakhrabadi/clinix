# Clinix Backend - Complete API Documentation

## 🚀 Quick Start

```shell
# Navigate to the backend directory
cd back-end/

# Create and activate virtual environment
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux (or git bash):
source venv/bin/activate

# Install requirements from custom PyPI repository
pip install -r requirements.txt --no-cache-dir

## or install with runflare mirror
pip install -r requirements.txt -i https://mirror-pypi.runflare.com/simple --no-cache-dir

## or install with iranserver's pypi nexus mirror
pip install -r requirements.txt -i https://nexus.iranserver.dev/repository/pypi-proxy/simple --no-cache-dir

# Run the Django development server
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to access the API.

---

# 🔐 AUTHENTICATION ENDPOINTS

## 1️⃣ **Register User**
### `POST /api/v1/auth/register/`

**Public endpoint** - No authentication required

#### Request Body
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "password": "StrongPass123!",
  "password2": "StrongPass123!"
}
```

#### Success Response (201 CREATED)
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 3,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "is_active": true,
    "date_joined": "2026-02-04T12:00:00Z"
  },
  "refresh": "<REFRESH_TOKEN>",
  "access": "<ACCESS_TOKEN>"
}
```

#### Error Responses
**400 Bad Request** - Email already exists
```json
{
  "email": ["Email already exists."]
}
```

**400 Bad Request** - Passwords don't match
```json
{
  "password": ["Password fields didn't match."]
}
```

#### cURL Example
```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "password": "StrongPass123!",
    "password2": "StrongPass123!"
  }'
```

---

## 2️⃣ **Login User**
### `POST /api/v1/auth/login/`

**Public endpoint** - No authentication required

#### Request Body
```json
{
  "username": "johndoe",
  "password": "StrongPass123!"
}
```

#### Success Response (200 OK)
```json
{
  "message": "Login successful",
  "user": {
    "id": 3,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "is_active": true,
    "date_joined": "2026-02-04T12:00:00Z"
  },
  "refresh": "<REFRESH_TOKEN>",
  "access": "<ACCESS_TOKEN>"
}
```

#### Error Responses
**401 Unauthorized** - Invalid credentials
```json
{
  "error": "Invalid credentials"
}
```

#### cURL Example
```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "StrongPass123!"
  }'
```

---

## 3️⃣ **Logout User**
### `POST /api/v1/auth/logout/`

🔒 **Requires authentication**

#### Headers
```
Authorization: Bearer <ACCESS_TOKEN>
Content-Type: application/json
```

#### Request Body
```json
{
  "refresh": "<REFRESH_TOKEN>"
}
```

#### Success Response (200 OK)
```json
{
  "message": "Logout successful"
}
```

#### Error Responses
**400 Bad Request** - Token blacklisted
```json
{
  "error": "Token is blacklisted"
}
```

#### cURL Example
```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/logout/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "<REFRESH_TOKEN>"
  }'
```

---

## 4️⃣ **Refresh Access Token**
### `POST /api/v1/auth/token/refresh/`

**Public endpoint** - Requires valid refresh token

#### Request Body
```json
{
  "refresh": "<REFRESH_TOKEN>"
}
```

#### Success Response (200 OK)
```json
{
  "access": "<NEW_ACCESS_TOKEN>"
}
```

#### Error Responses
**401 Unauthorized** - Invalid or expired token
```json
{
  "detail": "Token is invalid or expired",
  "code": "token_not_valid"
}
```

#### cURL Example
```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "<REFRESH_TOKEN>"
  }'
```

---

## 5️⃣ **Verify Token**
### `POST /api/v1/auth/token/verify/`

**Public endpoint** - Verifies access token validity

#### Request Body
```json
{
  "token": "<ACCESS_TOKEN>"
}
```

#### Success Response (200 OK)
```json
{}
```

#### Error Responses
**401 Unauthorized** - Invalid or expired token
```json
{
  "detail": "Token is invalid or expired",
  "code": "token_not_valid"
}
```

#### cURL Example
```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/token/verify/ \
  -H "Content-Type: application/json" \
  -d '{
    "token": "<ACCESS_TOKEN>"
  }'
```

---

## 6️⃣ **Forgot Password**
### `POST /api/v1/auth/forgot_password/`

**Public endpoint** - No authentication required

#### Request Body
```json
{
  "email": "user@example.com"
}
```

#### Success Response (200 OK)
```json
{
  "message": "Password reset email sent",
  "reset_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

> ⚠️ **Note**: In production, `reset_id` should not be returned. This is only for testing purposes.

#### Error Responses
**400 Bad Request** - Email doesn't exist
```json
{
  "email": ["No user with this email exists."]
}
```

**404 Not Found** - User not found
```json
{
  "error": "User with this email does not exist"
}
```

#### cURL Example
```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/forgot_password/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com"
  }'
```

---

## 7️⃣ **Reset Password**
### `POST /api/v1/auth/reset_password/`

**Public endpoint** - Requires valid reset ID

#### Request Body
```json
{
  "reset_id": "550e8400-e29b-41d4-a716-446655440000",
  "password": "NewStrongPass123!",
  "password2": "NewStrongPass123!"
}
```

#### Success Response (200 OK)
```json
{
  "message": "Password reset successfully"
}
```

#### Error Responses
**400 Bad Request** - Passwords don't match
```json
{
  "password": ["Password fields didn't match."]
}
```

**400 Bad Request** - Invalid reset ID
```json
{
  "reset_id": ["Invalid reset ID."]
}
```

**404 Not Found** - Invalid reset ID
```json
{
  "error": "Invalid reset ID"
}
```

**400 Bad Request** - Reset link expired
```json
{
  "error": "Reset link has expired"
}
```

#### cURL Example
```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/reset_password/ \
  -H "Content-Type: application/json" \
  -d '{
    "reset_id": "550e8400-e29b-41d4-a716-446655440000",
    "password": "NewStrongPass123!",
    "password2": "NewStrongPass123!"
  }'
```

---

# 👤 USER MANAGEMENT ENDPOINTS

## 8️⃣ **List All Users**
### `GET /api/v1/users/`

🔒 **Requires authentication** - Any authenticated user

#### Headers
```
Authorization: Bearer <ACCESS_TOKEN>
```

#### Success Response (200 OK)
```json
[
  {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "first_name": "Admin",
    "last_name": "User",
    "is_active": true,
    "date_joined": "2025-01-01T12:00:00Z"
  },
  {
    "id": 3,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "is_active": true,
    "date_joined": "2026-02-04T12:00:00Z"
  }
]
```

#### cURL Example
```bash
curl -X GET http://127.0.0.1:8000/api/v1/users/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

---

## 9️⃣ **Get User Details**
### `GET /api/v1/users/{id}/`

🔒 **Requires authentication** - Any authenticated user

#### Success Response (200 OK)
```json
{
  "id": 3,
  "username": "johndoe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "is_active": true,
  "date_joined": "2026-02-04T12:00:00Z"
}
```

#### Error Responses
**404 Not Found** - User doesn't exist
```json
{
  "detail": "Not found."
}
```

#### cURL Example
```bash
curl -X GET http://127.0.0.1:8000/api/v1/users/3/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

---

## 🔟 **Create User (Admin Only)**
### `POST /api/v1/users/`

🔒 **Requires admin privileges**

#### Error Responses
**403 Forbidden** - Non-admin user
```json
{
  "detail": "You do not have permission to perform this action."
}
```

---

## 1️⃣1️⃣ **Update/Delete User (Admin Only)**
### `PUT / PATCH / DELETE /api/v1/users/{id}/`

🔒 **Requires admin privileges**

* ✅ Admin → Allowed
* ❌ Normal user → 403 Forbidden

---

# 🏠 MISC ENDPOINTS

## 1️⃣2️⃣ **API Root**
### `GET /api/v1/`

**Public endpoint** - No authentication required

#### Success Response (200 OK)
```json
{
  "auth": "http://127.0.0.1:8000/api/v1/auth/",
  "users": "http://127.0.0.1:8000/api/v1/users/"
}
```

#### cURL Example
```bash
curl -X GET http://127.0.0.1:8000/api/v1/
```

---

## 1️⃣3️⃣ **Home/Protected Endpoint**
### `GET /api/v1/home/`

🔒 **Requires authentication** - Any authenticated user

#### Success Response (200 OK)
```json
{
  "message": "Welcome johndoe",
  "user": {
    "id": 3,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "is_active": true,
    "date_joined": "2026-02-04T12:00:00Z"
  }
}
```

#### cURL Example
```bash
curl -X GET http://127.0.0.1:8000/api/v1/home/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

---

# 🛠️ ADMIN PANEL

## Django Admin Interface
### `GET /admin/`

**Session-based authentication** - Not JWT-based

### Setup
1. Create a superuser:
```bash
python manage.py createsuperuser
```

2. Visit: `http://127.0.0.1:8000/admin/`

3. Login with username/password (session authentication)

> ⚠️ **Note**: JWT tokens do not work with Django Admin. Use session-based login.

---

# ⚠️ IMPORTANT NOTES & GOTCHAS

## Security Considerations

### 1. **Reset ID Exposure**
- **Development/Testing**: `reset_id` is returned in the response
- **Production**: Should only return `{"message": "Password reset email sent"}`

### 2. **Duplicate Validations**
- Reset ID is validated in both serializer and view
- Email existence is checked twice (serializer and view)
- **Recommendation**: Consolidate validation logic in serializers

### 3. **Token Management**
- Always store refresh tokens securely
- Implement token blacklisting for enhanced security
- Set appropriate token expiration times

## Error Handling Patterns

### 400 vs 404 Errors
- **400 Bad Request**: Validation errors (passwords don't match, invalid format)
- **404 Not Found**: Resource doesn't exist (user not found, invalid reset ID)

### Authentication Errors
- **401 Unauthorized**: Invalid/missing credentials
- **403 Forbidden**: Insufficient permissions

## Best Practices

### 1. **Rate Limiting**
Consider implementing rate limiting for:
- Login attempts
- Password reset requests
- Registration endpoints

### 2. **Password Security**
- Minimum 8 characters
- Require mix of uppercase, lowercase, numbers, and symbols
- Implement password strength validation

### 3. **Email Configuration**
For production:
- Use environment variables for email credentials
- Implement email queueing for password reset emails
- Set up email templates

### 4. **Token Expiry**
Recommended settings:
- Access token: 15-30 minutes
- Refresh token: 7 days
- Password reset link: 10-15 minutes

---

# 🧪 TESTING THE API

## Complete Authentication Flow Example

```bash
# 1. Register a new user
curl -X POST http://127.0.0.1:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "first_name": "Test",
    "last_name": "User",
    "password": "TestPass123!",
    "password2": "TestPass123!"
  }'

# 2. Login with the new user
curl -X POST http://127.0.0.1:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "TestPass123!"
  }'

# 3. Access protected endpoint
curl -X GET http://127.0.0.1:8000/api/v1/home/ \
  -H "Authorization: Bearer <ACCESS_TOKEN_FROM_STEP_2>"

# 4. List all users
curl -X GET http://127.0.0.1:8000/api/v1/users/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"

# 5. Refresh token when expired
curl -X POST http://127.0.0.1:8000/api/v1/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "<REFRESH_TOKEN_FROM_STEP_2>"
  }'

# 6. Logout
curl -X POST http://127.0.0.1:8000/api/v1/auth/logout/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "<REFRESH_TOKEN>"
  }'
```

## Password Reset Flow Example

```bash
# 1. Request password reset
curl -X POST http://127.0.0.1:8000/api/v1/auth/forgot_password/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com"
  }'

# 2. Reset password (using reset_id from response or email)
curl -X POST http://127.0.0.1:8000/api/v1/auth/reset_password/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser2",
    "password": "StrongPass123!",
    "password2": "StrongPass123!",
    "reset_id": "12a7601b-5977-4643-92e0-3a5a6f5cf22e"
  }'
```

---

# 📁 PROJECT STRUCTURE

```
clinix-backend/
├── back-end/
│   ├── venv/                    # Virtual environment
│   ├── requirements.txt         # Dependencies
│   ├── manage.py               # Django management script
│   ├── clinix/                 # Main project directory
│   │   ├── __init__.py
│   │   ├── settings.py         # Project settings
│   │   ├── urls.py            # Main URL routing
│   │   └── wsgi.py
│   ├── core/                   # Main app
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py          # Database models
│   │   ├── serializers.py     # API serializers
│   │   ├── views.py           # API views
│   │   ├── urls.py            # App URL routing
│   │   └── permissions.py     # Custom permissions
│   ├── static/                # Static files
│   ├── templates/             # HTML templates
│   └── db.sqlite3             # Database (development)
├── README.md                  # This documentation
└── .env.example              # Environment variables template
```

---

# 🚨 TROUBLESHOOTING

## Common Issues

### 1. **Virtual Environment Issues**
```bash
# If activation fails on Windows
.\venv\Scripts\activate

# If python command not found
python3 -m venv venv
source venv/bin/activate
```

### 2. **Package Installation Issues**
```bash
# If custom repository fails, try without it
pip install -r requirements.txt

# Or use default PyPI
pip install -r requirements.txt -i https://pypi.org/simple
```

### 3. **Database Migration Issues**
```bash
# Reset migrations (development only)
python manage.py migrate --fake core zero
python manage.py makemigrations
python manage.py migrate
```

### 4. **Port Already in Use**
```bash
# Kill process on port 8000
# Linux/Mac:
sudo lsof -t -i tcp:8000 | xargs kill -9

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or use a different port
python manage.py runserver 8001
```

---

# 📞 SUPPORT

For issues, questions, or contributions:

1. Check the troubleshooting section above
2. Verify all environment variables are set
3. Ensure all dependencies are installed
4. Check Django logs: `python manage.py runserver --verbosity 2`

---

**Clinix Backend** - A comprehensive Django REST Framework authentication system with JWT support, password reset functionality, and user management.