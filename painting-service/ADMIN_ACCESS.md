# Admin Access Instructions

## How to Access Admin Panel

1. **Use the secure URL:**
   ```
   http://localhost:5000/secure-admin-access/color-craft-admin-2024
   ```

2. **Login credentials:**
   - Username: `admin`
   - Password: `admin123`

3. **Access Flow:**
   - Visit secure URL → Redirected to login → Enter credentials → Access dashboard

## Security Features

- ✅ All admin routes protected
- ✅ Direct URL access blocked
- ✅ Secret access key required
- ✅ Session timeout (4 hours)
- ✅ CSRF protection

## Emergency Access

If you get locked out:
1. Restart the Flask application
2. Check the secure access URL is correct
3. Clear browser cookies if needed