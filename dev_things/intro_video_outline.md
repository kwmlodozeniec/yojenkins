# Intro Video Outline


## Tools - Options

1. Photos App / Audacity App
   - Audio and video have to be started seperately
   - Needt to align audio and video
2. OSB - Open Broadcaster Software - THIS IS THE ONE
   - https://obsproject.com/


## TODO

- Doc strings
   - Auth menu, explain how it works
   - Create job, add note that by default a blank.empty job will be created


## Video Meta


- Video length max: 15:00 minutes

------------------------------------------------------------------------------------

## Pre-Recording

- Web UI
   - Start up server
   - Remove all jobs
   - Remove all users
   - Remove all tokens
   - Tear down server
- yojenkins
   - Remove credentials file
   - Clear history

------------------------------------------------------------------------------------

## Script Outline

- Start off with Documentation on screen


> LESS UMMMMMMMs!!!
> MORE MOUSE POINTING
> Better cadence, less whispering

### Intro

- What is yojenkins?
   - `yojenkins` is a CLI tool for interfacing with and managing Jenkins servers from the terminal
   - This tool can be used to make some Jenkins tasks more efficient
   - You can use it for anything from build maonagement to monitoring to account administration to secondary node configuration
- For more information, documentation, and examples go to yojenkins.com
- **Let's dive into it!**


### Development Server Setup

- Lets start off by quickly deploying a full fledged jenkins server using `yojenkins`
- `yojenkins server server-deploy`
- Note that this command relies on Docker to be active
- Show in UI
- Note about not using it in production

### Main Menu

- Quickly go through a few menu items
   - account
   - auth
   - job
   - etc

> NOTE: Obviously this is yojenkins version 0.0.55, this menu may look different in future versions


### Authentication

- Set up authentication - 1 min
   - First thing we want to do is set up a autnethication profile
   - If you ware familiar to how AWS authenticates with local credentials, this is similar
   - The point here is to set up credentials once and not worry about it again
   - Configuring a profile
      - `yojenkins auth configure`
      - `yojenkins auth show --yaml`
   - Adding a profile token
      - `yojenkins auth --help`
      - `yojenkins auth token`
      - `yojenkins auth token --profile default`
      - `yojenkins auth show --yaml`
      - bat out the `credentials` file

- Show output formatting
   - `yojenkins server info`
   - pretty, yaml, toml, xml


### Jobs and Builds

- Create a job (something continous)
   - Build a blank job
       - `yojenkins job create my_blank_job .`
   - Create a simple job
      - Show the configuration file
         - `bat new_job_config.xml `
      - `yojenkins job create --config-file new_job_config.xml "My First Job" .`
      - Check UI


- Build the job
   - `yojenkins job build my_blank_job`
   - `yojenkins job build "My First Job"`


- Get build logs
   - `yojenkins build logs "My First Job" --latest`
   - `yojenkins build logs "My First Job" --tail 10`
   - `yojenkins build logs "My First Job" --tail 0.10`
   - `yojenkins build logs "My First Job" --follow`


- Build monitor UI
   - `yojenkins build monitor "My First Job" --latest`
       - Show `H` menu
       - Press `S` for sound
       - Press Abort to make a sound
   - `yojenkins build monitor my_blank_job --latest --sound`


### Accounts

- Create a new user
   - `yojenkins account list --yaml`
   - `yojenkins account info --yaml admin` 
   - `yojenkins account create --email user@jenkins.com --description "My first user" my_user_1 12345`
   - Show in UI:
      - Dashboard > People > my_user_1
      - Manage Jenkins > Configure Global Security > Matrix

- Add permssions to new user
   - `yojenkins account permission-list --yaml --list`
   - Run update persmission: hudson.model.Run.UPDATE
   - ``yojenkins account permission --action add --permission-id hudson.model.Item.CREATE,hudson.model.Item.DELETE my_user_1``
   - Show in UI 


### Various tools

- Running custom rest-request with existing credentials
   - `yojenkins tools rest-request "me/api/json"`
   - `yojenkins tools rest-request --request-type POST "manage"`
   - `yojenkins tools rest-request --request-type POST "manage" --raw`
   - `yojenkins tools rest-request --request-type POST "manage" --raw --clean-html`


- Running groovy scripts on server
    - Note that this requires the user to have the correct permissions
    - `yojenkins tools script --file ./my_groovy_script.groovy`


- Show yojenkins history
    - Note that the history files lives in `~/.yojenkins` directory
    - ``yojenkins tools history``
    - ``yojenkins tools history --clear`` 

- Show help, debug option
   - Explain --help
   - `yojenkins server info --debug`

### Outro

- This concludes the overview intro video.

- Please go to yojenkins.com for more information.

- Thanks for taking the time to consider yojenkins.

- I hope you will consider using it. Bye