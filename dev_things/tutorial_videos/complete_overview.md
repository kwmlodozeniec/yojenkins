# Intro Video Outline



## TODO



------------------------------------------------------------------------------------


## Setup

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


### Intro

- Hello and welcome to an overview of `yojenkins` CLI
- This video should show you what yojenkins is, and some basic functions
- For more information, documentation, and examples go to `yojenkins.com`
- What is yojenkins?
   - `yojenkins` is a CLI tool for interfacing with and managing Jenkins servers from the terminal
   - This tool can be used to make some Jenkins tasks more efficient
   - You can use it for anything from build maonagement to monitoring to account administration to secondary node configuration
   - So if you are doing anything with Jenkins server, you may be interested in `yojenkins`

- **Alright, let's dive into it!**

------------------------------------------------------------------------------------

### Development Server Setup

- To start off we need a Jenkins server address
- `yojenkins` allows you to quickly deploy a local development server for testing, training, demo purposes.
- Lets start off by setting up this full fledged local Jenkins server using `yojenkins`
- `yojenkins server server-deploy`
- Note that this command relies on Docker to be active
- Show in UI
- Note about not using it in production

------------------------------------------------------------------------------------

### Main Menu

- Quickly go through a few menu items
   - account
   - auth
   - job
   - etc

> NOTE: Obviously this is yojenkins version 0.0.55, this menu may look different in future versions

------------------------------------------------------------------------------------

### Authentication

- Set up authentication - 1 min
   - First thing we want to do is set up a autnethication profile
   - If you ware familiar to how AWS authenticates with local credentials, this is similar
   - The point here is to set up credentials once and not worry about it again
   - Configuring a profile
      - `yojenkins auth --help`
      - `yojenkins auth configure`
      - `yojenkins auth show`
   - Adding a profile token
      - `yojenkins auth --help`
      - `yojenkins auth token`
      - `yojenkins auth token --profile default`
      - `yojenkins auth show --yaml`
      - cat out the `credentials` file

------------------------------------------------------------------------------------

### Output Formatting

- Show output formatting
   - `yojenkins server info`
   - pretty, yaml, toml, xml

------------------------------------------------------------------------------------

### Jobs and Builds

- Create a job (something continuous)
   - Build a blank job
       - `yojenkins job create my_empty_job .`
   - Create a simple job
      - Show the configuration file
         - `cat new_job_config.xml `
      - `yojenkins job create --config-file new_job_config.xml "My Job" .`
      - Check UI


- Build the job
   - `yojenkins job build my_empty_job`
   - `yojenkins job build "My Job"`


- Get build logs
   - `yojenkins build logs "My Job" --latest`
   - `yojenkins build logs "My Job" --tail 10`
   - `yojenkins build logs "My Job" --tail 0.10`
   - `yojenkins build logs "My Job" --follow`


- Build monitor UI
   - `yojenkins build monitor "My Job" --latest`
       - Show `H` menu
       - Press `S` for sound
       - Press Abort to make a sound
   - `yojenkins build monitor my_empty_job --latest --sound`


------------------------------------------------------------------------------------

### Accounts

- Create a new user
   - `yojenkins account list --yaml`
   - `yojenkins account info --yaml admin` 
   - `yojenkins account create --email user@jenkins.com --description "My first user" my_user_1 12345`
   - Show in UI:
      - Dashboard > People > my_user_1
      - Manage Jenkins > Configure Global Security > Matrix

- Add permissions to new user
   - `yojenkins account permission-list --yaml --list`
   - Run update permission: hudson.model.Run.UPDATE
   - ``yojenkins account permission --action add --permission-id hudson.model.Item.CREATE,hudson.model.Item.DELETE my_user_1``
   - Show in UI 

------------------------------------------------------------------------------------

### Other Useful Tools

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

------------------------------------------------------------------------------------

### Outro

- This concludes the overview intro video.

- If you need any more information, and for documentation, check out `yojenkins.com`

- Thanks for taking the time to watch this video and consider yojenkins.

- I hope you will consider using it. Thank you.