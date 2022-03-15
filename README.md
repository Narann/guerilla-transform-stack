# guerilla-transform-stack

`guerilla_transform_stack` is a Python package to manipulate Guerilla transform
stack as Python object.

This package expose `TransformStack`, a wrapper class around the Guerilla
transform stack of a scene graph node.

## Usage

The first step is to wrap the Guerilla node with `TransformStack` class:  

```pycon
>>> import guerilla
>>> import guerilla_transform_stack as gts
>>> node = guerilla.pynode('mynode')
>>> node_ts = gts.TransformStack(node)
>>> node_ts
TransformStack('mynode')
```

Then you can add, access and manipulate transforms:

```pycon
>>> node_ts.is_empty
True
>>> euler = node_ts.add('euler')  # Create an euler transform.
>>> euler
TransformEuler('mynode|Euler')
>>> node_ts['Euler']  # Access transform from its name.
TransformEuler('mynode|Euler')
>>> target = node_ts.add('target')
>>> target.is_on_top  # New transform nodes are added on top.
True
>>> len(node_ts)  # Get transform count.
2
>>> target.move_down()
>>> target.move_up()
>>> node_ts.top
TransformTarget('mynode|Target')
>>> euler_tmp = node_ts.add('euler')
>>> euler_tmp.delete()  # Remove transform.
```

Transform stack object can be iterated (from bottom to top):

```pycon
>>> for transform in node_ts:
...   print transform
...
TransformEuler('mynode|Euler')
TransformTarget('mynode|Target')
```

Original Guerilla node is accessible with the `node` property:

```pycon
>>> node_ts.node
<guerilla.SceneGraphNode object at 0x7f34498eb490>
```
