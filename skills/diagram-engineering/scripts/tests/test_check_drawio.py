"""Draw.io structure, collisions and SVG checks; no editor or renderer runs."""

import base64
from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import subprocess
import sys
import unittest
import urllib.parse
import xml.etree.ElementTree as ET
import zlib

from _support import WorkspaceTestCase, load_script

checker = load_script("check_drawio")
SVG = "<svg xmlns='http://www.w3.org/2000/svg' width='10' height='10'><rect width='10' height='10'/></svg>"


def model():
    return ET.fromstring('<mxGraphModel><root><mxCell id="0"/><mxCell id="1" parent="0"/></root></mxGraphModel>')


def vertex(graph, cid="a", x=0, y=0, width=100, height=60, parent="1", style="rounded=0;", value="", **attributes):
    cell = ET.SubElement(graph.find("root"), "mxCell", id=cid, parent=parent,
                         vertex="1", style=style, value=value, **attributes)
    ET.SubElement(cell, "mxGeometry", x=str(x), y=str(y), width=str(width), height=str(height), **{"as": "geometry"})
    return cell


def edge(graph, source="a", target="b", style="edgeStyle=orthogonalEdgeStyle;rounded=0;"):
    cell = ET.SubElement(graph.find("root"), "mxCell", id="edge", parent="1", edge="1",
                         source=source, target=target, style=style)
    ET.SubElement(cell, "mxGeometry", relative="1", **{"as": "geometry"})
    return cell


def inspect(graph):
    errors, warnings = [], []
    totals = checker.check_model("page", graph, errors, warnings)
    return errors, warnings, totals


def svg_uri(svg=SVG):
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()


class DrawioTests(WorkspaceTestCase):
    def test_load_native_and_compressed_pages(self):
        graph = model()
        vertex(graph)
        serialized = ET.tostring(graph, encoding="unicode")
        raw = self.write("native.drawio", serialized)
        self.assertEqual(checker.load_models(raw)[0][0], "page-1")
        compressor = zlib.compressobj(wbits=-15)
        compressed = compressor.compress(urllib.parse.quote(serialized, safe="").encode()) + compressor.flush()
        wrapped = self.write("compressed.drawio", '<mxfile><diagram name="Compressed">'
                             + base64.b64encode(compressed).decode() + '</diagram></mxfile>')
        loaded = checker.load_models(wrapped)
        self.assertEqual(loaded[0][0], "Compressed")
        self.assertEqual(inspect(loaded[0][1])[0], [])

    def test_invalid_documents_and_empty_pages(self):
        for source in ("<wrong/>", "<mxfile/>", "<mxfile><diagram/></mxfile>", "<mxfile>"):
            with self.subTest(source=source):
                path = self.write("bad.drawio", source)
                with self.assertRaises((ValueError, ET.ParseError)):
                    checker.load_models(path)

    def test_valid_components_and_connected_edge(self):
        graph = model()
        vertex(graph)
        vertex(graph, "b", x=250)
        edge(graph)
        errors, warnings, totals = inspect(graph)
        self.assertEqual(errors, [])
        self.assertTrue(any("automatic routing" in warning for warning in warnings))
        self.assertEqual(totals[2], 1)

    def test_explicit_route_detects_component_and_estimated_label_collision(self):
        graph = model()
        vertex(graph, "a", x=0)
        vertex(graph, "b", x=400)
        vertex(graph, "obstacle", x=200)
        connection = edge(graph, style="edgeStyle=orthogonalEdgeStyle;rounded=0;exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
        connection.set("value", "Authentication")
        errors, warnings, _ = inspect(graph)
        self.assertEqual(errors, [])
        self.assertTrue(any("crosses component obstacle" in w for w in warnings), warnings)
        self.assertTrue(any("estimated edge label edge overlaps obstacle" in w for w in warnings), warnings)

    def test_estimated_edge_labels_overlap(self):
        graph = model()
        vertex(graph, "a")
        vertex(graph, "b", x=400)
        style = "edgeStyle=orthogonalEdgeStyle;rounded=0;exitX=1;exitY=0.5;entryX=0;entryY=0.5;"
        first = edge(graph, style=style)
        first.set("value", "First connection")
        second = edge(graph, style=style)
        second.set("id", "edge2")
        second.set("value", "Second connection")
        warnings = inspect(graph)[1]
        self.assertTrue(any("estimated edge labels overlap: edge and edge2" in w for w in warnings), warnings)

    def test_offset_edge_label_avoids_false_overlap(self):
        graph = model()
        vertex(graph, "a")
        vertex(graph, "b", x=400)
        style = "edgeStyle=orthogonalEdgeStyle;rounded=0;exitX=1;exitY=0.5;entryX=0;entryY=0.5;"
        first = edge(graph, style=style)
        first.set("value", "First connection")
        second = edge(graph, style=style)
        second.set("id", "edge2")
        second.set("value", "Second connection")
        ET.SubElement(second.find("mxGeometry"), "mxPoint", x="0", y="60", **{"as": "offset"})
        self.assertFalse(any("estimated edge labels overlap" in w for w in inspect(graph)[1]))

    def test_boundary_title_overlap_and_routes_in_both_skills(self):
        graph = model()
        vertex(graph, "frame", x=100, y=0, width=400, height=300,
               value="Network boundary", style="fillColor=none;dashed=1;align=left;verticalAlign=top;fontSize=14;", **{"data-role": "boundary"})
        vertex(graph, "caption", x=120, y=0, width=80, height=20, style="text;", value="Caption")
        vertex(graph, "a", x=0, y=0, width=30, height=30)
        vertex(graph, "b", x=400, y=0, width=30, height=30)
        route_style = "edgeStyle=none;noEdgeStyle=1;rounded=0;exitX=1;exitY=0.5;entryX=0;entryY=0.5;"
        first = edge(graph, style=route_style)
        first.set("value", "Connection to network")
        second = edge(graph, style=route_style)
        second.set("id", "edge2")
        warnings = inspect(graph)[1]
        self.assertTrue(any("boundary title frame overlaps edge label" in w for w in warnings), warnings)
        self.assertTrue(any("boundary title frame overlaps text caption" in w for w in warnings), warnings)
        self.assertTrue(any("edge edge crosses estimated boundary title frame" in w for w in warnings), warnings)
        self.assertTrue(any("edges edge and edge2 share a segment" in w for w in warnings), warnings)
        path = self.write("layout.drawio", ET.tostring(graph, encoding="unicode"))
        arch = Path(__file__).resolve().parents[3] / "architecture-documentation/scripts/check_drawio.py"
        result = subprocess.run([sys.executable, "-B", str(arch), str(path)], capture_output=True, text=True)
        self.assertIn("boundary title frame overlaps edge label", result.stdout)
        self.assertIn("edges edge and edge2 share a segment", result.stdout)

    def test_route_crossing_and_disjoint_routes(self):
        graph = model()
        vertex(graph, "a", x=0, y=100, width=20, height=20)
        vertex(graph, "b", x=400, y=100, width=20, height=20)
        vertex(graph, "c", x=200, y=0, width=20, height=20)
        vertex(graph, "d", x=200, y=200, width=20, height=20)
        first = edge(graph, style="edgeStyle=none;noEdgeStyle=1;exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
        second = edge(graph, source="c", target="d", style="edgeStyle=none;noEdgeStyle=1;exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
        second.set("id", "edge2")
        self.assertTrue(any("edges edge and edge2 cross" in w for w in inspect(graph)[1]))
        graph.find("root/mxCell[@id='c']/mxGeometry").set("x", "500")
        graph.find("root/mxCell[@id='d']/mxGeometry").set("x", "500")
        self.assertFalse(any("edges edge and edge2 cross" in w for w in inspect(graph)[1]))

    def test_layout_helpers_match_and_ignore_degenerate_segments(self):
        from layout_checks import _relationship
        self.assertIsNone(_relationship((1, 1), (1, 1), (1, 1), (1, 1)))
        scripts = Path(__file__).resolve().parents[1]
        other = scripts.parents[1] / "architecture-documentation/scripts/layout_checks.py"
        self.assertEqual((scripts / "layout_checks.py").read_bytes(), other.read_bytes())

    def test_duplicate_ids(self):
        graph = model()
        vertex(graph)
        vertex(graph)
        self.assertTrue(any("duplicated id" in error for error in inspect(graph)[0]))

    def test_missing_base_cells_and_vertices(self):
        graph = model()
        self.assertTrue(any("no vertices" in error for error in inspect(graph)[0]))
        graph.find("root").remove(graph.find("root/mxCell[@id='1']"))
        vertex(graph)
        self.assertTrue(any("base cells" in error for error in inspect(graph)[0]))

    def test_missing_parent(self):
        graph = model()
        vertex(graph, parent="missing")
        self.assertTrue(any("missing parent" in error for error in inspect(graph)[0]))

    def test_parent_cycle(self):
        graph = model()
        vertex(graph, "a", parent="b")
        vertex(graph, "b", parent="a")
        self.assertTrue(any("parent cycle" in error for error in inspect(graph)[0]))

    def test_nonfinite_negative_and_zero_geometry(self):
        for changes in ({"x": "nan"}, {"y": "inf"}, {"width": -1}, {"height": 0}, {"x": "bad"}):
            with self.subTest(changes=changes):
                graph = model()
                vertex(graph, **changes)
                self.assertTrue(inspect(graph)[0])

    def test_missing_geometry(self):
        graph = model()
        cell = vertex(graph)
        cell.remove(cell.find("mxGeometry"))
        self.assertTrue(any("no geometry" in error for error in inspect(graph)[0]))

    def test_edge_endpoints_must_resolve_to_vertices(self):
        for target in ("missing", "0", ""):
            with self.subTest(target=target):
                graph = model()
                vertex(graph)
                edge(graph, target=target)
                self.assertTrue(any("target must resolve" in error for error in inspect(graph)[0]))

    def test_overlapping_components(self):
        graph = model()
        vertex(graph)
        vertex(graph, "b", x=20)
        self.assertTrue(any("components overlap" in error for error in inspect(graph)[0]))

    def test_nested_relative_geometry_uses_each_ancestor_once(self):
        graph = model()
        vertex(graph, "outer", x=100, y=100, width=500, height=500)
        vertex(graph, "inner", x=50, y=50, width=300, height=300, parent="outer")
        cell = vertex(graph, "child", x=0.5, y=0.5, width=40, height=40, parent="inner")
        cell.find("mxGeometry").set("relative", "1")
        ET.SubElement(cell.find("mxGeometry"), "mxPoint", x="5", y="5", **{"as": "offset"})
        # Correct absolute child position is 305,305. A double-counted ancestor
        # would cause a false outside-parent error or miss the collision here.
        vertex(graph, "obstacle", x=310, y=310, width=30, height=30)
        errors = inspect(graph)[0]
        self.assertFalse(any("outside parent" in error for error in errors))
        self.assertTrue(any("components overlap" in error for error in errors))

    def test_parent_containment_and_anchor_exception(self):
        graph = model()
        vertex(graph, "parent", width=100, height=100)
        child = vertex(graph, "child", x=90, width=40, height=40, parent="parent")
        self.assertTrue(any("outside parent" in error for error in inspect(graph)[0]))
        child.set("data-role", "anchor")
        self.assertEqual(inspect(graph)[0], [])

    def test_provider_markup_counts_for_all_four_vendors(self):
        graph = model()
        for index, shape in enumerate(("mxgraph.aws4.lambda", "mxgraph.azure.function", "mxgraph.gcp2.compute", "mxgraph.ibm.cloud")):
            vertex(graph, str(index + 2), x=index * 200, width=78, height=78, style=f"shape={shape};")
        errors, _, totals = inspect(graph)
        self.assertEqual(errors, [])
        self.assertEqual(totals[3], {"aws": 1, "azure_native": 1, "google_native": 1, "ibm_native": 1, "embedded_svg": 0})

    def test_overlapping_icons_and_inline_label_warning(self):
        graph = model()
        vertex(graph, width=78, height=78, style="shape=mxgraph.ibm.cloud;", value="Label")
        vertex(graph, "b", x=20, width=78, height=78, style="shape=mxgraph.ibm.cloud;")
        errors, warnings, _ = inspect(graph)
        self.assertTrue(any("icons overlap" in error for error in errors))
        self.assertTrue(any("inline label" in warning for warning in warnings))

    def test_label_collision_and_icon_contact_warning(self):
        graph = model()
        vertex(graph, style="text;", value="First label")
        vertex(graph, "b", x=10, style="text;", value="Second label")
        vertex(graph, "icon", x=25, width=78, height=78, style="shape=mxgraph.ibm.cloud;")
        errors, warnings, _ = inspect(graph)
        self.assertTrue(any("labels overlap" in error for error in errors))
        self.assertTrue(any("runs into icon" in warning for warning in warnings))

    def test_embedded_svg_accepts_percent_and_base64_encoding(self):
        for uri in (svg_uri(), "data:image/svg+xml," + urllib.parse.quote(SVG)):
            self.assertIsNone(checker.validate_embedded_svg(uri))
            self.assertEqual(checker.style_map("shape=image;image=" + uri + ";html=1;")["image"], uri)

    def test_svg_rejects_active_external_and_malformed_content(self):
        payloads = ["<not-svg/>", "<svg>", "<svg><script/></svg>", "<svg><foreignObject/></svg>",
                    '<svg onload="alert(1)"/>', '<svg><image href="https://example.invalid/x.svg"/></svg>',
                    '<svg><style>@import "https://example.invalid/x.css";</style></svg>',
                    '<svg><path style="fill:url(https://example.invalid/x)"/></svg>']
        for payload in payloads:
            with self.subTest(payload=payload):
                self.assertIsNotNone(checker.validate_embedded_svg(svg_uri(payload)))
        self.assertIsNotNone(checker.validate_embedded_svg("data:image/svg+xml;base64,%%%"))

    def test_external_and_raster_images_fail(self):
        for uri in ("https://example.invalid/icon.svg", "data:image/png;base64,YQ=="):
            graph = model()
            vertex(graph, style=f"shape=image;image={uri};")
            self.assertTrue(any("must embed SVG" in error for error in inspect(graph)[0]))

    def test_provider_inventory_binds_svg_to_each_vendor(self):
        graph = model()
        vertex(graph, style="shape=image;image=" + svg_uri() + ";")
        for provider in ("aws", "azure", "google", "ibm"):
            inventory = {"icons": [{"page": "page", "cell_id": "a", "provider": provider, "source": "reviewed-source"}]}
            self.assertEqual(checker.inventory_counts([("page", graph)], inventory)[provider], 1)

    def test_inventory_rejects_unresolved_duplicate_and_conflicting_rows(self):
        graph = model()
        vertex(graph, style="shape=mxgraph.ibm.cloud;")
        row = {"page": "page", "cell_id": "a", "provider": "ibm", "source": "reviewed-source"}
        cases = [{"icons": [row, row]}, {"icons": [dict(row, cell_id="missing")]},
                 {"icons": [dict(row, provider="aws")]}, {"icons": [dict(row, source="")]},
                 {"icons": [dict(row, provider="unknown")]}, {"icons": ["bad"]}, {}]
        for inventory in cases:
            with self.subTest(inventory=inventory):
                with self.assertRaises(ValueError):
                    checker.inventory_counts([("page", graph)], inventory)

    def test_edge_route_crossing_and_style_warnings(self):
        graph = model()
        vertex(graph, "a", width=40, height=40)
        vertex(graph, "b", x=300, width=40, height=40)
        vertex(graph, "icon", x=140, y=0, width=46, height=46, style="shape=mxgraph.ibm.cloud;")
        connection = edge(graph, style="rounded=1;exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
        connection.set("value", "Note")
        errors, warnings, _ = inspect(graph)
        self.assertEqual(errors, [])
        for message in ("not sharp orthogonal", "crosses icon"):
            self.assertTrue(any(message in warning for warning in warnings), message)

    def test_cli_status_and_provider_enforcement(self):
        graph = model()
        vertex(graph)
        path = self.write("valid.drawio", ET.tostring(graph, encoding="unicode"))
        with redirect_stdout(io.StringIO()):
            self.assertEqual(checker.main([str(path)]), 0)
            self.assertEqual(checker.main(["--require-provider-icons", "ibm", str(path)]), 1)
            self.assertEqual(checker.main([str(self.workspace / "missing.drawio")]), 1)
            graph.find("root/mxCell[@id='a']").set("style", "shape=image;image=" + svg_uri() + ";")
            path.write_text(ET.tostring(graph, encoding="unicode"), encoding="utf-8")
            inventory = self.write("icons.json", json.dumps({"icons": [{"page": "page-1", "cell_id": "a", "provider": "ibm", "source": "reviewed-source"}]}))
            self.assertEqual(checker.main(["--require-provider-icons", "ibm", "--icon-inventory", str(inventory), str(path)]), 0)


if __name__ == "__main__":
    unittest.main()
