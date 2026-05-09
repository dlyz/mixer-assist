# x-air-mixer MCP

The mcp is designed to give access to agents (LLM) to the Behringer/Midas mixers to help users with configuration of the mixer.

## expand-node tool

Accepts a list of paths to required nodes (internal or leaf) and returns items for each requested path. If there are leaves (mixer parameters) in the node, includes their values.

The resulting text contains one block per requested path, in the same order as in the input list.
Blocks are separated by an empty line.

Result is a plain text, not a json.

Example of the result:

```text
/full/requested/path/to/the/node:
  - nodeA
  - nodeB
  - parameterC = 10
  - parameterD = 119
```

Example when path correspond to a single parameter:

```text
/full/requested/path/to/the/parameter/node = value_of_the_parameter
```

Example for multiple paths:

```text
/path/one:
  - nodeA
  - parameterB = 10

/path/two = 5.6
```

## describe-node tool

Similar to expand node, but also return full description of each node.
For leaves (parameters) full description consists of: current value, units, type, constraints, description.
If some element is absent, it is simply skipped.

Format of parameter:

```text
= {current_value}
{type}, in {units}, {constraints}
{description}
```

Example of the result:

```text
/full/requested/path/to/the/node:
  - nodeA
  - nodeB
  - parameterC = 5.6
    float, in dB, in range [-60, 10]
    some important parameter, use it in such case
  - parameterD = 119
      int
```

Example when path correspond to a single parameter:

```text
/full/requested/path/to/the/parameter/node = 5.6
float, in dB, in range [-60, 10]
some important parameter, use it in such case
```

## set-parameters tool

Sets new values to specified list of parameters. The argument is a list of objects with fields:

- `path`: requested parameter path
- `value`: new value

Example input:

```json
[
  { "path": "/channels/01/config/name", "value": "Lead Vox" },
  { "path": "/channels/01/mix/main_fader", "value": "-12.0" }
]
```

Ideally, use of this tool must be confirmed by the human.

The values are applied one by one in the original order.
After the value application, it's value is read back and will be returned in the results.
If there is an error applying some parameter, the tool execution is interrupted.

The results consists of the list of parameters from the with their actual values.
The list is either full or ends with an error.
If the exception is ValueError, IndexError and such, the message from the error is returned back, along with the suggestion to use corresponding describe-node tool to check for value constraints. Other types of exceptions considered as internal error, the error is fully logged and the returned result is a general message about internal error.

Result is a plain text, not a json.
Example of the interrupted result.

```text
/path/to/first/parameter = 17
/path/to/second/parameter = some_value

PARAMETER ASSIGNMENT INTERRUPTED
FAILED TO SET /path/to/third/parameter = 1000500
ERROR: value is invalid
SUGGESTION: ...
```
