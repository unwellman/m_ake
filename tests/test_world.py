import pytest
import m_ake as mk
from m_ake.file_io import world
import yaml
import jax.numpy as jnp

parabola = """
id: parabola
shape: parametric
material: white
data:
    x: t
    y: t**2/16
    parameter: [-32, 32]
    scale: 8
    arc_sample: 1000
    cycle: False
"""

def test_spline_parabola ():
    dct = yaml.load(parabola, Loader=yaml.Loader)
    points = world.World_importer.spline(dct)
    assert points[:, 0] == pytest.approx(jnp.array([-32, 64]))
    assert points[:, -1] == pytest.approx(jnp.array([32, 64]))

circle = """
id: circle
shape: parametric
material: white
data:
    x: 32*jnp.cos(jnp.pi*t)
    y: 32*jnp.sin(jnp.pi*t)
    parameter: [0, 2]
    scale: 8
    arc_sample: 1000
    cycle: True
"""
def test_spline_circle ():
    """
    Note that you shouldn't actually use spline this way---there will be
    a dedicated circle primitive that is much more performant. This is mostly
    just a test of the cycle attribute.
    """
    dct = yaml.load(circle, Loader=yaml.Loader)
    points = world.World_importer.spline(dct)
    assert points[:, 0] == pytest.approx(jnp.array([32, 0]))
    assert points[:, -1] == pytest.approx(jnp.array([32, 0]))

def test_materials ():
    pass

def test_geometry ():
    pass

def test_world_import ():
    pass

