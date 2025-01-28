### Graph Web Indexing
My inspiration for https://www.spydr.dev/
#### For more information regarding Google's current indexing standard to power search, refer to: https://www.youtube.com/watch?v=knDDGYHnnSI

To re-create:
### Prerequisites:
Python3<br>
Express.Js<br>
Node.Js<br>

### Installation:
First, clone:
```
git clone git@github.com:Fadeleke57/spyderweb.git
cd spydrweb
```

Install the requirements and set up any required credentials in MongoDB, Neo4J, and Scrapy.
```
pip install -r requirements.txt
```

Run Crawler:
```
scrapy crawl time
```

Run Crawler with a specified search term:
```
scrapy crawl time --a search_term="{TERM}"
```

Run Client:
```
npm install
npm run dev
```

Run Backend:
```
npm install
node server.js
```









