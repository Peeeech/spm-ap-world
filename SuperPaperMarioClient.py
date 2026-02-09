import os
import asyncio
import typing

import Utils

from NetUtils import NetworkItem, ClientStatus
from worlds.super_paper_mario.items import item_name_to_id, item_id_to_name
from worlds.super_paper_mario import netmemoryaccess_client as localClient
from MultiServer import mark_raw
from CommonClient import CommonContext, server_loop, \
    gui_enabled, ClientCommandProcessor, logger, get_base_parser
from Utils import async_start

client_data_path = os.path.expandvars("~/.config/Archipelago/Clients/SuperPaperMario")

class SuperPaperMarioCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext):
        super().__init__(ctx)

    def _cmd_receive(self, item: str):
        """Receive an Item based off either its String-Name or Item-ID."""
        
        #Normalize received item to both name and id, so we can use either for the command
        try:
            item_id = int(item)
            item_name = self.ctx.item_id_to_name(item_id)
        except ValueError:
            item_id = self.ctx.item_name_to_id(f"{item.upper()}")
            item_name = self.ctx.item_id_to_name(item_id)

        self.output(f"Manually receiving item: {item_name}")

        index=len(self.ctx.items_received)
        
        # temporary fake NetworkItem
        fake = NetworkItem(
            location=-1,
            player=self.ctx.slot,
            flags=0,
            item=self.ctx.item_name_to_id(item_name)
        )
        self.ctx.items_received.append(fake)
        localClient.item(fake.item, index)

    
class SuperPaperMarioContext(CommonContext):
    tags = {"AP"}
    game = "Manual_SuperPaperMario_L5050PeeeeeechSeaturtle"
    command_processor = SuperPaperMarioCommandProcessor
    items_handling = 0b111

    def __init__(self, args):
        super().__init__(args)
        self.game = "Manual_SuperPaperMario_L5050PeeeeeechSeaturtle"
        self.item_name_to_id = item_name_to_id
        self.item_id_to_name = item_id_to_name

    async def server_auth(self, password_requested=False):
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        if cmd == "Connected":
            logger.info("\n\n Yippee! You connected to SPM AP :3 \n\n")

        if cmd == "ReceivedItems":
            for item in args["items"]:
                ni = NetworkItem(*item)
                logger.info(
                    f"Item received: {ni.item} "
                    f"(from player {ni.player}, index {ni.index})"
                )
        

def main():
    print("\nStarting Super Paper Mario Client...\n")
    Utils.init_logging("SuperPaperMarioClient", exception_logger="Client")

    async def _main():
        ctx = SuperPaperMarioContext(None)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

        """if gui_enabled:
            ctx.run_gui()"""
        ctx.run_cli()

        await ctx.exit_event.wait()
        await ctx.shutdown()

    import colorama

    colorama.just_fix_windows_console()

    asyncio.run(_main())
    colorama.deinit()

if __name__ == "__main__":
    parser = get_base_parser(description="Super Paper Mario Client, for text interfacing.")
    args = parser.parse_args()
    main()
