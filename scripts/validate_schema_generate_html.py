#!/usr/bin/env python3
"""
SQL Validate - Documentation Generator
Automatically generates index.html documentation for all SQL files in the directory.

Usage:
    python validate_schema_generate_html.py
"""

import os
import glob
from datetime import datetime
from pathlib import Path


def count_tables_in_sql(sql_content):
    """Count the number of CREATE TABLE statements in SQL content."""
    return sql_content.upper().count('CREATE TABLE')


def get_database_name(sql_content):
    """Extract database name from CREATE DATABASE statement."""
    for line in sql_content.split('\n'):
        if 'CREATE DATABASE' in line.upper():
            # Extract database name
            parts = line.strip().rstrip(';').split()
            if len(parts) >= 3:
                return parts[2]
    return "Unknown"


def escape_html(text):
    """Escape HTML special characters."""
    return (text.replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace("'", '&#39;'))


def detect_anomalies(sql_content):
    """Detect potential anomalies in SQL schema."""
    anomalies = {
        'tables_without_primary_key': 0,
        'tables_without_indexes': 0,
        'tables_with_single_column': 0,
        'missing_foreign_keys': 0,
        'long_table_names': 0,
        'nullable_columns': 0,
        'total': 0
    }
    
    lines = sql_content.upper().split('\n')
    current_table = None
    table_has_pk = False
    table_has_index = False
    table_columns = []
    table_name = None
    
    for i, line in enumerate(lines):
        line = line.strip()
        
        # Detect new table creation
        if line.startswith('CREATE TABLE'):
            # Save previous table info
            if current_table:
                if not table_has_pk:
                    anomalies['tables_without_primary_key'] += 1
                if not table_has_index:
                    anomalies['tables_without_indexes'] += 1
                if len(table_columns) == 1:
                    anomalies['tables_with_single_column'] += 1
            
            # Start new table
            parts = line.split()
            if len(parts) >= 3:
                table_name = parts[2].strip('(').strip(';')
                current_table = table_name
                if len(table_name) > 30:
                    anomalies['long_table_names'] += 1
            table_has_pk = False
            table_has_index = False
            table_columns = []
        
        # Detect columns
        elif current_table and ('CHAR' in line or 'VARCHAR' in line or 'DECIMAL' in line or 'INTEGER' in line or 'DATE' in line):
            if 'CREATE' not in line and 'ALTER' not in line and 'INDEX' not in line:
                table_columns.append(line)
                # Check for nullable columns (without NOT NULL)
                if 'NOT NULL' not in line and 'DEFAULT' not in line and ',' in line:
                    anomalies['nullable_columns'] += 1
        
        # Detect primary key
        elif 'PRIMARY KEY' in line or 'ADD CONSTRAINT' in line and 'PRIMARY KEY' in line:
            table_has_pk = True
        
        # Detect indexes
        elif 'CREATE INDEX' in line or 'CREATE UNIQUE INDEX' in line:
            table_has_index = True
        
        # Detect potential missing foreign keys (columns starting with FKY_ but no actual FK constraint)
        elif 'FKY_' in line and 'FOREIGN KEY' not in line:
            if ',' in line or ';' in line:
                anomalies['missing_foreign_keys'] += 1
    
    # Check last table
    if current_table:
        if not table_has_pk:
            anomalies['tables_without_primary_key'] += 1
        if not table_has_index:
            anomalies['tables_without_indexes'] += 1
        if len(table_columns) == 1:
            anomalies['tables_with_single_column'] += 1
    
    # Calculate total anomalies
    anomalies['total'] = sum(v for k, v in anomalies.items() if k != 'total')
    
    return anomalies


def analyze_sql_file(filepath):
    """Analyze a SQL file and return metadata."""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    lines = content.split('\n')
    line_count = len(lines)
    table_count = count_tables_in_sql(content)
    db_name = get_database_name(content)
    filename = os.path.basename(filepath)
    anomalies = detect_anomalies(content)
    
    # Get file size
    file_size = os.path.getsize(filepath)
    size_kb = file_size / 1024
    
    return {
        'filename': filename,
        'filepath': filepath,
        'content': content,
        'lines': line_count,
        'tables': table_count,
        'database': db_name,
        'size_kb': round(size_kb, 2),
        'anomalies': anomalies
    }


def generate_html(sql_files):
    """Generate HTML documentation from SQL files."""
    
    current_date = datetime.now().strftime("%B %Y")
    
    # Generate tab buttons
    tab_buttons = []
    tab_contents = []
    
    # Add overview tab button
    tab_buttons.append('<button class="nav-tab active" onclick="showTab(\'overview\')">Overview</button>')
    
    # Generate tabs for each SQL file
    for i, sql_file in enumerate(sql_files):
        tab_id = sql_file['database'].lower().replace(' ', '_')
        active_class = ''  # Only overview is active by default
        
        tab_buttons.append(
            f'<button class="nav-tab" onclick="showTab(\'{tab_id}\')">{sql_file["database"]} Database</button>'
        )
    
    # Generate overview content
    overview_cards = []
    colors = [
        {'bg': '#f0f7ff', 'border': '#0366d6', 'color': '#0366d6'},
        {'bg': '#f0fff4', 'border': '#28a745', 'color': '#28a745'},
        {'bg': '#fff5f5', 'border': '#dc3545', 'color': '#dc3545'},
        {'bg': '#fffbeb', 'border': '#f59e0b', 'color': '#f59e0b'},
        {'bg': '#f3e8ff', 'border': '#9333ea', 'color': '#9333ea'},
        {'bg': '#ecfdf5', 'border': '#10b981', 'color': '#10b981'},
    ]
    
    for i, sql_file in enumerate(sql_files):
        color = colors[i % len(colors)]
        anomaly_count = sql_file['anomalies']['total']
        anomaly_color = '#28a745' if anomaly_count == 0 else '#f59e0b' if anomaly_count < 10 else '#dc3545'
        
        overview_cards.append(f'''
                        <div style="padding: 20px; background: {color['bg']}; border-left: 4px solid {color['border']}; border-radius: 6px;">
                            <h4 style="color: {color['color']}; margin-bottom: 10px;">{sql_file['database']} Database</h4>
                            <p style="font-size: 14px; color: #586069;">{sql_file['filename']} - Database schema definition</p>
                            <div style="margin-top: 15px;">
                                <span class="stat-item"><span class="label">Tables:</span> <span class="value">{sql_file['tables']}</span></span>
                                <span class="stat-item" style="margin-left: 15px;"><span class="label">Lines:</span> <span class="value">{sql_file['lines']:,}</span></span>
                                <span class="stat-item" style="margin-left: 15px;"><span class="label">Size:</span> <span class="value">{sql_file['size_kb']} KB</span></span>
                            </div>
                            <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid rgba(0,0,0,0.1);">
                                <span class="stat-item">
                                    <span class="label">⚠️ Anomalies:</span> 
                                    <span class="value" style="background: {anomaly_color};">{anomaly_count}</span>
                                </span>
                            </div>
                        </div>
        ''')
    
    overview_content = f'''
        <div id="overview-tab" class="tab-content active">
            <div class="sql-info">
                <h2>📋 Database Migration Overview</h2>
                <p style="margin-top: 10px; color: #586069;">This documentation contains the complete database schema for {len(sql_files)} database(s) in the Sample Project.</p>
                
                <div style="margin-top: 30px;">
                    <h3 style="margin-bottom: 15px; color: #24292e;">Database Summary</h3>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-top: 20px;">
                        {''.join(overview_cards)}
                    </div>
                </div>

                <div style="margin-top: 30px; padding: 20px; background: #fff5f5; border-left: 4px solid #dc3545; border-radius: 6px;">
                    <h3 style="color: #dc3545; margin-bottom: 15px;">⚠️ Schema Anomalies Detected</h3>
                    <p style="color: #586069; margin-bottom: 15px;">The following potential issues were detected in the database schemas:</p>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px;">
                        <div style="padding: 15px; background: white; border-radius: 6px; border: 1px solid #e1e4e8;">
                            <div style="font-weight: 600; color: #dc3545; margin-bottom: 5px;">Tables Without Primary Keys</div>
                            <div style="font-size: 24px; font-weight: bold; color: #24292e;">{sum(f['anomalies']['tables_without_primary_key'] for f in sql_files)}</div>
                        </div>
                        <div style="padding: 15px; background: white; border-radius: 6px; border: 1px solid #e1e4e8;">
                            <div style="font-weight: 600; color: #f59e0b; margin-bottom: 5px;">Tables Without Indexes</div>
                            <div style="font-size: 24px; font-weight: bold; color: #24292e;">{sum(f['anomalies']['tables_without_indexes'] for f in sql_files)}</div>
                        </div>
                        <div style="padding: 15px; background: white; border-radius: 6px; border: 1px solid #e1e4e8;">
                            <div style="font-weight: 600; color: #0366d6; margin-bottom: 5px;">Single Column Tables</div>
                            <div style="font-size: 24px; font-weight: bold; color: #24292e;">{sum(f['anomalies']['tables_with_single_column'] for f in sql_files)}</div>
                        </div>
                        <div style="padding: 15px; background: white; border-radius: 6px; border: 1px solid #e1e4e8;">
                            <div style="font-weight: 600; color: #9333ea; margin-bottom: 5px;">Potential Missing Foreign Keys</div>
                            <div style="font-size: 24px; font-weight: bold; color: #24292e;">{sum(f['anomalies']['missing_foreign_keys'] for f in sql_files)}</div>
                        </div>
                        <div style="padding: 15px; background: white; border-radius: 6px; border: 1px solid #e1e4e8;">
                            <div style="font-weight: 600; color: #f59e0b; margin-bottom: 5px;">Long Table Names (&gt;30 chars)</div>
                            <div style="font-size: 24px; font-weight: bold; color: #24292e;">{sum(f['anomalies']['long_table_names'] for f in sql_files)}</div>
                        </div>
                        <div style="padding: 15px; background: white; border-radius: 6px; border: 1px solid #e1e4e8;">
                            <div style="font-weight: 600; color: #28a745; margin-bottom: 5px;">Nullable Columns</div>
                            <div style="font-size: 24px; font-weight: bold; color: #24292e;">{sum(f['anomalies']['nullable_columns'] for f in sql_files)}</div>
                        </div>
                    </div>
                    <p style="margin-top: 15px; color: #586069; font-size: 14px;">
                        <strong>Note:</strong> These are potential issues that may require review. Some may be intentional design decisions.
                    </p>
                </div>

                <div style="margin-top: 30px; padding: 20px; background: #fffbeb; border-left: 4px solid #f59e0b; border-radius: 6px;">
                    <h3 style="color: #f59e0b; margin-bottom: 10px;">ℹ️ Information</h3>
                    <ul style="margin-left: 20px; color: #586069; line-height: 1.8;">
                        <li>All scripts are in SQL format compatible with DB2/SQL Server</li>
                        <li>Scripts include table creation, indexes, and foreign key constraints</li>
                        <li>Generated from mainframe migration process</li>
                        <li>Click on individual tabs to view complete SQL scripts</li>
                        <li>Total files: {len(sql_files)}</li>
                        <li>Total tables: {sum(f['tables'] for f in sql_files)}</li>
                        <li>Total lines: {sum(f['lines'] for f in sql_files):,}</li>
                        <li>Total anomalies detected: {sum(f['anomalies']['total'] for f in sql_files)}</li>
                    </ul>
                </div>
            </div>
        </div>
    '''
    
    # Generate content tabs for each SQL file
    for sql_file in sql_files:
        tab_id = sql_file['database'].lower().replace(' ', '_')
        escaped_content = escape_html(sql_file['content'])
        
        tab_content = f'''
        <div id="{tab_id}-tab" class="tab-content">
            <div class="sql-info">
                <h2>{sql_file['database']} Database Schema</h2>
                <p>Database: {sql_file['database']}</p>
                <div class="stats">
                    <div class="stat-item">
                        <span class="label">File:</span>
                        <span class="value">{sql_file['filename']}</span>
                    </div>
                    <div class="stat-item">
                        <span class="label">Total Lines:</span>
                        <span class="value">{sql_file['lines']:,}</span>
                    </div>
                    <div class="stat-item">
                        <span class="label">Tables:</span>
                        <span class="value">{sql_file['tables']}</span>
                    </div>
                    <div class="stat-item">
                        <span class="label">Size:</span>
                        <span class="value">{sql_file['size_kb']} KB</span>
                    </div>
                    <div class="stat-item">
                        <span class="label">Anomalies:</span>
                        <span class="value" style="background: {'#28a745' if sql_file['anomalies']['total'] == 0 else '#f59e0b' if sql_file['anomalies']['total'] < 10 else '#dc3545'};">{sql_file['anomalies']['total']}</span>
                    </div>
                </div>
                
                {f"""
                <div style="margin-top: 20px; padding: 15px; background: #fff5f5; border-left: 4px solid #dc3545; border-radius: 6px;">
                    <h3 style="color: #dc3545; margin-bottom: 10px; font-size: 16px;">⚠️ Anomaly Breakdown</h3>
                    <ul style="margin-left: 20px; color: #586069; line-height: 1.8; font-size: 14px;">
                        <li>Tables without primary key: <strong>{sql_file['anomalies']['tables_without_primary_key']}</strong></li>
                        <li>Tables without indexes: <strong>{sql_file['anomalies']['tables_without_indexes']}</strong></li>
                        <li>Single column tables: <strong>{sql_file['anomalies']['tables_with_single_column']}</strong></li>
                        <li>Potential missing foreign keys: <strong>{sql_file['anomalies']['missing_foreign_keys']}</strong></li>
                        <li>Long table names (&gt;30 chars): <strong>{sql_file['anomalies']['long_table_names']}</strong></li>
                        <li>Nullable columns: <strong>{sql_file['anomalies']['nullable_columns']}</strong></li>
                    </ul>
                </div>
                """ if sql_file['anomalies']['total'] > 0 else ""}
            </div>
            <div class="sql-code">
                <div class="code-header">
                    <span class="filename">{sql_file['filename']}</span>
                    <button class="copy-btn" onclick="copyCode('{tab_id}-code')">Copy Code</button>
                </div>
                <pre id="{tab_id}-code">{escaped_content}</pre>
            </div>
        </div>
        '''
        tab_contents.append(tab_content)
    
    # Generate complete HTML
    html_template = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SQL Schema Validation -  Overview</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica', 'Arial', sans-serif;
            line-height: 1.6;
            color: #24292e;
            background-color: #f6f8fa;
        }}

        .container {{
            max-width: 1280px;
            margin: 0 auto;
            padding: 20px;
        }}

        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 0;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}

        header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}

        header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}

        .nav-tabs {{
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }}

        .nav-tab {{
            padding: 12px 24px;
            background: white;
            border: 2px solid #e1e4e8;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 600;
            font-size: 14px;
        }}

        .nav-tab:hover {{
            border-color: #667eea;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(102, 126, 234, 0.2);
        }}

        .nav-tab.active {{
            background: #667eea;
            color: white;
            border-color: #667eea;
        }}

        .tab-content {{
            display: none;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            overflow: hidden;
        }}

        .tab-content.active {{
            display: block;
        }}

        .sql-info {{
            padding: 20px;
            background: #f6f8fa;
            border-bottom: 2px solid #e1e4e8;
        }}

        .sql-info h2 {{
            color: #667eea;
            margin-bottom: 10px;
        }}

        .sql-info .stats {{
            display: flex;
            gap: 30px;
            flex-wrap: wrap;
            margin-top: 15px;
        }}

        .stat-item {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .stat-item .label {{
            font-weight: 600;
            color: #586069;
        }}

        .stat-item .value {{
            background: #667eea;
            color: white;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.9em;
        }}

        .sql-code {{
            padding: 0;
            position: relative;
        }}

        .code-header {{
            background: #2d3748;
            color: white;
            padding: 12px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .code-header .filename {{
            font-family: 'Monaco', 'Courier New', monospace;
            font-size: 14px;
        }}

        .copy-btn {{
            background: #667eea;
            color: white;
            border: none;
            padding: 6px 16px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
            transition: background 0.3s ease;
        }}

        .copy-btn:hover {{
            background: #5568d3;
        }}

        .copy-btn.copied {{
            background: #48bb78;
        }}

        pre {{
            margin: 0;
            padding: 20px;
            overflow-x: auto;
            background: #1e1e1e;
            color: #d4d4d4;
            font-family: 'Monaco', 'Courier New', monospace;
            font-size: 13px;
            line-height: 1.5;
            max-height: 600px;
            overflow-y: auto;
        }}

        .search-container {{
            margin-bottom: 20px;
            padding: 15px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}

        .search-input {{
            width: 100%;
            padding: 12px;
            border: 2px solid #e1e4e8;
            border-radius: 6px;
            font-size: 14px;
            transition: border-color 0.3s ease;
        }}

        .search-input:focus {{
            outline: none;
            border-color: #667eea;
        }}

        footer {{
            text-align: center;
            padding: 30px;
            color: #586069;
            margin-top: 40px;
        }}

        .info-banner {{
            background: #e7f3ff;
            border-left: 4px solid #0366d6;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 6px;
        }}

        .info-banner p {{
            color: #0366d6;
            margin: 0;
        }}

        @media (max-width: 768px) {{
            header h1 {{
                font-size: 1.8em;
            }}
            
            .nav-tabs {{
                flex-direction: column;
            }}
            
            .nav-tab {{
                width: 100%;
            }}

            pre {{
                font-size: 11px;
            }}
        }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>📊 </h1>
            <p>Sample  - Database Schema Documentation</p>
        </div>
    </header>

    <div class="container">
        <div class="info-banner">
            <p>🤖 This documentation was automatically generated from SQL files on {datetime.now().strftime("%B %d, %Y at %H:%M")}</p>
        </div>

        <div class="search-container">
            <input type="text" class="search-input" id="searchInput" placeholder="🔍 Search across all SQL files...">
        </div>

        <div class="nav-tabs">
            {''.join(tab_buttons)}
        </div>

        {overview_content}
        {''.join(tab_contents)}
    </div>

    <footer>
        <p>Vigneshuvi Sample -  PostgreSQL Database SQL Scripts</p>
        <p style="margin-top: 10px; font-size: 0.9em;">Generated: {current_date}</p>
        <p style="margin-top: 5px; font-size: 0.8em; color: #959da5;">
            Auto-generated by generate_html.py | {len(sql_files)} SQL file(s) processed
        </p>
    </footer>

    <script>
        // Tab switching
        function showTab(tabName) {{
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => {{
                tab.classList.remove('active');
            }});
            
            // Remove active class from all nav tabs
            document.querySelectorAll('.nav-tab').forEach(tab => {{
                tab.classList.remove('active');
            }});
            
            // Show selected tab
            document.getElementById(tabName + '-tab').classList.add('active');
            
            // Add active class to clicked nav tab
            event.target.classList.add('active');
        }}

        // Copy code functionality
        function copyCode(elementId) {{
            const code = document.getElementById(elementId).textContent;
            navigator.clipboard.writeText(code).then(() => {{
                const btn = event.target;
                const originalText = btn.textContent;
                btn.textContent = '✓ Copied!';
                btn.classList.add('copied');
                setTimeout(() => {{
                    btn.textContent = originalText;
                    btn.classList.remove('copied');
                }}, 2000);
            }});
        }}

        // Simple search functionality
        document.getElementById('searchInput').addEventListener('input', function(e) {{
            const searchTerm = e.target.value.toLowerCase();
            if (searchTerm.length > 2) {{
                // Search through all pre elements
                document.querySelectorAll('pre').forEach(pre => {{
                    const content = pre.textContent.toLowerCase();
                    if (content.includes(searchTerm)) {{
                        // Highlight the parent tab
                        const tabContent = pre.closest('.tab-content');
                        if (tabContent && !tabContent.classList.contains('active')) {{
                            console.log('Found in:', tabContent.id);
                        }}
                    }}
                }});
            }}
        }});
    </script>
</body>
</html>'''
    
    return html_template


def main():
    """Main function to generate HTML documentation."""
    print("🔍 Scanning for SQL files...")
    
    # Get the parent directory (project root) where SQL files are located
    script_dir = Path(__file__).parent.parent
    
    # Find all SQL files
    sql_pattern = str(script_dir / "database-scripts/*.sql")
    sql_files = glob.glob(sql_pattern)
    
    if not sql_files:
        print("❌ No SQL files found in the directory!")
        return
    
    print(f"✅ Found {len(sql_files)} SQL file(s)")
    
    # Analyze each SQL file
    analyzed_files = []
    for sql_file in sorted(sql_files):
        print(f"   📄 Analyzing {os.path.basename(sql_file)}...")
        file_data = analyze_sql_file(sql_file)
        analyzed_files.append(file_data)
        print(f"      → {file_data['tables']} tables, {file_data['lines']:,} lines, {file_data['anomalies']['total']} anomalies")
    
    # Generate HTML
    print("\n🔨 Generating HTML documentation...")
    html_content = generate_html(analyzed_files)
    
    # Write HTML file
    output_file = script_dir / "docs/index.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ HTML documentation generated successfully!")
    print(f"📁 Output: {output_file}")
    print(f"\n📊 Summary:")
    print(f"   Total SQL files: {len(analyzed_files)}")
    print(f"   Total tables: {sum(f['tables'] for f in analyzed_files)}")
    print(f"   Total lines: {sum(f['lines'] for f in analyzed_files):,}")
    print(f"   Total size: {sum(f['size_kb'] for f in analyzed_files):.2f} KB")
    print(f"\n⚠️  Anomaly Summary:")
    print(f"   Total anomalies detected: {sum(f['anomalies']['total'] for f in analyzed_files)}")
    print(f"   - Tables without primary keys: {sum(f['anomalies']['tables_without_primary_key'] for f in analyzed_files)}")
    print(f"   - Tables without indexes: {sum(f['anomalies']['tables_without_indexes'] for f in analyzed_files)}")
    print(f"   - Single column tables: {sum(f['anomalies']['tables_with_single_column'] for f in analyzed_files)}")
    print(f"   - Potential missing foreign keys: {sum(f['anomalies']['missing_foreign_keys'] for f in analyzed_files)}")
    print(f"   - Long table names (>30 chars): {sum(f['anomalies']['long_table_names'] for f in analyzed_files)}")
    print(f"   - Nullable columns: {sum(f['anomalies']['nullable_columns'] for f in analyzed_files)}")
    print(f"\n🌐 Open index.html in your browser to view the documentation!")


if __name__ == "__main__":
    main()
