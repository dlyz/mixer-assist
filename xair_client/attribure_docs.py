def get_class_attribute_docs(cls: type):
    import ast
    import inspect
    import textwrap
    from typing import cast

    docs: dict[str, str] = {}

    source = inspect.getsource(cls)
    tree = ast.parse(textwrap.dedent(source))
    class_def = cast(ast.ClassDef, tree.body[0])

    for i, node in enumerate(class_def.body):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    member_name = target.id

                    # is next one a string literal?
                    if i + 1 < len(class_def.body):
                        next_node = class_def.body[i + 1]
                        if isinstance(next_node, ast.Expr) and isinstance(next_node.value, ast.Constant):
                            if isinstance(next_node.value.value, str):
                                docs[member_name] = inspect.cleandoc(next_node.value.value)

    return docs
