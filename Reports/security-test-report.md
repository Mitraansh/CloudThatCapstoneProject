# Security Test Report

## Scope
- Authentication and token validation.
- Image upload content-type and size validation.
- Database access via parameterized queries.
- Chatbot route access control.

## Findings
- Signup and login use password hashing.
- Protected endpoints require a bearer token.
- Upload only accepts JPEG/PNG and enforces a 2 MB limit.
- No database write access from chat queries.

## Residual Risks
- The token is HMAC-based and not rotated.
- The OpenRouter API key must not be committed.
