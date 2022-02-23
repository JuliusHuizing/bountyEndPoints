# ReadMe

# Set Up & Trouble Shooting:
## Solving problems with exposing right port on right host:
* run in detached mode -d (e.g. docker run -dp 5001:5001 image-tag)
Ensure right ports and host:
* https://www.reddit.com/r/docker/comments/6f3idv/noob_question_dockered_flask_app_dropping/
* ensure right host: https://stackoverflow.com/questions/20212894/how-do-i-get-flask-to-run-on-port-80


## Querrying the endpoint:
https://idratherbewriting.com/learnapidoc/docapis_doc_parameters.html


## Deplpoying / Deleting on AWS Lightsail:
https://aws.amazon.com/getting-started/hands-on/serve-a-flask-app/

### When redeploying
* Do not forget to
* First build a new docker image locally
* then use that to build a new docker image on lightsail
* change the flaskservice nam (number) in public-endpoints before making the container service.
* Finally, build the service.


### failing to deploy:
* probably due to building on arm (mac), and then arms version image causing problems on the linux running instance:
* https://stackoverflow.com/questions/67361936/exec-user-process-caused-exec-format-error-in-aws-fargate-service
* e.g. instead of a regular build, use buildx to specifcally build for amd:
* $ docker buildx build --platform=linux/amd64 -t {wantedTagName for Image} .