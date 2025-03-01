import click
from db_connection import get_connection
from queries import TRANSACTION_INSERT, TRANSACTION_SELECT_ALL, TRANSACTION_SELECT_BY_ID, TRANSACTION_UPDATE, TRANSACTION_DELETE

def add_commands(cli):
    """Adds Transaction-related commands to the CLI."""
    @cli.group()
    def transaction():
        """Commands for managing the Transaction table."""
        pass

    @transaction.command()
    @click.option('--user-id', required=True, type=int, help="User ID")
    @click.option('--course-id', required=True, type=int, help="Course ID")
    @click.option('--amount', required=True, type=float, help="Transaction amount")
    def create(user_id, course_id, amount):
        """Create a new transaction."""
        conn = get_connection()
        if conn is None:
            return
        try:
            with conn.cursor() as cur:
                cur.execute(TRANSACTION_INSERT, (user_id, course_id, amount))
                transaction_id = cur.fetchone()[0]
                conn.commit()
                click.echo(click.style(f"Created transaction with ID: {transaction_id}", fg='green'))
        except Exception as e:
            conn.rollback()
            click.echo(f"Error creating transaction: {e}")
        finally:
            conn.close()

    @transaction.command()
    def list():
        """List all transactions."""
        conn = get_connection()
        if conn is None:
            return
        try:
            with conn.cursor() as cur:
                cur.execute(TRANSACTION_SELECT_ALL)
                transactions = cur.fetchall()
                if not transactions:
                    click.echo("No transactions found.")
                    return
                for t in transactions:
                    click.echo(f"ID: {t[0]}, User ID: {t[1]}, Course ID: {t[2]}, Amount: ${t[3]:.2f}")
        except Exception as e:
            click.echo(f"Error listing transactions: {e}")
        finally:
            conn.close()

    @transaction.command()
    @click.option('--id', required=True, type=int, help="Transaction ID to retrieve")
    def get(id):
        """Get a transaction by ID."""
        conn = get_connection()
        if conn is None:
            return
        try:
            with conn.cursor() as cur:
                cur.execute(TRANSACTION_SELECT_BY_ID, (id,))
                transaction = cur.fetchone()
                if transaction:
                    click.echo(f"ID: {transaction[0]}, User ID: {transaction[1]}, Course ID: {transaction[2]}, Amount: ${transaction[3]:.2f}")
                else:
                    click.echo(f"Transaction with ID {id} not found.")
        except Exception as e:
            click.echo(f"Error retrieving transaction: {e}")
        finally:
            conn.close()

    @transaction.command()
    @click.option('--id', required=True, type=int, help="Transaction ID to update")
    @click.option('--amount', type=float, help="New transaction amount")
    def update(id, amount):
        """Update a transaction's details."""
        conn = get_connection()
        if conn is None:
            return
        try:
            with conn.cursor() as cur:
                cur.execute(TRANSACTION_SELECT_BY_ID, (id,))
                current = cur.fetchone()
                if not current:
                    click.echo(f"Transaction with ID {id} not found.")
                    return
                new_amount = amount if amount is not None else current[3]
                cur.execute(TRANSACTION_UPDATE, (new_amount, id))
                conn.commit()
                click.echo(f"Updated transaction ID: {id}")
        except Exception as e:
            conn.rollback()
            click.echo(f"Error updating transaction: {e}")
        finally:
            conn.close()

    @transaction.command()
    @click.option('--id', required=True, type=int, help="Transaction ID to delete")
    @click.confirmation_option(prompt="Are you sure you want to delete this transaction?")
    def delete(id):
        """Delete a transaction by ID."""
        conn = get_connection()
        if conn is None:
            return
        try:
            with conn.cursor() as cur:
                cur.execute(TRANSACTION_DELETE, (id,))
                if cur.rowcount > 0:
                    conn.commit()
                    click.echo(f"Deleted transaction ID: {id}")
                else:
                    click.echo(f"Transaction with ID {id} not found.")
        except Exception as e:
            conn.rollback()
            click.echo(f"Error deleting transaction: {e}")
        finally:
            conn.close()