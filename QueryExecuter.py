from SPARQLWrapper import SPARQLWrapper, JSON, XML, N3, RDF

symptoms_list = []
sdd = {}
dd = {}


class QueryExecuter:

    type_str = ""

    def find_symptoms(self, age, type):

            if type == "adult cow":
                type_str = "cow_afflict_age"
            elif type == "calf":
                type_str = "calf_afflict_age"

            sparql = SPARQLWrapper("http://localhost:3030/cow_ontology/")
            sparql.setQuery("""prefix cow: <http://localhost/cow_ontology.owl#>
                            PREFIX vcard: <http://www.w3.org/2000/01/rdf-schema#>
                            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

                            SELECT ?symp_name
                            WHERE{
                              ?Symp cow:symp_name ?symp_name .
                            {SELECT ?Symp
                              WHERE{
                                VALUES (?value) { ( """+str(age)+""" ) ( 0 ) }
                                  ?Disease cow:"""+type_str+""" ?value .
                                  ?Disease cow:has ?Symp .
                              }
                              }
                            }
                            """)

            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()

            for result in results["results"]["bindings"]:
                current_symptom = result["symp_name"]["value"]
                if current_symptom not in symptoms_list:
                    symptoms_list.append(current_symptom)
                sdd[current_symptom] = []

            self.find_diseases(age, type_str)

            return symptoms_list

    def find_diseases(self,age,type_str):
        sparql = SPARQLWrapper("http://localhost:3030/cow_ontology/")
        sparql.setQuery("""PREFIX cow: <http://localhost/cow_ontology.owl#>
                        PREFIX vcard: <http://www.w3.org/2000/01/rdf-schema#>
                        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

                        SELECT ?Disease ?disease_name
                        WHERE
                        {
                          VALUES (?value) { ( """+str(age)+""" ) ( 0 ) }
                                  ?Disease cow:"""+type_str+""" ?value .
                          ?Disease cow:disease_name ?disease_name .
                        }
                        """)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        for result in results["results"]["bindings"]:
            current_disease = result["disease_name"]["value"]


            sparql.setQuery("""prefix cow: <http://localhost/cow_ontology.owl#>
                            PREFIX vcard: <http://www.w3.org/2000/01/rdf-schema#>
                            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

                            SELECT (COUNT(?symps) AS ?symp)
                            WHERE
                            {
                              ?Disease cow:disease_name \""""+current_disease+"""\" .
                              ?Disease cow:has ?symps .
                            }
                                    """)

            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()
            for result in results["results"]["bindings"]:
                #print(result["symp"]["value"])
                dd[current_disease] = [int(result["symp"]["value"]),int(0),int(0)]

            sparql.setQuery("""prefix cow: <http://localhost/cow_ontology.owl#>
                                PREFIX vcard: <http://www.w3.org/2000/01/rdf-schema#>
                                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

                                SELECT ?symp_name
                                WHERE{
                                  ?symps cow:symp_name ?symp_name
                                  {SELECT ?symps
                                  WHERE
                                  {
                                    ?Disease cow:disease_name \""""+current_disease+"""\" .
                                    ?Disease cow:has ?symps .
                                  }
                                  }
                                }""")

            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()
            for result in results["results"]["bindings"]:
                #print(result["symp_name"]["value"])
                sdd[result["symp_name"]["value"]].append(current_disease)


    def get_symp_disease_list(self):
        return sdd

    def get_disease_frequency_list(self):
        return dd