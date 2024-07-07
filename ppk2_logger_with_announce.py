### python ppk2_logger_with_announce.py <voltage_level> [<com_port>]
import os
import time
from datetime import datetime
import serial
from pynrfjprog.LowLevel import API, DeviceFamily
import threading
import queue
import sys

# Function to configure and start the PPK2
def configure_and_start_ppk2(voltage_level):
    api = API(DeviceFamily.NRF52)
    api.open()
    api.connect_to_emu_without_snr()
    api.power_downdetection_start()
    api.power_off()
    
    print(f"Setting voltage level to {voltage_level}V")
    api.set_user_voltage(voltage_level)
    api.power_up()

    # Configure to sample at maximum rate (100 kHz)
    api.set_device_mode(device_mode=api.DeviceMode.PowerProfiler, period_us=10)
    api.start_measuring()

    return api

# Function to log serial data
def log_serial_data(port, baudrate=115200, log_file="serial_log.txt", data_queue=None):
    ser = serial.Serial(port, baudrate, timeout=1)
    with open(log_file, 'w') as f:
        while True:
            if ser.in_waiting:
                line = ser.readline().decode('utf-8').rstrip()
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                f.write(f"{timestamp}, {line}\n")
                data_queue.put(line)
            time.sleep(0.01)

# Function to print serial data to stdout
def print_serial_data(data_queue):
    while True:
        try:
            line = data_queue.get(timeout=1)
            print(f"Serial Output: {line}")
        except queue.Empty:
            pass

# Function to log power consumption and logic levels
def log_power_and_logic(api, log_file="ppk_log.txt"):
    with open(log_file, 'w') as f:
        while True:
            result = api.measurement_get_result()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            f.write(f"{timestamp}, {result['current']}, {result['voltage']}, {result['logic_levels']}\n")
            time.sleep(0.01)

# Main function
def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <voltage_level> [<com_port>]")
        sys.exit(1)

    voltage_level = float(sys.argv[1])
    serial_port = sys.argv[2] if len(sys.argv) > 2 else 'COM3'  # Default to 'COM3' if not provided

    print(f"Starting with voltage level: {voltage_level}V")
    print("Powering on the Device Under Test in:")
    for i in range(4, 0, -1):
        print(i)
        time.sleep(1)

    # Configure PPK2
    api = configure_and_start_ppk2(voltage_level)

    serial_log_file = "serial_log_{}.txt".format(datetime.now().strftime("%Y%m%d_%H%M%S"))
    ppk_log_file = "ppk_log_{}.txt".format(datetime.now().strftime("%Y%m%d_%H%M%S"))

    data_queue = queue.Queue(maxsize=100)  # Buffer to hold serial data

    try:
        # Start threads for logging serial data, power consumption, and printing serial data
        serial_thread = threading.Thread(target=log_serial_data, args=(serial_port, 115200, serial_log_file, data_queue))
        ppk_thread = threading.Thread(target=log_power_and_logic, args=(api, ppk_log_file))
        print_thread = threading.Thread(target=print_serial_data, args=(data_queue,))

        serial_thread.start()
        ppk_thread.start()
        print_thread.start()

        serial_thread.join()
        ppk_thread.join()
        print_thread.join()

    except KeyboardInterrupt:
        print("Stopping logging...")
    finally:
        api.stop_measuring()
        api.close()

if __name__ == "__main__":
    main()
