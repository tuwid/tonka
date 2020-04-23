# Tonka 
## YASB (Yet Another Slack Bot) that helps you keep track of who owns what.

I had an itch and I scratched it, there was this situation where I needed to check outdated docs and ask people on slack to get the owner of a service so at the end I decided to write somethings small with a dynamodb backend to help me keep track of teams and microservices and who owns what

Since I truly believe that the best UI is no UI (and things should work on their own but thats another topic) I went with a chat interface 

```
This bot supports these cool things:
!teams                                           
!teams add <team> <lead>                    
!teams del <team>                           
!teams add_member <team> <member>         
!teams del_member <team> <member>         
!teams add_room <team> <slack_room>     
!teams del_room <team> <slack_room>     
!teams update_po <team> <member>      
!teams show <team>                      

!services                               
!services show <service>                
!services add <service> <service_owner> 
!services del <service>                 
!services update_repo <service> <repo_url>  
!services update_link <service> <svc_link>  

```

## Running the stuff
You can either build the container and run it from there, use `virtualenv` in python or run it from your own machine 
Make sure you have these envrionement variables `AWS_PROFILE`, `SLACK_API_KEY`, `AUTHORIZED_SLACK_CHANNELS`, `AUTHORIZED_USERS` 

## Local development:
run 
```
docker run -p 8000:8000 amazon/dynamodb-local
```
and set the endpoint to localhost:8000 with an aws_key/secret to something random and initalize the tables with `python3 table_init.py` 
