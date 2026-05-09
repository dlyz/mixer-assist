# X Air Assist

Works with X Air compatible Behringer/Midas mixers.

This project includes:

- MCP server to plug it to any AI agent, that can discover, read and change mixer parameters.
- REPL where you can do the same using console interface.
- xair_client python library, that you can use to write scripts with full type checker support, including autocompletion.

## Constraints

- Tested only on Midas MR-18 FW 1.25
- Not all available parameters and operations are implemented yet.
  See [OSC commands](https://behringer.world/wiki/doku.php?id=x-air_osc), not implemented: Action, Preferences, Snapshots, Status.
- Some descriptions may be inaccurate or inadequately precise for LLMs.
- At this stage, API is a subject to change.

## Acknowledgements

- [xair-api-python](https://github.com/onyx-and-iris/xair-api-python) for implementations insights.
- [magical-mixers](https://github.com/matiasbarrios/magical-mixers) for effect parameters specification (though they have been corrected a little, see fx_types/types).
