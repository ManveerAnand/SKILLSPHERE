import click
from db_connection import get_connection
from queries import COURSE_INSERT, COURSE_SELECT_ALL, COURSE_SELECT_BY_ID, COURSE_UPDATE, COURSE_DELETE

def add_commands(cli):
    """Adds Course-related commands to the CLI."""
    @cli.group()
    def course():
        """Commands for managing the Course table."""
        pass

    @course.command()
    @click.option('--title', required=True, help="Course title")
    @click.option('--instructor-id', required=True, type=int, help="Instructor's user ID")
    @click.option('--description', required=True, help="Course description")
    @click.option('--price', required=True, type=float, help="Course price")
    def create(title, instructor_id, description, price):
        """Create a new course."""
        conn = get_connection()
        if conn is None:
            return
        try:
            with conn.cursor() as cur:
                cur.execute(COURSE_INSERT, (title, instructor_id, description, price))
                course_id = cur.fetchone()[0]
                conn.commit()
                click.echo(click.style(f"Created course with ID: {course_id}", fg='green'))
        except psycopg2.IntegrityError as e:
            conn.rollback()
            click.echo(f"Error: Instructor ID {instructor_id} does not exist.")
        except Exception as e:
            conn.rollback()
            click.echo(f"Error creating course: {e}")
        finally:
            conn.close()

    @course.command()
    def list():
        """List all courses."""
        conn = get_connection()
        if conn is None:
            return
        try:
            with conn.cursor() as cur:
                cur.execute(COURSE_SELECT_ALL)
                courses = cur.fetchall()
                if not courses:
                    click.echo("No courses found.")
                    return
                for c in courses:
                    click.echo(f"ID: {c[0]}, Title: {c[1]}, Instructor ID: {c[2]}, Description: {c[3]}, Price: ${c[4]:.2f}")
        except Exception as e:
            click.echo(f"Error listing courses: {e}")
        finally:
            conn.close()

    @course.command()
    @click.option('--id', required=True, type=int, help="Course ID to retrieve")
    def get(id):
        """Get a course by ID."""
        conn = get_connection()
        if conn is None:
            return
        try:
            with conn.cursor() as cur:
                cur.execute(COURSE_SELECT_BY_ID, (id,))
                course = cur.fetchone()
                if course:
                    click.echo(f"ID: {course[0]}, Title: {course[1]}, Instructor ID: {course[2]}, Description: {course[3]}, Price: ${course[4]:.2f}")
                else:
                    click.echo(f"Course with ID {id} not found.")
        except Exception as e:
            click.echo(f"Error retrieving course: {e}")
        finally:
            conn.close()

    @course.command()
    @click.option('--id', required=True, type=int, help="Course ID to update")
    @click.option('--title', help="New title")
    @click.option('--description', help="New description")
    @click.option('--price', type=float, help="New price")
    def update(id, title, description, price):
        """Update a course's details."""
        conn = get_connection()
        if conn is None:
            return
        try:
            with conn.cursor() as cur:
                cur.execute(COURSE_SELECT_BY_ID, (id,))
                current = cur.fetchone()
                if not current:
                    click.echo(f"Course with ID {id} not found.")
                    return
                new_title, new_desc, new_price = title or current[1], description or current[3], price if price is not None else current[4]
                cur.execute(COURSE_UPDATE, (new_title, new_desc, new_price, id))
                conn.commit()
                click.echo(f"Updated course ID: {id}")
        except Exception as e:
            conn.rollback()
            click.echo(f"Error updating course: {e}")
        finally:
            conn.close()

    @course.command()
    @click.option('--id', required=True, type=int, help="Course ID to delete")
    @click.confirmation_option(prompt="Are you sure you want to delete this course?")
    def delete(id):
        """Delete a course by ID."""
        conn = get_connection()
        if conn is None:
            return
        try:
            with conn.cursor() as cur:
                cur.execute(COURSE_DELETE, (id,))
                if cur.rowcount > 0:
                    conn.commit()
                    click.echo(f"Deleted course ID: {id}")
                else:
                    click.echo(f"Course with ID {id} not found.")
        except Exception as e:
            conn.rollback()
            click.echo(f"Error deleting course: {e}")
        finally:
            conn.close()