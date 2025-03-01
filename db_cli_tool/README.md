 # Database CLI Tool

A command-line interface (CLI) tool for performing CRUD (Create, Read, Update, Delete) operations on a PostgreSQL database. This tool manages tables for an E-Learning Platform (LMS), including `User`, `Course`, `Chapter`, `Enrollment`, `Transaction`, `Feature_Store`, and `Feature_Store_Audit`. Built with Python, it leverages `click` for the CLI and `psycopg2` for database connectivity, offering a robust and user-friendly way to interact with the LMS database.

## Features

- Full CRUD operations for all tables.
- Modular design with separate files for each table’s commands.
- Error handling for database connectivity and operations.
- Support for PostgreSQL’s `JSONB` data type for flexible metadata storage.
- Normalized database schema in 3NF for data integrity and efficiency.

## Setup

Follow these steps to set up and run the CLI tool locally:

1. **Install Dependencies**:
   Ensure you have Python 3.x installed, then install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure the Database**:
   - Set up a PostgreSQL database instance (e.g., locally or via a service like ElephantSQL).
   - Create the database schema by running the provided SQL script (see [schema.sql](#database-schema)).
   - Update the database connection parameters in `db_connection.py`:
     ```python
     DB_PARAMS = {
         "dbname": "your_db_name",
         "user": "your_username",
         "password": "your_password",
         "host": "localhost",
         "port": "5432"
     }
     ```

3. **Run the Tool**:
   From the project root directory, execute:
   ```bash
   python db_tool.py --help
   ```
   This displays all available commands.

## Usage Examples

Here are some practical examples to get you started:

### Create a User
```bash
python db_tool.py user create --name "John Doe" --email "john@example.com" --role "student"
```
*Output*: `Created user with ID: 1`

### List All Courses
```bash
python db_tool.py course list
```
*Output*: Lists all courses with their IDs, titles, descriptions, and prices.

### Enroll a User in a Course
```bash
python db_tool.py enrollment create --user-id 1 --course-id 1
```
*Output*: `Created enrollment with ID: 1`

### Update a Transaction Amount
```bash
python db_tool.py transaction update --id 1 --amount 59.99
```
*Output*: `Updated transaction ID: 1`

### Delete a Feature Store Entry
```bash
python db_tool.py feature_store delete --id 1
```
*Output*: `Deleted feature_store ID: 1`

## CLI Commands

Below is a complete list of commands organized by table:

### User Commands
- `user create --name <name> --email <email> --role <role>`: Create a new user.
- `user list`: List all users.
- `user get --id <id>`: Retrieve a user by ID.
- `user update --id <id> [--name <name>] [--email <email>] [--role <role>]`: Update user details.
- `user delete --id <id>`: Delete a user.

### Course Commands
- `course create --title <title> --instructor-id <id> --description <desc> --price <price>`: Create a new course.
- `course list`: List all courses.
- `course get --id <id>`: Retrieve a course by ID.
- `course update --id <id> [--title <title>] [--description <desc>] [--price <price>]`: Update course details.
- `course delete --id <id>`: Delete a course.

### Chapter Commands
- `chapter create --course-id <id> --title <title> --video-url <url> --content <content>`: Create a new chapter.
- `chapter list`: List all chapters.
- `chapter get --id <id>`: Retrieve a chapter by ID.
- `chapter update --id <id> [--course-id <id>] [--title <title>] [--video-url <url>] [--content <content>]`: Update chapter details.
- `chapter delete --id <id>`: Delete a chapter.

### Enrollment Commands
- `enrollment create --user-id <id> --course-id <id>`: Enroll a user in a course.
- `enrollment list`: List all enrollments.
- `enrollment get --id <id>`: Retrieve an enrollment by ID.
- `enrollment update --id <id> [--user-id <id>] [--course-id <id>]`: Update enrollment details.
- `enrollment delete --id <id>`: Delete an enrollment.

### Transaction Commands
- `transaction create --user-id <id> --course-id <id> --amount <amount>`: Create a new transaction.
- `transaction list`: List all transactions.
- `transaction get --id <id>`: Retrieve a transaction by ID.
- `transaction update --id <id> --amount <amount>`: Update transaction amount.
- `transaction delete --id <id>`: Delete a transaction.

### Feature Store Commands
- `feature_store create --course-id <id> --metadata <json> --version <version>`: Create a feature store entry.
- `feature_store list`: List all feature store entries.
- `feature_store get --id <id>`: Retrieve a feature store entry by ID.
- `feature_store update --id <id> [--metadata <json>] [--version <version>]`: Update feature store details.
- `feature_store delete --id <id>`: Delete a feature store entry.

### Feature Store Audit Commands
- `feature_store_audit create --feature-store-id <id> --change-description <desc>`: Create an audit entry.
- `feature_store_audit list`: List all audit entries.
- `feature_store_audit get --id <id>`: Retrieve an audit entry by ID.
- `feature_store_audit delete --id <id>`: Delete an audit entry.


## Requirements

The `requirements.txt` file includes:
```
click==8.1.3
psycopg2-binary==2.9.3
```

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details (create one if needed).

## Acknowledgments

- Built as part of a DBMS course project.
- Thanks to the open-source community for tools like `click` and `psycopg2`.
