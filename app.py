"""
app.py  -  Pharmacy Management System  (GUI)

A Tkinter desktop application over the SQLite pharmacy database.
There is one tab per table that lets the user Add, Update, Delete,
Search and View records, plus a Reports tab that shows summary
information built from JOINs and aggregate queries.

Run:
    python app.py
(The database is built automatically on first run.)
"""

import os
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

import db
import init_db


# =====================================================================
# Table definitions
# Each field: col, label, kind
#   kind = "pk"   -> primary key (auto, read-only)
#          "text" / "int" / "real" / "date"  -> normal entry
#          "auto" -> value computed by the app (read-only)
#          "fk"   -> dropdown; also needs ref_table / ref_pk / ref_display
# =====================================================================
TABLE_META = {
    "Category": {
        "pk": "category_id",
        "fields": [
            {"col": "category_id",   "label": "Category ID",   "kind": "pk"},
            {"col": "category_name", "label": "Category Name",  "kind": "text"},
            {"col": "description",   "label": "Description",    "kind": "text"},
        ],
    },
    "Supplier": {
        "pk": "supplier_id",
        "fields": [
            {"col": "supplier_id",    "label": "Supplier ID",     "kind": "pk"},
            {"col": "supplier_name",  "label": "Supplier Name",   "kind": "text"},
            {"col": "contact_person", "label": "Contact Person",  "kind": "text"},
            {"col": "phone",          "label": "Phone",           "kind": "text"},
            {"col": "email",          "label": "Email",           "kind": "text"},
            {"col": "address",        "label": "Address",         "kind": "text"},
        ],
    },
    "Medicine": {
        "pk": "medicine_id",
        "fields": [
            {"col": "medicine_id",    "label": "Medicine ID",   "kind": "pk"},
            {"col": "medicine_name",  "label": "Medicine Name", "kind": "text"},
            {"col": "category_id",    "label": "Category",      "kind": "fk",
             "ref_table": "Category", "ref_pk": "category_id", "ref_display": "category_name"},
            {"col": "supplier_id",    "label": "Supplier",      "kind": "fk",
             "ref_table": "Supplier", "ref_pk": "supplier_id", "ref_display": "supplier_name"},
            {"col": "unit_price",     "label": "Unit Price",    "kind": "real"},
            {"col": "stock_quantity", "label": "Stock Qty",     "kind": "int"},
            {"col": "expiry_date",    "label": "Expiry (YYYY-MM-DD)", "kind": "date"},
            {"col": "batch_no",       "label": "Batch No",      "kind": "text"},
        ],
    },
    "Customer": {
        "pk": "customer_id",
        "fields": [
            {"col": "customer_id",   "label": "Customer ID",   "kind": "pk"},
            {"col": "customer_name", "label": "Customer Name", "kind": "text"},
            {"col": "phone",         "label": "Phone",         "kind": "text"},
            {"col": "email",         "label": "Email",         "kind": "text"},
            {"col": "address",       "label": "Address",       "kind": "text"},
        ],
    },
    "Employee": {
        "pk": "employee_id",
        "fields": [
            {"col": "employee_id",   "label": "Employee ID",   "kind": "pk"},
            {"col": "employee_name", "label": "Employee Name", "kind": "text"},
            {"col": "role",          "label": "Role",          "kind": "text"},
            {"col": "phone",         "label": "Phone",         "kind": "text"},
            {"col": "salary",        "label": "Salary",        "kind": "real"},
            {"col": "hire_date",     "label": "Hire Date (YYYY-MM-DD)", "kind": "date"},
        ],
    },
    "Sale": {
        "pk": "sale_id",
        "fields": [
            {"col": "sale_id",        "label": "Sale ID",   "kind": "pk"},
            {"col": "customer_id",    "label": "Customer",  "kind": "fk",
             "ref_table": "Customer", "ref_pk": "customer_id", "ref_display": "customer_name"},
            {"col": "employee_id",    "label": "Employee",  "kind": "fk",
             "ref_table": "Employee", "ref_pk": "employee_id", "ref_display": "employee_name"},
            {"col": "sale_date",      "label": "Sale Date (YYYY-MM-DD)", "kind": "date"},
            {"col": "payment_method", "label": "Payment Method", "kind": "text"},
            {"col": "total_amount",   "label": "Total Amount (auto)", "kind": "auto"},
        ],
    },
    "Sale_Item": {
        "pk": "sale_item_id",
        "fields": [
            {"col": "sale_item_id", "label": "Sale Item ID", "kind": "pk"},
            {"col": "sale_id",      "label": "Sale",         "kind": "fk",
             "ref_table": "Sale", "ref_pk": "sale_id", "ref_display": "sale_date"},
            {"col": "medicine_id",  "label": "Medicine",     "kind": "fk",
             "ref_table": "Medicine", "ref_pk": "medicine_id", "ref_display": "medicine_name"},
            {"col": "quantity",     "label": "Quantity",     "kind": "int"},
            {"col": "unit_price",   "label": "Unit Price",   "kind": "real"},
            {"col": "subtotal",     "label": "Subtotal (auto)", "kind": "auto"},
        ],
    },
}

# Order of the tabs.
TABLE_ORDER = ["Category", "Supplier", "Medicine", "Customer",
               "Employee", "Sale", "Sale_Item"]


# =====================================================================
# Reports : name -> SQL (each is run live against the database)
# =====================================================================
REPORTS = {
    "Medicine stock (with category & supplier)":
        """SELECT m.medicine_id AS ID, m.medicine_name AS Medicine,
                  c.category_name AS Category, s.supplier_name AS Supplier,
                  m.unit_price AS Price, m.stock_quantity AS Stock,
                  m.expiry_date AS Expiry
           FROM Medicine m
           JOIN Category c ON m.category_id = c.category_id
           JOIN Supplier s ON m.supplier_id = s.supplier_id
           ORDER BY m.medicine_name;""",

    "Low stock medicines (Stock < 100)":
        """SELECT medicine_id AS ID, medicine_name AS Medicine,
                  stock_quantity AS Stock, unit_price AS Price
           FROM Medicine
           WHERE stock_quantity < 100
           ORDER BY stock_quantity ASC;""",

    "Medicines expiring on/before 2026-09-30":
        """SELECT medicine_id AS ID, medicine_name AS Medicine,
                  expiry_date AS Expiry, stock_quantity AS Stock
           FROM Medicine
           WHERE expiry_date <= '2026-09-30'
           ORDER BY expiry_date ASC;""",

    "Sales summary per customer":
        """SELECT c.customer_id AS ID, c.customer_name AS Customer,
                  COUNT(sl.sale_id) AS Orders,
                  ROUND(COALESCE(SUM(sl.total_amount), 0), 2) AS Total_Spent
           FROM Customer c
           LEFT JOIN Sale sl ON c.customer_id = sl.customer_id
           GROUP BY c.customer_id, c.customer_name
           ORDER BY Total_Spent DESC;""",

    "Sales handled per employee":
        """SELECT e.employee_id AS ID, e.employee_name AS Employee, e.role AS Role,
                  COUNT(sl.sale_id) AS Sales_Handled,
                  ROUND(COALESCE(SUM(sl.total_amount), 0), 2) AS Revenue
           FROM Employee e
           LEFT JOIN Sale sl ON e.employee_id = sl.employee_id
           GROUP BY e.employee_id
           ORDER BY Revenue DESC;""",

    "Revenue by category":
        """SELECT c.category_name AS Category,
                  ROUND(COALESCE(SUM(si.subtotal), 0), 2) AS Revenue,
                  COALESCE(SUM(si.quantity), 0) AS Units_Sold
           FROM Category c
           JOIN Medicine m ON m.category_id = c.category_id
           JOIN Sale_Item si ON si.medicine_id = m.medicine_id
           GROUP BY c.category_id
           ORDER BY Revenue DESC;""",

    "Invoice details (every sale item)":
        """SELECT sl.sale_id AS Sale, sl.sale_date AS Date,
                  cu.customer_name AS Customer, em.employee_name AS Served_By,
                  m.medicine_name AS Medicine, si.quantity AS Qty,
                  si.unit_price AS Price, ROUND(si.subtotal, 2) AS Subtotal
           FROM Sale sl
           JOIN Customer cu ON sl.customer_id = cu.customer_id
           JOIN Employee em ON sl.employee_id = em.employee_id
           JOIN Sale_Item si ON si.sale_id = sl.sale_id
           JOIN Medicine m ON si.medicine_id = m.medicine_id
           ORDER BY sl.sale_id;""",

    "Inventory valuation (stock value)":
        """SELECT m.medicine_id AS ID, m.medicine_name AS Medicine,
                  m.stock_quantity AS Stock, m.unit_price AS Price,
                  ROUND(m.stock_quantity * m.unit_price, 2) AS Stock_Value
           FROM Medicine m
           ORDER BY Stock_Value DESC;""",
}


def heading_text(col):
    """Turn a column name like 'medicine_name' into 'Medicine Name'."""
    return col.replace("_", " ").title()


def column_width(col):
    if col.endswith("_id"):
        return 70
    if "name" in col:
        return 160
    if col in ("description", "address", "email"):
        return 180
    return 110


# =====================================================================
# A generic Create / Read / Update / Delete tab for one table.
# =====================================================================
class CrudTab(ttk.Frame):
    def __init__(self, master, app, table):
        super().__init__(master, padding=10)
        self.app = app
        self.table = table
        self.meta = TABLE_META[table]
        self.pk = self.meta["pk"]
        self.fields = self.meta["fields"]
        self.cols = [f["col"] for f in self.fields]

        self.vars = {}                 # col -> StringVar
        self.fk_widgets = {}           # col -> Combobox
        self.fk_to_id = {}             # col -> {display: id}
        self.fk_to_display = {}        # col -> {id: display}
        self.selected_pk = None

        self._build_form()
        self._build_buttons()
        self._build_search()
        self._build_tree()
        self.refresh()

    # ---------------------------------------------------------------- form
    def _build_form(self):
        frame = ttk.LabelFrame(self, text="Record details", padding=10)
        frame.pack(fill="x", padx=2, pady=2)

        for i, f in enumerate(self.fields):
            r, c = i // 2, (i % 2) * 2
            ttk.Label(frame, text=f["label"] + ":").grid(
                row=r, column=c, sticky="e", padx=6, pady=5)

            var = tk.StringVar()
            self.vars[f["col"]] = var

            if f["kind"] == "fk":
                widget = ttk.Combobox(frame, textvariable=var,
                                      state="readonly", width=30)
                self.fk_widgets[f["col"]] = widget
            elif f["kind"] in ("pk", "auto"):
                widget = ttk.Entry(frame, textvariable=var,
                                   state="readonly", width=32)
            else:
                widget = ttk.Entry(frame, textvariable=var, width=32)

            widget.grid(row=r, column=c + 1, sticky="we", padx=6, pady=5)

        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(3, weight=1)

    def reload_fk_options(self):
        """(Re)build dropdown lists and id<->label maps for FK fields."""
        for f in self.fields:
            if f["kind"] != "fk":
                continue
            rows = db.fetch_all(
                f"SELECT {f['ref_pk']} AS id, {f['ref_display']} AS disp "
                f"FROM {f['ref_table']} ORDER BY id")
            to_id, to_disp, values = {}, {}, []
            for row in rows:
                disp = f"{row['id']} - {row['disp']}"
                to_id[disp] = row["id"]
                to_disp[row["id"]] = disp
                values.append(disp)
            self.fk_to_id[f["col"]] = to_id
            self.fk_to_display[f["col"]] = to_disp
            self.fk_widgets[f["col"]]["values"] = values

    # ------------------------------------------------------------- buttons
    def _build_buttons(self):
        bar = ttk.Frame(self)
        bar.pack(fill="x", pady=(8, 2))
        ttk.Button(bar, text="Add",     command=self.add_record).pack(side="left", padx=4)
        ttk.Button(bar, text="Update",  command=self.update_record).pack(side="left", padx=4)
        ttk.Button(bar, text="Delete",  command=self.delete_record).pack(side="left", padx=4)
        ttk.Button(bar, text="Clear form", command=self.clear_form).pack(side="left", padx=4)

    # -------------------------------------------------------------- search
    def _build_search(self):
        bar = ttk.Frame(self)
        bar.pack(fill="x", pady=(2, 6))
        ttk.Label(bar, text="Search:").pack(side="left", padx=(4, 4))
        self.search_var = tk.StringVar()
        entry = ttk.Entry(bar, textvariable=self.search_var, width=30)
        entry.pack(side="left", padx=4)
        entry.bind("<Return>", lambda e: self.do_search())
        ttk.Button(bar, text="Search",   command=self.do_search).pack(side="left", padx=4)
        ttk.Button(bar, text="Show all", command=self.show_all).pack(side="left", padx=4)
        self.count_var = tk.StringVar(value="")
        ttk.Label(bar, textvariable=self.count_var).pack(side="right", padx=6)

    # ---------------------------------------------------------------- tree
    def _build_tree(self):
        frame = ttk.LabelFrame(self, text="Records  (click a row to edit)", padding=6)
        frame.pack(fill="both", expand=True, padx=2, pady=2)

        self.tree = ttk.Treeview(frame, columns=self.cols, show="headings",
                                 selectmode="browse", height=10)
        for col in self.cols:
            self.tree.heading(col, text=heading_text(col))
            self.tree.column(col, width=column_width(col), anchor="w")

        vsb = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    # ------------------------------------------------------------- helpers
    def refresh(self, where="", params=()):
        self.reload_fk_options()
        rows = db.fetch_all(
            f"SELECT {', '.join(self.cols)} FROM {self.table} {where} "
            f"ORDER BY {self.pk}", params)
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert("", "end", values=[row[c] for c in self.cols])
        self.count_var.set(f"{len(rows)} record(s)")

    def on_select(self, _event):
        sel = self.tree.selection()
        if not sel:
            return
        values = self.tree.item(sel[0], "values")
        record = dict(zip(self.cols, values))
        self.selected_pk = record[self.pk]
        for f in self.fields:
            col, val = f["col"], record[f["col"]]
            if f["kind"] == "fk":
                # show "id - name" in the dropdown
                try:
                    val_id = int(val)
                except (ValueError, TypeError):
                    val_id = val
                self.vars[col].set(self.fk_to_display[col].get(val_id, ""))
            else:
                self.vars[col].set("" if val is None else val)

    def clear_form(self):
        self.selected_pk = None
        for f in self.fields:
            self.vars[f["col"]].set("")
        self.tree.selection_remove(self.tree.selection())

    def collect_values(self):
        """Read editable form fields. Returns {col: value}. Raises ValueError."""
        out = {}
        for f in self.fields:
            if f["kind"] in ("pk", "auto"):
                continue
            raw = self.vars[f["col"]].get().strip()
            if f["kind"] == "fk":
                if raw == "":
                    out[f["col"]] = None
                else:
                    out[f["col"]] = self.fk_to_id[f["col"]].get(raw)
            elif f["kind"] == "int":
                out[f["col"]] = None if raw == "" else self._to_number(raw, f["label"], int)
            elif f["kind"] == "real":
                out[f["col"]] = None if raw == "" else self._to_number(raw, f["label"], float)
            else:  # text / date
                out[f["col"]] = raw if raw != "" else None
        return out

    @staticmethod
    def _to_number(raw, label, caster):
        try:
            return caster(raw)
        except ValueError:
            kind = "whole number" if caster is int else "number"
            raise ValueError(f"'{label}' must be a {kind}.")

    # --------------------------------------------------------------- CRUD
    def add_record(self):
        try:
            vals = self.collect_values()
            if self.table == "Sale_Item":
                vals["subtotal"] = self._line_subtotal(vals)
            cols = list(vals.keys())
            placeholders = ", ".join(["?"] * len(cols))
            db.execute(f"INSERT INTO {self.table} ({', '.join(cols)}) "
                       f"VALUES ({placeholders})", tuple(vals.values()))
            self._after_change()
            messagebox.showinfo("Added", f"New record added to {self.table}.")
        except ValueError as e:
            messagebox.showwarning("Invalid input", str(e))
        except sqlite3.Error as e:
            messagebox.showerror("Could not add record", self._friendly(e))

    def update_record(self):
        if self.selected_pk is None:
            messagebox.showwarning("No selection",
                                   "Select a record from the list first.")
            return
        try:
            vals = self.collect_values()
            if self.table == "Sale_Item":
                vals["subtotal"] = self._line_subtotal(vals)
            assignments = ", ".join([f"{c} = ?" for c in vals])
            params = tuple(vals.values()) + (self.selected_pk,)
            db.execute(f"UPDATE {self.table} SET {assignments} "
                       f"WHERE {self.pk} = ?", params)
            self._after_change()
            messagebox.showinfo("Updated", "Record updated successfully.")
        except ValueError as e:
            messagebox.showwarning("Invalid input", str(e))
        except sqlite3.Error as e:
            messagebox.showerror("Could not update record", self._friendly(e))

    def delete_record(self):
        if self.selected_pk is None:
            messagebox.showwarning("No selection",
                                   "Select a record from the list first.")
            return
        if not messagebox.askyesno("Confirm delete",
                                   f"Delete this record from {self.table}?"):
            return
        try:
            db.execute(f"DELETE FROM {self.table} WHERE {self.pk} = ?",
                       (self.selected_pk,))
            self._after_change()
            messagebox.showinfo("Deleted", "Record deleted.")
        except sqlite3.Error as e:
            messagebox.showerror("Could not delete record", self._friendly(e))

    def _line_subtotal(self, vals):
        qty = vals.get("quantity") or 0
        price = vals.get("unit_price") or 0
        return round(qty * price, 2)

    def _after_change(self):
        """Refresh this tab and any tabs whose data may have changed."""
        # keep Sale totals and dropdowns consistent across the app
        if self.table == "Sale_Item":
            db.execute(
                "UPDATE Sale SET total_amount = ROUND(("
                "  SELECT COALESCE(SUM(subtotal), 0) FROM Sale_Item si "
                "  WHERE si.sale_id = Sale.sale_id), 2)")
            self.app.refresh_tab("Sale")
        if self.table == "Sale":
            self.app.refresh_tab("Sale_Item")
        self.clear_form()
        self.refresh()
        self.app.refresh_related_dropdowns(self.table)

    def do_search(self):
        term = self.search_var.get().strip()
        if term == "":
            self.refresh()
            return
        likes = " OR ".join([f"CAST({c} AS TEXT) LIKE ?" for c in self.cols])
        params = tuple([f"%{term}%"] * len(self.cols))
        self.refresh(where="WHERE " + likes, params=params)

    def show_all(self):
        self.search_var.set("")
        self.refresh()


# =====================================================================
# Reports tab : pick a report and view it.
# =====================================================================
class ReportsTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=10)

        top = ttk.Frame(self)
        top.pack(fill="x", pady=4)
        ttk.Label(top, text="Choose a report:").pack(side="left", padx=4)
        self.choice = tk.StringVar()
        self.combo = ttk.Combobox(top, textvariable=self.choice, state="readonly",
                                  width=45, values=list(REPORTS.keys()))
        self.combo.pack(side="left", padx=4)
        self.combo.bind("<<ComboboxSelected>>", lambda e: self.run_report())
        ttk.Button(top, text="Run report", command=self.run_report).pack(side="left", padx=4)
        self.info = tk.StringVar(value="")
        ttk.Label(top, textvariable=self.info).pack(side="right", padx=6)

        frame = ttk.LabelFrame(self, text="Result", padding=6)
        frame.pack(fill="both", expand=True, pady=4)
        self.tree = ttk.Treeview(frame, show="headings", height=15)
        vsb = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        self.combo.current(0)
        self.run_report()

    def run_report(self):
        sql = REPORTS[self.choice.get()]
        with db.get_connection() as conn:
            cur = conn.execute(sql)
            headers = [d[0] for d in cur.description]
            rows = cur.fetchall()

        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = headers
        for h in headers:
            self.tree.heading(h, text=h)
            width = 90 if h in ("ID", "Qty", "Stock", "Orders") else 150
            self.tree.column(h, width=width, anchor="w")
        for row in rows:
            self.tree.insert("", "end", values=[row[h] for h in headers])
        self.info.set(f"{len(rows)} row(s)")


# =====================================================================
# Main application window
# =====================================================================
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pharmacy Management System")
        self.geometry("980x680")
        self.minsize(820, 600)

        try:
            ttk.Style().theme_use("clam")
        except tk.TclError:
            pass

        # header
        header = tk.Frame(self, bg="#0b5d8a")
        header.pack(fill="x")
        tk.Label(header, text="Pharmacy Management System", bg="#0b5d8a",
                 fg="white", font=("Segoe UI", 16, "bold")).pack(side="left",
                                                                  padx=14, pady=10)
        tk.Label(header, text="DBMS Lab Project", bg="#0b5d8a", fg="#cfe6f4",
                 font=("Segoe UI", 10)).pack(side="right", padx=14)

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=8, pady=8)

        self.crud_tabs = {}
        for table in TABLE_ORDER:
            tab = CrudTab(notebook, self, table)
            self.crud_tabs[table] = tab
            notebook.add(tab, text=table.replace("_", " "))

        notebook.add(ReportsTab(notebook), text="Reports")

    def refresh_tab(self, table):
        if table in self.crud_tabs:
            self.crud_tabs[table].refresh()

    def refresh_related_dropdowns(self, changed_table):
        """When a parent table changes, refresh child tabs' dropdown lists."""
        for tab in self.crud_tabs.values():
            for f in tab.fields:
                if f.get("ref_table") == changed_table:
                    tab.reload_fk_options()
                    break


def main():
    # Build the database automatically on first run.
    if not os.path.exists(db.DB_PATH):
        print("Database not found, building it now...")
        init_db.build()
    App().mainloop()


if __name__ == "__main__":
    main()
