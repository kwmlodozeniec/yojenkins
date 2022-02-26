# Overview

## TODO

Some fancy slide

## Target Time

3:00 minutes


## Setup

- Pull up docs
- Pull up blank terminal
- Set up folders and jobs
- Start a few builds

- Terminal and UI side by side with auto refresh


## Script

**Intro**
    - This is a quick overview/intro video of the `yojenkins` CLI tool
    - This is only a short explanation with a small demo at the end
    - I won't be going into how to install or setup `yojenkins`
    - If you want much more information, visit yojenkins.com


1. **What is yojenkins?**
   - `yojenkins` is a CLI tool for interfacing with and managing Jenkins servers from the terminal
   - This tool can be used to make some Jenkins tasks more efficient
   - You can use it for anything from 
        - build management
        - build monitoring
        - account administration
        - secondary node configuration
        - ...and much much more

2. **Some of the reasons to use `yojenkins` include**
   - Convenience
   - Jenkins server UI can slow
   - Automation and scripting
   - Love for the terminal!

5. **Quick demo**
    - Jenkins server running locally inside a Docker container that was quickly set up with `yojenkins`
    - Show terminal and ui side by side
    - Menu navigation
    - There are definitely many more yojenkins commands to show you, however, this is a quick demo

    - Show each command

    - A few sample commands
        - Create a folder - `yojenkins folder create`
        - Create a job - `yojenkins job create`
        - Start a job - `yojenkins job build`
        - Follow buld logs - `yojenkins build logs ..... --follow`
        - Monitor a build - `yojenkins build monitor .... --sound`
        - Delete the folder - `yojenkins folder delete`
    - Show the menu
        - `yojenkins`

4. Information and Documentation
    - For more information, documentation, and examples go to `yojenkins.com`
