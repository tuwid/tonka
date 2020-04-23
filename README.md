# Tonka 
## YASB (Yet Another Slack Bot)
### some bot with a dynamodb backend to help me keep track of teams and microservices and who owns what

```
This bot supports these cool things:
*!teams*                                           
*!teams add <team> <lead>*                    
*!teams del <team>*                           
*!teams add_member <team> <member>*         
*!teams del_member <team> <member>*         
*!teams add_room <team> <slack_room>*     
*!teams del_room <team> <slack_room>*     
*!teams update_po <team> <member>*      
*!teams show <team>*                      

*!services*                               
*!services show <service>*                
*!services add <service> <service_owner>* 
*!services del <service>*                 
*!services update_repo <service> <repo_url>*  
*!services update_link <service> <svc_link>*  

```

Local development:
run `docker run -p 8000:8000 amazon/dynamodb-local` and initalize the tables with `python3 table_init.py` 
