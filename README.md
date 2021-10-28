# Droplet Deployer

Simple Flask app which deploys a droplet onto Digital ocean.

Behind the scenes there's [Pulumi](github.com/pulumi/pulumi) being used.

## Background

I have been Terraform user for a while and it is a industry-wide recognized standard tool for deployment of IaC.

Pulumi is written to overcome the hurdle of learning a custom language, allowing developers and DevOps to use standard programming languages such as Python, Go, JavaScript, TypeScript, and C#, to deploy their stacks. I can see merits of using Pulumi where a new team is completely unfamiliar with Terraform but has existing software development skills.
This is not to say that HCL is a difficult language to learn. People with existing software engineering and development skills can quickly pickup Terraform and they will also be well supported by communities as it is an extremely popular tool, if not the tool of choice.

If you are interested in learning more around how Pulumi differs from Terraform, there's a comparision on Pulumi's [website](https://www.pulumi.com/docs/intro/vs/terraform/).

I wanted to write this app to be able to understand Pulumi better so I'm ready for when oppurtunity arise for the use of Pulumi :).


## Getting started

There are a few steps to get stack setup.

Export a config passphrase for encrypting your secrets.

```
export PULUMI_CONFIG_PASSPHRASE=password
```

Export your Digitalocean Token.

```
export DIGITALOCEAN_TOKEN="<YOUR_DO_TOKEN>"
```

Install pulumi engine using curl. For more info, see [here](https://www.pulumi.com/docs/get-started/install/).

```
curl -fsSL https://get.pulumi.com | sh
```

Create a local state backend. Only good for testing or development use.

```
pulumi login --local
```

Install pulumi digitalocean plugin.

```
pulumi plugin install resource digitalocean v4.8.0
```

Setup your `venv`.
```
python3 -m venv venv
```

Install requirements under your `venv`.
```
venv/bin/python3 -m pip install -r requirements.txt
```

And final step is to run the flask application using `flask run` command.

```
FLASK_RUN_PORT=1337 FLASK_ENV=development FLASK_APP=app venv/bin/flask run
```

## Listing Droplets

Hitting the root of the webserver or `/list` would list all the pulumi stacks containing droplets managed by the tool.

```
curl 127.0.0.1:1337

# or

curl 127.0.0.1:1337/list
```

## Creating Droplet

Provide the name of droplet you want to create. This will also be set as Pulumi stack name.

Using curl hit `/add` endpoint.

```
curl -H 'Content-Type: application/json' -d '{"name": "test"}' 127.0.0.1:1337/add
```

## Delete a single Droplet

Provide the name of droplet you want to delete. This also deletes Pulumi stack.

Using curl hit `/delete` endpoint with HTTP method `DELETE` providing instance name as below.

```
curl -X DELETE -H 'Content-Type: application/json' -d '{"name": "test"}' 127.0.0.1:1337/delete
```

## Delete ALL Droplets

The tool also provides ability to delete all droplets and the complete stack managed via this Pulumi setup.

```
curl -X DELETE 127.0.0.1:1337/deleteAll
```

## Acknowledgement

Inspired by similar, feature rich and much better project https://github.com/komalali/self-service-platyform/.
