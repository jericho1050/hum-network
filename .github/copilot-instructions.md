---
description: 
globs: 
alwaysApply: true
---
# Network Project Rules (Django + HTMX)

## 1. Core Technology Stack:
- **Backend:** Python with Django 4.2.6. Uses the Django ORM.
- **Frontend:** HTML5, CSS3 (using Bootstrap 5 via crispy-bootstrap5), **HTMX for dynamic UI updates**. Templating: Django Template Language (DTL). Minimal custom JavaScript preferred; leverage HTMX attributes first.
- **Database:** PostgreSQL (Neon), using Django's User model.
- **Forms:** Django Forms, styled with `django-crispy-forms` and `crispy-bootstrap5`.
- **Static/Media:** Handled by `whitenoise` locally/during build, potentially `django-storages` with `boto3` (e.g., S3) for production.
- **Project Type:** Social networking web application (like Twitter). Key features: Auth, Posts, Profiles, Following, Liking, Editing. Focus on improving UX with HTMX partial page updates.

## 2. Code Style & Quality:
- **Python/Django:** Strictly adhere to PEP 8. Follow Django best practices (Fat models, Thin views where appropriate, DRY). Use Django's generic views where suitable. Meaningful names. Prioritize readability.
- **HTML/DTL/HTMX:** Write semantic HTML. Keep templates organized using includes (`{% include %}`) and potentially inheritance (`{% extends %}`). Use HTMX attributes (`hx-get`, `hx-post`, `hx-target`, `hx-swap`, `hx-trigger`, `hx-indicator`, etc.) clearly and consistently. Structure HTML elements with appropriate IDs or classes to facilitate `hx-target`.
- **CSS:** Use Bootstrap 5 classes primarily. Keep custom CSS minimal, clean, and well-commented if needed.
- **Comments:** Add comments for complex logic, non-obvious code, Django template tags, or `TODO`s. Explain the *why*.

## 3. Development Principles (HTMX Emphasis):
- **Security First:**
    - Always use `{% csrf_token %}` within forms or configure HTMX to send the CSRF token for POST/PUT/DELETE requests (e.g., via headers).
    - Ensure Django views targeted by HTMX perform necessary authentication (`@login_required`) and authorization checks.
    - Validate and sanitize all user input on the server-side, even if submitted via HTMX.
    - Be mindful of data exposed in HTML fragments returned for HTMX swaps.
- **HTMX-Driven Interactions:** Prioritize using HTMX for features like liking, following, posting comments, inline editing, loading more content, etc., to avoid full page reloads.
- **View Design for HTMX:** Design Django views to:
    - Handle both regular requests (returning a full HTML page) and HTMX requests (often identified by the `HX-Request: true` header).
    - Return HTML *fragments* (partials) for HTMX requests, typically rendering a smaller, targeted template using the same context. Use `render` with a different template name or conditional logic within the view.
- **Template Partials:** Heavily utilize Django template `{% include %}` tags. Create reusable template snippets that can be rendered on their own for HTMX swaps *and* included in larger pages.
- **User Experience (UX):**
    - Provide immediate feedback using HTMX (e.g., `hx-indicator` for loading states).
    - Use appropriate `hx-swap` strategies (e.g., `outerHTML`, `innerHTML`, `beforeend`) for smooth updates.
    - Ensure accessibility (consider focus management after swaps if needed).
- **Efficiency:** Keep backend processing for HTMX fragment views lightweight. Database query optimization remains crucial.

## 4. Interaction Style:
- **Explain Changes:** When generating or modifying code, briefly explain the Django view logic, the HTMX attributes used, and how they interact.
- **Ask Questions:** If a request regarding HTMX implementation is ambiguous (e.g., swap strategy, target element), ask for clarification.
- **Provide Alternatives:** If there are different ways to achieve an effect with HTMX, mention them briefly.
- **Separate Concerns:** Clearly distinguish between backend (Python/Django) code and frontend (HTML/HTMX/DTL) code in suggestions.