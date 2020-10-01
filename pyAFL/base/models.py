class AFLObject(object):
    def _get_object_from_db(self, **kwargs):
        """
        Searches local DB for queried object.

        Parameters
        ----------
            **kwargs : query terms

        Returns
        -------
            Database object if found;
            else None
        """

        return None