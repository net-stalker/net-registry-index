#!/usr/bin/env python
"""Module proving getting current datetime"""
from datetime import datetime

def main():
    """Main function"""
    curr_date = datetime.now().date().strftime('%Y-%m-%d')
    print(curr_date)

if __name__ == "__main__":
    main()
 