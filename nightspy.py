import psutil
import time
import logging
import os
from datetime import datetime

# Configure logging to save spy data to a stealth log file
logging.basicConfig(
    filename=f"nightspy_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
)

def night_spy_scan():
    """Scans running processes and logs their details."""
    try:
        print("\033[94m[*] NightSpyPy activated. Scanning system... \033[0m")
        logging.info("NightSpyPy scan initiated.")
        
        # Iterate through all running processes
        for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
            try:
                proc_info = proc.as_dict(attrs=['pid', 'name', 'memory_info', 'cpu_percent'])
                pid = proc_info['pid']
                name = proc_info['name']
                memory = proc_info['memory_info'].rss / (1024 * 1024)  # Convert to MB
                cpu = proc_info['cpu_percent']
                
                # Log process details
                log_message = f"PID: {pid}, Name: {name}, Memory: {memory:.2f} MB, CPU: {cpu:.2f}%"
                logging.info(log_message)
                
                # Display sample in console (limited to avoid clutter)
                if pid % 10 == 0:  # Show every 10th process
                    print(f"\033[92m[SPY] {log_message}\033[0m")
                    
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                logging.warning(f"Error accessing process {proc.pid}. Skipping.")
                continue
                
        print("\033[94m[*] Scan complete. Data logged to nightspy_*.log.\033[0m")
        logging.info("NightSpyPy scan completed.")
        
    except Exception as e:
        print(f"\033[91m[!] NightSpyPy error: {str(e)}\033[0m")
        logging.error(f"Error during scan: {str(e)}")

def main():
    """Main function to run NightSpyPy."""
    print("\033[95m=== NightSpyPy v1.0 - Stealth System Monitor ===\033[0m")
    print("\033[95mPress Ctrl+C to terminate the mission.\033[0m")
    
    try:
        while True:
            night_spy_scan()
            time.sleep(5)  # Scan every 5 seconds
    except KeyboardInterrupt:
        print("\n\033[93m[*] NightSpyPy terminated by agent.\033[0m")
        logging.info("NightSpyPy terminated by user.")
    except Exception as e:
        print(f"\033[91m[!] Critical error: {str(e)}\033[0m")
        logging.error(f"Critical error: {str(e)}")

if __name__ == "__main__":
    main()