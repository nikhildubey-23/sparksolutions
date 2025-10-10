- [x] Modify base.html to change Docs nav item to dropdown with Python and HTML options
- [x] Add /python and /html routes in app.py
- [x] Create templates/python.html with Python content, highlighting, search, and copy scripts
- [x] Create templates/html.html with HTML content, highlighting, search, and copy scripts
- [x] Modify templates/docs.html to remove sidebar and content sections

## Make previous_work.html Responsive
- [ ] Enhance existing @media (max-width: 768px) in static/css/main.css: Stack hero stats vertically, adjust fonts/padding for hero, filter nav, and project cards
- [ ] Add new @media (max-width: 480px) in static/css/main.css: Further reduce sizes for very small mobile screens
- [ ] Add @media (min-width: 769px) and (max-width: 1024px) in static/css/main.css: Tablet-specific adjustments
- [ ] Test changes: Run server if needed, use browser to verify mobile responsiveness, update TODO.md with completion

## Contact Page Fixes
- [x] Update templates/contact.html: Add mailto link for email, tel links for phones (remove trailing period), add class="single-line" to email <p>
- [x] Update static/css/main.css: Add .single-line { white-space: nowrap; }
- [x] Test changes on contact page
- [x] Mark as complete

## Fix Email Overflow on Mobile in Contact Page
- [x] Update static/css/main.css: Add @media (max-width: 768px) { .contact-page .single-line { white-space: normal; word-break: break-word; } }
- [ ] Test on mobile: Refresh page, check in browser dev tools or device at <768px width to ensure email wraps without overflow
- [ ] Update TODO.md to mark complete
