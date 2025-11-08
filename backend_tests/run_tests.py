#!/usr/bin/env python3
"""
Main test runner for Siress backend APIs
"""
import sys
import time
import requests
from datetime import datetime
from test_api import test_backend_apis

def main():
    print(" Starting Siress Backend Test Suite...")
    print(f" Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    start_time = time.time()
    
    try:
        test_backend_apis()
    except Exception as e:
        print(f" Test suite failed with error: {e}")
        sys.exit(1)
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\n Test duration: {duration:.2f} seconds")
    print(" Test suite completed!")

if __name__ == "__main__":
    main()