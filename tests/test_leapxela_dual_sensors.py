import numpy as np

from leapxela.fk_taxel import TAXEL_MAP_JSON, build_taxel_ids_in_fk_order
from leapxela.flex_force import fit_kelvin_voigt, kelvin_voigt_force
from leapxela.sensors import primary_source, resolve_heatmap_sources


def test_kelvin_voigt_force_matches_linear_model():
    displacement = np.array([[[1.0, -2.0, 3.0], [0.5, 0.25, -0.5]]])
    velocity = np.array([[[0.1, 0.2, -0.3], [1.0, -1.0, 0.0]]])
    stiffness = np.array([10.0, 20.0, 30.0])
    damping = np.array([0.5, 1.0, 1.5])

    force = kelvin_voigt_force(displacement, velocity, stiffness, damping)

    np.testing.assert_allclose(force, stiffness * displacement + damping * velocity)


def test_fit_kelvin_voigt_recovers_coefficients():
    rng = np.random.default_rng(0)
    displacement = rng.normal(size=(8, 4, 3))
    velocity = rng.normal(size=(8, 4, 3))
    expected_stiffness = np.array([4.0, 5.0, 6.0])
    expected_damping = np.array([0.1, 0.2, 0.3])
    force = expected_stiffness * displacement + expected_damping * velocity

    stiffness, damping = fit_kelvin_voigt(displacement, velocity, force, True)

    np.testing.assert_allclose(stiffness, expected_stiffness, atol=1e-10)
    np.testing.assert_allclose(damping, expected_damping, atol=1e-10)


def test_sparsh_fk_order_covers_hardware_taxels_once():
    order = build_taxel_ids_in_fk_order(TAXEL_MAP_JSON)

    assert order.shape == (368,)
    np.testing.assert_array_equal(np.sort(order), np.arange(368))


def test_sensor_mode_heatmap_resolution():
    assert primary_source("contact") == "contact"
    assert primary_source("sparsh") == "sparsh"
    assert primary_source("both") == "contact"
    assert resolve_heatmap_sources("both", "both") == ["contact", "sparsh"]
    assert resolve_heatmap_sources("sparsh", "primary") == ["sparsh"]
