    headlines = []
        links = []

        # Find all occurrences of the "<h3 class="title">" tag
        headline_start_tags = [m.start() for m in re.finditer(r'<h3 class="title">', html_content)]

        for start_tag in headline_start_tags:
            # Find the end of the headline tag
            end_tag = html_content.find('</h3>', start_tag)

            # Extract the headline text
            headline = html_content[start_tag + len('<h3 class="title">'):end_tag].strip()
            headlines.append(headline)

            # Find the start of the link tag
            link_start = html_content.rfind('<a href="', 0, start_tag)

            # Find the end of the link tag
            link_end = html_content.find('">', link_start)

            # Extract the link URL
            link = html_content[link_start + len('<a href="'):link_end]
            links.append(link)

        return headlines, links