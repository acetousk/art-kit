#!/bin/bash
# Device check for the art kit. Run on Fedora Live (or after install). Changes nothing.
ok() { echo "✅ $1"; }; bad() { echo "❌ $1"; }; info() { echo "ℹ️  $1"; }
[ "$(uname -m)" = x86_64 ] && ok "CPU: $(grep -m1 'model name' /proc/cpuinfo | cut -d: -f2 | xargs), $(nproc) threads" || bad "CPU is not x86_64"
[ "$(nproc)" -ge 4 ] || bad "Fewer than 4 CPU threads"
ram=$(awk '/MemTotal/{printf "%.1f", $2/1048576}' /proc/meminfo)
awk "BEGIN{exit !($ram >= 3.5)}" && ok "RAM: $ram GB" || bad "RAM: $ram GB (need 4 GB)"
for d in /sys/block/nvme* /sys/block/sd*; do [ -e "$d" ] || continue; n=$(basename "$d")
  [ "$(cat "$d/removable")" = 1 ] && continue
  gb=$(( $(cat "$d/size") * 512 / 1000000000 )); rot=$(cat "$d/queue/rotational")
  [ "$rot" = 0 ] && [ "$gb" -ge 60 ] && ok "Disk $n: ${gb} GB SSD" || bad "Disk $n: ${gb} GB, rotational=$rot"
done
command -v smartctl >/dev/null && for d in /dev/nvme0 /dev/sda; do [ -e $d ] && sudo smartctl -H $d 2>/dev/null | grep -i "result\|status"; done
for b in /sys/class/power_supply/BAT*; do [ -e "$b" ] || continue
  f=$(cat "$b"/energy_full 2>/dev/null || cat "$b"/charge_full); d=$(cat "$b"/energy_full_design 2>/dev/null || cat "$b"/charge_full_design)
  h=$(( f * 100 / d )); [ "$h" -ge 70 ] && ok "Battery health: $h %" || bad "Battery health: $h % (want 70 %+)"
done
gpu=$(lspci 2>/dev/null | grep -i 'vga\|3d\|display' | cut -d: -f3 | xargs); info "Graphics: $gpu"
echo "$gpu" | grep -qi nvidia && ! echo "$gpu" | grep -qi 'intel\|amd' && bad "NVIDIA only (avoid)"
pen=$(grep -i -B1 -A8 'Name=.*\(pen\|stylus\|wacom\|ipts\)' /proc/bus/input/devices | grep -c 'ABS=.*')
[ "$pen" -gt 0 ] && ok "Pen device found: $(grep -io 'Name=.*\(pen\|stylus\|wacom\|ipts\).*' /proc/bus/input/devices | head -1)" || bad "No pen device (on a Surface this is normal on Fedora Live; see docs/1)"
grep -qi 'touchscreen\|touch' /proc/bus/input/devices && ok "Touch device found" || bad "No touchscreen found"
ls /sys/class/net | grep -q '^wl' && ok "Wi-Fi card: $(ls /sys/class/net | grep '^wl' | head -1)" || bad "No Wi-Fi card"
command -v mokutil >/dev/null && info "Secure Boot: $(mokutil --sb-state 2>/dev/null)"
info "Now open tools/pen-test.html in Firefox and test the pen."
