# X Air Assist

Works with X Air compatible Behringer/Midas mixers.

This project includes:

- MCP server to plug it to any AI agent, that can discover, read and change mixer parameters.
- REPL where you can do the same using console interface.
- xair_client python library, that you can use to write scripts with full type checker support, including autocompletion.

Code is mostly written/rewritten by hand, only unimportant parts may be fully ai-generated.

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
  See [OSC commands](https://behringer.world/wiki/doku.php?id=x-air_osc), not implemented: Action, Preferences, Status.
  Also not implemented: automix, solo control.
- Some descriptions may be inaccurate or inadequately precise for LLMs.
- At this stage, API is a subject to change.

## Acknowledgements

- [xair-api-python](https://github.com/onyx-and-iris/xair-api-python) for implementations insights.
- [magical-mixers](https://github.com/matiasbarrios/magical-mixers) for effect parameters specification (though they have been corrected a little, see fx_types/types).

## TODO

- Fix reading old value after the write.
- Make terminology more consistent and compliant with industry.
  - Describe snapshot recall scope elements.
  - 'Path' term is used for internal OSC commands as well as for external api. That leads to confusion in the code and in some error messages that will mention internal paths.
  - Figure out how stereo/dual fx inserts work for one insert, for two inserts, for one stereo insert, for mono/stereo send/return. Update descriptions accordingly.
- Channel insert fx slots may conflict with each other. M Air checks for that. Maybe move insert props to the fx.
- Add installation steps to readme with UV.

## Useful resources

- [X AIR Mixer Series Remote Control Protocol](https://cdn-media.empowertribe.com/d63bb4c3a61942dda28f5ea5953d735d/M%20AIR%20Remote%20Control%20Protocol.pdf) - vague, nothing specific.
- [MR12/MR18 manual](https://www.bhphotovideo.com/lit_files/628199.pdf) with each effect description.
- [UNOFFICIAL X32/M32 OSC REMOTE PROTOCOL](https://www.academia.edu/9709659/UNOFFICIAL_X32_OSC_REMOTE_PROTOCOL) - all parameters spec for fxes.
