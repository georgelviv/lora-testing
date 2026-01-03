from lora_hardware_model import modules_reset, modules_ping, modules_command

ports = [
  "/dev/cu.usbserial-59680236201",
  # "/dev/cu.usbserial-575E0981281"
]

for port in ports:
  modules_ping(port_filter=port)
print("Done")