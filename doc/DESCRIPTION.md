lubm queries
============

following is a short description of the **LUBM** queries used for federated **SPARQL** processing. The design is inspired from [Waterloo SPARQL Diversity Test Suite (WatDiv)](http://db.uwaterloo.ca/watdiv/)

Description
-----------

| Query | Shape  | Scaling |
|:------|:-------|--------:|
| lq1  	| linear | scaling |
| lq2  	| linear | constant|
| lq3  	| linear | constant|
| lq4  	| linear | scaling |
| lq5  	| star   | constant|
| lq6  	| star   | scaling |
| lq7  	| star   | scaling |
| lq8  	| star   | scaling |
| lq9  	| flake  | constant|
| lq10  | flake  | constant|
| lq11  | flake  | constant|
| lq12  | complex| constant|
| lq12  | complex| constant|
| lq14  | complex| constant|

LINEAR-shaped Queries
---------------------

**LQ1**
```sparql
PREFIX lubm: <http://www.lehigh.edu/~zhp2/2004/0401/univ-bench.owl#>
SELECT *
WHERE{
        ?researchGroups lubm:subOrganizationOf ?department .
        ?department lubm:name "Department1" .
}
```

**LQ2**
```sparql
PREFIX lubm: <http://www.lehigh.edu/~zhp2/2004/0401/univ-bench.owl#>
SELECT *
WHERE{
        ?department lubm:subOrganizationOf ?university .
        ?professor lubm:worksFor ?department .
        ?student lubm:advisor ?professor .
        ?student lubm:memberOf <http://www.Department1.University0.edu> .
}
```

**LQ3**
```sparql
PREFIX lubm: <http://www.lehigh.edu/~zhp2/2004/0401/univ-bench.owl#>
SELECT *
WHERE{
        ?resgroup lubm:subOrganizationOf ?department .
        ?professor lubm:worksFor ?department .
        ?student lubm:advisor ?professor .
        ?student lubm:memberOf <http://www.Department1.University0.edu> .
}
```

**LQ4**
```sparql
PREFIX lubm: <http://www.lehigh.edu/~zhp2/2004/0401/univ-bench.owl#>
SELECT *
WHERE{
        ?advisor lubm:emailAddress ?email .
        ?advisor lubm:worksFor ?department .
        ?department lubm:name "Department1" .
}
```

STAR-shaped Queries
-------------------

**LQ5**
```sparql
PREFIX lubm: <http://www.lehigh.edu/~zhp2/2004/0401/univ-bench.owl#>
SELECT *
WHERE{
        ?student lubm:advisor ?advisor .
        ?student lubm:name ?name .
        ?student lubm:undergraduateDegreeFrom ?university .
        ?student lubm:takesCourse <http://www.Department1.University0.edu/GraduateCourse33> .
}
```

**LQ6**
```sparql
PREFIX lubm: <http://www.lehigh.edu/~zhp2/2004/0401/univ-bench.owl#>
SELECT *
WHERE {
        ?professor lubm:emailAddress ?mail .
        ?professor lubm:telephone ?phone .
        ?professor lubm:doctoralDegreeFrom ?doctor .
        ?professor lubm:name "FullProfessor1" .
}
```

**LQ7**
```sparql
PREFIX lubm: <http://www.lehigh.edu/~zhp2/2004/0401/univ-bench.owl#>
SELECT *
WHERE {
        ?student  lubm:memberOf  ?department .
        ?student  lubm:takesCourse  ?course .
        ?student  lubm:advisor ?advisor .
        ?student  lubm:teachingAssistantOf  ?tacourse .
        ?student  lubm:emailAddress ?email .
        ?student  lubm:name ?name .
        ?student  lubm:telephone ?telephone .
        ?student  lubm:undergraduateDegreeFrom <http://www.University0.edu> .
}
```

**LQ8**
```sparql
PREFIX lubm: <http://www.lehigh.edu/~zhp2/2004/0401/univ-bench.owl#>
SELECT *
WHERE {
        ?student  lubm:memberOf  ?department .
        ?student  lubm:takesCourse  ?course .
        ?student  lubm:advisor ?advisor .
        ?student  lubm:teachingAssistantOf  ?tacourse .
        ?student  lubm:emailAddress ?email .
        ?student  lubm:name "GraduateStudent71" .
        ?student  lubm:telephone ?telephone .
        ?student  lubm:undergraduateDegreeFrom ?university .
}
```

FLAKE-shaped Queries
--------------------

**LQ9**
```sparql
PREFIX lubm: <http://www.lehigh.edu/~zhp2/2004/0401/univ-bench.owl#>
SELECT *
WHERE {
        ?student lubm:advisor ?advisor .
        ?advisor lubm:worksFor ?department .
        ?department lubm:subOrganizationOf ?university .
        ?student lubm:name ?name .
        ?student lubm:telephone ?tel .
        ?student lubm:takesCourse <http://www.Department12.University1.edu/Course1> .
}
```

**LQ10**
```sparql
PREFIX lubm: <http://www.lehigh.edu/~zhp2/2004/0401/univ-bench.owl#>
SELECT *
WHERE {
        ?department lubm:name ?name .
        ?resgroup lubm:subOrganizationOf ?department .
        ?department lubm:subOrganizationOf <http://www.University0.edu> .
        ?student lubm:memberOf ?department .
        ?student lubm:advisor ?professor .
        ?student lubm:takesCourse ?course .
}
```

**LQ11**
```sparql
PREFIX lubm: <http://www.lehigh.edu/~zhp2/2004/0401/univ-bench.owl#>
SELECT *
WHERE {
        ?department lubm:name ?name .
        ?resgroup lubm:subOrganizationOf ?department .
        ?department lubm:subOrganizationOf ?university .
        ?student lubm:memberOf ?department .
        ?student lubm:advisor ?professor .
        ?student lubm:takesCourse <http://www.Department1.University0.edu/GraduateCourse33> .
}
```

COMPLEX-shaped Queries
----------------------

**LQ12**
```sparql
PREFIX lubm: <http://www.lehigh.edu/~zhp2/2004/0401/univ-bench.owl#>
SELECT *
WHERE {
        ?department lubm:subOrganizationOf ?university .
        ?resgroup lubm:subOrganizationOf ?department .
        ?student lubm:memberOf ?department .
        ?department lubm:name ?name .
        ?student lubm:advisor ?professor .
        ?publication lubm:publicationAuthor ?professor .
        ?publication lubm:publicationAuthor <http://www.Department1.University10.edu/AssociateProfessor1>.
}
```

**LQ13**
```sparql
PREFIX lubm: <http://www.lehigh.edu/~zhp2/2004/0401/univ-bench.owl#>
SELECT *
WHERE {
        ?department lubm:subOrganizationOf ?university .
        ?resgroup lubm:subOrganizationOf ?department .
        ?student lubm:memberOf ?department .
        ?student lubm:advisor ?professor .
        ?student lubm:takesCourse ?course .
        ?publication lubm:publicationAuthor ?professor .
        ?publication lubm:publicationAuthor <http://www.Department1.University10.edu/AssociateProfessor1> .
        ?publication lubm:name ?title .
}
```

**LQ14**
```sparql
PREFIX lubm: <http://www.lehigh.edu/~zhp2/2004/0401/univ-bench.owl#>
SELECT *
WHERE{
        ?student lubm:advisor ?advisor .
        ?advisor lubm:worksFor ?department .
        ?department lubm:subOrganizationOf <http://www.University0.edu> .
        ?head lubm:headOf ?department .
        ?head lubm:emailAddress ?email .
        ?head lubm:doctoralDegreeFrom ?alma .
        ?student lubm:name ?name .
        ?student lubm:telephone ?tel .
        ?student lubm:takesCourse ?course .
}
```

Thanks a lot to
---------------
* [University of Zurich](http://www.ifi.uzh.ch/ddis.html) and the [Swiss National Science Foundation](http://www.snf.ch/en/Pages/default.aspx) for generously funding the research that led to this software.
