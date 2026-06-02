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

## Mixer Architecture

### Strip

A **strip** is the fundamental mixer element.

Every strip represents a signal-processing path with a common set of properties such as:

- Name, color
- Mute
- Fader level
- Routing controls
- DSP blocks (where supported by the hardware)

All mixer elements derive from the Strip concept.

### Channel Strips

A **channel strip** is a strip that introduces a signal into the mixing engine and can distribute that signal to one or more buses through sends.

Channel strips are signal-producing paths rather than summing paths.

The following mixer elements are modeled as channel strips:

- Channels (mono)
- Aux Returns (stereo)
- FX Returns (stereo)

Although Aux Returns may be used for external inputs, they are labeled as a "return" because their processing behavior is much closer to FX Returns than to Channels.

### Bus Strips

A **bus strip** is a strip whose primary purpose is to collect and combine signals from multiple channel strips.

Bus strips are summing paths rather than signal-producing paths.

The following mixer elements are modeled as bus strips:

- Buses (mono, could be linked in stereo pairs)
- FX Sends (mono)
- Main LR (stereo)

### Mix sends

A **mix send** is a routing relationship between a channel strip and a bus strip.
Each send defines how much signal from a specific channel strip is contributed to a specific bus strip.

```text
Channel Strip 1 ──┐
Channel Strip 2 ──┼──► Bus Strip
Channel Strip 3 ──┘
```

Typical mix send parameters include:

- Level (fader)
- Mute
- Tap point (pre/post fader, where supported)

### Routing

Routing is separate from mixing.
While mix sends determine how signals are mixed in a path from channel strips to bus strips,
routing determines where signals originate and where they are delivered in those channel and bus strips.

- Channel strip signal sources (Ins) are configured in strips config, and strips preamp sections.
  One source could be routed to multiple channel strips.
  Possible sources:
  - Physical mixer input.
  - USB Return (USB in).
  - FX Return (fixed for fx return channel strips).
- All strip physical destinations (Outs) are configured in mixer's routing section.
  One strip could be routed to multiple destinations.
  Possible destinations:
  - Physical aux out (usually bound to buses, but can be bound to arbitrary source: channel or bus strips or even USB returns).
  - USB Send (USB out).
  - Ultranet out.
  - Main out (physical stereo)
  - Phones out (physical stereo out for monitoring)

## Acknowledgements

- [xair-api-python](https://github.com/onyx-and-iris/xair-api-python) for implementations insights.
- [magical-mixers](https://github.com/matiasbarrios/magical-mixers) for effect parameters specification (though they have been corrected a little, see fx_types/types).

## TODO

- Fix node and property description according to new terminology.
- Describe snapshot recall scope elements.
- Channel insert fx slots may conflict with each other. M Air checks for that. Maybe move insert props to the fx.
- RTA and meters
- Add installation steps to readme with UV.


## Useful resources

- [X AIR Mixer Series Remote Control Protocol](https://cdn-media.empowertribe.com/d63bb4c3a61942dda28f5ea5953d735d/M%20AIR%20Remote%20Control%20Protocol.pdf) - vague, nothing specific.
- [MR12/MR18 manual](https://www.bhphotovideo.com/lit_files/628199.pdf) with each effect description.
- [UNOFFICIAL X32/M32 OSC REMOTE PROTOCOL](https://www.academia.edu/9709659/UNOFFICIAL_X32_OSC_REMOTE_PROTOCOL) - all parameters spec for fxes.
