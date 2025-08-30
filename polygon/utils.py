from polygon.schemas import TableSchema, ColumnSchema


def copy_group_by_mapping(copy_from: TableSchema, copy_to: TableSchema, env):
    for group_id in range(max(copy_from.ctx['groups_considered'])):
        for tuple_id in range(copy_from.ancestors[0].bound):
            env.formulas.append(
                env.grouping(copy_to.table_id, tuple_id, group_id) == env.grouping(copy_from.table_id, tuple_id, group_id),
                label='misc'
            )

    env.formulas.append(env.size(copy_to.table_id) == env.size(copy_from.table_id), label='misc')
    copy_to.ctx['groups_considered'] = copy_from.ctx['groups_considered']
    copy_to.lineage = copy_from.lineage


def create_empty_table(row: int, col: int, env):
    table_id = env.next_table_id()
    table_name = f'empty_table_{row}x{col}'
    table_schema = TableSchema(table_id, table_name, row)

    for column_id in range(col):
        column_schema = ColumnSchema(column_id, str(column_id), 'int', table_name=table_name)
        table_schema.append(column_schema)

    return table_schema


def chunkify(lst, n):
    """Partition a list into n approximately equal-sized chunks."""
    size = len(lst) // n
    remainder = len(lst) % n
    chunks = [lst[i * size + min(i, remainder):(i + 1) * size + min(i + 1, remainder)] for i in range(n)]
    return chunks
