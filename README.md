### Graph Web Indexing
My inspiration for https://www.spydr.dev/
#### For more information regarding Google's current indexing standard to power search, refer to: https://www.youtube.com/watch?v=knDDGYHnnSI

To re-create:
### Prerequisites:
Python3<br>
Express.Js<br>
Node.Js<br>

<h4>
 Web Crawler Pipeline:
</h4>  
<ul>
 <li>I initialized a Scrapy Spider with connections to a Neo4j driver</li>
 <li>Using the beautiful <a href="https://radimrehurek.com/gensim/">genism library</a>, I created a makeshift TF-IDF model that dynamically computes a similarity score between article nodes in the graph. It was slow at first, so I removed mandatory NLTK tokenization and made it an optional parameter for slightly more accurate results</li>
 <li>The flow looks like this: Model instantiated -> parent-child article text is extracted -> corpus about the subject matter is generated to train the model -> article text is transformed into a bag-of-words -> perform a text frequency inverse text frequency between both articles -> similarity score calculated </li>
 <li>Upon a Scrapy crawl with a set of root nodes, children's articles are connected to their parent articles and weighted by this similarity score</li>
 <li>Results are dumped to the Neo4j graph</li>
</ul>

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









