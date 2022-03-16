"""
This module is means to be executed inside Guerilla.
"""

import unittest


class TestGuerillaTransformStack(unittest.TestCase):

    def test_all(self):

        import guerilla
        import guerilla_transform_stack as gts

        with guerilla.Modifier() as mod:
            foo_node = mod.createnode("FOO", "SceneGraphNode")

        ts = gts.TransformStack(foo_node)

        self.assertIs(ts.node, foo_node)
        self.assertEqual(len(ts), 0)
        self.assertTrue(ts.is_empty)

        with self.assertRaises(ValueError):
            _ = ts.top

        with self.assertRaises(ValueError):
            _ = ts.bottom

        t_euler1 = ts.add('euler', "my_euler1")

        self.assertEqual(len(ts), 1)
        self.assertEqual(ts["my_euler1"], t_euler1)
        self.assertEqual(ts.top, t_euler1)
        self.assertEqual(ts.bottom, t_euler1)
        self.assertFalse(ts.is_empty)

        self.assertIsInstance(t_euler1, gts.transform_stack.TransformEuler)
        self.assertEqual(t_euler1.node.name, "my_euler1")
        self.assertTrue(t_euler1.is_alone)
        self.assertTrue(t_euler1.is_on_top)
        self.assertTrue(t_euler1.is_on_bottom)
        self.assertFalse(t_euler1.is_on_middle)

        self.assertTrue(list(ts), [t_euler1])

        t_euler2 = ts.add('euler', "my_euler2")

        self.assertEqual(len(ts), 2)
        self.assertEqual(ts["my_euler2"], t_euler2)
        self.assertEqual(ts.top, t_euler2)
        self.assertEqual(ts.bottom, t_euler1)
        self.assertFalse(ts.is_empty)

        self.assertIsInstance(t_euler2, gts.transform_stack.TransformEuler)
        self.assertEqual(t_euler2.node.name, "my_euler2")
        self.assertFalse(t_euler2.is_alone)
        self.assertTrue(t_euler2.is_on_top)
        self.assertFalse(t_euler2.is_on_bottom)
        self.assertFalse(t_euler2.is_on_middle)

        self.assertFalse(t_euler1.is_on_top)
        self.assertTrue(t_euler1.is_on_bottom)
        self.assertFalse(t_euler1.is_on_middle)

        self.assertTrue(list(ts), [t_euler1, t_euler2])

        t_euler3 = ts.add('euler', "my_euler3")

        self.assertEqual(len(ts), 3)
        self.assertEqual(ts["my_euler3"], t_euler3)
        self.assertEqual(ts.top, t_euler3)
        self.assertEqual(ts.bottom, t_euler1)
        self.assertFalse(ts.is_empty)

        self.assertIsInstance(t_euler3, gts.transform_stack.TransformEuler)
        self.assertEqual(t_euler3.node.name, "my_euler3")
        self.assertFalse(t_euler3.is_alone)
        self.assertTrue(t_euler3.is_on_top)
        self.assertFalse(t_euler3.is_on_bottom)
        self.assertFalse(t_euler3.is_on_middle)

        self.assertFalse(t_euler2.is_on_top)
        self.assertFalse(t_euler2.is_on_bottom)
        self.assertTrue(t_euler2.is_on_middle)

        self.assertFalse(t_euler1.is_on_top)
        self.assertTrue(t_euler1.is_on_bottom)
        self.assertFalse(t_euler1.is_on_middle)

        self.assertTrue(list(ts), [t_euler1, t_euler2, t_euler3])

    def test_target(self):

        import guerilla
        import guerilla_transform_stack as gts

        with guerilla.Modifier() as mod:
            foo_node = mod.createnode("FOOTarget", "SceneGraphNode")

        ts = gts.TransformStack(foo_node)

        self.assertIs(ts.node, foo_node)
        self.assertEqual(len(ts), 0)
        self.assertTrue(ts.is_empty)

        with self.assertRaises(ValueError):
            _ = ts.top

        with self.assertRaises(ValueError):
            _ = ts.bottom

        t_target1 = ts.add('target', "my_target1")

        self.assertEqual(len(ts), 1)
        self.assertEqual(ts["my_target1"], t_target1)
        self.assertEqual(ts.top, t_target1)
        self.assertEqual(ts.bottom, t_target1)
        self.assertFalse(ts.is_empty)

        self.assertIsInstance(t_target1, gts.transform_stack.TransformTarget)
        self.assertEqual(t_target1.node.name, "my_target1")
        self.assertEqual(t_target1.target.name, "FOOTargetmy_target1")
        self.assertTrue(t_target1.is_alone)
        self.assertTrue(t_target1.is_on_top)
        self.assertTrue(t_target1.is_on_bottom)
        self.assertFalse(t_target1.is_on_middle)

        self.assertTrue(list(ts), [t_target1])

        t_target2 = ts.add('target', "my_target2")

        self.assertEqual(len(ts), 2)
        self.assertEqual(ts["my_target2"], t_target2)
        self.assertEqual(ts.top, t_target2)
        self.assertEqual(ts.bottom, t_target1)
        self.assertFalse(ts.is_empty)

        self.assertIsInstance(t_target2, gts.transform_stack.TransformTarget)
        self.assertEqual(t_target2.node.name, "my_target2")
        self.assertEqual(t_target2.target.name, "FOOTargetmy_target2")
        self.assertFalse(t_target2.is_alone)
        self.assertTrue(t_target2.is_on_top)
        self.assertFalse(t_target2.is_on_bottom)
        self.assertFalse(t_target2.is_on_middle)

        self.assertFalse(t_target1.is_on_top)
        self.assertTrue(t_target1.is_on_bottom)
        self.assertFalse(t_target1.is_on_middle)

        self.assertTrue(list(ts), [t_target1, t_target2])

    def test_baked(self):

        import guerilla
        import guerilla_transform_stack as gts

        with guerilla.Modifier() as mod:
            foo_node = mod.createnode("FOOBaked", "SceneGraphNode")

        ts = gts.TransformStack(foo_node)

        self.assertIs(ts.node, foo_node)
        self.assertEqual(len(ts), 0)
        self.assertTrue(ts.is_empty)

        with self.assertRaises(ValueError):
            _ = ts.top

        with self.assertRaises(ValueError):
            _ = ts.bottom

        t_baked1 = ts.add('baked', "my_baked1")

        self.assertEqual(len(ts), 1)
        self.assertEqual(ts["my_baked1"], t_baked1)
        self.assertEqual(ts.top, t_baked1)
        self.assertEqual(ts.bottom, t_baked1)
        self.assertFalse(ts.is_empty)

        self.assertIsInstance(t_baked1, gts.transform_stack.TransformBaked)
        self.assertEqual(t_baked1.node.name, "my_baked1")
        self.assertTrue(t_baked1.is_alone)
        self.assertTrue(t_baked1.is_on_top)
        self.assertTrue(t_baked1.is_on_bottom)
        self.assertFalse(t_baked1.is_on_middle)

        self.assertTrue(list(ts), [t_baked1])

        t_baked2 = ts.add('baked', "my_baked2")

        self.assertEqual(len(ts), 2)
        self.assertEqual(ts["my_baked2"], t_baked2)
        self.assertEqual(ts.top, t_baked2)
        self.assertEqual(ts.bottom, t_baked1)
        self.assertFalse(ts.is_empty)

        self.assertIsInstance(t_baked2, gts.transform_stack.TransformBaked)
        self.assertEqual(t_baked2.node.name, "my_baked2")
        self.assertFalse(t_baked2.is_alone)
        self.assertTrue(t_baked2.is_on_top)
        self.assertFalse(t_baked2.is_on_bottom)
        self.assertFalse(t_baked2.is_on_middle)

        self.assertFalse(t_baked1.is_on_top)
        self.assertTrue(t_baked1.is_on_bottom)
        self.assertFalse(t_baked1.is_on_middle)

        self.assertTrue(list(ts), [t_baked1, t_baked2])

    def test_constraint(self):

        import guerilla
        import guerilla_transform_stack as gts

        with guerilla.Modifier() as mod:
            foo_node = mod.createnode("FOOConstraint", "SceneGraphNode")
            constraint_node = mod.createnode("FOOConstraintNode",
                                             "SceneGraphNode")

        ts = gts.TransformStack(foo_node)

        self.assertIs(ts.node, foo_node)
        self.assertEqual(len(ts), 0)
        self.assertTrue(ts.is_empty)

        with self.assertRaises(ValueError):
            _ = ts.top

        with self.assertRaises(ValueError):
            _ = ts.bottom

        t_constraint1 = ts.add('constraint', "my_constraint1")

        self.assertEqual(len(ts), 1)
        self.assertEqual(ts["my_constraint1"], t_constraint1)
        self.assertEqual(ts.top, t_constraint1)
        self.assertEqual(ts.bottom, t_constraint1)
        self.assertFalse(ts.is_empty)

        self.assertIsInstance(t_constraint1,
                              gts.transform_stack.TransformConstraint)
        self.assertEqual(t_constraint1.node.name, "my_constraint1")
        self.assertTrue(t_constraint1.is_alone)
        self.assertTrue(t_constraint1.is_on_top)
        self.assertTrue(t_constraint1.is_on_bottom)
        self.assertFalse(t_constraint1.is_on_middle)

        self.assertTrue(list(ts), [t_constraint1])

        t_constraint2 = ts.add('constraint', "my_constraint2")

        self.assertEqual(len(ts), 2)
        self.assertEqual(ts["my_constraint2"], t_constraint2)
        self.assertEqual(ts.top, t_constraint2)
        self.assertEqual(ts.bottom, t_constraint1)
        self.assertFalse(ts.is_empty)

        self.assertIsInstance(t_constraint2,
                              gts.transform_stack.TransformConstraint)
        self.assertEqual(t_constraint2.node.name, "my_constraint2")
        self.assertFalse(t_constraint2.is_alone)
        self.assertTrue(t_constraint2.is_on_top)
        self.assertFalse(t_constraint2.is_on_bottom)
        self.assertFalse(t_constraint2.is_on_middle)

        self.assertFalse(t_constraint1.is_on_top)
        self.assertTrue(t_constraint1.is_on_bottom)
        self.assertFalse(t_constraint1.is_on_middle)

        self.assertTrue(list(ts), [t_constraint1, t_constraint2])

        t_constraint1.add(constraint_node)

        # Ensure constrained node follow constraint.
        id_mtx = guerilla.matrix()
        mtx = guerilla.matrix.createcomposite(0.4, 0.5, 0.6,
                                              10, 20, 30,
                                              1, 2, 3)

        # Same as identity matrix (world center).
        for a, b in zip(ts.node.getworldmatrix().asarray(), id_mtx.asarray()):
            self.assertAlmostEqual(a, b, places=6)

        for a, b in zip(constraint_node.getworldmatrix().asarray(),
                        id_mtx.asarray()):
            self.assertAlmostEqual(a, b, places=6)

        # Move constraint node.
        constraint_node.setworldmatrix(mtx)

        for a, b in zip(ts.node.getworldmatrix().asarray(), mtx.asarray()):
            self.assertAlmostEqual(a, b, places=6)

        ts.node.setworldmatrix(id_mtx)  # Ensure node don't move.

        for a, b in zip(ts.node.getworldmatrix().asarray(), mtx.asarray()):
            self.assertAlmostEqual(a, b, places=6)

        t_constraint1.clear()

        for a, b in zip(ts.node.getworldmatrix().asarray(), id_mtx.asarray()):
            self.assertAlmostEqual(a, b, places=6)

    def test_shake(self):

        import guerilla
        import guerilla_transform_stack as gts

        with guerilla.Modifier() as mod:
            foo_node = mod.createnode("FOOShake", "SceneGraphNode")

        ts = gts.TransformStack(foo_node)

        self.assertIs(ts.node, foo_node)
        self.assertEqual(len(ts), 0)
        self.assertTrue(ts.is_empty)

        with self.assertRaises(ValueError):
            _ = ts.top

        with self.assertRaises(ValueError):
            _ = ts.bottom

        t_shake1 = ts.add('shake', "my_shake1")

        self.assertEqual(len(ts), 1)
        self.assertEqual(ts["my_shake1"], t_shake1)
        self.assertEqual(ts.top, t_shake1)
        self.assertEqual(ts.bottom, t_shake1)
        self.assertFalse(ts.is_empty)

        self.assertIsInstance(t_shake1,
                              gts.transform_stack.TransformShake)
        self.assertEqual(t_shake1.node.name, "my_shake1")
        self.assertTrue(t_shake1.is_alone)
        self.assertTrue(t_shake1.is_on_top)
        self.assertTrue(t_shake1.is_on_bottom)
        self.assertFalse(t_shake1.is_on_middle)

        self.assertTrue(list(ts), [t_shake1])

        t_shake2 = ts.add('shake', "my_shake2")

        self.assertEqual(len(ts), 2)
        self.assertEqual(ts["my_shake2"], t_shake2)
        self.assertEqual(ts.top, t_shake2)
        self.assertEqual(ts.bottom, t_shake1)
        self.assertFalse(ts.is_empty)

        self.assertIsInstance(t_shake2,
                              gts.transform_stack.TransformShake)
        self.assertEqual(t_shake2.node.name, "my_shake2")
        self.assertFalse(t_shake2.is_alone)
        self.assertTrue(t_shake2.is_on_top)
        self.assertFalse(t_shake2.is_on_bottom)
        self.assertFalse(t_shake2.is_on_middle)

        self.assertFalse(t_shake1.is_on_top)
        self.assertTrue(t_shake1.is_on_bottom)
        self.assertFalse(t_shake1.is_on_middle)

        self.assertTrue(list(ts), [t_shake1, t_shake2])


def test():
    suite = unittest.TestSuite()

    for attr in dir(TestGuerillaTransformStack):
        if attr.startswith('test_'):
            suite.addTest(TestGuerillaTransformStack(attr))

    runner = unittest.TextTestRunner()
    runner.run(suite)

    # unittest.main(exit=False)
