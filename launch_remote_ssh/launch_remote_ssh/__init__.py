# BSD 3-Clause License
#
# Copyright (c) 2023, Northwestern University MSR
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Author: Nick Morales

from .replace_text_substitution import ReplaceTextSubstitution
from .execute_process_remote_ssh import ExecuteProcessRemoteSSH
from .docker_run_remote_ssh import DockerRunRemoteSSH
from .node_remote_ssh import NodeRemoteSSH
from .launch_remote_ssh import LaunchRemoteSSH
from .flexible_frontend_launch_defaults import FlexibleFrontendLaunchDefaults
from .find_package_remote import FindPackagePrefixRemote, FindPackageShareRemote
from .install_remote_ssh import copy_install_space, copy_single_package_install

__all__ = [
    'ReplaceTextSubstitution',
    'ExecuteProcessRemoteSSH',
    'DockerRunRemoteSSH',
    'NodeRemoteSSH',
    'LaunchRemoteSSH',
    'FlexibleFrontendLaunchDefaults',
    'FindPackagePrefixRemote',
    'FindPackageShareRemote',
    'copy_install_space',
    'copy_single_package_install',
]
