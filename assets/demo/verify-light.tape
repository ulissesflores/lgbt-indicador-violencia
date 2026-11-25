# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Carlos Ulisses Flores (Codex Hash Ltda.)
#
# Record the README demo GIF (light theme): seal verification, then the full quick check.
#
# This VHS tape types two commands in a clean shell, with no network: first the verification of
# the SHA-256 seal of every distributed file, then the fast replication run with the tests that
# lock every published number. The tape pins the recording machine to Python 3.14.
#
# Inputs
# ------
# - the repository at its final seal (make_provenance.py and run_all.py are executed by the
#   tape)
#
# Outputs
# -------
# - assets/demo/verify-light.gif
#
# Usage
# -----
# vhs assets/demo/verify-light.tape
#
# Status
# ------
# No registration status is claimed for this file.
#
# Author
# ------
# Carlos Ulisses Flores (Codex Hash Research Laboratory),
# ORCID https://orcid.org/0000-0002-6034-7765.
# Repository: https://github.com/ulissesflores/lgbt-indicador-violencia

# README demo: the seal verifies, then the tests that lock every published number run. No network.
# Recorded with charmbracelet/vhs from the repository root, after the final seal:
#   vhs assets/demo/verify-light.tape
Output assets/demo/verify-light.gif
Set Shell "bash"
Set FontSize 16
Set Width 1200
Set Height 420
Set Padding 24
Set Theme "Builtin Light"
Set TypingSpeed 35ms
Env PS1 "$ "
Env PYTHONDONTWRITEBYTECODE "1"
Hide
# the recording machine pins its replication environment to Python 3.14
Type "alias python3=python3.14 && clear" Enter
Show
Type "# 1. The seal: SHA-256 of every distributed file and one chain hash (stdlib only)" Enter
Sleep 400ms
Type "python3 -I make_provenance.py --verify" Enter
Sleep 3s
Type "# 2. Integrity, the tests that lock every published number, and the seal again" Enter
Sleep 400ms
Type "python3 -I -u run_all.py --rapido 2>&1 | tail -n 8" Enter
# wait for the run to end (tail prints only when it finishes; run time varies by machine),
# then hold the final screen
Wait+Screen@120s /passaram/
Sleep 5s
