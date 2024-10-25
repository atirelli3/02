#!/bin/bash

# Supported arg(s)
#
# - create: install a new system (arch only for the moment)
#   + nouefi: disable the uefi check (this mean no secure boot also)
# - build: build a base user environtment

action=$1    # Action
subaction=$2 # Subaction (if supported by the main action)

# =========================    UTILITY FUNCTION(s)    ==========================
print_debug() { echo -e "\e[${1}m${2}\e[0m"; }  # Native print/debug output w/ color
print_success() { print_debug "32" "$1"; }      # Green
print_info() { print_debug "36" "$1"; }         # Cyan
print_warning() { print_debug "33" "$1"; }      # Yellow
print_error() { print_debug "31" "$1"; }        # Red


# =============================    MAIN SCRIPT    ==============================

# => Create action ($1: 'create')
if [[ "$1" = "create" ]]; then
  # Check prerequisites => system is in UEFI mode
  if [[ "$subaction" != "nouefi" && ! -d /sys/firmware/efi/efivars ]]; then
    print_error "FAILED => UEFI mode not detected! Please pass 'nouefi' to bypass."
    exit 1
  fi

  if [[ "$subaction" = "nouefi" ]]; then
  fi

  # Launch the ansible playbook for the arch installation
fi
