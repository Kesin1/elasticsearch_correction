
# Table of Contents

1.  [Limit the number of results](#org899460b)
2.  [permettre au FRONT de récupérer le mot clé d'approximation](#org4b6658f)


<a id="org899460b"></a>

# Limit the number of results

[search<sub>request</sub><sub>body</sub> from<sub>size</sub>](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-request-body.html#request-body-search-from-size)
Inside the body of the request you can add

    "from" : 0, "size" : 10,

like

    {
        "from" : 0, "size" : 10,
        "query": {
    	"bool": {
    	    "minimum_should_match": "1",
    	    "should": [
    		{
    		    "multi_match": {
    			"query": "banane",
    			"fuzziness": "AUTO",
    			"type": "most_fields",
    			"fields": [
    			    "title^5",
    			    "title.stemmed^5",
    			    "titleReword^3",
    			    "titleReword.stemmed^3"
    			]
    		    }
    		}
    	    ]
    	}
        }
    }


<a id="org4b6658f"></a>

# permettre au FRONT de récupérer le mot clé d'approximation

Inside the search request body we use a suggester
[Suggesters](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-suggesters.html)

    "suggest": {
        "text": "banane",
        "suggest-title": {
    	"term": {
    	    "field": "title"
    	}
        },
        "suggest-responses": {
    	"term": {
    	    "field": "responses.body"
    	}
        }

With that we get this inside the response body

      "suggest": {
        "suggest-responses": [
    	{
    	    "text": "banane",
    	    "offset": 0,
    	    "length": 6,
    	    "options": [
    		{
    		    "text": "banque",
    		    "score": 0.6666666,
    		    "freq": 26
    		},
    		{
    		    "text": "bagage",
    		    "score": 0.6666666,
    		    "freq": 1
    		},
    		{
    		    "text": "bonne",
    		    "score": 0.6,
    		    "freq": 1
    		}
    	    ]
    	}
        ],
        "suggest-title": [
    	{
    	    "text": "banane",
    	    "offset": 0,
    	    "length": 6,
    	    "options": [
    		{
    		    "text": "banque",
    		    "score": 0.6666666,
    		    "freq": 7
    		}
    	    ]
    	}
        ]
    }

Each options array contains an option object that includes the:

-   suggested text,
-   its document frequency and
-   score compared to the suggest entry text.

The meaning of the score depends on the used suggester. The term suggester’s score is based on the edit distance.

So you can retrieve the words, by inspecting the suggester. You might filter them by the frequency.

