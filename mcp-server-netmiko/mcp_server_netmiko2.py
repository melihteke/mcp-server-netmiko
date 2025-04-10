import os
from mcp.server.fastmcp import FastMCP
from netmiko import ConnectHandler

class McpHandler:
    def __init__(self):
        """Initialize the MCP server"""
        self.mcp = FastMCP("McpHandler")

        @self.mcp.tool()
        def send_command_tool(device: str, command: str) -> str:
            """Send a command to a network device via SSH"""
            return self.send_command(device, command)

    def send_command(self, device: str, command: str) -> str:
        """Send a command to a network device via SSH"""
        device_params = {
            "device_type": os.getenv("DEVICE_TYPE", "cisco_ios"),
            "host": device,
            "username": os.getenv("DEVICE_USERNAME", "admin"),
            "password": os.getenv("DEVICE_PASSWORD", "password"),
            "secret": os.getenv("DEVICE_SECRET", "enable_password"),
        }

        use_textfsm = os.getenv("USE_TEXTFSM", "false").lower() == "true"
        use_genie = os.getenv("USE_GENIE", "false").lower() == "true"

        with ConnectHandler(**device_params) as ssh:
            ssh.enable()

            if use_textfsm:
                return ssh.send_command(command, use_textfsm=True)

            if use_genie:
                return ssh.send_command(command, use_genie=True)

            return ssh.send_command(command)

    def run(self):
        """Run the MCP server in specified transport mode"""
        transport_mode = os.getenv("MCP_TRANSPORT", "sse")  # or "stdio"
        self.mcp.run(transport=transport_mode)


if __name__ == "__main__":
    server = McpHandler()
    server.run()
