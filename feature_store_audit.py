import click
from db_connection import get_connection
from queries import FEATURE_STORE_AUDIT_INSERT, FEATURE_STORE_AUDIT_SELECT_ALL, FEATURE_STORE_AUDIT_SELECT_BY_ID, FEATURE_STORE_AUDIT_DELETE

def add_commands(cli):
    """Adds Feature_Store_Audit-related commands to the CLI."""
    @cli.group()
    def feature_store_audit():
        """Commands for managing the Feature_Store_Audit table."""
        pass

    @feature_store_audit.command()
    @click.option('--feature-store-id', required=True, type=int, help="Feature_Store ID")
    @click.option('--change-description', required=True, help="Description of the change")
    def create(feature_store_id, change_description):
        """Create a new feature_store_audit entry."""
        conn = get_connection()
        if conn is None:
            return
        try:
            with conn.cursor() as cur:
                cur.execute(FEATURE_STORE_AUDIT_INSERT, (feature_store_id, change_description))
                audit_id = cur.fetchone()[0]
                conn.commit()
                click.echo(click.style(f"Created feature_store_audit with ID: {audit_id}", fg='green'))
        except Exception as e:
            conn.rollback()
            click.echo(f"Error creating feature_store_audit: {e}")
        finally:
            conn.close()

    @feature_store_audit.command()
    def list():
        """List all feature_store_audit entries."""
        conn = get_connection()
        if conn is None:
            return
        try:
            with conn.cursor() as cur:
                cur.execute(FEATURE_STORE_AUDIT_SELECT_ALL)
                audits = cur.fetchall()
                if not audits:
                    click.echo("No feature_store_audit entries found.")
                    return
                for a in audits:
                    click.echo(f"ID: {a[0]}, Feature_Store ID: {a[1]}, Change Description: {a[2]}")
        except Exception as e:
            click.echo(f"Error listing feature_store_audit: {e}")
        finally:
            conn.close()

    @feature_store_audit.command()
    @click.option('--id', required=True, type=int, help="Feature_Store_Audit ID to retrieve")
    def get(id):
        """Get a feature_store_audit entry by ID."""
        conn = get_connection()
        if conn is None:
            return
        try:
            with conn.cursor() as cur:
                cur.execute(FEATURE_STORE_AUDIT_SELECT_BY_ID, (id,))
                audit = cur.fetchone()
                if audit:
                    click.echo(f"ID: {audit[0]}, Feature_Store ID: {audit[1]}, Change Description: {audit[2]}")
                else:
                    click.echo(f"Feature_Store_Audit with ID {id} not found.")
        except Exception as e:
            click.echo(f"Error retrieving feature_store_audit: {e}")
        finally:
            conn.close()

    @feature_store_audit.command()
    @click.option('--id', required=True, type=int, help="Feature_Store_Audit ID to delete")
    @click.confirmation_option(prompt="Are you sure you want to delete this feature_store_audit entry?")
    def delete(id):
        """Delete a feature_store_audit entry by ID."""
        conn = get_connection()
        if conn is None:
            return
        try:
            with conn.cursor() as cur:
                cur.execute(FEATURE_STORE_AUDIT_DELETE, (id,))
                if cur.rowcount > 0:
                    conn.commit()
                    click.echo(f"Deleted feature_store_audit ID: {id}")
                else:
                    click.echo(f"Feature_Store_Audit with ID {id} not found.")
        except Exception as e:
            conn.rollback()
            click.echo(f"Error deleting feature_store_audit: {e}")
        finally:
            conn.close()