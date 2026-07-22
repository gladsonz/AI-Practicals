from flask import Flask, render_template, request, jsonify, session
import json
app = Flask(__name__)
app.secret_key = "car_diag_secret_2026"

QUESTIONS = [
    {
        "id": "q_main_symptom",
        "text": "What's the main problem you're experiencing with your car?",
        "options": [
            {"value": "wont_start",    "label": "Car won't start at all"},
            {"value": "engine_noise",  "label": "Strange engine noises (knocking, ticking, rattling)"},
            {"value": "overheating",   "label": "Engine overheating / temperature warning"},
            {"value": "stalling",      "label": "Engine stalls or cuts out while driving"},
            {"value": "brakes",        "label": "Brake problems (squealing, grinding, spongy pedal)"},
            {"value": "transmission",  "label": "Transmission / gear shifting issues"},
            {"value": "electrical",    "label": "Electrical / battery / lights not working"},
            {"value": "steering",      "label": "Steering or suspension issues (vibration, pulling)"},
            {"value": "exhaust",       "label": "Exhaust smoke or unusual smell"},
            {"value": "leaks",         "label": "Fluid leaks under the car"},
        ],
        "always_ask": True,
        "relevance": {}
    },
    # WON'T START
    {
        "id": "q_start_lights",
        "text": "When you turn the key / press start, do the dashboard lights come on?",
        "options": [
            {"value": "yes_all",    "label": "Yes – all lights come on normally"},
            {"value": "dim",        "label": "Yes, but they're very dim or flicker"},
            {"value": "no",         "label": "No – completely dark dashboard"},
            {"value": "click",      "label": "Lights on, but hear rapid clicking when starting"},
        ],
        "relevant_to": ["wont_start"],
        "relevance": {"dead_battery": 0.7, "bad_starter": 0.5, "bad_alternator": 0.4}
    },
    {
        "id": "q_start_sound",
        "text": "What sound (if any) do you hear when trying to start the car?",
        "options": [
            {"value": "nothing",        "label": "Complete silence"},
            {"value": "single_click",   "label": "One heavy click, then nothing"},
            {"value": "rapid_click",    "label": "Rapid clicking (like a machine gun)"},
            {"value": "cranks_no_fire", "label": "Engine cranks / turns over but won't fire up"},
            {"value": "grinding",       "label": "Grinding noise when cranking"},
        ],
        "relevant_to": ["wont_start"],
        "relevance": {"dead_battery": 0.7, "bad_starter": 0.8, "bad_alternator": 0.3, "fuel_delivery": 0.4}
    },
    {
        "id": "q_recent_drove",
        "text": "Did the car drive fine until it wouldn't start, or was it showing warning signs?",
        "options": [
            {"value": "fine_until_now", "label": "Drove fine until it suddenly wouldn't start"},
            {"value": "warning_signs",  "label": "Had warning signs (sluggish starts, warnings)"},
            {"value": "sat_parked",     "label": "Was parked for a long time (weeks/months)"},
        ],
        "relevant_to": ["wont_start"],
        "relevance": {"dead_battery": 0.5, "fuel_delivery": 0.3, "bad_alternator": 0.4}
    },
    # ENGINE NOISE
    {
        "id": "q_noise_type",
        "text": "What kind of noise is the engine making?",
        "options": [
            {"value": "knocking",   "label": "Deep knocking or banging from engine"},
            {"value": "ticking",    "label": "Rapid ticking or tapping sound"},
            {"value": "rattling",   "label": "Rattling or chain-like noise on startup"},
            {"value": "squealing",  "label": "High-pitched squealing from engine area"},
            {"value": "hissing",    "label": "Hissing or steam-like sound"},
        ],
        "relevant_to": ["engine_noise"],
        "relevance": {"rod_bearing": 0.7, "low_oil": 0.6, "timing_chain": 0.6, "belt_issue": 0.5}
    },
    {
        "id": "q_noise_when",
        "text": "When does the noise occur?",
        "options": [
            {"value": "cold_start",  "label": "Only when cold / first started"},
            {"value": "always",      "label": "All the time while running"},
            {"value": "under_load",  "label": "Under acceleration or load"},
            {"value": "idle_only",   "label": "Mainly at idle / sitting still"},
        ],
        "relevant_to": ["engine_noise"],
        "relevance": {"low_oil": 0.5, "timing_chain": 0.6, "rod_bearing": 0.4}
    },
    {
        "id": "q_oil_level",
        "text": "When did you last check the oil level?",
        "options": [
            {"value": "recently_full",  "label": "Recently – oil is full"},
            {"value": "recently_low",   "label": "Recently – oil was low"},
            {"value": "long_ago",       "label": "Haven't checked in a while"},
            {"value": "oil_light",      "label": "Oil warning light is on"},
        ],
        "relevant_to": ["engine_noise", "overheating", "stalling"],
        "relevance": {"low_oil": 0.9, "rod_bearing": 0.5, "engine_damage": 0.4}
    },
    # OVERHEATING
    {
        "id": "q_overheat_symptoms",
        "text": "What are you seeing / experiencing?",
        "options": [
            {"value": "temp_gauge",     "label": "Temperature gauge in the red"},
            {"value": "steam_hood",     "label": "Steam coming from under the hood"},
            {"value": "warning_light",  "label": "Coolant / temperature warning light"},
            {"value": "sweet_smell",    "label": "Sweet smell (like syrup) from engine"},
        ],
        "relevant_to": ["overheating"],
        "relevance": {"coolant_leak": 0.7, "thermostat_fault": 0.6, "radiator_issue": 0.5, "head_gasket": 0.4}
    },
    {
        "id": "q_coolant_level",
        "text": "Have you checked the coolant level?",
        "options": [
            {"value": "full",       "label": "Yes – coolant is full"},
            {"value": "low",        "label": "Yes – coolant is low or empty"},
            {"value": "not_checked","label": "Haven't checked"},
        ],
        "relevant_to": ["overheating"],
        "relevance": {"coolant_leak": 0.8, "head_gasket": 0.4, "thermostat_fault": 0.3}
    },
    {
        "id": "q_radiator_fan",
        "text": "Does the radiator fan run when the engine gets hot?",
        "options": [
            {"value": "yes",        "label": "Yes – fan runs when hot"},
            {"value": "no",         "label": "No – fan doesn't seem to run"},
            {"value": "not_sure",   "label": "Not sure"},
        ],
        "relevant_to": ["overheating"],
        "relevance": {"radiator_fan_fault": 0.9, "radiator_issue": 0.3}
    },
    # STALLING
    {
        "id": "q_stall_when",
        "text": "When does the engine stall?",
        "options": [
            {"value": "idle",       "label": "At idle / sitting in traffic"},
            {"value": "decelerate", "label": "When slowing down or braking"},
            {"value": "highway",    "label": "At highway speed"},
            {"value": "random",     "label": "Randomly with no pattern"},
        ],
        "relevant_to": ["stalling"],
        "relevance": {"fuel_delivery": 0.5, "idle_air_valve": 0.7, "spark_plugs": 0.5, "maf_sensor": 0.5}
    },
    {
        "id": "q_check_engine",
        "text": "Is the Check Engine light on?",
        "options": [
            {"value": "yes_solid",   "label": "Yes – solid light"},
            {"value": "yes_flashing","label": "Yes – flashing/blinking light"},
            {"value": "no",          "label": "No"},
        ],
        "relevant_to": ["stalling", "engine_noise", "exhaust"],
        "relevance": {"spark_plugs": 0.6, "maf_sensor": 0.5, "catalytic_converter": 0.4, "fuel_delivery": 0.4}
    },
    # BRAKES
    {
        "id": "q_brake_symptom",
        "text": "What exactly is happening with the brakes?",
        "options": [
            {"value": "squealing",  "label": "High-pitched squealing when braking"},
            {"value": "grinding",   "label": "Metal grinding noise when braking"},
            {"value": "spongy",     "label": "Brake pedal feels soft / spongy"},
            {"value": "vibration",  "label": "Vibration / pulsing when braking"},
            {"value": "pulling",    "label": "Car pulls to one side when braking"},
        ],
        "relevant_to": ["brakes"],
        "relevance": {"worn_brake_pads": 0.8, "warped_rotors": 0.7, "brake_fluid": 0.6, "brake_caliper": 0.5}
    },
    {
        "id": "q_brake_pad_age",
        "text": "When were the brake pads last replaced?",
        "options": [
            {"value": "recent",     "label": "Within the last year"},
            {"value": "2_3_years",  "label": "2–3 years ago"},
            {"value": "over_3",     "label": "More than 3 years ago"},
            {"value": "unknown",    "label": "Not sure"},
        ],
        "relevant_to": ["brakes"],
        "relevance": {"worn_brake_pads": 0.7, "warped_rotors": 0.4}
    },
    # TRANSMISSION
    {
        "id": "q_trans_type",
        "text": "Is your car automatic or manual (stick shift)?",
        "options": [
            {"value": "automatic",  "label": "Automatic"},
            {"value": "manual",     "label": "Manual / stick shift"},
        ],
        "relevant_to": ["transmission"],
        "relevance": {}
    },
    {
        "id": "q_trans_symptom",
        "text": "What's happening with the transmission or gears?",
        "options": [
            {"value": "slipping",   "label": "Gears slipping or revs rise without acceleration"},
            {"value": "rough_shift","label": "Rough, jerky, or delayed gear changes"},
            {"value": "wont_engage","label": "Won't go into gear / gear stuck"},
            {"value": "noise_gear", "label": "Clunking or whining noise when shifting"},
        ],
        "relevant_to": ["transmission"],
        "relevance": {"trans_fluid": 0.7, "trans_damage": 0.5, "clutch_wear": 0.6}
    },
    # ELECTRICAL
    {
        "id": "q_elec_symptom",
        "text": "What electrical issue are you experiencing?",
        "options": [
            {"value": "dead_battery",   "label": "Battery keeps dying / car won't start"},
            {"value": "lights_dim",     "label": "Lights dimming while driving"},
            {"value": "no_accessories", "label": "Radio / windows / accessories not working"},
            {"value": "warning_lights", "label": "Multiple dashboard warning lights on"},
        ],
        "relevant_to": ["electrical"],
        "relevance": {"dead_battery": 0.8, "bad_alternator": 0.7, "blown_fuse": 0.6, "bad_ecm": 0.3}
    },
    {
        "id": "q_battery_age",
        "text": "How old is the car battery?",
        "options": [
            {"value": "under2",  "label": "Less than 2 years"},
            {"value": "2_4",     "label": "2–4 years"},
            {"value": "over4",   "label": "More than 4 years"},
            {"value": "unknown", "label": "Not sure"},
        ],
        "relevant_to": ["electrical", "wont_start"],
        "relevance": {"dead_battery": 0.7}
    },
    # STEERING
    {
        "id": "q_steering_symptom",
        "text": "What steering or suspension issue are you noticing?",
        "options": [
            {"value": "vibration",  "label": "Steering wheel vibrates at speed"},
            {"value": "pulling",    "label": "Car drifts / pulls to one side"},
            {"value": "stiff",      "label": "Steering feels heavy or stiff"},
            {"value": "clunking",   "label": "Clunking noise over bumps"},
            {"value": "loose",      "label": "Steering feels loose or wandering"},
        ],
        "relevant_to": ["steering"],
        "relevance": {"wheel_balance": 0.8, "alignment": 0.7, "power_steering": 0.6, "worn_suspension": 0.6}
    },
    # EXHAUST
    {
        "id": "q_smoke_color",
        "text": "What color is the smoke or what smell are you noticing?",
        "options": [
            {"value": "white",  "label": "White / grey smoke from exhaust"},
            {"value": "blue",   "label": "Blue or bluish smoke"},
            {"value": "black",  "label": "Black, sooty smoke"},
            {"value": "smell",  "label": "Rotten egg / sulphur smell"},
            {"value": "burning","label": "Burning smell (rubber or plastic)"},
        ],
        "relevant_to": ["exhaust"],
        "relevance": {"head_gasket": 0.7, "oil_burning": 0.8, "rich_mixture": 0.7, "catalytic_converter": 0.6}
    },
    # LEAKS
    {
        "id": "q_leak_color",
        "text": "What color / type is the fluid leaking?",
        "options": [
            {"value": "clear_water",    "label": "Clear water (likely just A/C condensation)"},
            {"value": "green_orange",   "label": "Green, orange, or pink (coolant)"},
            {"value": "brown_black",    "label": "Dark brown or black (engine oil)"},
            {"value": "red_pink",       "label": "Red or pinkish (transmission / power steering fluid)"},
            {"value": "clear_oily",     "label": "Clear and oily / slippery (brake fluid)"},
        ],
        "relevant_to": ["leaks"],
        "relevance": {"coolant_leak": 0.9, "oil_leak": 0.9, "trans_fluid": 0.7, "brake_fluid": 0.8}
    },
    {
        "id": "q_leak_location",
        "text": "Where under the car is the leak coming from?",
        "options": [
            {"value": "front",  "label": "Front of the car (under the engine)"},
            {"value": "middle", "label": "Middle underside"},
            {"value": "rear",   "label": "Rear / near exhaust or trunk"},
            {"value": "wheels", "label": "Near a wheel"},
        ],
        "relevant_to": ["leaks"],
        "relevance": {"coolant_leak": 0.4, "oil_leak": 0.5, "brake_fluid": 0.5, "trans_fluid": 0.4}
    },
]

DIAGNOSES = {
    "dead_battery": {
        "label": "Dead or Failing Battery",
        "description": "The battery has lost charge or capacity and can no longer start the car.",
        "fixes": ["Jump-start and drive for 30+ min to recharge", "Test battery voltage with a multimeter (should be 12.4V+)", "Replace battery if over 4 years old or below 12V", "Check for parasitic drain if it keeps dying"],
        "severity": "medium"
    },
    "bad_starter": {
        "label": "Faulty Starter Motor",
        "description": "The starter motor that cranks the engine is failing or has failed.",
        "fixes": ["Listen for a single heavy click — classic starter sign", "Tap the starter with a wrench as a temporary fix", "Have the starter tested at an auto parts store (free)", "Replace starter motor (shop or DIY if mechanically able)"],
        "severity": "medium"
    },
    "bad_alternator": {
        "label": "Failing Alternator",
        "description": "The alternator isn't charging the battery while driving, causing slow drain.",
        "fixes": ["Have alternator output tested (auto parts stores do this free)", "Look for dimming lights and battery warning light", "Replace alternator — typically a 1–2 hour repair", "Check drive belt condition while you're in there"],
        "severity": "high"
    },
    "fuel_delivery": {
        "label": "Fuel Delivery Problem",
        "description": "The engine isn't receiving enough fuel — could be pump, filter, or injectors.",
        "fixes": ["Listen for the fuel pump hum when you turn the key (should hear it)", "Replace fuel filter if not done in 30,000+ miles", "Have fuel pressure tested at a shop", "Fuel pump replacement if pressure is low"],
        "severity": "high"
    },
    "low_oil": {
        "label": "Low Oil / No Oil Pressure",
        "description": "Critically low oil is causing metal-on-metal contact — STOP DRIVING IMMEDIATELY.",
        "fixes": ["STOP ENGINE NOW if oil light is on — serious damage risk", "Check dipstick and add correct oil grade immediately", "Investigate source of oil loss (leak or burning)", "Full oil change and inspection recommended"],
        "severity": "critical"
    },
    "rod_bearing": {
        "label": "Rod Bearing Failure (Engine Knock)",
        "description": "Deep knocking indicates rod bearing wear — this is a serious engine issue.",
        "fixes": ["Stop driving — continued use risks catastrophic engine failure", "Have a mechanic diagnose immediately", "Oil pressure check and oil analysis recommended", "Repair cost can be high — get a full assessment before proceeding"],
        "severity": "critical"
    },
    "timing_chain": {
        "label": "Timing Chain / Belt Issue",
        "description": "Rattling on startup suggests timing chain stretch or tensioner failure.",
        "fixes": ["Do NOT ignore — timing failure can destroy the engine instantly", "Schedule immediate inspection with a mechanic", "Timing chain/belt and tensioner replacement", "Change oil regularly to prevent future recurrence"],
        "severity": "high"
    },
    "belt_issue": {
        "label": "Serpentine or Accessory Belt Worn",
        "description": "A squealing or slipping belt is causing noise and may leave you stranded.",
        "fixes": ["Inspect belt for cracks, fraying, or glazing", "Replace serpentine belt (affordable, ~$30–80 part)", "Check belt tensioner as well — often replaced together", "Most belts should be replaced every 60,000–100,000 miles"],
        "severity": "medium"
    },
    "coolant_leak": {
        "label": "Coolant Leak",
        "description": "Coolant is escaping, causing overheating risk. Find and fix the leak urgently.",
        "fixes": ["Top up coolant immediately as a short-term fix only", "Pressure test cooling system to find leak source", "Common culprits: hose, radiator, water pump, expansion tank", "Do NOT drive with empty coolant — engine damage guaranteed"],
        "severity": "high"
    },
    "thermostat_fault": {
        "label": "Faulty Thermostat",
        "description": "A stuck-closed thermostat prevents coolant flow, causing rapid overheating.",
        "fixes": ["Thermostat replacement is a relatively cheap repair ($15–50 part)", "Flush cooling system while it's apart", "Easy DIY job on most engines", "Can also cause car to run too cold if stuck open"],
        "severity": "medium"
    },
    "radiator_issue": {
        "label": "Radiator Blockage or Failure",
        "description": "The radiator is not dissipating heat effectively.",
        "fixes": ["Flush radiator with radiator flush product", "Inspect for external damage, bent fins, or blockage", "Radiator replacement if cracked or severely clogged", "Check coolant condition — rusty coolant blocks radiators"],
        "severity": "medium"
    },
    "radiator_fan_fault": {
        "label": "Radiator Fan Not Working",
        "description": "Without fan cooling at low speeds, the engine will overheat in traffic.",
        "fixes": ["Check fan fuse and relay first (cheap fix)", "Test fan motor directly with 12V source", "Replace fan motor or fan assembly if faulty", "Some cars have dual fans — test both"],
        "severity": "high"
    },
    "head_gasket": {
        "label": "Head Gasket Failure",
        "description": "A blown head gasket is serious — coolant and oil are mixing. Expensive repair.",
        "fixes": ["Stop driving immediately — catastrophic damage risk", "Signs: white exhaust smoke, coolant loss, milky oil", "Block test kit can confirm before committing to repair", "Head gasket replacement is labor-intensive — get multiple quotes"],
        "severity": "critical"
    },
    "spark_plugs": {
        "label": "Worn Spark Plugs or Ignition Issue",
        "description": "Fouled or worn spark plugs cause misfires, stalling, and poor performance.",
        "fixes": ["Replace spark plugs (typically every 30,000–100,000 miles depending on type)", "Inspect ignition coils and wires while you're at it", "Check for OBD fault codes (P030X = cylinder misfire)", "A tune-up often resolves stalling and rough running"],
        "severity": "medium"
    },
    "idle_air_valve": {
        "label": "Idle Air Control Valve (IAC) Dirty / Faulty",
        "description": "A dirty or faulty IAC causes rough or stalling idle — common issue.",
        "fixes": ["Clean IAC valve with throttle body cleaner (often free fix)", "Reset ECU after cleaning (disconnect battery for 10 min)", "Replace IAC valve if cleaning doesn't help", "Also check for vacuum leaks around intake"],
        "severity": "low"
    },
    "maf_sensor": {
        "label": "Mass Airflow (MAF) Sensor Fault",
        "description": "A dirty or failing MAF sensor gives the ECU wrong data, causing stalling.",
        "fixes": ["Clean MAF sensor with MAF sensor cleaner spray (don't use other cleaners)", "Check for OBD codes (P0100–P0103)", "Replace MAF sensor if cleaning doesn't resolve it", "Inspect air filter — a clogged filter damages MAF sensors"],
        "severity": "medium"
    },
    "worn_brake_pads": {
        "label": "Worn Brake Pads",
        "description": "Brake pads are at or near end of life — replacement is urgent for safety.",
        "fixes": ["Have brake pads inspected immediately", "Replace pads AND inspect rotors at the same time", "Most pads last 25,000–65,000 miles depending on driving style", "Squealing is the wear indicator — grinding means it's too late"],
        "severity": "high"
    },
    "warped_rotors": {
        "label": "Warped Brake Rotors",
        "description": "Rotors have heat-warped, causing vibration and pulsing under braking.",
        "fixes": ["Resurface rotors if within minimum thickness spec", "Replace rotors if too thin to resurface", "Check brake caliper slides — sticking calipers cause rotor warping", "Always replace pads and rotors together for best results"],
        "severity": "medium"
    },
    "brake_fluid": {
        "label": "Low or Contaminated Brake Fluid",
        "description": "Spongy pedal often means air in the system or dangerously low brake fluid.",
        "fixes": ["Check brake fluid reservoir level immediately", "If low, inspect for brake fluid leak near wheels or master cylinder", "Bleed brakes if pedal is spongy after topping up", "Flush brake fluid every 2 years — it absorbs moisture"],
        "severity": "high"
    },
    "brake_caliper": {
        "label": "Seized / Sticking Brake Caliper",
        "description": "A seized caliper causes uneven braking, pulling, and excessive heat.",
        "fixes": ["You'll often smell burning from the affected wheel", "Have brakes inspected — sticking caliper can cause brake fire", "Rebuild or replace the affected caliper", "Replace brake pads and rotors on that axle as well"],
        "severity": "high"
    },
    "trans_fluid": {
        "label": "Low or Degraded Transmission Fluid",
        "description": "Transmission fluid needs to be at the right level and condition to shift properly.",
        "fixes": ["Check transmission fluid level and condition (should be red/pink, not brown)", "Top up or do a full fluid change if overdue", "Most automatics need fluid change every 30,000–60,000 miles", "Using wrong fluid type causes severe damage — check spec"],
        "severity": "medium"
    },
    "trans_damage": {
        "label": "Transmission Internal Damage",
        "description": "Internal transmission damage is a serious and potentially expensive repair.",
        "fixes": ["Stop driving hard — gentle driving reduces further damage", "Have transmission scanned for fault codes", "Get a professional assessment before any major investment", "Rebuilt or used transmission may be more cost-effective than repair"],
        "severity": "critical"
    },
    "clutch_wear": {
        "label": "Worn Clutch (Manual Transmission)",
        "description": "The clutch disc is worn and slipping under load.",
        "fixes": ["Avoid 'riding the clutch' to slow wear", "Full clutch replacement (pressure plate, disc, release bearing)", "Check flywheel for scoring at same time", "Clutch typically lasts 50,000–100,000 miles depending on driving style"],
        "severity": "high"
    },
    "blown_fuse": {
        "label": "Blown Fuse",
        "description": "A failed fuse is causing a circuit to stop working.",
        "fixes": ["Check fuse box (inside cabin and under hood) for blown fuses", "Fuse diagrams are in your owner's manual or inside the fuse box lid", "Always replace with the same amperage fuse", "Recurring blown fuses indicate a short circuit — investigate further"],
        "severity": "low"
    },
    "bad_ecm": {
        "label": "ECU / ECM Fault",
        "description": "The engine control module may have a fault causing multiple system issues.",
        "fixes": ["Read fault codes with OBD2 scanner first", "Check for software updates or recalls for your model", "ECU replacement or reprogramming is a specialist job", "Verify power and ground connections to ECU first"],
        "severity": "high"
    },
    "wheel_balance": {
        "label": "Wheel Imbalance",
        "description": "Unbalanced wheels cause steering vibration, typically at highway speeds.",
        "fixes": ["Wheel balancing at any tyre shop (usually very affordable)", "Also inspect tyres for uneven wear or damage", "Rotate tyres while there for even wear", "Vibration that starts above 60mph is usually a balance issue"],
        "severity": "low"
    },
    "alignment": {
        "label": "Wheel Alignment Off",
        "description": "Misaligned wheels cause pulling, uneven tyre wear, and handling issues.",
        "fixes": ["Four-wheel alignment at a tyre/alignment shop", "Check for bent rims or worn suspension components first", "Alignment needed after hitting a pothole or curb", "Check tyre wear pattern — inner or outer wear = alignment issue"],
        "severity": "low"
    },
    "power_steering": {
        "label": "Power Steering Fault",
        "description": "Power steering (hydraulic or electric) is failing, making steering heavy.",
        "fixes": ["For hydraulic: check power steering fluid level", "For electric: check for EPS warning light on dashboard", "Inspect power steering pump for leaks or noise", "Electric power steering faults often need dealer diagnosis"],
        "severity": "medium"
    },
    "worn_suspension": {
        "label": "Worn Suspension / Shock Absorbers",
        "description": "Worn shocks, struts, or bushings causing noise, vibration, and handling issues.",
        "fixes": ["Have suspension inspected — bounce test each corner of car", "Replace shocks/struts in pairs (front or rear)", "Inspect ball joints, tie rod ends, and bushings", "Worn suspension increases tyre wear and braking distance"],
        "severity": "medium"
    },
    "oil_burning": {
        "label": "Engine Burning Oil (Blue Smoke)",
        "description": "Oil is entering the combustion chamber and burning — valve seals or rings.",
        "fixes": ["Monitor oil level closely and top up regularly", "Blue smoke on startup = valve seals; on acceleration = piston rings", "Oil consumption test can quantify severity", "Valve seal replacement is cheaper than full ring job"],
        "severity": "medium"
    },
    "rich_mixture": {
        "label": "Running Rich (Black Smoke)",
        "description": "Too much fuel in the mixture — wasting fuel and producing soot.",
        "fixes": ["Check for OBD fault codes — often O2 sensor or injector related", "Inspect and replace air filter if clogged", "Check for stuck-open injector or faulty fuel pressure regulator", "Poor fuel economy accompanies this issue"],
        "severity": "medium"
    },
    "catalytic_converter": {
        "label": "Catalytic Converter Failing",
        "description": "The catalytic converter is clogged, damaged, or past its service life.",
        "fixes": ["Rotten egg smell is a classic sign", "Will trigger Check Engine light with O2 sensor codes", "Catalytic converter replacement can be expensive — check for recalls", "Address underlying causes first (burning oil, running rich) or new cat will fail too"],
        "severity": "medium"
    },
    "oil_leak": {
        "label": "Engine Oil Leak",
        "description": "Oil is leaking externally — find and fix the source before it causes damage.",
        "fixes": ["Check valve cover gasket, oil pan gasket, and rear main seal", "Use UV dye kit to trace leak source precisely", "Monitor oil level while planning repair", "Small gasket leaks are cheap fixes — don't delay"],
        "severity": "medium"
    },
    "engine_damage": {
        "label": "Serious Engine Damage",
        "description": "Continued operation with low/no oil or overheating may have caused internal engine damage.",
        "fixes": ["Stop driving immediately", "Have a compression test done to assess damage", "Oil pressure test and inspection by a mechanic", "Repair cost depends on extent — get full diagnosis before decisions"],
        "severity": "critical"
    },
}

SCORING_RULES = {
    ("q_main_symptom", "wont_start"): {"dead_battery": 0.4, "bad_starter": 0.3, "bad_alternator": 0.2, "fuel_delivery": 0.2},
    ("q_main_symptom", "engine_noise"): {"low_oil": 0.4, "rod_bearing": 0.3, "timing_chain": 0.3, "belt_issue": 0.2},
    ("q_main_symptom", "overheating"): {"coolant_leak": 0.4, "thermostat_fault": 0.3, "radiator_issue": 0.3, "radiator_fan_fault": 0.2},
    ("q_main_symptom", "stalling"): {"spark_plugs": 0.3, "idle_air_valve": 0.3, "fuel_delivery": 0.3, "maf_sensor": 0.3},
    ("q_main_symptom", "brakes"): {"worn_brake_pads": 0.5, "warped_rotors": 0.3, "brake_fluid": 0.2, "brake_caliper": 0.2},
    ("q_main_symptom", "transmission"): {"trans_fluid": 0.4, "trans_damage": 0.3, "clutch_wear": 0.2},
    ("q_main_symptom", "electrical"): {"dead_battery": 0.4, "bad_alternator": 0.3, "blown_fuse": 0.3, "bad_ecm": 0.1},
    ("q_main_symptom", "steering"): {"wheel_balance": 0.4, "alignment": 0.4, "power_steering": 0.3, "worn_suspension": 0.3},
    ("q_main_symptom", "exhaust"): {"head_gasket": 0.3, "oil_burning": 0.3, "rich_mixture": 0.3, "catalytic_converter": 0.2},
    ("q_main_symptom", "leaks"): {"coolant_leak": 0.3, "oil_leak": 0.3, "trans_fluid": 0.2, "brake_fluid": 0.2},

    ("q_start_lights", "no"): {"dead_battery": 0.8, "bad_alternator": 0.3},
    ("q_start_lights", "dim"): {"dead_battery": 0.6, "bad_alternator": 0.5},
    ("q_start_lights", "click"): {"dead_battery": 0.5, "bad_starter": 0.4},
    ("q_start_sound", "nothing"): {"dead_battery": 0.7, "bad_starter": 0.3},
    ("q_start_sound", "rapid_click"): {"dead_battery": 0.9},
    ("q_start_sound", "single_click"): {"bad_starter": 0.8, "dead_battery": 0.3},
    ("q_start_sound", "cranks_no_fire"): {"fuel_delivery": 0.6, "spark_plugs": 0.4, "dead_battery": -0.3},
    ("q_start_sound", "grinding"): {"bad_starter": 0.7},
    ("q_recent_drove", "sat_parked"): {"dead_battery": 0.7},
    ("q_recent_drove", "warning_signs"): {"bad_alternator": 0.5, "fuel_delivery": 0.3},

    ("q_noise_type", "knocking"): {"rod_bearing": 0.9, "low_oil": 0.5},
    ("q_noise_type", "ticking"): {"low_oil": 0.7, "timing_chain": 0.4},
    ("q_noise_type", "rattling"): {"timing_chain": 0.8},
    ("q_noise_type", "squealing"): {"belt_issue": 0.8},
    ("q_noise_type", "hissing"): {"coolant_leak": 0.6, "head_gasket": 0.4},
    ("q_noise_when", "cold_start"): {"timing_chain": 0.6, "low_oil": 0.4},
    ("q_noise_when", "always"): {"rod_bearing": 0.6, "low_oil": 0.5},
    ("q_oil_level", "oil_light"): {"low_oil": 0.95, "engine_damage": 0.5},
    ("q_oil_level", "recently_low"): {"low_oil": 0.7, "oil_leak": 0.4},
    ("q_oil_level", "long_ago"): {"low_oil": 0.5},

    ("q_overheat_symptoms", "steam_hood"): {"coolant_leak": 0.8, "head_gasket": 0.4},
    ("q_overheat_symptoms", "sweet_smell"): {"coolant_leak": 0.7, "head_gasket": 0.6},
    ("q_coolant_level", "low"): {"coolant_leak": 0.8, "head_gasket": 0.3},
    ("q_coolant_level", "full"): {"thermostat_fault": 0.5, "radiator_fan_fault": 0.4, "coolant_leak": -0.3},
    ("q_radiator_fan", "no"): {"radiator_fan_fault": 0.95},

    ("q_stall_when", "idle"): {"idle_air_valve": 0.8, "maf_sensor": 0.4},
    ("q_stall_when", "decelerate"): {"idle_air_valve": 0.6, "spark_plugs": 0.4},
    ("q_stall_when", "highway"): {"fuel_delivery": 0.7, "maf_sensor": 0.5},
    ("q_check_engine", "yes_flashing"): {"spark_plugs": 0.8, "catalytic_converter": 0.5},
    ("q_check_engine", "yes_solid"): {"maf_sensor": 0.5, "spark_plugs": 0.4, "catalytic_converter": 0.3},

    ("q_brake_symptom", "squealing"): {"worn_brake_pads": 0.8},
    ("q_brake_symptom", "grinding"): {"worn_brake_pads": 0.95},
    ("q_brake_symptom", "spongy"): {"brake_fluid": 0.8, "brake_caliper": 0.3},
    ("q_brake_symptom", "vibration"): {"warped_rotors": 0.85},
    ("q_brake_symptom", "pulling"): {"brake_caliper": 0.7, "alignment": 0.4},
    ("q_brake_pad_age", "over_3"): {"worn_brake_pads": 0.6, "warped_rotors": 0.3},

    ("q_trans_symptom", "slipping"): {"trans_fluid": 0.5, "clutch_wear": 0.6, "trans_damage": 0.4},
    ("q_trans_symptom", "rough_shift"): {"trans_fluid": 0.7, "trans_damage": 0.3},
    ("q_trans_symptom", "wont_engage"): {"trans_damage": 0.6, "clutch_wear": 0.5},
    ("q_trans_type", "manual"): {"clutch_wear": 0.3, "trans_damage": -0.1},

    ("q_elec_symptom", "dead_battery"): {"dead_battery": 0.8, "bad_alternator": 0.5},
    ("q_elec_symptom", "lights_dim"): {"bad_alternator": 0.8},
    ("q_elec_symptom", "no_accessories"): {"blown_fuse": 0.8},
    ("q_elec_symptom", "warning_lights"): {"bad_ecm": 0.5, "bad_alternator": 0.3},
    ("q_battery_age", "over4"): {"dead_battery": 0.7},
    ("q_battery_age", "2_4"): {"dead_battery": 0.3},

    ("q_steering_symptom", "vibration"): {"wheel_balance": 0.85},
    ("q_steering_symptom", "pulling"): {"alignment": 0.75, "brake_caliper": 0.3},
    ("q_steering_symptom", "stiff"): {"power_steering": 0.85},
    ("q_steering_symptom", "clunking"): {"worn_suspension": 0.85},
    ("q_steering_symptom", "loose"): {"alignment": 0.5, "worn_suspension": 0.6},

    ("q_smoke_color", "white"): {"head_gasket": 0.75, "coolant_leak": 0.4},
    ("q_smoke_color", "blue"): {"oil_burning": 0.9},
    ("q_smoke_color", "black"): {"rich_mixture": 0.85},
    ("q_smoke_color", "smell"): {"catalytic_converter": 0.75},
    ("q_smoke_color", "burning"): {"brake_caliper": 0.4, "worn_brake_pads": 0.3},

    ("q_leak_color", "green_orange"): {"coolant_leak": 0.95},
    ("q_leak_color", "brown_black"): {"oil_leak": 0.95},
    ("q_leak_color", "red_pink"): {"trans_fluid": 0.8, "power_steering": 0.5},
    ("q_leak_color", "clear_oily"): {"brake_fluid": 0.85},
    ("q_leak_color", "clear_water"): {"coolant_leak": -0.5},
}

SYMPTOM_QUESTION_MAP = {
    "wont_start":    ["q_start_lights", "q_start_sound", "q_recent_drove", "q_battery_age"],
    "engine_noise":  ["q_noise_type", "q_noise_when", "q_oil_level"],
    "overheating":   ["q_overheat_symptoms", "q_coolant_level", "q_radiator_fan", "q_oil_level"],
    "stalling":      ["q_stall_when", "q_check_engine", "q_oil_level"],
    "brakes":        ["q_brake_symptom", "q_brake_pad_age"],
    "transmission":  ["q_trans_type", "q_trans_symptom"],
    "electrical":    ["q_elec_symptom", "q_battery_age"],
    "steering":      ["q_steering_symptom"],
    "exhaust":       ["q_smoke_color", "q_check_engine"],
    "leaks":         ["q_leak_color", "q_leak_location"],
}

def get_question_by_id(qid):
    return next((q for q in QUESTIONS if q["id"] == qid), None)

def compute_scores(answers):
    scores = {diag: 0.0 for diag in DIAGNOSES}
    for (qid, val), boosts in SCORING_RULES.items():
        if answers.get(qid) == val:
            for diag, boost in boosts.items():
                if diag in scores:
                    scores[diag] = min(1.0, max(0.0, scores[diag] + boost))
    return scores

def get_next_question_id(answers, asked_ids):
    main = answers.get("q_main_symptom")
    if not main:
        return "q_main_symptom"
    queue = SYMPTOM_QUESTION_MAP.get(main, [])
    for qid in queue:
        if qid not in asked_ids:
            return qid
    return None

def get_all_ranked_diagnoses(scores):
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)

def format_results(top_diags):
    results = []
    for diag_id, score in top_diags:
        d = DIAGNOSES[diag_id]
        results.append({
            "id": diag_id,
            "label": d["label"],
            "description": d["description"],
            "fixes": d["fixes"],
            "severity": d["severity"],
            "confidence": round(score * 100)
        })
    return results

@app.route("/")
def index():
    session.clear()
    return render_template("index.html")

@app.route("/api/start", methods=["POST"])
def start():
    session["answers"] = {}
    session["asked"] = []
    first_q = get_question_by_id("q_main_symptom")
    return jsonify({"question": first_q})

@app.route("/api/answer", methods=["POST"])
def answer():
    data = request.json
    qid = data["question_id"]
    val = data["answer"]
    answers = session.get("answers", {})
    asked = session.get("asked", [])
    answers[qid] = val
    if qid not in asked:
        asked.append(qid)
    session["answers"] = answers
    session["asked"] = asked
    scores = compute_scores(answers)
    ranked_diags = get_all_ranked_diagnoses(scores)
    next_qid = get_next_question_id(answers, asked)
    is_decisive = False
    if len(ranked_diags) > 1:
        top_score = ranked_diags[0][1]
        runner_up_score = ranked_diags[1][1]
        if top_score >= 0.85 and (top_score - runner_up_score >= 0.30):
            is_decisive = True
    elif len(ranked_diags) == 1 and ranked_diags[0][1] > 0:
        is_decisive = True
    if is_decisive or next_qid is None:
        decisive_result = ranked_diags[:1]
        return jsonify({"done": True, "diagnoses": format_results(decisive_result)})
    next_q = get_question_by_id(next_qid)
    asked_count = len(asked)
    total_expected = 1 + len(SYMPTOM_QUESTION_MAP.get(answers.get("q_main_symptom", ""), []))
    return jsonify({
        "done": False,
        "question": next_q,
        "progress": {"asked": asked_count, "total": total_expected}
    })

if __name__ == "__main__":
    app.run(debug=True)