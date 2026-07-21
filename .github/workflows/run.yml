name: Create Temporary Email

on:
  workflow_dispatch:  # دستی اجرا میشه

jobs:
  create-email:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v4
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install requests
    
    - name: Create email
      run: python create_email.py
    
    - name: Save email info
      uses: actions/upload-artifact@v4
      with:
        name: email-info
        path: email_info.txt
