#!/usr/bin/env python
from datetime import datetime

def main():
    curr_date = datetime.now().date().strftime('%Y-%m-%d')
    print(curr_date)

if __name__ == "__main__":
    main()