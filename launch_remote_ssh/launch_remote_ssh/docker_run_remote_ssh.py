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

from typing import Optional
from typing import Iterable
from typing import Text
from typing import List

from uuid import uuid4

from launch.some_substitutions_type import SomeSubstitutionsType
from launch import LaunchDescription
from launch.frontend import expose_action
from launch.frontend import Entity
from launch.frontend import Parser
from launch.action import Action
from launch.condition import Condition
from launch.actions import ExecuteProcess
from launch.utilities import normalize_to_list_of_substitutions
from launch_ros.actions import Node

from .replace_text_substitution import ReplaceTextSubstitution

# https://answers.ros.org/question/364152/remotely-launch-nodes-in-ros2/

@expose_action('docker_run_remote_ssh')
class DockerRunRemoteSSH(LaunchDescription):
    def __init__(
        self, *,
        user: SomeSubstitutionsType,
        machine: SomeSubstitutionsType,
        port: Optional[SomeSubstitutionsType] = None,
        image: SomeSubstitutionsType,
        options: Optional[SomeSubstitutionsType] = None,
        container_command: Optional[SomeSubstitutionsType] = None,
        condition: Optional[Condition] = None
    ):
        # Store arguments
        self.__user = normalize_to_list_of_substitutions(user)
        self.__machine = normalize_to_list_of_substitutions(machine)
        self.__port = None if port is None else normalize_to_list_of_substitutions(port)
        self.__image = normalize_to_list_of_substitutions(image)
        self.__container_command = None if container_command is None else normalize_to_list_of_substitutions(container_command)
        self.__condition = condition
        self.__uuid = uuid4()

        # Use a custom port if specified
        port_list = []
        if self.__port is not None:
            port_list.append(' -p ')
            port_list += self.__port

        # Compile process name into list with shortened UUID at the end
        # TODO(anyone) - this has a max of 80 characters. Can this be enforced still using
        # substitutions?
        process_name_list = []
        process_name_list += self.__machine
        process_name_list += [
            '_',
            self.uuid_short
        ]

        # Replace any dots with underscores
        process_name_list = [
            ReplaceTextSubstitution(
                normalize_to_list_of_substitutions(process_name_list),
                '.',
                '_',
            )
        ]

        # Compile command into list
        command_list = []

        command_list += ['docker run']
        command_list += [' --name ']
        command_list += ['cntr_']
        command_list += process_name_list
        
        if options is not None:
            command_list += [' ']
            command_list += options

        command_list += [' ']
        command_list += self.__image
        command_list += [' ']
        command_list += self.__container_command

        # Build full command
        self.__full_command = [
            '{ outer_stdout=$(readlink -f /proc/self/fd/3); } 3>&1 && screen -DmS ',
        ]
        self.__full_command += process_name_list
        self.__full_command += [
            ' bash -i -c "ssh ',
        ]
        self.__full_command += port_list
        self.__full_command += [
            ' -t ',
        ]
        self.__full_command += self.__user
        self.__full_command += [
            '@',
        ]
        self.__full_command += self.__machine
        self.__full_command += [
            ' \'bash -i -c \\"'
        ]
        self.__full_command += command_list
        self.__full_command += [
            '\\"\' > $outer_stdout"',
        ]

        docker_kill_command = ['ssh ']
        docker_kill_command += port_list
        docker_kill_command += [' -t ']
        docker_kill_command += self.__user
        docker_kill_command += ['@']
        docker_kill_command += self.__machine
        docker_kill_command += [' "bash -c \'']
        docker_kill_command += ['docker kill ']
        docker_kill_command += ['cntr_']
        docker_kill_command += process_name_list
        docker_kill_command += ['\'"']

        super().__init__(
            initial_entities = [
                ExecuteProcess(
                    name=process_name_list,
                    cmd=[self.__full_command],
                    output="screen",
                    shell=True,
                    emulate_tty=True,
                    condition=self.__condition,
                ),
                Node(
                    package='launch_remote_ssh',
                    executable='remote_docker_process_handler',
                    name='remote_docker_process_handler_' + self.uuid_short,
                    namespace=['machine_',ReplaceTextSubstitution(ReplaceTextSubstitution(self.__machine, '.', '_'),'-','_')],
                    output='screen',
                    parameters=[{'screen_process_name': process_name_list,
                                 'docker_kill_command': docker_kill_command}],
                    condition=self.__condition,
                ),
            ]
        )

    @property
    def uuid_full(self) -> Text:
        """Getter for full uuid."""
        return f'{self.__uuid.int:x}'

    @property
    def uuid_short(self) -> Text:
        """Getter for short uuid."""
        return f'{self.uuid_full:.12}'

    @classmethod
    def parse(
        self,
        entity: Entity,
        parser: Parser,
        ignore: Optional[List[str]] = None
    ):
        # Adapted from parse method here:
        # https://github.com/ros2/launch/blob/rolling/launch/launch/actions/execute_process.py

        # Even though this is not derived from the Action class,
        # we're treating it like an action, so use the Action class
        # parsing method to get the condition kwarg
        _, kwargs = Action().parse(entity, parser)

        if ignore is None:
            ignore = []

        if 'user' not in ignore:
            kwargs['user'] = parser.parse_substitution(entity.get_attr('user'))

        if 'machine' not in ignore:
            kwargs['machine'] = parser.parse_substitution(entity.get_attr('machine'))

        if 'cmd' not in ignore:
            kwargs['cmd'] = self._parse_cmdline(entity.get_attr('cmd'), parser)

        if 'port' not in ignore:
            port = entity.get_attr('port', optional=True)
            if port is not None:
                kwargs['port'] = parser.parse_substitution(port)
        
        return self, kwargs
    
    @classmethod
    def _parse_cmdline(
        self,
        cmd: Text,
        parser: Parser
    ) -> List[SomeSubstitutionsType]:
        # TODO(anyone) this is not yet well tested

        result = []
        for sub in parser.parse_substitution(cmd):
            result.append(sub)

        return result