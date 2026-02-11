#!/usr/bin/env python3
"""
Update GitHub Username in All Files

This script replaces 'YOUR_USERNAME' with your actual GitHub username
in all documentation and web files.

Usage:
    python update_github_username.py your_actual_username
"""

import sys
import os

def update_files(username):
    """Update all files with the GitHub username."""
    
    files_to_update = [
        'web/index.html',
        'web/download.html',
        'DEPLOYMENT_GUIDE.md',
        'CONTRIBUTING.md',
        'SETUP_YOUR_GITHUB.md',
        'INSTALL.md',
        'GITHUB_SETUP.md',
        'GET_STARTED_NOW.md'
    ]
    
    updated_count = 0
    
    for filepath in files_to_update:
        if not os.path.exists(filepath):
            print(f"⚠️  Skipping {filepath} (not found)")
            continue
            
        try:
            # Read file
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Count replacements
            count = content.count('YOUR_USERNAME')
            
            if count == 0:
                print(f"✓ {filepath} (already updated)")
                continue
            
            # Replace
            new_content = content.replace('YOUR_USERNAME', username)
            
            # Write back
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✓ {filepath} ({count} replacements)")
            updated_count += 1
            
        except Exception as e:
            print(f"❌ Error updating {filepath}: {e}")
    
    return updated_count

def main():
    """Main function."""
    
    print("=" * 60)
    print("🔧 GitHub Username Updater")
    print("=" * 60)
    print()
    
    # Get username
    if len(sys.argv) < 2:
        print("Usage: python update_github_username.py YOUR_GITHUB_USERNAME")
        print()
        username = input("Enter your GitHub username: ").strip()
        if not username:
            print("❌ No username provided. Exiting.")
            return
    else:
        username = sys.argv[1].strip()
    
    print(f"📝 Updating files with username: {username}")
    print()
    
    # Update files
    count = update_files(username)
    
    print()
    print("=" * 60)
    if count > 0:
        print(f"✅ Success! Updated {count} files.")
        print()
        print("Your links:")
        print(f"  Repository: https://github.com/{username}/OpenLiveCaption")
        print(f"  Releases:   https://github.com/{username}/OpenLiveCaption/releases")
        print(f"  Website:    https://{username}.github.io/OpenLiveCaption/")
        print()
        print("Next steps:")
        print("  1. Review the changes: git diff")
        print("  2. Commit: git add . && git commit -m 'Update GitHub username'")
        print("  3. Push: git push")
    else:
        print("ℹ️  All files already updated or no changes needed.")
    print("=" * 60)

if __name__ == '__main__':
    main()
