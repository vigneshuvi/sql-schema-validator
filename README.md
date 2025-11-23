# SSQL Validator & Documentation Generator

This Python script automatically scans SQL files, analyzes database schemas, detects anomalies, and generates a clean, mobile-friendly HTML documentation page — perfect for schema validation and GitHub Pages publishing.

## 📋 Features

- **Automatic Discovery**: Scans and processes all `.sql` files in the directory
- **Database Analysis**: Extracts database names, table counts, and file statistics
- **Anomaly Detection**: Automatically detects potential schema issues including:
  - Tables without primary keys
  - Tables without indexes
  - Single column tables
  - Potential missing foreign keys
  - Long table names (>30 characters)
  - Nullable columns
- **Interactive UI**: Tab-based navigation with search functionality
- **Copy to Clipboard**: One-click code copying for each SQL file
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **GitHub Pages Ready**: Single HTML file with no external dependencies

## 🚀 Usage

### Basic Usage

Simply run the script in the directory containing your SQL files:

```bash
python3 validate_schema_generate_html.py
```

The script will:
1. Scan for all `.sql` files in the current directory
2. Analyze each file (count tables, lines, extract database name)
3. Detect potential schema anomalies
4. Generate a beautiful `index.html` documentation page
5. Display a summary of processed files and anomalies detected

### Output

After running the script, you'll get:
- **index.html** - Complete documentation page ready to open in browser

## 📊 Generated Documentation Includes

- **Overview Page**: Summary of all databases with statistics
- **Anomaly Dashboard**: Comprehensive breakdown of detected schema issues across all databases
- **Individual Tabs**: Each SQL file gets its own tab with:
  - Database name
  - Number of tables
  - Total lines of code
  - File size
  - Anomaly count with color-coded indicators
  - Detailed anomaly breakdown (if anomalies detected)
  - Full SQL source code with copy button
- **Search Functionality**: Search across all SQL files
- **Responsive Design**: Mobile-friendly interface

## 🔄 Updating Documentation

Whenever you add, remove, or modify SQL files:

```bash
python3 generate_html.py
```

The script will regenerate the entire documentation based on current SQL files.

## 📦 Requirements

- Python 3.6 or higher
- No external dependencies (uses only Python standard library)

## 🌐 Deploying to GitHub Pages

1. **Add files to your repository**:
   ```bash
   git add index.html generate_html.py
   git commit -m "Add SQL documentation"
   git push
   ```

2. **Enable GitHub Pages**:
   - Go to your repository on GitHub
   - Navigate to Settings → Pages
   - Select the branch and folder containing `index.html`
   - Click Save

3. **Access your documentation**:
   -  Documentation will be available at:
   - `https://github.com/vigneshuvi/sql-schema-validator`

## 🛠️ Customization

### Changing Colors

Edit the `colors` list in the `generate_html()` function:

```python
colors = [
    {'bg': '#f0f7ff', 'border': '#0366d6', 'color': '#0366d6'},
    {'bg': '#f0fff4', 'border': '#28a745', 'color': '#28a745'},
    # Add more color schemes...
]
```

### Adding Custom Styling

The script uses embedded CSS. Modify the `<style>` section in the `html_template` string.

### Custom Analysis

Add your own analysis functions:

```python
def analyze_sql_file(filepath):
    # Add custom analysis here
    view_count = content.upper().count('CREATE VIEW')
    # Return in the dictionary
```

### Understanding Anomalies

The script detects the following potential issues:

1. **Tables without primary keys**: Tables lacking a PRIMARY KEY constraint, which can impact data integrity
2. **Tables without indexes**: Tables with no indexes created, potentially affecting query performance
3. **Single column tables**: Tables containing only one column, which may indicate design issues
4. **Potential missing foreign keys**: Columns with FKY_ prefix but no actual FOREIGN KEY constraint defined
5. **Long table names**: Table names exceeding 30 characters, which may cause compatibility issues
6. **Nullable columns**: Columns allowing NULL values without explicit defaults

**Note**: These are potential issues detected through pattern matching. Some may be intentional design decisions and should be reviewed by a database architect.

## 📝 Example Output

```
🔍 Scanning for SQL files...
✅ Found 3 SQL file(s)
   📄 Analyzing s00c62a.sql...
      → 44 tables, 1,557 lines, 15 anomalies
   📄 Analyzing s08c62a.sql...
      → 140 tables, 7,593 lines, 48 anomalies
   📄 Analyzing s26c62a.sql...
      → 18 tables, 690 lines, 8 anomalies

🔨 Generating HTML documentation...
✅ HTML documentation generated successfully!
📁 Output: /path/to/index.html

📊 Summary:
   Total SQL files: 3
   Total tables: 202
   Total lines: 9,840
   Total size: 406.26 KB

⚠️  Anomaly Summary:
   Total anomalies detected: 71
   - Tables without primary keys: 12
   - Tables without indexes: 8
   - Single column tables: 3
   - Potential missing foreign keys: 35
   - Long table names (>30 chars): 5
   - Nullable columns: 8

🌐 Open index.html in your browser to view the documentation!
```

## 🤝 Integration with CI/CD

### GitHub Actions Example

Create `.github/workflows/generate-docs.yml`:

```yaml
name: Generate SQL Documentation

on:
  push:
    paths:
      - '**.sql'
  workflow_dispatch:

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'
      
      - name: Generate Documentation
        run: |
          cd database-scripts
          python3 generate_html.py
      
      - name: Commit Changes
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add index.html
          git commit -m "Auto-update SQL documentation" || exit 0
          git push
```

## 📄 License

This script is provided as-is for the Vigneshuvi.

## 🐛 Troubleshooting

### No SQL files found
- Ensure you're running the script in the correct directory
- Check that your SQL files have the `.sql` extension

### Encoding errors
- The script handles common encoding issues automatically
- Files are read with UTF-8 encoding and error handling

### Large files
- The script can handle large SQL files
- Generated HTML has scrollable code sections

## 💡 Tips

1. **Run after every SQL change**: Keep documentation up-to-date
2. **Use version control**: Track documentation changes with git
3. **Test locally first**: Open index.html in browser before deploying
4. **Customize for your needs**: Modify the script to add custom analysis

## 📞 Support


- For SQL issues or questions about the GitHub Actions pipeline, contact vigneshuvi.

---

**Generated by 🤖 and Maintain by the Vignesh**
