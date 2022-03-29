# Chauffeur
[Chauffeur](https://github.com/rjpolackwich/chauffeur) was designed to provide an intiutive and easy to get started with building and making [Overpass](https://python-overpy.readthedocs.io/en/latest/) queries in Python. It is also built to empower users who are interested in using the OverpassQureryLanguage primitives to do things like data QA, data "gardening," and otherwise through the consruction of more complex and logical queries. 

In building Chauffeur, attention was taken to creating interfaces and naming conventions that shed light on some of the less understood aspects of Overpass, as well as [Open Street Map](https://wiki.openstreetmap.org/wiki/Main_Page)(OSM). The more we know about the kind of data out there on OSM, the better judements we can make when, eg, building QA metrics on results, as well as optimizing query requests, etc. Chauffeur is supposed to empower researchers to develop these kind of data intuitions and statistics by abstracting the Query Language itself, providing best practices as taken from Overpass, providing access to formatting and service params, and defining preconfigured objects for different use cases.

## Getting Started

```
import chauffeur as cfr
```
The main entrypoint is the `chauffeur.QueryBuilder` object. It provides the interfaces for query construction, parameterization, and execution. Initialize a `QueryBuilder` to get started.
```
qb = cfr.QueryBuilder()
```
### Request and Query Parameters
The `settings` interface let's a user define Overpass-specific request+response parameters. Examples include global bounding boxes, global date filters, server timeouts, and data limits, as well as response format. Chauffeur defaults to the Overpass default request params, which means a blank string. If the Overpass default params aren't optimal for your query, you can change them:

```
qb.settings.timeout = 3600 # Set the Overpass server timeout in seconds
qb.settings.maxsize = int(cfr.QuerySettings.MAXSIZE_LIMIT / 2) # Set the return payload to max 1GB
qb.settings.payload_format = 'json' # Return results in JSON format instead of default XML
```
These params can also be passed as keywords during `QueryBuilder` initialization.

The `output_mode` interface is meant to bridge the "print" concept in OverpassQL. The query output controls, or mode descriptors, are relevant to the way Overpass processes queries and returns information. The defaults are consistent with Overpass, but can be changed:
```
qb.output_mode.GEOMETRY = cfr.fmt.Geometry.CENTER_POINT
qb.output_mode.VERBOSITY = cfe.fmt.Verbosity.VERBOSE
print(qb.output_mode)
```

### Defining Query Statements with Filters
Chaufeur provides various query filters accessible via the main `chauffeur` module. These are: `chauffeur.UserFilter`, `chauffeur.IdFilter`, `chauffeur.BboxFilter`, and `chauffeur.TagFilter`. The following demonstrates some of the ways the `TagFilter` can be used to search for OSM tags, which are defined as key-value pairs.

The following defines a filter for schools - namely, a tag with key "amenity" and value "school":
```
schools = cfr.TagFilter("amenity", "school")
```
This would filter elements that have an "amenity" key that includes the tag value "school". To extend the search to include other elements, you can include them as a list of values: 
```
places_of_study = cfr.TagFilter("amenity", ["school", "university", "college"])
```
Instead of creating three different filters on the same tag key, chauffeur concatenates the values into a regex string, which is supported by Overpass and is considered a best practice.

We can match a tag key with any value whatsoever by excluding input vals:
```
any_amenity = cfr.TagFilter("amenity")
```
Filtering by non-existence is supported as well:
```
no_amenities = cfr.TagFilter("amenity", exists=False) # Disallow any object with "amenity" key and any values
amenities_no_learning = cfr.TagFilter("amenity", ["school", "university", "college"], exists=False) # Find amenities without educational tags
```
Features of interest are often characterized by multiple combinations of tag filter values. We can create compound tag filters through union:
```
railstations = cfr.TagFilter("railway", "station") + cfr.TagFilter("public_transport", "station")
```

### Building and Setting Query Statements
The OSM type paradigm is used to classify the "geometry" of an element, so to speak, which can be one of Node, Way, or Relation. A query statement consist of a stated set of elements to search for, and one of more filters. Chauffeur provides a query element interface for defining query statements.

The following asks for school tags classified as node objects in OSM:
```
schools_as_node_types = cfr.NodeQuery(filters=schools)
```
But not all schools are nodes; we might like to get ways and relations as well:
```
schools_as_all_types = cfr.NodeWayRelationQuery()
schools_as_all_types.add_filter(schools)
```
We can add more filters to the school query, or can combine the output of this query with something else we might be interested in, again using the plus sign for unioning:
```
beerstores = cfr.TagFilter("shop", "alcohol")
beerstores_as_all_types = cfr.NodeWayRelationQuery(filters=beerstores)
schools_and_beerstores_query = schools_as_all_types + beerstores_as_all_types
```
Finally, we set the constructed query statement to the `QueryBuilder` object.
```
qb.qsx.append(schools_and_beerstores_query)
```

### Setting AOI's and Getting Output
We can set settings, output formats, etc as we see fit. But because we have not included any cfr.BoundingBox filters, we are searching the whole world. Setting the QueryBuilder.GLobalBoundingBox attribute defines a bounding box filter for each statement in the whole query, and is part of the settings component; it is considered good practice to specify AOIs in this way:
```
qb.GlobalBoundingBox = [50.6,7.0,50.8,7.3] # A bbox framing the German city of Bonn
```
The underlying OverpassQL string can be accessed through a property:
```
qb.raw_query_string
```
Finally, we can perform a query of all Node, Way, and Relation elements that identify both schools and beer stores in Bonn, Germany, by submitting our request to the Overpass servers, and get our results back as JSON:
```
results = qb.request()
```






