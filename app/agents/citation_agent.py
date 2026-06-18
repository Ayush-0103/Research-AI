class CitationAgent:

    def extract_sources(
        self,
        research_data
    ):

        citations = []

        seen_urls = set()

        for section in research_data:

            for result in section["results"]:

                url = result["url"]

                if url not in seen_urls:

                    citations.append(
                        {
                            "title": result["title"],
                            "url": url
                        }
                    )

                    seen_urls.add(url)

        return citations