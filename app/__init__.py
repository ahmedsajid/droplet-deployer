from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
import os
import pulumi
from pulumi import automation as auto
import pulumi_digitalocean as do

app = Flask(__name__)
region = "nyc3"
project_name = "droplet_deployer"

def pulumi_droplet(instance_name):
    droplet = do.Droplet(
        instance_name,
        image="ubuntu-18-04-x64",
        region=region,
        size="s-1vcpu-1gb"
    )

@app.route("/", methods=["GET"])
@app.route("/list", methods=["GET"])
def api_list():
    try:
        ws = auto.LocalWorkspace(project_settings=auto.ProjectSettings(name=project_name, runtime="python"))
        stacks = ws.list_stacks()
        return jsonify(ids=[stack.name for stack in stacks])
    except Exception as exn:
        return make_response(str(exn), 500)

@app.route("/add", methods=["POST"])
def api_add():
    data = request.get_json()
    instance_name = data['name']
    stack_name = data['name']
    def pulumi_program():
        return pulumi_droplet(instance_name)
    try:
        # create a new stack, generating our pulumi program on the fly from the POST body
        stack = auto.create_stack(
            stack_name=str(stack_name),
            project_name=project_name,
            program=pulumi_program,
        )
        # deploy the stack, tailing the logs to stdout
        stack.up(on_output=print)
        return jsonify(message=f"stack '{stack_name}' successfully created!")
    except auto.StackAlreadyExistsError as exn:
        return make_response(str(exn), 409)

@app.route("/delete", methods=["DELETE"])
def api_delete():
    data = request.get_json()
    instance_name = data['name']
    stack_name = data['name']

    try:
        stack = auto.select_stack(stack_name=stack_name,
                                  project_name=project_name,
                                  # noop program for destroy
                                  program=lambda *args: None)
        stack.destroy(on_output=print)
        stack.workspace.remove_stack(stack_name)
        return jsonify(message=f"stack '{stack_name}' successfully removed!")
    except auto.StackNotFoundError:
        return make_response(f"stack '{stack_name}' does not exist", 404)
    except auto.ConcurrentUpdateError:
        return make_response(f"stack '{stack_name}' already has update in progress", 409)
    except Exception as exn:
        return make_response(str(exn), 500)

@app.route("/deleteAll", methods=["DELETE"])
def api_deleteall():
    # Get list of stacks
    try:
        ws = auto.LocalWorkspace(project_settings=auto.ProjectSettings(name=project_name, runtime="python"))
        stacks = ws.list_stacks()
    except Exception as exn:
        return make_response(str(exn), 500)

    # Loop over stacks and destroy them
    for stack in stacks:
        stack_name = stack.name
        print("destroying stack: " + stack_name)
        try:
            stack = auto.select_stack(stack_name=stack_name,
                                      project_name=project_name,
                                      # noop program for destroy
                                      program=lambda *args: None)
            stack.destroy(on_output=print)
            stack.workspace.remove_stack(stack_name)
        except Exception as exn:
            return make_response(str(exn), 500)
    return jsonify(message=f"All stacks have been successfully destroyed!")

if __name__ == "__main__":
    app.run()
