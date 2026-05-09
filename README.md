# X Air Assist

Works with X Air compatible Behringer/Midas mixers.

This project includes:

- MCP server to plug it to any AI agent, that can discover, read and change mixer parameters.
- REPL where you can do the same using console interface.
- xair_client python library, that you can use to write scripts with full type checker support, including autocompletion.

## MCP config example

This one should work with Claude Desktop, for example. Probably with other MCP clients too.

```json
{
	"mcpServers": {
		"x-air-mixer": {
			"command": "uv",
			"args": [
				"--directory",
				"/full/path/to/mixer-assist",
				"run",
				"mcp_server.py",
				"--ip",
				"XXX.XXX.XXX.XXX"
			],
		}
	}
}
```

## REPL

```cmd
uv run python repl.py --ip XXX.XXX.XXX.XXX
```

You can navigate the parameter tree (common path syntax works, like absolute paths starts with `/`, `.` and `..` works as usual).
`ls` command lists children nodes in the current nodes, including current parameter values.
`ds` command is like `ls`, but with descriptions for the node and it's children.
`<path> = <value>` could be used to set new value for a parameter.

## Constraints

- Tested only on Midas MR-18 FW 1.25
- Not all available parameters and operations are implemented yet.
  See [OSC commands](https://behringer.world/wiki/doku.php?id=x-air_osc), not implemented: Action, Preferences, Snapshots, Status.
- Some descriptions may be inaccurate or inadequately precise for LLMs.
- At this stage, API is a subject to change.

## Acknowledgements

- [xair-api-python](https://github.com/onyx-and-iris/xair-api-python) for implementations insights.
- [magical-mixers](https://github.com/matiasbarrios/magical-mixers) for effect parameters specification (though they have been corrected a little, see fx_types/types).
