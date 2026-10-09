"""Help / FAQ text. Single source of truth used by the in-app Help screen and the docs.

Quality goal Q10 (Improve Documentation): keeping help text in one module means the
manual, FAQ and UI tooltips cannot drift apart.
"""

FAQS = [
    ("How do I log in for the first time?",
     "Use username 'admin' and password 'Admin@123', then open Users and create your own account."),
    ("How do I add a product?",
     "Open Products and click Add. SKU and Name are required; SKU must be unique."),
    ("How do I record stock coming in or going out?",
     "Select a product, then click Stock In or Stock Out and enter the quantity. Every movement is saved in Stock History."),
    ("Why can't I issue more stock than I have?",
     "This is a Poka-Yoke (error-prevention) rule: the system refuses Stock Out above the available quantity."),
    ("What does a red row mean?",
     "The quantity is at or below the product's reorder level. Re-order it soon."),
    ("How do I export a report?",
     "Open Reports and choose Excel, PDF or CSV. The Excel file also holds movements, FMEA and defects."),
    ("How do I back up my data?",
     "Open Reports and click Backup Database. Copies are stored in data/backups/."),
    ("Who can delete records?",
     "Only users with the admin role. Every change is written to the Audit Log."),
    ("What is the Quality (TQM) page?",
     "It holds the Defect Log (checksheet), the FMEA matrix with RPN = S x O x D, and the Pareto and Fishbone charts."),
    ("What are the keyboard shortcuts?",
     "Ctrl+1 ... Ctrl+9 switch pages, F1 opens Help, Ctrl+F focuses search, Ctrl+Q quits."),
    ("Where is the full manual?",
     "In Help > User Manual, or docs/USER_MANUAL.md in the GitHub repository."),
]

TOOLTIPS = {
    "sku": "Unique product code, e.g. EL-001. Saved in upper case.",
    "reorder": "When quantity falls to this number the row turns red.",
    "severity": "1 = no effect ... 10 = hazardous / total failure.",
    "occurrence": "1 = almost never ... 10 = almost certain.",
    "detection": "1 = always detected ... 10 = cannot be detected.",
}
