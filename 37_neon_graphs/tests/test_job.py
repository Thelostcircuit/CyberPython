import tempfile
import unittest
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from numpy.testing import assert_allclose  # noqa: E402

import job  # noqa: E402


class NeonGraphs(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_pulse_chart(self):
        t = np.linspace(0, 1, 50)
        fig = job.pulse_chart(t, np.sin(t), "Wing C")
        ax = fig.axes[0]
        self.assertEqual((ax.get_title(), ax.get_xlabel(), ax.get_ylabel()), ("Wing C", "t (s)", "activity"))
        assert_allclose(ax.lines[0].get_ydata(), np.sin(t))

    def test_wing_bars(self):
        ax = job.wing_bars({"C": 9402, "A": 120, "B": 77}).axes[0]
        self.assertEqual([p.get_height() for p in ax.patches], [9402, 120, 77])
        fig = ax.figure
        fig.canvas.draw()
        self.assertEqual([t.get_text() for t in ax.get_xticklabels()], ["C", "A", "B"])

    def test_hot_scatter(self):
        ax = job.hot_scatter([1, 2, 3, 4], [10, 80, 20, 95], 70).axes[0]
        self.assertEqual([t.get_text() for t in ax.get_legend().get_texts()], ["normal", "hot"])
        normal, hot = ax.collections
        assert_allclose(normal.get_offsets(), [[1, 10], [3, 20]])
        assert_allclose(hot.get_offsets(), [[2, 80], [4, 95]])

    def test_panels(self):
        fig = job.panels({"temp": [1, 2], "power": [3, 4], "pulse": [5, 6]})
        self.assertEqual([ax.get_title() for ax in fig.axes], ["temp", "power", "pulse"])
        self.assertTrue(fig.axes[0].get_shared_x_axes().joined(fig.axes[0], fig.axes[2]))
        single = job.panels({"only": [1, 2, 3]})
        self.assertEqual(single.axes[0].get_title(), "only")

    def test_hist(self):
        fig, counts = job.activity_hist([0.1, 0.2, 0.25, 0.9, 0.95, 0.99], 2)
        self.assertEqual(counts, [3, 3])
        self.assertTrue(all(type(c) is int for c in counts))
        self.assertEqual(len(fig.axes[0].patches), 2)

    def test_annotate(self):
        ax = job.annotate_peak([0, 1, 2, 3], [1, 5, 2, 0]).axes[0]
        notes = [t for t in ax.texts if t.get_text() == "peak"]
        self.assertEqual(len(notes), 1)
        self.assertEqual(tuple(notes[0].xy), (1, 5))

    def test_heatmap(self):
        m = np.arange(12).reshape(3, 4)
        fig = job.rack_heatmap(m)
        self.assertEqual(len(fig.axes), 2)
        self.assertEqual(fig.axes[0].images[0].get_array().shape, (3, 4))
        self.assertEqual(fig.axes[0].images[0].get_cmap().name, "magma")

    def test_save_png(self):
        fig, ax = plt.subplots(figsize=(4, 2))
        ax.plot([1, 2])
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "report.png"
            self.assertEqual(job.save_png(fig, p, 50), (200, 100))
            self.assertEqual(p.read_bytes()[:8], b"\x89PNG\r\n\x1a\n")


if __name__ == "__main__":
    unittest.main()
