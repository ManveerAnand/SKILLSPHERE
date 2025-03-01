import click
from db_connection import get_connection
from queries import CHAPTER_INSERT

def add_commands(cli):
    """Adds Chapter-related commands to the CLI."""
    @cli.group()
    def chapter():
        """Commands for managing the Chapter table."""
        pass

    @chapter.command()
    @click.option('--course-id', required=True, type=int, help="Course ID")
    @click.option('--title', required=True, help="Chapter title")
    @click.option('--content', required=True, help="Chapter content")
    def create(course_id, title, content):
        """Create a new chapter."""
        conn = get_connection()
        if conn is None:
            return
        try:
            with conn.cursor() as cur:
                cur.execute(CHAPTER_INSERT, (course_id, title, content))
                chapter_id = cur.fetchone()[0]
                conn.commit()
                click.echo(f"Created chapter with ID: {chapter_id}")
        except Exception as e:
            conn.rollback()
            click.echo(f"Error creating chapter: {e}")
        finally:
            conn.close()

    # Skeleton for other commands
    @chapter.command()
    def list():
        """List all chapters (not implemented)."""
        click.echo("List chapters - implementation pending.")

    @chapter.command()
    @click.option('--id', required=True, type=int)
    def get(id):
        """Get a chapter by ID (not implemented)."""
        click.echo("Get chapter - implementation pending.")

    @chapter.command()
    @click.option('--id', required=True, type=int)
    def update(id):
        """Update a chapter (not implemented)."""
        click.echo("Update chapter - implementation pending.")

    @chapter.command()
    @click.option('--id', required=True, type=int)
    def delete(id):
        """Delete a chapter (not implemented)."""
        click.echo("Delete chapter - implementation pending.")