# queries.py

# User queries (assuming these already exist)
USER_INSERT = "INSERT INTO \"User\" (name, email, role) VALUES (%s, %s, %s) RETURNING user_id"
USER_SELECT_ALL = "SELECT user_id, name, email, role FROM \"User\""
USER_SELECT_BY_ID = "SELECT user_id, name, email, role FROM \"User\" WHERE user_id = %s"
USER_UPDATE = "UPDATE \"User\" SET name = %s, email = %s, role = %s WHERE user_id = %s"
USER_DELETE = "DELETE FROM \"User\" WHERE user_id = %s"

# Course queries (assuming these already exist)
COURSE_INSERT = "INSERT INTO \"Course\" (title, instructor_id, description, price) VALUES (%s, %s, %s, %s) RETURNING course_id"
COURSE_SELECT_ALL = "SELECT course_id, title, instructor_id, description, price FROM \"Course\""
COURSE_SELECT_BY_ID = "SELECT course_id, title, instructor_id, description, price FROM \"Course\" WHERE course_id = %s"
COURSE_UPDATE = "UPDATE \"Course\" SET title = %s, description = %s, price = %s WHERE course_id = %s"
COURSE_DELETE = "DELETE FROM \"Course\" WHERE course_id = %s"

# Enrollment queries
ENROLLMENT_INSERT = "INSERT INTO \"Enrollment\" (user_id, course_id) VALUES (%s, %s) RETURNING enrollment_id"
ENROLLMENT_SELECT_ALL = "SELECT enrollment_id, user_id, course_id FROM \"Enrollment\""
ENROLLMENT_SELECT_BY_ID = "SELECT enrollment_id, user_id, course_id FROM \"Enrollment\" WHERE enrollment_id = %s"
ENROLLMENT_UPDATE = "UPDATE \"Enrollment\" SET user_id = %s, course_id = %s WHERE enrollment_id = %s"
ENROLLMENT_DELETE = "DELETE FROM \"Enrollment\" WHERE enrollment_id = %s"

# Transaction queries
TRANSACTION_INSERT = "INSERT INTO \"Transaction\" (user_id, course_id, amount) VALUES (%s, %s, %s) RETURNING transaction_id"
TRANSACTION_SELECT_ALL = "SELECT transaction_id, user_id, course_id, amount FROM \"Transaction\""
TRANSACTION_SELECT_BY_ID = "SELECT transaction_id, user_id, course_id, amount FROM \"Transaction\" WHERE transaction_id = %s"
TRANSACTION_UPDATE = "UPDATE \"Transaction\" SET amount = %s WHERE transaction_id = %s"
TRANSACTION_DELETE = "DELETE FROM \"Transaction\" WHERE transaction_id = %s"

# Feature_Store queries
FEATURE_STORE_INSERT = "INSERT INTO \"Feature_Store\" (course_id, metadata, version) VALUES (%s, %s, %s) RETURNING feature_store_id"
FEATURE_STORE_SELECT_ALL = "SELECT feature_store_id, course_id, metadata, version FROM \"Feature_Store\""
FEATURE_STORE_SELECT_BY_ID = "SELECT feature_store_id, course_id, metadata, version FROM \"Feature_Store\" WHERE feature_store_id = %s"
FEATURE_STORE_UPDATE = "UPDATE \"Feature_Store\" SET metadata = %s, version = %s WHERE feature_store_id = %s"
FEATURE_STORE_DELETE = "DELETE FROM \"Feature_Store\" WHERE feature_store_id = %s"

# Feature_Store_Audit queries
FEATURE_STORE_AUDIT_INSERT = "INSERT INTO \"Feature_Store_Audit\" (feature_store_id, change_description) VALUES (%s, %s) RETURNING audit_id"
FEATURE_STORE_AUDIT_SELECT_ALL = "SELECT audit_id, feature_store_id, change_description FROM \"Feature_Store_Audit\""
FEATURE_STORE_AUDIT_SELECT_BY_ID = "SELECT audit_id, feature_store_id, change_description FROM \"Feature_Store_Audit\" WHERE audit_id = %s"
FEATURE_STORE_AUDIT_DELETE = "DELETE FROM \"Feature_Store_Audit\" WHERE audit_id = %s"

# Chapter queries
CHAPTER_INSERT = "INSERT INTO \"Chapter\" (course_id, title, video_url, content) VALUES (%s, %s, %s, %s) RETURNING chapter_id"
CHAPTER_SELECT_ALL = "SELECT chapter_id, course_id, title, video_url, content FROM \"Chapter\""
CHAPTER_SELECT_BY_ID = "SELECT chapter_id, course_id, title, video_url, content FROM \"Chapter\" WHERE chapter_id = %s"
CHAPTER_UPDATE = "UPDATE \"Chapter\" SET course_id = %s, title = %s, video_url = %s, content = %s WHERE chapter_id = %s"
CHAPTER_DELETE = "DELETE FROM \"Chapter\" WHERE chapter_id = %s"