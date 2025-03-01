import click
from db_connection import get_connection
from queries import ENROLLMENT_INSERT, ENROLLMENT_SELECT_ALL, ENROLLMENT_SELECT_BY_ID, ENROLLMENT_UPDATE, ENROLLMENT_DELETE

def add_commands(cli):
    """Adds Enrollment-related commands to the CLI."""
    @cli.group()
    def enrollment():
        """Commands for managing the Enrollment table."""
        pass

    @enrollment.command()
    @click.option('--user-id', required=True, type=int, help="User ID")
    @click.option('--course-id', required=True, type=int, help="Course ID")
    def create(user_id, course_id):
        """Create a new enrollment."""
        conn = get_connection()
        if conn is None:
            return
        try:
            with conn.cursor() as cur:
                cur.execute(ENROLLMENT_INSERT, (user_id, course_id))
                enrollment_id = cur.fetchone()[0]
                conn.commit()
                click.echo(click.style(f"Created enrollment with ID: {enrollment_id}", fg='green'))
        except Exception as e:
            conn.rollback()
            click.echo(f"Error creating enrollment: {e}")
        finally:
            conn.close()

    @enrollment.command()
    def list():
        """List all enrollments."""
        conn = get_connection()
        if conn is None:
            return
        try:
            with conn.cursor() as cur:
                cur.execute(ENROLLMENT_SELECT_ALL)
                enrollments = cur.fetchall()
                if not enrollments:
                    click.echo("No enrollments found.")
                    return
                for e in enrollments:
                    click.echo(f"ID: {e[0]}, User ID: {e[1]}, Course ID: {e[2]}")
        except Exception as e:
            click.echo(f"Error listing enrollments: {e}")
        finally:
            conn.close()

    @enrollment.command()
    @click.option('--id', required=True, type=int, help="Enrollment ID to retrieve")
    def get(id):
        """Get an enrollment by ID."""
        conn = get_connection()
        if conn is None:
            return
        try:
            with conn.cursor() as cur:
                cur.execute(ENROLLMENT_SELECT_BY_ID, (id,))
                enrollment = cur.fetchone()
                if enrollment:
                    click.echo(f"ID: {enrollment[0]}, User ID: {enrollment[1]}, Course ID: {enrollment[2]}")
                else:
                    click.echo(f"Enrollment with ID {id} not found.")
        except Exception as e:
            click.echo(f"Error retrieving enrollment: {e}")
        finally:
            conn.close()

    @enrollment.command()
    @click.option('--id', required=True, type=int, help="Enrollment ID to update")
    @click.option('--user-id', type=int, help="New User ID")
    @click.option('--course-id', type=int, help="New Course ID")
    def update(id, user_id, course_id):
        """Update an enrollment's details."""
        conn = get_connection()
        if conn is None:
            return
        try:
            with conn.cursor() as cur:
                cur.execute(ENROLLMENT_SELECT_BY_ID, (id,))
                current = cur.fetchone()
                if not current:
                    click.echo(f"Enrollment with ID {id} not found.")
                    return
                new_user_id = user_id if user_id is not None else current[1]
                new_course_id = course_id if course_id is not None else current[2]
                cur.execute(ENROLLMENT_UPDATE, (new_user_id, new_course_id, id))
                conn.commit()
                click.echo(f"Updated enrollment ID: {id}")
        except Exception as e:
            conn.rollback()
            click.echo(f"Error updating enrollment: {e}")
        finally:
            conn.close()

    @enrollment.command()
    @click.option('--id', required=True, type=int, help="Enrollment ID to delete")
    @click.confirmation_option(prompt="Are you sure you want to delete this enrollment?")
    def delete(id):
        """Delete an enrollment by ID."""
        conn = get_connection()
        if conn is None:
            return
        try:
            with conn.cursor() as cur:
                cur.execute(ENROLLMENT_DELETE, (id,))
                if cur.rowcount > 0:
                    conn.commit()
                    click.echo(f"Deleted enrollment ID: {id}")
                else:
                    click.echo(f"Enrollment with ID {id} not found.")
        except Exception as e:
            conn.rollback()
            click.echo(f"Error deleting enrollment: {e}")
        finally:
            conn.close()