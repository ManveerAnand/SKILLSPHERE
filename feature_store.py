import click
from db_connection import get_connection
from queries import FEATURE_STORE_INSERT, FEATURE_STORE_SELECT_ALL, FEATURE_STORE_SELECT_BY_ID, FEATURE_STORE_UPDATE, FEATURE_STORE_DELETE

def add_commands(cli):
    """Adds Feature_Store-related commands to the CLI."""
    @cli.group()
    def feature_store():
        """Commands for managing the Feature_Store table."""
        pass

    @feature_store.command()
    @click.option('--course-id', required=True, type=int, help="Course ID")
    @click.option('--metadata', required=True, help="Feature metadata (JSON string)")
    @click.option('--version', required=True, type=int, help="Feature version")
    def create(course_id, metadata, version):
        """Create a new feature_store entry."""
        conn = get_connection()
        if conn is None:
            return
        try:
            with conn.cursor() as cur:
                cur.execute(FEATURE_STORE_INSERT, (course_id, metadata, version))
                feature_store_id = cur.fetchone()[0]
                conn.commit()
                click.echo(click.style(f"Created feature_store with ID: {feature_store_id}", fg='green'))
        except Exception as e:
            conn.rollback()
            click.echo(f"Error creating feature_store: {e}")
        finally:
            conn.close()

    @feature_store.command()
    def list():
        """List all feature_store entries."""
        conn = get_connection()
        if conn is None:
            return
        try:
            with conn.cursor() as cur:
                cur.execute(FEATURE_STORE_SELECT_ALL)
                feature_stores = cur.fetchall()
                if not feature_stores:
                    click.echo("No feature_store entries found.")
                    return
                for fs in feature_stores:
                    click.echo(f"ID: {fs[0]}, Course ID: {fs[1]}, Metadata: {fs[2]}, Version: {fs[3]}")
        except Exception as e:
            click.echo(f"Error listing feature_store: {e}")
        finally:
            conn.close()

    @feature_store.command()
    @click.option('--id', required=True, type=int, help="Feature_Store ID to retrieve")
    def get(id):
        """Get a feature_store entry by ID."""
        conn = get_connection()
        if conn is None:
            return
        try:
            with conn.cursor() as cur:
                cur.execute(FEATURE_STORE_SELECT_BY_ID, (id,))
                feature_store = cur.fetchone()
                if feature_store:
                    click.echo(f"ID: {feature_store[0]}, Course ID: {feature_store[1]}, Metadata: {feature_store[2]}, Version: {feature_store[3]}")
                else:
                    click.echo(f"Feature_Store with ID {id} not found.")
        except Exception as e:
            click.echo(f"Error retrieving feature_store: {e}")
        finally:
            conn.close()

    @feature_store.command()
    @click.option('--id', required=True, type=int, help="Feature_Store ID to update")
    @click.option('--metadata', help="New metadata (JSON string)")
    @click.option('--version', type=int, help="New version")
    def update(id, metadata, version):
        """Update a feature_store entry's details."""
        conn = get_connection()
        if conn is None:
            return
        try:
            with conn.cursor() as cur:
                cur.execute(FEATURE_STORE_SELECT_BY_ID, (id,))
                current = cur.fetchone()
                if not current:
                    click.echo(f"Feature_Store with ID {id} not found.")
                    return
                new_metadata = metadata if metadata is not None else current[2]
                new_version = version if version is not None else current[3]
                cur.execute(FEATURE_STORE_UPDATE, (new_metadata, new_version, id))
                conn.commit()
                click.echo(f"Updated feature_store ID: {id}")
        except Exception as e:
            conn.rollback()
            click.echo(f"Error updating feature_store: {e}")
        finally:
            conn.close()

    @feature_store.command()
    @click.option('--id', required=True, type=int, help="Feature_Store ID to delete")
    @click.confirmation_option(prompt="Are you sure you want to delete this feature_store entry?")
    def delete(id):
        """Delete a feature_store entry by ID."""
        conn = get_connection()
        if conn is None:
            return
        try:
            with conn.cursor() as cur:
                cur.execute(FEATURE_STORE_DELETE, (id,))
                if cur.rowcount > 0:
                    conn.commit()
                    click.echo(f"Deleted feature_store ID: {id}")
                else:
                    click.echo(f"Feature_Store with ID {id} not found.")
        except Exception as e:
            conn.rollback()
            click.echo(f"Error deleting feature_store: {e}")
        finally:
            conn.close()