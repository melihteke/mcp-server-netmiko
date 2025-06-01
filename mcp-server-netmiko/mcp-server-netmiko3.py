from fastmcp import FastMCP
from netmiko import ConnectHandler, NetMikoAuthenticationException, NetMikoTimeoutException

mcp = FastMCP("Network CLI Executor & Config MCP")

def connect_device(host, username, password, device_type):
    """Reusable connection function."""
    return ConnectHandler(
        device_type=device_type,
        host=host,
        username=username,
        password=password
    )

@mcp.tool()
def run_cli_commands(
    host: str,
    username: str,
    password: str,
    device_type: str,
    commands: list[str]
) -> dict:
    """
    Connect to a network device and run a list of show/debug commands.
    """
    try:
        conn = connect_device(host, username, password, device_type)
        output = {cmd: conn.send_command(cmd) for cmd in commands}
        conn.disconnect()
        return {"result": output}
    except (NetMikoAuthenticationException, NetMikoTimeoutException) as e:
        return {"error": f"Connection error: {str(e)}"}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def send_config_commands(
    host: str,
    username: str,
    password: str,
    device_type: str,
    config_commands: list[str]
) -> dict:
    """
    Connect and push configuration commands to a network device.
    """
    try:
        conn = connect_device(host, username, password, device_type)
        output = conn.send_config_set(config_commands)
        conn.disconnect()
        return {"result": output}
    except (NetMikoAuthenticationException, NetMikoTimeoutException) as e:
        return {"error": f"Connection error: {str(e)}"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run(transport="sse")