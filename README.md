# Purdue-TC Controlled Dataset Collection

This repository provides scripts and configuration files to **collect controlled network traffic datasets** for traffic classification research.  
The datasets capture application flows under systematically varied network conditions (capacity, delay, background traffic, user behavior), enabling reproducible experiments on data augmentation and traffic classification methods.

---

## System Resources

Experiments were conducted on a high-performance server with the following specifications:

- **CPU:** 2 × Intel E5-2630 v3 (Haswell, 8 cores each, 2.40 GHz)  
- **RAM:** 128 GB ECC DDR4 (1866 MHz)  
- **Storage:**  
  - 2 × 1.2 TB 10K RPM SAS HDDs  
  - 1 × 480 GB Intel DC S3500 SSD  
- **OS:** Ubuntu 20.04 (UBUNTU20-64-STD)

---

## Dataset Description

The dataset consists of flows from **five application types**:

1. **Video Streaming (VS):** DASH streaming of Big Buck Bunny & Elephants Dream at multiple resolutions.  
2. **Video Conferencing (VC):** Two-way audio-video calls with aiortc.  
3. **Web Browsing:** Selenium-based scripted browsing of top-500 websites with realistic wait times.  
4. **FTP:** File transfers generated from synthetic file distributions.  
5. **Email:** POP3 client/server fetching messages with polling.

Each application is run across controlled conditions of:

- **Bottleneck link capacities:** 5, 10, 100, 200 Mbps  
- **Round-trip times (RTT):** 1, 10, 50, 75 ms  
- **Background traffic:** On/Off UDP traffic at different rates  
- **User behavior:** Varying think times for browsing sessions

These systematic variations produce a **rich dataset** for evaluating traffic classification robustness.

---

## Setup & Installation

### 1. Install Dependencies

Run the provided installation scripts in order:

```bash
sudo bash install_script_part1.sh
sudo bash install_script_part2.sh
```

These scripts install Docker, Containernet, traffic generators, and supporting libraries.

### 2. Configure Dataset Paths

Update the **base directory** in `controlled_config.ini`:

```ini
[PATHS]
base = /path/to/REPO
```

This path will be used for mounting volumes such as FTP, Web, Video Streaming, and Conferencing traces. This path is where the repository is located.

### 3. Run Experiments

Start the experiment pipeline:

```bash
sudo ./run_experiments.sh
```

This script will:
- Launch the dumbbell topology in Containernet  
- Deploy client/server containers with applications  
- Execute workloads across configurations  
- Save packet traces into the configured dataset paths  

---

## Reference

If you use this dataset in your work, please cite:

>>>
---

## License

This project is released for academic and research use. Please check the repository’s license file for details.
