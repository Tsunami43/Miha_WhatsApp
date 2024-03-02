from .commands import router as router_commands
from .menu import router as router_menu
from .account import router as router_account
routers = [
    router_commands,
    router_menu,
    router_account
]