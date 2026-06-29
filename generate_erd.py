"""
generate_erd.py  -  Draw the Entity Relationship Diagram as a PNG.

Produces report/ERD.png showing all entities, their attributes,
primary keys (PK), foreign keys (FK) and the one-to-many relationships
between them.

Run:
    python generate_erd.py
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE_DIR, "report")
OUT_FILE = os.path.join(OUT_DIR, "ERD.png")

HEADER_H = 0.55
ROW_H = 0.34
BOX_W = 3.0

HEADER_COLOR = "#0b5d8a"
BOX_COLOR = "#ffffff"
EDGE_COLOR = "#1f3b4d"
PK_COLOR = "#8a3b00"
FK_COLOR = "#0a6b2e"
LINE_COLOR = "#5a5a5a"

# entity -> (center_x, center_y, [(attribute, key)])
ENTITIES = {
    "Category": (3.0, 11.3, [
        ("category_id", "PK"), ("category_name", ""), ("description", "")]),
    "Supplier": (14.0, 11.0, [
        ("supplier_id", "PK"), ("supplier_name", ""), ("contact_person", ""),
        ("phone", ""), ("email", ""), ("address", "")]),
    "Medicine": (8.5, 10.2, [
        ("medicine_id", "PK"), ("medicine_name", ""), ("category_id", "FK"),
        ("supplier_id", "FK"), ("unit_price", ""), ("stock_quantity", ""),
        ("expiry_date", ""), ("batch_no", "")]),
    "Sale_Item": (8.5, 6.0, [
        ("sale_item_id", "PK"), ("sale_id", "FK"), ("medicine_id", "FK"),
        ("quantity", ""), ("unit_price", ""), ("subtotal", "")]),
    "Sale": (8.5, 2.0, [
        ("sale_id", "PK"), ("customer_id", "FK"), ("employee_id", "FK"),
        ("sale_date", ""), ("payment_method", ""), ("total_amount", "")]),
    "Customer": (3.0, 2.2, [
        ("customer_id", "PK"), ("customer_name", ""), ("phone", ""),
        ("email", ""), ("address", "")]),
    "Employee": (14.0, 2.0, [
        ("employee_id", "PK"), ("employee_name", ""), ("role", ""),
        ("phone", ""), ("salary", ""), ("hire_date", "")]),
}

# (parent "one" side, child "many" side)
RELATIONSHIPS = [
    ("Category", "Medicine"),
    ("Supplier", "Medicine"),
    ("Customer", "Sale"),
    ("Employee", "Sale"),
    ("Sale", "Sale_Item"),
    ("Medicine", "Sale_Item"),
]


def box_geometry(name):
    cx, cy, attrs = ENTITIES[name]
    box_h = HEADER_H + len(attrs) * ROW_H
    return cx, cy, BOX_W / 2.0, box_h / 2.0


def edge_point(cx, cy, hw, hh, tx, ty):
    """Point where the line from the box centre toward (tx,ty) meets the box edge."""
    dx, dy = tx - cx, ty - cy
    sx = hw / abs(dx) if dx != 0 else float("inf")
    sy = hh / abs(dy) if dy != 0 else float("inf")
    s = min(sx, sy)
    return cx + dx * s, cy + dy * s


def draw_entity(ax, name):
    cx, cy, hw, hh = box_geometry(name)
    attrs = ENTITIES[name][2]
    left, right = cx - hw, cx + hw
    top, bottom = cy + hh, cy - hh

    # body
    ax.add_patch(Rectangle((left, bottom), BOX_W, 2 * hh, facecolor=BOX_COLOR,
                           edgecolor=EDGE_COLOR, linewidth=1.5, zorder=3))
    # header
    ax.add_patch(Rectangle((left, top - HEADER_H), BOX_W, HEADER_H,
                           facecolor=HEADER_COLOR, edgecolor=EDGE_COLOR,
                           linewidth=1.5, zorder=4))
    ax.text(cx, top - HEADER_H / 2, name, color="white", fontsize=11,
            fontweight="bold", ha="center", va="center", zorder=5)

    # attributes
    for i, (attr, key) in enumerate(attrs):
        y = top - HEADER_H - (i + 0.5) * ROW_H
        if key == "PK":
            ax.text(left + 0.18, y, attr + "  (PK)", fontsize=9, fontweight="bold",
                    color=PK_COLOR, ha="left", va="center", zorder=5)
        elif key == "FK":
            ax.text(left + 0.18, y, attr + "  (FK)", fontsize=9, style="italic",
                    color=FK_COLOR, ha="left", va="center", zorder=5)
        else:
            ax.text(left + 0.18, y, attr, fontsize=9, color="#222222",
                    ha="left", va="center", zorder=5)


def draw_relationship(ax, parent, child):
    pcx, pcy, phw, phh = box_geometry(parent)
    ccx, ccy, chw, chh = box_geometry(child)
    px, py = edge_point(pcx, pcy, phw, phh, ccx, ccy)
    cxp, cyp = edge_point(ccx, ccy, chw, chh, pcx, pcy)

    ax.plot([px, cxp], [py, cyp], color=LINE_COLOR, linewidth=1.4, zorder=1)

    # cardinality labels: "1" near the parent, "N" near the child
    length = ((cxp - px) ** 2 + (cyp - py) ** 2) ** 0.5
    ux, uy = (cxp - px) / length, (cyp - py) / length
    bbox = dict(boxstyle="round,pad=0.12", fc="white", ec="none")
    ax.text(px + ux * 0.45, py + uy * 0.45, "1", fontsize=11, fontweight="bold",
            color="#b00000", ha="center", va="center", zorder=6, bbox=bbox)
    ax.text(cxp - ux * 0.45, cyp - uy * 0.45, "N", fontsize=11, fontweight="bold",
            color="#b00000", ha="center", va="center", zorder=6, bbox=bbox)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    fig, ax = plt.subplots(figsize=(13.5, 10.5))
    ax.set_xlim(0, 17.5)
    ax.set_ylim(0, 13.7)
    ax.axis("off")

    ax.text(8.75, 13.3, "Pharmacy Management System  -  Entity Relationship Diagram",
            fontsize=15, fontweight="bold", ha="center", va="center", color="#13303f")

    for parent, child in RELATIONSHIPS:
        draw_relationship(ax, parent, child)
    for name in ENTITIES:
        draw_entity(ax, name)

    # legend
    ax.text(0.3, 0.5,
            "PK = Primary Key      FK = Foreign Key      1 ---- N = one-to-many relationship",
            fontsize=10, ha="left", va="center", color="#333333")

    fig.savefig(OUT_FILE, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("ERD written to:", OUT_FILE)


if __name__ == "__main__":
    main()
