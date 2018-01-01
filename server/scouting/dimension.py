import psycopg2.extras

conn = psycopg2.connect("dbname=scouting host=localhost user=irs1318 password=irs1318")
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


class DimensionDal(object):

    @staticmethod
    def build_dimension_dicts(dim_table):
        name_to_id = {}
        id_to_name = {}

        cur.execute("SELECT id, name FROM " + dim_table)
        res = cur.fetchall()
        for row in res:
            row_dict = dict(row)
            name_to_id[row_dict['name']] = row_dict['id']
            id_to_name[row_dict['id']] = row_dict['name']
        return name_to_id, id_to_name

    @staticmethod
    def build_task_option_dicts():
        name_to_id = {}
        id_to_name = {}

        cur.execute("SELECT id, task_name||'-'||option_name as name FROM task_options")
        res = cur.fetchall()
        for row in res:
            row_dict = dict(row)
            name_to_id[row_dict['name']] = row_dict['id']
            id_to_name[row_dict['id']] = row_dict['name']
        return name_to_id, id_to_name