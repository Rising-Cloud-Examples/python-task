# python-task
This guide will walk you through the simple steps needed to build and run a Python app on Rising Cloud.  

If you'd prefer to watch a video, check out our YouTube of the tutorial.

[![Video Player](https://cms.risingcloud.com/uploads/Video_Player_b69c4aa4ff.png)](https://www.youtube.com/watch?v=M3rqmB9s1h4)

# 1. Install the Rising Cloud Command Line Interface (CLI)
In order to run the Rising Cloud commands in this guide, you will need to [install](https://risingcloud.com/docs/install) the Rising Cloud Command Line Interface. This program provides you with the utilities to setup your Rising Cloud Task or Web Service, upload your application to Rising Cloud, setup authentication, and more.

# 2. Login to Rising Cloud Using the CLI
Using a command line console (called terminal on Mac OS X and command prompt on Windows) run the Rising Cloud login command. The interface will request your Rising Cloud email address and password.

```risingcloud login```

# 3. Initialize Your Rising Cloud Task
Create a new directory to place your project files in, then open this directory with your command line.

Using the command line in your project directory, run the following command replacing $TASK with your unique task name.

Your unique task name must be at least 12 characters long and consist of only alphanumeric characters and hyphens (-). This task name is unique to all tasks on Rising Cloud. A unique URL will be provided to you for sending jobs to your task.

If a task name is not available, the CLI will return with an error so you can try again.

```risingcloud init -s $TASK```

This creates a risingcloud.yaml file in your project directory. This file can be used to configure the build script.

# 4. Create Your Rising Cloud Task

Create your echo script

In your project directory, create a echo.py with the following code:

```
import json
if __name__ == "__main__":
    with open('request.json', 'r') as req_file:
        request = json.load(req_file)
    with open('response.json', 'w+') as res_file:
        response = {}
        response['echo'] = request
        json.dump(response, res_file)
```

This python script opens the request.json file which is the input of a Rising Cloud Job, creates a response.json and writes it under the “echo” field in a new JSON object in the response.json, which is the output of a Rising Cloud job.

**Configure your risingcloud.yaml**

When you ran Rising Cloud init, a risingcloud.yaml should have generated in your project directory. Unless you want to freeze your Python program, no build steps are necessary, so leave the build line in the risingcloud.yaml as build: []. In the deps stage, we need to install python. Change the deps step to:

```
deps: 
- apt-get update
- apt-get -y upgrade
- apt-get install -y python3
```
Now, change the run step to

```run: python3 echo.py```

# 5. Build and Deploy Your Rising Cloud Task

Use the push command to push your updated risingcloud.yaml to your Task on Rising Cloud.

```risingcloud push```

Use the build command to zip, upload, and build your app on Rising Cloud.

```risingcloud build```

Use the deploy command to deploy your app as soon as the build is complete.  Change $TASK to your unique task name.

```risingcloud deploy $TASK```

Alternatively, you could also use a combination to push, build and deploy all at once.

```risingcloud build -r -d```

You can set environment variables for your app either from a file, your risingcloud.yaml, or each variable one by one.

```
risingcloud setenv —file /path/to/.env
risingcloud setenv —var $NAME=$VALUE
```

Rising Cloud will now build out the infrastructure necessary to run and scale your application including networking, load balancing and DNS.  Allow DNS a few minutes to propogate and then your app will be ready and available to use!

# 6. Queue Jobs for your Rising Cloud Task

**Make requests**

Rising Cloud will take some time to build and deploy your application. Once it is done, a POST HTTP request to your task at https://{your_task_code}.risingcloud.app/risingcloud/jobs with the following application/json request body:

```{"hello": "world!"}```

should yield an HTTP response with a body that looks like:

```{"jobId": "<id of job>"}```

To get the status of the job, make a GET HTTP request to your task at https://{your_task_code}.risingcloud.app/risingcloud/jobs/{id of job}, which should respond with a JSON object in the response body. As this example script is extremely fast and simple, the job should complete before you send this request. You can verify this by checking whether the status field in the response JSON is “Completed” and that the result is

```{"echo": {"hello":  "world!"}}```

Congratulations, you’ve successfully used Python on Rising Cloud!
