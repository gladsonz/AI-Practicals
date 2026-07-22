QUESTIONS = [
    {
        "id": "q_main_symptom",
        "text": "What is the primary issue you are experiencing with your laptop?",
        "options": [
            {"value": "power",        "label": "Power or booting issues (won't turn on, boot loops)"},
            {"value": "display",      "label": "Display or screen issues (blank screen, lines, flickering)"},
            {"value": "performance",  "label": "Performance issues (sluggishness, freezing, crashes)"},
            {"value": "battery",      "label": "Battery or charging issues (not holding charge, swelling)"},
            {"value": "audio",        "label": "Audio problems (no sound, crackling speaker, mic dead)"},
            {"value": "input",        "label": "Keyboard or trackpad issues (unresponsive keys, ghost clicks)"},
            {"value": "connectivity", "label": "Network or port issues (Wi-Fi dropping, USB ports dead)"},
            {"value": "cooling",      "label": "Overheating or fan noise (burning smell, loud whirring)"},
            {"value": "storage",      "label": "Storage or OS errors (blue screens, missing files)"},
        ],
        "always_ask": True,
        "relevance": {}
    },
    # POWER BRANCH
    {
        "id": "q_power_state",
        "text": "What happens when you press the power button?",
        "options": [
            {"value": "completely_dead", "label": "Absolutely nothing — no lights, no fans"},
            {"value": "lights_no_boot",   "label": "Status lights turn on, but screen stays black"},
            {"value": "boot_loop",       "label": "Starts to boot, then suddenly cuts power and restarts"},
            {"value": "blink_code",      "label": "Power/battery light blinks in a recurring pattern"},
        ],
        "relevant_to": ["power"],
        "relevance": {}
    },
    {
        "id": "q_charger_status",
        "text": "Does the laptop's charging indicator light turn on when plugged in?",
        "options": [
            {"value": "no_light",     "label": "No light at all"},
            {"value": "solid_light",   "label": "Yes, solid charging light"},
            {"value": "flickering",    "label": "The light flickers if I wiggle the cord"},
        ],
        "relevant_to": ["power", "battery"],
        "relevance": {}
    },
    # DISPLAY BRANCH
    {
        "id": "q_display_symptom",
        "text": "What does the screen look like?",
        "options": [
            {"value": "pitch_black",   "label": "Completely black, but I hear fans running"},
            {"value": "flicker_lines", "label": "Flickering, distorted colors, or permanent lines"},
            {"value": "faint_image",   "label": "Very faint image visible only under a flashlight"},
            {"value": "visual_blocks", "label": "Strange blocks, checkerboards, or frozen artifacts"},
        ],
        "relevant_to": ["display"],
        "relevance": {}
    },
    {
        "id": "q_external_monitor",
        "text": "If you plug the laptop into an external TV or monitor, does an image display there?",
        "options": [
            {"value": "works_external", "label": "Yes, the external monitor works perfectly"},
            {"value": "blank_external", "label": "No, the external monitor is also blank"},
            {"value": "not_tested",     "label": "I don't have an external monitor to test"},
        ],
        "relevant_to": ["display"],
        "relevance": {}
    },
    # PERFORMANCE BRANCH
    {
        "id": "q_perf_type",
        "text": "How is the performance degradation showing up?",
        "options": [
            {"value": "constant_slow",  "label": "Slow all the time, even moving the cursor is delayed"},
            {"value": "sudden_freeze",  "label": "Freezes or locks up entirely after a few minutes of use"},
            {"value": "bsod_crash",     "label": "Crashes to a Blue/Black screen with an error code"},
        ],
        "relevant_to": ["performance"],
        "relevance": {}
    },
    # BATTERY BRANCH
    {
        "id": "q_battery_physical",
        "text": "Are there any physical changes to the chassis or trackpad?",
        "options": [
            {"value": "swollen_case", "label": "The trackpad is lifting or the case looks warped/bulging"},
            {"value": "normal_case",  "label": "No physical changes, case looks flat and intact"},
        ],
        "relevant_to": ["battery"],
        "relevance": {}
    },
    # INPUT BRANCH
    {
        "id": "q_input_accident",
        "text": "Has the laptop been exposed to any liquids or drops recently?",
        "options": [
            {"value": "liquid_spill", "label": "Yes, a liquid spill occurred on the keyboard area"},
            {"value": "hard_drop",     "label": "Yes, it was dropped or sustained an impact"},
            {"value": "no_accidents",  "label": "No accidents or physical trauma"},
        ],
        "relevant_to": ["input", "power", "storage"],
        "relevance": {}
    },
    # COOLING BRANCH
    {
        "id": "q_cooling_behavior",
        "text": "What do the cooling fans sound like?",
        "options": [
            {"value": "jet_engine", "label": "Running at maximum speed constantly, even when idle"},
            {"value": "dead_silent", "label": "Completely silent, no air movement at all"},
            {"value": "grinding",    "label": "Making a clicking, buzzing, or grinding noise"},
        ],
        "relevant_to": ["cooling", "performance"],
        "relevance": {}
    },
    # STORAGE BRANCH
    {
        "id": "q_storage_sound_error",
        "text": "Do you hear any mechanical noises or see specific boot errors?",
        "options": [
            {"value": "clicking_sound", "label": "Faint clicking or ticking sound from inside the chassis"},
            {"value": "no_boot_device", "label": "Error screen saying 'No Bootable Device' or 'Insert Boot Disk'"},
            {"value": "stuck_loading",   "label": "Stuck infinitely on the Windows/macOS spinning logo"},
        ],
        "relevant_to": ["storage"],
        "relevance": {}
    }
]

DIAGNOSES = {
    # 1-6: Power / Boot Issues
    "dead_battery": {
        "label": "Completely Deep-Discharged Battery",
        "description": "The battery voltage has fallen below safe operational thresholds.",
        "fixes": ["Leave plugged into an OEM charger for 4 hours without turning it on", "Perform a hard reset by holding the power button for 30 seconds while unplugged"],
        "severity": "low"
    },
    "bad_charger": {
        "label": "Faulty Power Adapter",
        "description": "The charging brick or USB-C cable is no longer delivering required voltage or current.",
        "fixes": ["Test with a known working adapter of matching wattage", "Inspect the cable for fraying or sharp kinks"],
        "severity": "medium"
    },
    "broken_dc_jack": {
        "label": "Damaged DC Input Jack",
        "description": "The physical charging port inside the laptop has broken pins or cracked solder joints.",
        "fixes": ["Avoid wiggling the cord to prevent a short circuit", "Take it to a technician to solder a replacement port"],
        "severity": "high"
    },
    "motherboard_short": {
        "label": "Motherboard Component Short Circuit",
        "description": "A capacitor, MOSFET, or IC on the main system board has blown, safely preventing power-on.",
        "fixes": ["Requires professional board-level repair with a multimeter and thermal camera"],
        "severity": "critical"
    },
    "failed_bios": {
        "label": "Corrupted BIOS/UEFI Firmware",
        "description": "The system motherboard firmware is corrupted, stalling execution before the screen initializes.",
        "fixes": ["Attempt a vendor-specific BIOS recovery key combination (e.g., Win + B for HP)", "Remove CMOS battery to clear NVRAM"],
        "severity": "high"
    },
    "bad_power_button": {
        "label": "Defective Power Button Mechanism",
        "description": "The physical switch or keyboard-integrated power trace is open and cannot signal the board.",
        "fixes": ["If integrated into the keyboard, replace the complete keyboard assembly", "Inspect the ribbon connection"],
        "severity": "medium"
    },

    # 7-12: Display / Screen Issues
    "cracked_lcd": {
        "label": "Physically Cracked LCD Matrix",
        "description": "The inner glass layer of the display pane is shattered, leaking liquid crystals.",
        "fixes": ["Replace the LCD screen panel entirely", "Use an external monitor as a temporary desktop substitute"],
        "severity": "high"
    },
    "bad_display_cable": {
        "label": "Loose or Worn eDP Display Cable",
        "description": "The video ribbon cable routed through the display hinge is loose or pinched.",
        "fixes": ["Reseat the eDP connector on the back of the LCD display and motherboard"],
        "severity": "medium"
    },
    "failed_gpu": {
        "label": "Failing Dedicated Graphics Card (GPU)",
        "description": "The discrete graphics chip has experienced thermal degradation or solder ball failure.",
        "fixes": ["Disable dGPU in BIOS to force internal processor graphics", "Requires motherboard replacement or BGA reballing"],
        "severity": "critical"
    },
    "dead_backlight": {
        "label": "Failed Screen Backlight Inverter/LEDs",
        "description": "The display matrix displays pixels, but the lighting system fails to illuminate them.",
        "fixes": ["Check for blown fuses on the motherboard screen circuit", "Replace the LCD panel assembly"],
        "severity": "high"
    },
    "stuck_pixels": {
        "label": "Stuck or Dead Panel Pixels",
        "description": "Sub-pixels are physically stuck on a single color configuration.",
        "fixes": ["Run an online pixel-flashing software utility for 30 minutes", "Apply light pressure with a microfibre cloth"],
        "severity": "low"
    },
    "display_driver_crash": {
        "label": "Corrupted Display Graphics Driver",
        "description": "The operating system video driver is crashing instantly upon initialization.",
        "fixes": ["Boot into Safe Mode", "Run Display Driver Uninstaller (DDU) and install the latest stable OEM driver"],
        "severity": "medium"
    },

    # 13-18: Performance / Stability Issues
    "thermal_throttling": {
        "label": "Aggressive Thermal Throttling",
        "description": "The CPU/GPU dropping speeds drastically to protect itself from excessive structural heat.",
        "fixes": ["Clean out dust blocks from heatsink radiator fins", "Change Windows performance profile to balanced"],
        "severity": "medium"
    },
    "ram_failure": {
        "label": "Defective or Unseated RAM Module",
        "description": "Random Access Memory chips have corrupted blocks or poor pin contact.",
        "fixes": ["Remove RAM stick, clean gold contacts with an eraser, and snap firmly back into slot", "Run MemTest86 tool"],
        "severity": "high"
    },
    "maxed_out_cpu": {
        "label": "CPU Saturation by Background Exploits",
        "description": "An orphaned task or hidden routine is hogging 100% of available processing threads.",
        "fixes": ["Open Task Manager/Activity Monitor and force terminate high-utilization tasks", "Disable startup apps"],
        "severity": "low"
    },
    "drive_fragmentation": {
        "label": "Severe Storage Fragmentation (HDD Only)",
        "description": "Mechanical hard drive files are scattered across surfaces, forcing excessive read heads seeking delay.",
        "fixes": ["Run Windows Defragment and Optimize Drives tool", "Upgrade system to a modern Solid State Drive (SSD)"],
        "severity": "low"
    },
    "malware_infection": {
        "label": "Active Malware or Crypto-Miner Infection",
        "description": "Malicious code running silently is draining CPU and bus cycles.",
        "fixes": ["Perform an offline boot scan with Windows Defender or Malwarebytes"],
        "severity": "medium"
    },
    "outdated_chipset": {
        "label": "Outdated Chipset/ACPI Driver Stack",
        "description": "System architecture interfaces are running suboptimally due to legacy configurations.",
        "fixes": ["Install official motherboard chipset interface utilities directly from the factory vendor portal"],
        "severity": "low"
    },

    # 19-23: Battery Capacity & Degradation
    "battery_degradation": {
        "label": "Naturally Worn Battery Cells",
        "description": "The lithium-ion structural chemistry has chemically degraded over hundreds of charge cycles.",
        "fixes": ["Generate a health check profile (powercfg /batteryreport)", "Replace battery pack when full charge falls below 50%"],
        "severity": "medium"
    },
    "calibration_error": {
        "label": "OS Battery Gauge Miscalibration",
        "description": "The internal fuel gauge microchip disagrees with actual operating system charge predictions.",
        "fixes": ["Charge to 100%, discharge completely until system forces shutdown, then recharge to full uninterrupted"],
        "severity": "low"
    },
    "counterfeit_charger": {
        "label": "Incompatible or Underpowered Power Supply",
        "description": "The laptop throttles charging speeds because it doesn't recognize correct charging protocol handshakes.",
        "fixes": ["Avoid generic multi-adapters", "Only utilize power bricks matching the exact manufacturer voltage requirements"],
        "severity": "medium"
    },
    "heavy_background_drain": {
        "label": "Aggressive OS App Power Drain",
        "description": "Apps with high power usage configurations are waking sleeping processor states repeatedly.",
        "fixes": ["Audit background permissions", "Enable eco/battery saver modes"],
        "severity": "low"
    },
    "swollen_battery": {
        "label": "Severely Swollen Battery Cells",
        "description": "Internal gas accumulation has bloated structural lining. CRITICAL FIRE RISK.",
        "fixes": ["Power off system immediately, unplug, and carefully extract swollen battery pack", "Dispose safely at a recycling facility"],
        "severity": "critical"
    },

    # 24-28: Audio Anomalies
    "blown_speakers": {
        "label": "Blown Out Speaker Diaphragms",
        "description": "The thin voice coil or cone membrane inside the laptop speaker enclosure has torn physically.",
        "fixes": ["Lower internal system volume gain", "Replace the internal left/right audio speaker sub-modules"],
        "severity": "low"
    },
    "audio_driver_crash": {
        "label": "Corrupted Audio Architecture Driver",
        "description": "Software layer handling high definition audio pipelines has fallen into an error lock.",
        "fixes": ["Open Device Manager, uninstall the High Definition Audio Controller device, and restart to reinstall"],
        "severity": "low"
    },
    "broken_headphone_jack": {
        "label": "Damaged 3.5mm Headphone Switch",
        "description": "Physical logic contacts inside the headphone port are bent, trapping the OS in permanent headphone state.",
        "fixes": ["Carefully clear debris out using compressed air or an antistatic toothpick", "Switch to Bluetooth output"],
        "severity": "medium"
    },
    "muted_software": {
        "label": "Orphaned Software Exclusivity Mute",
        "description": "An application has claimed exclusive audio channel control and muted alternative pipelines.",
        "fixes": ["Reset default sound map selections within platform sound panels"],
        "severity": "low"
    },
    "mic_hardware_failure": {
        "label": "Defective Webcam/Bezel Microphone Array",
        "description": "The microphone array trace along the webcam PCB is severed or electrically dead.",
        "fixes": ["Verify application privacy permissions allow access to microphone hardware", "Use a USB headset alternative"],
        "severity": "low"
    },

    # 29-33: Input Devices
    "liquid_damage_keyboard": {
        "label": "Corroded Keyboard Membrane Circuitry",
        "description": "Spilled fluid dried inside matrix paths, causing trace shorts or phantom keystrokes.",
        "fixes": ["Disconnect battery immediately to reduce electrolysis damage", "Replace internal keyboard assembly"],
        "severity": "high"
    },
    "sticky_keys_hardware": {
        "label": "Debris Contaminated Key Switches",
        "description": "Dust particles, crumbs, or dried liquids are impeding mechanical scissor switch travel.",
        "fixes": ["Carefully remove keycap and scrub mechanisms with 99% isopropyl alcohol"],
        "severity": "low"
    },
    "trackpad_driver_disabled": {
        "label": "Disabled Trackpad Driver Interface",
        "description": "Trackpad is offline due to a disabled function key sequence toggled by mistake.",
        "fixes": ["Press designated function key combination (e.g., Fn + F6 or F9) to restore tracking logic"],
        "severity": "low"
    },
    "broken_keyboard_ribbon": {
        "label": "Loose Keyboard Interface Ribbon",
        "description": "The ultra-thin locking flip bar on the internal motherboard keyboard connector has backed out.",
        "fixes": ["Open rear chassis access panels, flip open the trace lock tab, reseat the ribbon, and clamp shut"],
        "severity": "medium"
    },
    "trackpad_hardware_failure": {
        "label": "Defective Trackpad Dome Switch",
        "description": "The structural underlying sensor array or click plate has lost elastic tension.",
        "fixes": ["Replace trackpad sensor plate module situated underneath the battery cradle"],
        "severity": "medium"
    },

    # 34-39: Connectivity & Ports
    "failed_wifi_card": {
        "label": "Defective Wi-Fi/Bluetooth PCIe Card",
        "description": "The integrated wireless network controller module has suffered hardware failure.",
        "fixes": ["Swap internal M.2 Wi-Fi component card module", "Verify internal main/aux coaxial antenna lines are snapped on"],
        "severity": "medium"
    },
    "broken_usb_port": {
        "label": "Physically Broken USB Port Pins",
        "description": "Plastic guides inside a USB connection port have fractured, bending internal lines.",
        "fixes": ["Insulate exposed interior metal pin connectors to stop motherboard short-circuits", "Use an alternate hub port"],
        "severity": "medium"
    },
    "outdated_wifi_driver": {
        "label": "Incompatible Wireless Adapter Driver",
        "description": "The current network interface driver configuration is causing connection timing drops with modern routers.",
        "fixes": ["Update driver using a wired ethernet connection or flash drive"],
        "severity": "low"
    },
    "router_ip_conflict": {
        "label": "Local Network DHCP IP Address Conflict",
        "description": "The local access point router assigned a duplicate local IP network assignment mapping to the machine.",
        "fixes": ["Open command prompt and run 'ipconfig /release' followed by 'ipconfig /renew'"],
        "severity": "low"
    },
    "bluetooth_stack_crash": {
        "label": "Corrupted OS Bluetooth Subsystem Stack",
        "description": "Operating system configuration parameters for wireless discovery are locked.",
        "fixes": ["Restart the core Bluetooth Support Service within system management services panels"],
        "severity": "low"
    },
    "hdmi_port_failure": {
        "label": "Damaged Video Interface Port (HDMI)",
        "description": "Broken micro-solder structural links joining the high definition media port to the system path.",
        "fixes": ["Switch layout processing outputs to a USB-C Alt-Mode DisplayPort connection"],
        "severity": "medium"
    },

    # 40-44: Thermal System
    "seized_fan": {
        "label": "Seized Bearing Cooling Fan Assembly",
        "description": "Internal dust build-up or a failed sleeve bearing has mechanically locked the laptop fan rotor blades.",
        "fixes": ["Replace the structural cooling fan unit entirely", "Do not operate system under heavy loads while fan is dead"],
        "severity": "high"
    },
    "dried_thermal_paste": {
        "label": "Dried Out Thermal Interface Material",
        "description": "Factory thermal paste has hardened into a crust, losing its thermal transfer capabilities.",
        "fixes": ["Remove heatsink array, scrape clean old compound with alcohol, and apply fresh thermal compound"],
        "severity": "high"
    },
    "blocked_vents": {
        "label": "Choked Heat Dissipation Air Vents",
        "description": "Dust blankets have accumulated behind exhaust radiator fins, trapping heat inside the case.",
        "fixes": ["Blast reverse bursts of compressed air into the exhaust grilles while pinning fan blades steady"],
        "severity": "low"
    },
    "fan_curve_glitch": {
        "label": "Corrupted Embedded Controller (EC) Fan Profile",
        "description": "The motherboard embedded controller firmware is failing to scale fan speeds up alongside temperature hikes.",
        "fixes": ["Update to latest motherboard manufacturer firmware version", "Force override with custom software tools like HWinfo"],
        "severity": "medium"
    },
    "failed_heatpipe": {
        "label": "Ruptured Internal Heatsink Vapor Pipe",
        "description": "The vacuum seal on the copper heatpipe cracked, evaporating the inner fluid phase tracking structure.",
        "fixes": ["Replace entire assembly block line including copper runners"],
        "severity": "high"
    },

    # 45-50: Storage & Filesystem
    "failing_hdd": {
        "label": "Failing Mechanical Disk Drive (Bad Sectors)",
        "description": "Physical disk sectors are demagnetizing or mechanical components are failing. BACKUP DATA NOW.",
        "fixes": ["Check SMART health status immediately", "Clone data structure immediately to an SSD drive"],
        "severity": "critical"
    },
    "nvme_overheating": {
        "label": "NVMe M.2 Solid State Drive Overheating",
        "description": "High performance storage cells are exceeding maximum operational temperature limits.",
        "fixes": ["Apply an ultra-thin thermal pad conductor to diffuse heat outward into chassis base"],
        "severity": "medium"
    },
    "corrupted_os_files": {
        "label": "Corrupted System Core Filesystem",
        "description": "Crucial operating system files are corrupt due to a sudden power loss or failed update.",
        "fixes": ["Run administrative check tool 'sfc /scannow' or execute an OS system restoration snapshot"],
        "severity": "medium"
    },
    "full_system_drive": {
        "label": "Saturated System Allocation Partition",
        "description": "Primary storage space is completely full, leaving no storage space for operating system swap files.",
        "fixes": ["Run storage clean up tools", "Purge heavy caching directories"],
        "severity": "low"
    },
    "loose_storage_drive": {
        "label": "Loose Storage Interface Connection Slot",
        "description": "Impact shock or thermal expansion backed the NVMe/SATA connection drive out of its pin layout slot.",
        "fixes": ["Unscrew access lid, back drive out cleanly from port socket slot, reinsert squarely, and tighten down secure anchor screw"],
        "severity": "medium"
    },
    "bitlocker_lockout": {
        "label": "BitLocker/FileVault Security Encryption Lockout",
        "description": "Platform configuration adjustments triggered drive tamper protection, demanding raw encryption safety keys.",
        "fixes": ["Retrieve unique multi-digit raw hardware safety alphanumeric string recovery key via registered user cloud accounts"],
        "severity": "high"
    }
}

SCORING_RULES = {
    # Power Branch Weights
    ("q_main_symptom", "power"): {"dead_battery": 0.3, "bad_charger": 0.3, "broken_dc_jack": 0.2, "motherboard_short": 0.2, "failed_bios": 0.2, "bad_power_button": 0.2},
    ("q_power_state", "completely_dead"): {"dead_battery": 0.6, "bad_charger": 0.6, "broken_dc_jack": 0.7, "motherboard_short": 0.5, "bad_power_button": 0.5},
    ("q_power_state", "lights_no_boot"): {"failed_bios": 0.7, "ram_failure": 0.6, "failed_gpu": 0.5, "dead_backlight": 0.4},
    ("q_power_state", "boot_loop"): {"failed_bios": 0.5, "corrupted_os_files": 0.5, "thermal_throttling": 0.4, "ram_failure": 0.3},
    ("q_power_state", "blink_code"): {"ram_failure": 0.8, "failed_bios": 0.6, "motherboard_short": 0.4},
    ("q_charger_status", "no_light"): {"bad_charger": 0.8, "broken_dc_jack": 0.8, "motherboard_short": 0.6, "dead_battery": 0.4},
    ("q_charger_status", "flickering"): {"broken_dc_jack": 0.9, "bad_charger": 0.5},
    ("q_charger_status", "solid_light"): {"bad_power_button": 0.5, "failed_bios": 0.4, "dead_battery": -0.3},

    # Display Branch Weights
    ("q_main_symptom", "display"): {"cracked_lcd": 0.4, "bad_display_cable": 0.4, "failed_gpu": 0.4, "dead_backlight": 0.4, "stuck_pixels": 0.3, "display_driver_crash": 0.3},
    ("q_display_symptom", "pitch_black"): {"dead_backlight": 0.7, "bad_display_cable": 0.5, "failed_gpu": 0.5},
    ("q_display_symptom", "flicker_lines"): {"bad_display_cable": 0.8, "cracked_lcd": 0.6, "failed_gpu": 0.4},
    ("q_display_symptom", "faint_image"): {"dead_backlight": 0.95},
    ("q_display_symptom", "visual_blocks"): {"failed_gpu": 0.9, "display_driver_crash": 0.5},
    ("q_external_monitor", "works_external"): {"cracked_lcd": 0.8, "bad_display_cable": 0.8, "dead_backlight": 0.7, "failed_gpu": -0.5},
    ("q_external_monitor", "blank_external"): {"failed_gpu": 0.8, "display_driver_crash": 0.6, "failed_bios": 0.4},

    # Performance Branch Weights
    ("q_main_symptom", "performance"): {"thermal_throttling": 0.4, "maxed_out_cpu": 0.4, "malware_infection": 0.4, "ram_failure": 0.2, "drive_fragmentation": 0.2, "outdated_chipset": 0.2},
    ("q_perf_type", "constant_slow"): {"maxed_out_cpu": 0.6, "malware_infection": 0.6, "drive_fragmentation": 0.7, "full_system_drive": 0.5, "outdated_chipset": 0.4},
    ("q_perf_type", "sudden_freeze"): {"thermal_throttling": 0.8, "ram_failure": 0.5, "nvme_overheating": 0.6, "seized_fan": 0.5},
    ("q_perf_type", "bsod_crash"): {"ram_failure": 0.7, "corrupted_os_files": 0.6, "failing_hdd": 0.5, "loose_storage_drive": 0.4},

    # Battery Branch Weights
    ("q_main_symptom", "battery"): {"battery_degradation": 0.5, "calibration_error": 0.4, "counterfeit_charger": 0.4, "heavy_background_drain": 0.3, "swollen_battery": 0.3},
    ("q_battery_physical", "swollen_case"): {"swollen_battery": 0.98},
    ("q_battery_physical", "normal_case"): {"swollen_battery": -0.5, "battery_degradation": 0.4},

    # Audio Branch Weights
    ("q_main_symptom", "audio"): {"blown_speakers": 0.5, "audio_driver_crash": 0.5, "broken_headphone_jack": 0.4, "muted_software": 0.4, "mic_hardware_failure": 0.3},

    # Input Branch Weights
    ("q_main_symptom", "input"): {"liquid_damage_keyboard": 0.4, "sticky_keys_hardware": 0.4, "trackpad_driver_disabled": 0.4, "broken_keyboard_ribbon": 0.4, "trackpad_hardware_failure": 0.4},
    ("q_input_accident", "liquid_damage_keyboard"): {"liquid_damage_keyboard": 0.95},
    ("q_input_accident", "hard_drop"): {"loose_storage_drive": 0.7, "cracked_lcd": 0.6, "failing_hdd": 0.5, "broken_keyboard_ribbon": 0.4},

    # Connectivity / Ports Branch Weights
    ("q_main_symptom", "connectivity"): {"failed_wifi_card": 0.4, "broken_usb_port": 0.4, "outdated_wifi_driver": 0.4, "router_ip_conflict": 0.3, "bluetooth_stack_crash": 0.3, "hdmi_port_failure": 0.3},

    # Cooling Branch Weights
    ("q_main_symptom", "cooling"): {"seized_fan": 0.4, "dried_thermal_paste": 0.4, "blocked_vents": 0.4, "fan_curve_glitch": 0.3, "failed_heatpipe": 0.3},
    ("q_cooling_behavior", "jet_engine"): {"blocked_vents": 0.8, "dried_thermal_paste": 0.7, "maxed_out_cpu": 0.5, "failed_heatpipe": 0.6},
    ("q_cooling_behavior", "dead_silent"): {"seized_fan": 0.9, "fan_curve_glitch": 0.6},
    ("q_cooling_behavior", "grinding"): {"seized_fan": 0.95},

    # Storage Branch Weights
    ("q_main_symptom", "storage"): {"failing_hdd": 0.4, "nvme_overheating": 0.3, "corrupted_os_files": 0.4, "full_system_drive": 0.3, "loose_storage_drive": 0.3, "bitlocker_lockout": 0.3},
    ("q_storage_sound_error", "clicking_sound"): {"failing_hdd": 0.95},
    ("q_storage_sound_error", "no_boot_device"): {"loose_storage_drive": 0.8, "failing_hdd": 0.7, "corrupted_os_files": 0.5, "bitlocker_lockout": 0.4},
    ("q_storage_sound_error", "stuck_loading"): {"corrupted_os_files": 0.8, "failing_hdd": 0.5, "malware_infection": 0.4}
}


def run_diagnostic():
    print("=" * 50)
    print("   TERMINAL LAPTOP DIAGNOSTIC TOOL")
    print("=" * 50)

    scores = {k: 0.0 for k in DIAGNOSES.keys()}
    asked = []
    main_symptom = None

    for q in QUESTIONS:
        # Determine if the question is relevant based on the main symptom
        is_relevant = q.get("always_ask", False) or (main_symptom and main_symptom in q.get("relevant_to", []))

        if is_relevant:
            print(f"\n{q['text']}")
            
            # Print available options
            for i, opt in enumerate(q["options"]):
                print(f"  [{i + 1}] {opt['label']}")

            # Input validation loop
            while True:
                try:
                    choice = int(input("\nSelect an option (enter the number): "))
                    if 1 <= choice <= len(q["options"]):
                        selected_val = q["options"][choice - 1]["value"]
                        break
                    else:
                        print("Invalid selection. Please choose a number from the list.")
                except ValueError:
                    print("Invalid input. Please enter a number.")

            # Record main symptom if this is the first question
            if q["id"] == "q_main_symptom":
                main_symptom = selected_val

            # Apply scoring rules
            rule_key = (q["id"], selected_val)
            if rule_key in SCORING_RULES:
                for diag, score in SCORING_RULES[rule_key].items():
                    scores[diag] += score

            asked.append(q["id"])

    # Calculate and display results
    print("\n" + "=" * 50)
    print("   DIAGNOSTIC RESULTS")
    print("=" * 50)

    # Sort diagnoses by score in descending order
    sorted_diagnoses = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    
    # Filter out low scores (Threshold > 0.3)
    top_results = [(k, v) for k, v in sorted_diagnoses[:3] if v > 0.3]

    if not top_results:
        print("\nNo definitive diagnosis could be found based on your answers.")
        print("Please consult a professional technician.")
    else:
        for diag_key, score in top_results:
            diag_info = DIAGNOSES[diag_key]
            print(f"\n[!] POTENTIAL ISSUE: {diag_info['label']} (Confidence Score: {score:.2f})")
            print(f"    Severity:    {diag_info['severity'].upper()}")
            print(f"    Description: {diag_info['description']}")
            print("    Suggested Fixes:")
            for fix in diag_info['fixes']:
                print(f"      - {fix}")

    print("\n" + "=" * 50)


if __name__ == "__main__":
    run_diagnostic() 