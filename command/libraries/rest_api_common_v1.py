#!/usr/bin/python
#-*-python-*-##################################################################
# Copyright 2020 - 2023 Inesonic, LLC
# 
# This file is licensed under two licenses.
#
# Inesonic Commercial License, Version 1:
#   All rights reserved.  Inesonic, LLC retains all rights to this software,
#   including the right to relicense the software in source or binary formats
#   under different terms.  Unauthorized use under the terms of this license is
#   strictly prohibited.
#
# GNU Public License, Version 3:
#   This program is free software: you can redistribute it and/or modify it
#   under the terms of the GNU General Public License as published by the Free
#   Software Foundation, either version 3 of the License, or (at your option)
#   any later version.
#   
#   This program is distributed in the hope that it will be useful, but WITHOUT
#   ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#   FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#   more details.
#   
#   You should have received a copy of the GNU General Public License along
#   with this program.  If not, see <https://www.gnu.org/licenses/>.
###############################################################################

"""
Python module that holds common resources used by the V1 version of the REST
API.

"""

###############################################################################
# Import:
#

import hashlib

###############################################################################
# Globals:
#

HASH_ALGORITHM = hashlib.sha256
"""
The hashing algorithm to be used to generate the key.

"""

HASH_BLOCK_SIZE = 64
"""
The block length to use for the HMAC.

"""

SECRET_LENGTH = HASH_BLOCK_SIZE - 8
"""
The required secret length.  Value is selected to provide good security while
also minimizing computation time for the selected hash algorithm.

"""

###############################################################################
# Main:
#

if __name__ == "__main__":
    import sys
    sys.stderr.write(
        "*** This module is not intended to be run as a script..\n"
    )
    exit(1)
