# TODO: Replace CSV with SQLAlchemy for Practice Results

## Steps to Complete

- [x] Add SQLAlchemy imports and setup in app.py
- [x] Define PracticeResult model with id, name, mobile, email, marks
- [x] Update /submit-practice route to save to DB instead of CSV
- [x] Update /admin route to query, sort, and filter from DB
- [x] Update /delete/<int:index> to /delete/<int:id> and delete by id
- [x] Ensure DB is created on app startup
- [x] Test /submit-practice for saving
- [x] Test /admin for loading, sorting, filtering
- [x] Test /delete/<id> for deletion
- [x] Verify no CSV file is used anymore
- [x] Update practice.html with student details form
- [x] Create admin panel templates
