# ReadMe

# Run locally
* go to the dir.
* $ poetry shell 
* $ poetry intstall
* $ python app.py
* go to the provided endpoint, and call
[endpoint]/cars?top=4&make=audi&model=a4&year=2008

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
* # Mac OS Monterey already uses port 5000
* https://medium.com/pythonistas/port-5000-already-in-use-macos-monterey-issue-d86b02edd36c



# New deployment workflow
1. save changes locally & test.
2. build now docker image locally:
docker buildx build --platform=linux/amd64 -t {tag} .
3. Push local container image to remote AWS lightsail:
aws lightsail push-container-image --service-name flask-service --label flask-container --image {tag}
4. Update reference to image (= output previous step) to local 'container.json' file.
5. Deploy to AWS lightsail:
aws lightsail create-container-service-deployment --service-name flask-service --containers file://containers.json --public-endpoint file://public-endpoint.json
6. Check whether the config of your deployment seems right:
aws lightsail get-container-services
7. clean up after yourself locally:
   * NB this removes all local container, corresponding volume, and images. If this is  not what you want, rm images in isolation.
docker rm -vf $(docker ps -aq)
docker rmi -f $(docker images -aq)


   
