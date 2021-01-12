import click
from .api import Api
from .utils import normalize_host

API = "API"
USERNAME = "USERNAME"
HOST = "HOST"


@click.group()
@click.option(
    "--host",
    required=True,
    envvar="JFROG_HOST",
    help="The base url of the jfrog saas instance. Alternatively, set JFROG_HOST env var",
)
@click.option(
    "--jfrog-username",
    required=True,
    envvar="JFROG_USERNAME",
    help="the username to authenticate with. Alternatively, set JFROG_USERNAME env var",
)
@click.option(
    "--jfrog-password",
    required=True,
    envvar="JFROG_PASSWORD",
    help="the password to authenticate with. Alternatively, set JFROG_PASSWORD env var",
)
@click.pass_context
def cli(ctx, host, jfrog_username, jfrog_password):
    """Jfrog saas instance cli"""

    normalized_host = normalize_host(host)
    
    ctx.ensure_object(dict)
    ctx.obj[HOST] = normalized_host
    ctx.obj[USERNAME] = jfrog_username
    ctx.obj[API] = Api(normalized_host, jfrog_username, jfrog_password)


@cli.group()
@click.pass_context
def system(ctx):
    """System commands"""
    pass


@system.command(name="ping")
@click.pass_context
def system_ping(ctx):
    """Ping system, ensuring saas instance is up"""
    
    click.echo(f"pinging {ctx.obj[HOST]}...")
    ok = ctx.obj.get(API).system.ping()
    if ok:
        click.echo(f"{ctx.obj[HOST]} is up and running :)")
    else:
        click.echo(f"{ctx.obj[HOST]} is down!")



@system.command(name="version")
@click.pass_context
def system_version(ctx):
    """Get system version and addons"""
    response = ctx.obj.get(API).system.version()

    version = response["version"]
    revision = response["revision"]
    addons = response["addons"]
    addons.sort()

    print(
        "System version info:\n\n"
        f"  version: {version}\n"
        f"  revision: {revision}\n"
        f"  addons: {','.join(addons)}"
    )


@cli.group()
@click.pass_context
def storage(ctx):
    """Commands for managing storaqe"""
    pass


@storage.command(name="info")
@click.pass_context
def storage_info(ctx):
    """Get storage usage summary for various storage types"""
    info = ctx.obj.get(API).storage.info()
    print(info)


@cli.group()
@click.pass_context
def user(ctx):
    """Manage users"""
    pass


@user.command(name="create")
@click.option("--username", required=True, help="name of user to create")
@click.option("--email", required=True, help="email for new user")
@click.option("--password", required=True, help="password for new user")
@click.option("--admin", default=False, help="if set, created user will be an admin. Default is false")
@click.option("--ui-access", default=False, help="if set, user will be able to access ui. Default is false")
@click.option("--groups", default=None, help="comma separated list of groups to place user in")
@click.pass_context
def user_create(ctx, username: str, email: str, password: str, admin: bool, ui_access: bool, groups: str):
    """Create a new user"""
    if groups is not None:
        groups = groups.split(',')

    click.echo(f"Attempting to create user {username}...")

    ctx.obj.get(API).user.create(username, email, password, admin, ui_access, groups)

    click.echo(f"User {username} created successfully")


@user.command(name="delete")
@click.option("--username", required=True, help="name of user to delete")
@click.pass_context
def user_delete(ctx, username):
    """Delete a user"""
    click.echo(f"Attempting to delete user {username}...")

    ctx.obj.get(API).user.delete(username)

    click.echo(f"User {username} deleted successfully")