from lora_hardware_model import modules_command

ports = [
  "/dev/cu.usbserial-59680236201",
  # "/dev/cu.usbserial-575E0981281"
]

for port in ports:
  modules_command("CONFIG_SYNC;ID=12,PL=200", port_filter=port)
print("Done")