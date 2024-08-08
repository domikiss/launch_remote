// BSD 3-Clause License
//
// Copyright (c) 2023, Northwestern University MSR
// All rights reserved.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are met:
//
// * Redistributions of source code must retain the above copyright notice, this
//   list of conditions and the following disclaimer.
// * Redistributions in binary form must reproduce the above copyright notice,
//   this list of conditions and the following disclaimer in the documentation
//   and/or other materials provided with the distribution.
// * Neither the name of the copyright holder nor the names of its
//   contributors may be used to endorse or promote products derived from
//   this software without specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
// AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
// IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
// DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
// FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
// DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
// SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
// CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
// OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
// OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
//
// Author: Nick Morales

#include <string>
#include "rclcpp/rclcpp.hpp"

// RAII node to terminate the indicated process
class RemoteDockerProcessHandler : public rclcpp::Node
{
public:
  RemoteDockerProcessHandler()
  : Node("remote_process_handler"),
  // get screen process name to kill
  screen_process_name_{declare_parameter<std::string>("screen_process_name")},
  // get docker container name to kill
  docker_kill_command_{declare_parameter<std::string>("docker_kill_command")},
  // construct kill command
  kill_command_{"screen -S " + screen_process_name_ + " -X quit"}
  {
  }
  ~RemoteDockerProcessHandler()
  {
    // execute kill commands
    system(kill_command_.c_str());
    system(docker_kill_command_.c_str());
  }

  const std::string screen_process_name() const
  {
    return screen_process_name_;
  }
  
  const std::string docker_kill_command() const
  {
    return docker_kill_command_;
  }
  
private:
  const std::string screen_process_name_ = "";
  const std::string docker_kill_command_ = "";
  const std::string kill_command_ = "";
};

int main(int argc, char * argv[])
{

  // Init ROS
  rclcpp::init(argc, argv);

  auto node = std::make_shared<RemoteDockerProcessHandler>();

  try
  {
    while (rclcpp::ok()) {
      rclcpp::spin_some(node);
    }
    RCLCPP_INFO_STREAM(node->get_logger(), "\nTERMINATING: " << node->screen_process_name());
    RCLCPP_INFO_STREAM(node->get_logger(), "\nKILLING CONTAINER: " << node->docker_kill_command());

    // Shutdown ROS
    rclcpp::shutdown();
  }
  catch (const rclcpp::exceptions::RCLError & e)
  {
  }

  return 0;
}