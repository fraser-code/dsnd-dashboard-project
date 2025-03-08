from employee_events.query_base import QueryBase


class Employee(QueryBase):

    name = "employee"

    def names(self):

        query = f"""
            SELECT first_name || ' ' || last_name AS full_name, employee_id
            FROM {self.name};
        """
        return self.pandas_query(query)

    def username(self, id):

        query = f"""
            SELECT first_name || ' ' || last_name AS full_name
            FROM {self.name}
            WHERE employee_id = {id};
        """
        return self.pandas_query(query)

    def model_data(self, id):

        query = f"""
            SELECT SUM(positive_events) AS positive_events,
                   SUM(negative_events) AS negative_events
            FROM {self.name}
            JOIN employee_events USING ({self.name}_id)
            WHERE {self.name}.{self.name}_id = {id};
        """
        return self.pandas_query(query)
