class MetaGenerator:

    def generate_metadata(self, chunk, company, domain, source):

        tags = self.generate_tags(chunk)
        metadata = {
            "company": company,
            "domain": domain,
            "source": source,
            "tags": tags
        }
        return metadata

    def generate_tags(self, chunk:str):
        tags = []
        c_low = chunk.lower()
        if 'vat' in c_low or 'tax' in c_low:
            tags.extend(['vat', 'tax', 'taxation'])
        
        if any(word in c_low for word in ['return', 'refund', 'cancel', 'exchange']):
            tags.append('return')

        if any (word in c_low for word in ['bank', 'visa', 'invoice', 'card', 'nordea']):
            tags.append('payments')

        if any(word in c_low for word in ['age', 'under 18', 'guardian', 'minor']):
            tags.append('legal_age')

        
        return list(set(tags))