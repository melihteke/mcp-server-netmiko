import os
from mcp.server.fastmcp import FastMCP
from netmiko import ConnectHandler

class McpHandler:
    def __init__(self):
        """Initialize the MCP server"""
        self.mcp = FastMCP("McpHandler")

        # Register the tool
        @self.mcp.tool()
        def send_command_tool(device: str, command: str) -> str:
            """Send a command to a network device via SSH"""
            return self.send_command(device, command)

    def send_command(self, device: str, command: str) -> str:
        """Send a command to a network device via SSH"""
        # Retrieve connection parameters from environment variables
        device_params = {
            "device_type": os.getenv("DEVICE_TYPE", "cisco_ios"),  # Default to Cisco IOS
            "host": device,
            "username": os.getenv("DEVICE_USERNAME", "admin"),
            "password": os.getenv("DEVICE_PASSWORD", "password"),
            "secret": os.getenv("DEVICE_SECRET", "enable_password"),
        }

        use_textfsm =  os.getenv("USE_TEXTFSM", "false").lower() == "true",
        use_genie = os.getenv("USE_GENIE", "false").lower() == "true",

        # Establish connection and send the command
        with ConnectHandler(**device_params) as ssh:
            ssh.enable()  # Enter enable mode if required

            if use_textfsm == "true":
                return ssh.send_command(command, use_textfsm=True)

            if use_genie == "true":
                return ssh.send_command(command, use_genie=True)

            return ssh.send_command(command)

    def run(self):
        """Run the MCP server"""
        # FastMCP.run() does not accept a 'port' argument, so we skip it
        self.mcp.run(transport="sse")


if __name__ == "__main__":
    server = McpHandler()
    server.run()
