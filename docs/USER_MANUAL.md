# Inventory Management System - User Manual

**Version 1.0.0 | BBAT104 TQM Project | Quality goal Q10: Improve Documentation**

## 1. Getting started
1. Install Python 3.10+ and run `pip install -r requirements.txt`.
2. Start the program with `python main.py`.
3. Log in with **admin / Admin@123**. Create your own account on the *Users* page and keep the admin password safe.

## 2. Screen overview
| Page | What it does |
| --- | --- |
| Dashboard | Key numbers, stock chart and the list of items to re-order |
| Products | Add, edit, delete and search products; Stock In / Stock Out |
| Categories / Suppliers | Maintain the lists used by the product form |
| Stock History | Read-only list of every stock movement |
| Reports | Export Excel, PDF or CSV; save the chart; back up the database |
| Quality (TQM) | Defect Log, FMEA matrix, Pareto and Fishbone charts |
| Audit Log | Who did what and when (admin only) |
| Users | Create accounts (admin only) |
| Help & FAQ | Searchable FAQ, this manual and keyboard shortcuts |
| About | Version, course and project information |

## 3. Everyday tasks
### Add a product
Products > **Add**. Fill in SKU (unique) and Name; pick Category and Supplier from the dropdowns; set Quantity, Reorder level and Price; **Save**.

### Receive or issue stock
Select the product > **Stock In** or **Stock Out** > enter the quantity. Stock Out above the available quantity is refused.

### Spot low stock
Rows turn red when quantity is at or below the reorder level. The Dashboard lists them too.

### Export a report
Reports > choose Excel, PDF or CSV > choose a file name.

### Back up
Reports > **Backup database**. Copies are saved in `data/backups/`. To restore, close the program and copy a backup over `data/inventory.db`.

## 4. Quality (TQM) tools
* **Defect Log** - log each bug (type, severity, status). This is your checksheet.
* **FMEA** - rate Severity, Occurrence, Detection from 1 to 10. RPN = S x O x D. Rows with RPN 200 or more turn red; fix those first.
* **SQC Charts** - *Pareto chart* shows which defect types cause ~80% of problems; *Fishbone diagram* shows root causes by People, Process, Software Code and Infrastructure.

## 5. Keyboard shortcuts
`Ctrl+1..9` switch pages, `F1` help, `Ctrl+F` search, double-click edits a row, `Ctrl+Q` quit.

## 6. Troubleshooting
| Problem | Fix |
| --- | --- |
| "Duplicate value" message | The SKU / name already exists. Search first, then edit the existing record. |
| "Only N units in stock" | You tried to issue more than available. Reduce the quantity or add stock first. |
| Cannot delete | Only admin users can delete. |
| Program will not start | Run `pip install -r requirements.txt` again and check you use Python 3.10+. |
