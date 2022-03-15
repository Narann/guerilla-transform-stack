"""
This module contains transform types.
"""
import math

import guerilla


def get_top_transform_plug(node):
    """Return input plug of the top transform node.

    Args:
        node (guerilla.SceneGraphNode): Parent scene graph node.

    Returns:
        guerilla.Plug:
    """
    # Get transform node on the top of the stack
    # In.Euler2.Out -> In.Euler1.Out -> Transform.node. (Return Euler2.Out).
    cur_plug = node.Transform

    while True:

        in_plug = cur_plug.getinput()

        if in_plug:
            cur_plug = in_plug.parent.In
        else:
            break

    return cur_plug


class Transform(object):
    """Base class representing a Guerilla transform node.

    Should not be instantiated.
    """
    def __init__(self, node=None):
        """

        Args:
            node (guerilla.Transform): Transform Guerilla node to wrap.
        """
        self.node = node

    def __repr__(self):
        return "{}('{}')".format(self.__class__.__name__, self.node.path)

    def __eq__(self, other):
        if isinstance(other, Transform):
            return self.node.path == other.node.path
        else:
            return False

    def __ne__(self, other):
        return self.node.path != other.node.path

    @staticmethod
    def _default_name():
        """Default Guerilla transform node name when created.

        This name is used at transform node creation, when no name is provided.

        Returns:
            str: Default Guerilla transform node name when created.
        """
        raise NotImplementedError

    @staticmethod
    def type_name():
        """type name ('euler', 'target', 'baked', 'constraint', 'shake').

        Returns:
            str: Type name.
        """
        raise NotImplementedError

    @staticmethod
    def guerilla_type_name():
        """Guerilla lua class name ('TransformEuler', 'TransformTarget', etc).

        Returns:
            str: Guerilla lua class name.
        """
        raise NotImplementedError

    @classmethod
    def create(cls, node, mod, name=None):
        """Create default typed transform on given Guerilla `node`.

        Args:
            node (guerilla.SceneGraphNode): Parent scene graph node.
            mod (guerilla.Modifier):
            name (str, optional): Transform node name.

        Returns:
            Transform: The created transform object.
        """
        if name is None:
            name = cls._default_name()

        transform_node = mod.createnode(name, cls.guerilla_type_name(), node)

        top_plug = get_top_transform_plug(node)

        mod.connect(top_plug, transform_node.Out)

        return cls(transform_node)

    def move_up(self):
        """Move Guerilla transform up.
        """
        self.node.moveup()

    def move_down(self):
        """Move Guerilla transform down.
        """
        self.node.movedown()

    def move_top(self):
        """Move Guerilla transform on top.
        """
        while not self.is_on_top:
            self.node.movetop()

    def move_bottom(self):
        """Move Guerilla transform on bottom.
        """
        while not self.is_on_bottom:
            self.node.movedown()

    @property
    def is_alone(self):
        """Return if transform is alone.

        Returns:
            bool: True if transform is alone.
        """
        return self.is_on_top and self.is_on_bottom

    @property
    def is_on_top(self):
        """Return if transform is on top.

        Returns:
            bool: True if transform is on top.
        """
        return self.node.In.get() is None

    @property
    def is_on_bottom(self):
        """Return if transform is on bottom.

        Returns:
            bool: True if transform is on bottom.
        """
        return any(out_plug.name == 'Transform'
                   for out_plug in self.node.Out.getoutputs())

    @property
    def is_on_middle(self):
        """Return if transform is in between top and bottom transform.

        Returns:
            bool: True if transform is between top and bottom transform.
        """
        return (self.node.In.getinput() is not None and
                all(out_plug.name != 'Transform'
                    for out_plug in self.node.Out.getoutputs()))

    def delete(self):
        """Delete Guerilla transform node.

        After calling `delete()`, `node` property is set to `None`.
        """
        self.node.delete()


class TransformEuler(Transform):
    """class representing a Guerilla euler transform node.
    """

    @staticmethod
    def _default_name():
        return "Euler"

    @staticmethod
    def type_name():
        return 'euler'

    @staticmethod
    def guerilla_type_name():
        return 'TransformEuler'

    @classmethod
    def create(cls, node, mod, name=None):
        """Create default euler transform on given Guerilla `node`.

        Args:
            node (guerilla.SceneGraphNode): Parent scene graph node.
            mod (guerilla.Modifier):
            name (str, optional): Transform node name.

        Returns:
            Transform: The created euler transform object.
        """
        if name is None:
            name = cls._default_name()

        transform_node = mod.createnode(name, cls.guerilla_type_name(), node)

        # If node has no transform, create transform from current
        # transformation.
        if node.Transform.getinput() is None:

            (sx, sy, sz,
             rx, ry, rz,
             tx, ty, tz) = node.getmatrix().decompose()

            transform_node.SX.set(sx)
            transform_node.SY.set(sy)
            transform_node.SZ.set(sz)
            transform_node.RX.set((rx*180.0)/math.pi)
            transform_node.RY.set((ry*180.0)/math.pi)
            transform_node.RZ.set((rz*180.0)/math.pi)
            transform_node.TX.set(tx)
            transform_node.TY.set(ty)
            transform_node.TZ.set(tz)

        # Get transform node on the top of the stack
        top_plug = get_top_transform_plug(node)

        mod.connect(top_plug, transform_node.Out)

        return cls(transform_node)


class TransformTarget(Transform):
    """class representing a Guerilla target transform node.
    """

    @staticmethod
    def _default_name():
        return "Target"

    @staticmethod
    def type_name():
        return 'target'

    @staticmethod
    def guerilla_type_name():
        return 'TransformTarget'

    @classmethod
    def create(cls, node, mod, name=None):
        """Create default target transform on given Guerilla `node`.

        Args:
            node (guerilla.SceneGraphNode): Parent scene graph node.
            mod (guerilla.Modifier):
            name (str, optional): Transform node name.

        Returns:
            Transform: The created target transform object.
        """
        if name is None:
            name = cls._default_name()

        transform_node = mod.createnode(name, cls.guerilla_type_name(), node)

        target_node = mod.createnode(transform_node.path.replace('|', ''),
                                     'Target', guerilla.Document())

        top_plug = get_top_transform_plug(node)

        # Offset target one in Z.
        mtx = top_plug.parent.getmatrix()
        transform = guerilla.transform(mtx.asarray())
        transform.translate(guerilla.point3(0.0, 0.0, 1.0))
        target_node.Transform.set(transform)

        mod.connect(transform_node.TargetWorldTransform,
                    target_node._WorldTransform)

        mod.connect(top_plug, transform_node.Out)

        return cls(transform_node)

    @property
    def target(self):
        """Return the target node connected to the transform.

        Returns:
            guerilla.Node:
        """
        return self.node.TargetWorldTransform.getinput().parent


class TransformBaked(Transform):
    """class representing a Guerilla baked transform node.
    """

    @staticmethod
    def _default_name():
        return "Baked"

    @staticmethod
    def type_name():
        return 'baked'

    @staticmethod
    def guerilla_type_name():
        return 'TransformBaked'


class TransformConstraint(Transform):
    """class representing a Guerilla constraint transform node.
    """

    @staticmethod
    def _default_name():
        return "Constraint"

    @staticmethod
    def type_name():
        return 'constraint'

    @staticmethod
    def guerilla_type_name():
        return 'TransformConstraint'

    def clear(self):
        """Clear list of constraining objects (like 'Clear' button).
        """
        self.node.Objects.removealldependencies()

    def add(self, node):
        """Add given node as a constraint to transform (like 'Add' button).

        Args:
            node (guerilla.SceneGraphNode): Node to add as constraint.
        """
        self.node.createplug("Weight{}".format(node.path.replace('|', '')),
                             "ConstraintTransformWeightPlug",
                             guerilla.types('float', desc={'min': 0,
                                                           'max': 1}),
                             4,
                             1)
        self.node.Objects.adddependency(node.Transform)


class TransformShake(Transform):
    """class representing a Guerilla constraint transform node.
    """

    @staticmethod
    def _default_name():
        return "Shake"

    @staticmethod
    def type_name():
        return 'shake'

    @staticmethod
    def guerilla_type_name():
        return 'TransformShake'
