# Instructions and Setup Guide

## Containerize the application using Docker

1. Build the Docker Image
  
```bash
$ docker build --platform linux/amd64 -t news-classifier .
```

2. Start the container:

```bash
$ docker run -p 80:80 news-classifier
```

3. Test the Docker container with an example request:

- Option 1: Using the web browser. 

  Visit `http://0.0.0.0:8000/docs`. You will see a /predict endpoint: 

![](https://corise-mlops.s3.us-west-2.amazonaws.com/project3/pic2.png)

You can click on "Try it now" which will let you modify the input request. Click on "Execute" to see the model prediction response from the web server:

![](https://corise-mlops.s3.us-west-2.amazonaws.com/project3/pic3.png)

  - Option 2: Using the command line:

```bash

$ curl -X 'POST' \
  'http://0.0.0.0/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "source": "<value>",
  "url": "<value>",
  "title": "<value>",
  "description": "<value>"
}'

```

## Local testing & examining logs

1. Find out the container id of the running container:
```bash
$ docker ps
```

This will return a response like the following:
```bash

CONTAINER ID   IMAGE                COMMAND                  CREATED         STATUS         PORTS                NAMES
3a45c7f7661c   news-classifier-w3   "uvicorn server:app …"   4 minutes ago   Up 4 minutes   0.0.0.0:80->80/tcp   happy_burnell
```

2. SSH into the container using the container id from above: 

```bash
$ docker exec -it <container id> /bin/sh
```

3. Tail the logs:
```bash

$ tail -f ../data/logs.out
```

4. Now when you send any request to the web server (from the browser, or another tab in the command line), you can see the log output coming through in `logs.out`. Test the web server with these requests and make sure you can see the outputs in `logs.out`:

```bash
{
  "source": "BBC Technology",
  "url": "http://news.bbc.co.uk/go/click/rss/0.91/public/-/2/hi/business/4144939.stm",
  "title": "System gremlins resolved at HSBC",
  "description": "Computer glitches which led to chaos for HSBC customers on Monday are fixed, the High Street bank confirms."
}
```

```bash
{
  "source": "Yahoo World",
  "url": "http://us.rd.yahoo.com/dailynews/rss/world/*http://story.news.yahoo.com/news?tmpl=story2u=/nm/20050104/bs_nm/markets_stocks_us_europe_dc",
  "title": "Wall Street Set to Open Firmer (Reuters)",
  "description": "Reuters - Wall Street was set to start higher on\Tuesday to recoup some of the prior session's losses, though high-profile retailer Amazon.com  may come under\pressure after a broker downgrade."
}
```

```bash
{
  "source": "New York Times",
  "url": "",
  "title": "Weis chooses not to make pickoff",
  "description": "Bill Belichick won't have to worry about Charlie Weis raiding his coaching staff for Notre Dame. But we'll have to see whether new Miami Dolphins coach Nick Saban has an eye on any of his former assistants."
}
```

```bash
{
  "source": "Boston Globe",
  "url": "http://www.boston.com/business/articles/2005/01/04/mike_wallace_subpoenaed?rss_id=BostonGlobe--BusinessNews",
  "title": "Mike Wallace subpoenaed",
  "description": "Richard Scrushy once sat down to talk with 60 Minutes correspondent Mike Wallace about allegations that Scrushy started a huge fraud while chief executive of rehabilitation giant HealthSouth Corp. Now, Scrushy wants Wallace to do the talking."
}
```

```bash
{
  "source": "Reuters World",
  "url": "http://www.reuters.com/newsArticle.jhtml?type=worldNewsstoryID=7228962",
  "title": "Peru Arrests Siege Leader, to Storm Police Post",
  "description": "LIMA, Peru (Reuters) - Peruvian authorities arrested a former army major who led a three-day uprising in a southern  Andean town and will storm the police station where some of his  200 supporters remain unless they surrender soon, Prime  Minister Carlos Ferrero said on Tuesday."
}
```

```bash
{
  "source": "The Washington Post",
  "url": "http://www.washingtonpost.com/wp-dyn/articles/A46063-2005Jan3.html?nav=rss_sports",
  "title": "Ruffin Fills Key Role",
  "description": "With power forward Etan Thomas having missed the entire season, reserve forward Michael Ruffin has done well in taking his place."
}
```
