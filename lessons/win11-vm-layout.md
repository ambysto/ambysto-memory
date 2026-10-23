---
title: Know the win11-dev VM layout: QEMU process, disks, forwards, console
kind: reference
applies_when: when a task needs to start, reach or inspect the Windows 11 test VM
projects: all
evidence: 2026-10-16 VM provisioning; global CLAUDE.md machine section
last_validated: 2026-10-22
status: active
---

A plain `qemu-system-x86_64` process (not libvirt, so `virsh` does not list it), started by `~/vms/start_win11.sh`: KVM, 8 cores, 32 GB, UEFI Secure Boot with swtpm.
Disks: `~/vms/disks/win11.qcow2` (system), `data.qcow2` (E:), `usb.qcow2` (F:, removable); snapshots in `~/vms/snapshots`. Monitor socket `~/vms/qemu-monitor.sock`; UEFI vars are raw, so snapshots are taken offline (`vm-snapshot.sh`), never with a live `savevm`.
User-mode NAT: host 2222 to guest SSH, host 33890 to guest RDP; console on VNC :5900. Check it is up with `ss -ltnp | grep 33890`.
SSH (OpenSSH for Windows, key auth): `ssh win11` (Ramune, admin, PowerShell 5.1) and `ssh win11-test` (ambytest).
Scripts and the full fact tables: `~/vms/bin` and `~/vms/README.md`.
