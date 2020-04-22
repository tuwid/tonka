# Tonka 
## YASB (Yet Another Slack Bot)
### some bot with a dynamodb backend to help me keep track of teams and microservices and who owns what

```
# !components
Components: ['jenkins','graylog','webhook','bamboo']

# !teams
Teams: ['ops','realiability','finance','core','compliance']

# !members ops
Members of ops are: ['Tuwi', 'Gazi', 'Berti', 'Mondi']

```


Local development:
run `docker run -p 8000:8000 amazon/dynamodb-local` and initalize the tables with `python3 table_init.py` 