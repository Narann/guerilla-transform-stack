from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

import guerilla

from .transform import (TransformEuler,
                        TransformTarget,
                        TransformBaked,
                        TransformConstraint,
                        TransformShake)


def iter_transforms(node):

    cur_plug = node.Transform

    while True:

        in_plug = cur_plug.getinput()

        if in_plug:
            node = in_plug.parent
            yield node
        else:
            raise StopIteration

        cur_plug = node.In


# All transform classes.
all_cls = (TransformEuler,
           TransformTarget,
           TransformBaked,
           TransformConstraint,
           TransformShake)

# Name to class relation of transform type name.
type_name_to_class = {cls.type_name(): cls
                      for cls in all_cls}

# Guerilla type name to class relation.
guerilla_type_name_to_class = {cls.guerilla_type_name(): cls
                               for cls in all_cls}


class TransformStack(object):
    """Main class representing the transform stack of a Guerilla node.

    Transform stack is represented like this:

    Euler4  <- Top
    Euler3  <-.- Middle
    Euler2  <-'
    Euler1  <- Bottom
    Node

    Iterator go from Euler1 to Euler4.
    """

    def __init__(self, node):
        """

        Args:
            node (guerilla.SceneGraphNode): Parent scene graph node.
        """
        self.node = node

    def __repr__(self):
        return "{}('{}')".format(self.__class__.__name__, self.node.path)

    def __getitem__(self, item):
        try:
            return next((t for t in self
                         if t.node.name == item))
        except StopIteration:
            raise KeyError("no Guerilla transform node with given name")

    def __iter__(self):
        """Iterate over transforms in a bottom to top order.

        Yields:
            Transform:
        """
        in_plug = self.node.Transform.getinput()

        while in_plug:

            cur_node = in_plug.parent

            yield self._node_to_transform(cur_node)

            in_plug = cur_node.In.getinput()

    def __len__(self):

        i = 0

        in_plug = self.node.Transform.getinput()

        while in_plug:

            i += 1

            in_plug = in_plug.parent.In.getinput()

        return i

    @staticmethod
    def __node_to_class(node):
        """Return transform class from Guerilla transform node.

        Args:
            node (guerilla.Transform): Guerilla transform node.

        Returns:
            type: Transform class to instantiate transform object.
        """
        class_name = guerilla.getclassname(node)

        try:
            return guerilla_type_name_to_class[class_name]
        except KeyError:
            raise TypeError("invalid Guerilla transform type '{}'"
                            .format(class_name))

    def _node_to_transform(self, node):
        """Return transform object from Guerilla transform node.

        Args:
            node (guerilla.Transform): Guerilla transform node.

        Returns:
            Transform: Transform object.
        """
        return self.__node_to_class(node)(node)

    def add(self, type_, name=None):
        """Add Guerilla transform node with given `type_`.

        Args:
            type_ (str): Transform type ('euler', 'target', 'baked',
              'contraint', 'shake').
            name (str, optional): Guerilla transform node name.

        Returns:
            Transform:
        """
        try:
            cls = type_name_to_class[type_]
        except KeyError:
            raise ValueError("invalid transform type argument")

        with guerilla.Modifier() as mod:
            return cls.create(self.node, mod, name)

    @property
    def top(self):
        """Return the transformation node at the top of the stack.

        Returns:
            Transform: Transformation node at the top of the stack.

        Raises:
            ValueError: If transform stack is empty.
        """
        transform_node = self.node.gettransform()

        if transform_node.path == self.node.path:
            raise ValueError("transform stack is empty for node '{}'"
                             .format(self.node.path))

        return self._node_to_transform(transform_node)

    @property
    def bottom(self):
        """Return the transformation node at the bottom of the stack.

        Returns:
            Transform: Transformation node at the bottom of the stack.

        Raises:
            ValueError: If transform stack is empty.
        """
        cur_plug = self.node.Transform

        in_plug = cur_plug.getinput()

        if in_plug is None:
            raise ValueError("transform stack is empty for node '{}'"
                             .format(self.node.path))

        return self._node_to_transform(in_plug.parent)

    @property
    def is_empty(self):
        """Return if transform stack is empty.

        Returns:
            bool: True if transform stack is empty.
        """
        return self.node.gettransform().path == self.node.path
