import click
from user import add_commands as add_user_commands
from course import add_commands as add_course_commands
from chapter import add_commands as add_chapter_commands
from enrollment import add_commands as add_enrollment_commands
from transaction import add_commands as add_transaction_commands
from feature_store import add_commands as add_feature_store_commands
from feature_store_audit import add_commands as add_feature_store_audit_commands

@click.group()
def cli():
    """CLI tool for performing CRUD operations on the database."""
    pass

# Register all table commands
add_user_commands(cli)
add_course_commands(cli)
add_chapter_commands(cli)
add_enrollment_commands(cli)
add_transaction_commands(cli)
add_feature_store_commands(cli)
add_feature_store_audit_commands(cli)

@cli.command()
def init_sample_data():
    """Insert sample data into the database for testing."""
    conn = get_connection()
    if conn is None:
        return
    try:
        with conn.cursor() as cur:
            # Sample users
            cur.execute(USER_INSERT, ("Alice", "alice@example.com", "instructor"))
            alice_id = cur.fetchone()[0]
            cur.execute(USER_INSERT, ("Bob", "bob@example.com", "student"))
            bob_id = cur.fetchone()[0]
            # Sample course
            cur.execute(COURSE_INSERT, ("Python 101", alice_id, "Intro to Python", 49.99))
            course_id = cur.fetchone()[0]
            conn.commit()
            click.echo("Sample data inserted: 2 users, 1 course.")
    except Exception as e:
        conn.rollback()
        click.echo(f"Error inserting sample data: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    cli()