import click
from db_connection import get_connection
from queries import USER_INSERT, USER_SELECT_ALL, USER_SELECT_BY_ID, USER_UPDATE, USER_DELETE

def add_commands(cli):
    """Adds User-related commands to the CLI."""
    @cli.group()
    def user():
        """Commands for managing the User table."""
        pass

    @user.command()
    @click.option('--name', required=True, help="User's name")
    @click.option('--email', required=True, help="User's email")
    @click.option('--role', required=True, help="User's role (e.g., student, instructor)")
    def create(name, email, role):
        """Create a new user."""
        conn = get_connection()
        if conn is None:
            return
        try:
            with conn.cursor() as cur:
                cur.execute(USER_INSERT, (name, email, role))
                user_id = cur.fetchone()[0]
                conn.commit()
                click.echo(click.style(f"Created user with ID: {user_id}", fg='green'))
        except Exception as e:
            conn.rollback()
            click.echo(f"Error creating user: {e}")
        finally:
            conn.close()

    @user.command()
    def list():
        """List all users."""
        conn = get_connection()
        if conn is None:
            return
        try:
            with conn.cursor() as cur:
                cur.execute(USER_SELECT_ALL)
                users = cur.fetchall()
                if not users:
                    click.echo("No users found.")
                    return
                for u in users:
                    click.echo(f"ID: {u[0]}, Name: {u[1]}, Email: {u[2]}, Role: {u[3]}")
        except Exception as e:
            click.echo(f"Error listing users: {e}")
        finally:
            conn.close()

    @user.command()
    @click.option('--id', required=True, type=int, help="User ID to retrieve")
    def get(id):
        """Get a user by ID."""
        conn = get_connection()
        if conn is None:
            return
        try:
            with conn.cursor() as cur:
                cur.execute(USER_SELECT_BY_ID, (id,))
                user = cur.fetchone()
                if user:
                    click.echo(f"ID: {user[0]}, Name: {user[1]}, Email: {user[2]}, Role: {user[3]}")
                else:
                    click.echo(f"User with ID {id} not found.")
        except Exception as e:
            click.echo(f"Error retrieving user: {e}")
        finally:
            conn.close()

    @user.command()
    @click.option('--id', required=True, type=int, help="User ID to update")
    @click.option('--name', help="New name")
    @click.option('--email', help="New email")
    @click.option('--role', help="New role")
    def update(id, name, email, role):
        """Update a user's details."""
        conn = get_connection()
        if conn is None:
            return
        try:
            with conn.cursor() as cur:
                cur.execute(USER_SELECT_BY_ID, (id,))
                current = cur.fetchone()
                if not current:
                    click.echo(f"User with ID {id} not found.")
                    return
                new_name, new_email, new_role = name or current[1], email or current[2], role or current[3]
                cur.execute(USER_UPDATE, (new_name, new_email, new_role, id))
                conn.commit()
                click.echo(f"Updated user ID: {id}")
        except Exception as e:
            conn.rollback()
            click.echo(f"Error updating user: {e}")
        finally:
            conn.close()

    @user.command()
    @click.option('--id', required=True, type=int, help="User ID to delete")
    @click.confirmation_option(prompt="Are you sure you want to delete this user?")
    def delete(id):
        """Delete a user by ID."""
        conn = get_connection()
        if conn is None:
            return
        try:
            with conn.cursor() as cur:
                cur.execute(USER_DELETE, (id,))
                if cur.rowcount > 0:
                    conn.commit()
                    click.echo(f"Deleted user ID: {id}")
                else:
                    click.echo(f"User with ID {id} not found.")
        except Exception as e:
            conn.rollback()
            click.echo(f"Error deleting user: {e}")
        finally:
            conn.close()