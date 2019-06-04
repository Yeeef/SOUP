import pydot
from ErrorHandler import *
from SymbolTable import *
import copy
from functools import reduce
from utils import *
import random


def traverse_skew_tree(node, stop_node_type=None):
    # TODO: find bug
    # FIXME: 改变了原有的顺序
    """
    遍历一种很特殊但是在我们的 parse tree 中频繁出现的一种结构（左递归导致的）
    能不能顺便做一个 compress ✅
    :param stop_node_type:
    :param node:
    :return: flattened subtree
    """
    if not isinstance(stop_node_type, list):
        stop_node_type = [stop_node_type]
    descending_leaves = []
    children = node.children
    for child in children:
        if isinstance(child, Node):
            if child.type in stop_node_type:
                descending_leaves.append(child)
            else:
                descending_leaves.extend(traverse_skew_tree(child, stop_node_type))
        elif child is None:
            pass
        else:
            # reach the leaf node
            descending_leaves.append(child)

    return tuple(descending_leaves)


def traverse_skew_tree_gen(node, stop_node_type=None):
    if node.type == stop_node_type:
        return [node]
    descending_leaves = []
    children = node.children
    for child in children:
        if isinstance(child, Node):
            if child.type == stop_node_type:
                descending_leaves.append(child)
            else:
                descending_leaves.extend(traverse_skew_tree(child, stop_node_type))
        elif child is None:
            pass
        else:
            # reach the leaf node
            descending_leaves.append(child)

    return tuple(descending_leaves)


def traverse_skew_tree_bool(node, stop_node_type, target_node_type):
    descending_leaves = []
    children = node.children
    if node.type != target_node_type:
        descending_leaves.append(node)
        return tuple(descending_leaves)
    for child in children:
        if isinstance(child, Node):
            if child.type.startswith(stop_node_type):
                descending_leaves.append(child)
            else:
                descending_leaves.extend(traverse_skew_tree_bool(child, stop_node_type, target_node_type))
        else:
            # reach the leaf node
            descending_leaves.append(child)

    return tuple(descending_leaves)


class Node(object):

    def __init__(self, t, lineno, *args):
        assert isinstance(lineno, int), type(lineno)
        self._type = t
        self._children = args
        self._lineno = lineno

    @property
    def children(self):
        return self._children

    @property
    def type(self):
        return self._type

    @property
    def lineno(self):
        return self._lineno

    # TODO: this __str__ is not clear
    def __str__(self):
        # s = "Node type: %s" % self._type/
        s = "type: " + str(self._type) + "\n"
        # s += "".join(["i: " + str(i) + "\n" for i in self._children])
        return s


def parse_range_from_range_node(Node):
    # parse tree error
    assert Node.type == 'range', Node.type
    assert len(Node.children) == 2, Node.children

    left_range_node, right_range_node = Node.children
    left_type, right_type = left_range_node.type, right_range_node.type
    left_val, *_ = left_range_node.children
    right_val, *_ = right_range_node.children
    # semantic error
    if left_type != right_type:
        SemanticLogger.error(left_range_node.lineno,
                             'left range type: `{}`, right range type: `{}`'.format(left_type, right_type))
    elif left_type not in ['integer', 'char']:
        SemanticLogger.error(left_range_node.lineno,
                             'arr only supprt integer / char indices, not {}'.format(left_type))

    elif left_val > right_val:
        SemanticLogger.error(left_range_node.lineno,
                             'left range val `{}` > right range val `{}`'.format(left_val, right_val))
        # raise Exception('left range val `{}` > right range val `{}`'.format(left_val, right_val))
    return left_type, left_val, right_val


def parse_type_definition_from_type_node(node, symbol_table):
    """
    parse type_definition node, only return information
    :param symbol_table:
    :param node:
    :return:
    """
    assert node.type == 'type_definition', node.type
    children = node.children
    assert len(children) == 2, children
    id_, type_node = children
    if type_node.type == 'alias':
        # most simple
        type_alias, *_ = type_node.children
        return 'alias', id_, type_alias
    elif type_node.type == 'sys_type':
        sys_type, *_ = type_node.children
        return 'sys_type', id_, sys_type
    elif type_node.type == 'record':
        name_and_type_list = parse_record_node(type_node, symbol_table)
        return 'record', id_, name_and_type_list
    else:
        # 1d array, complicated
        index_type, element_type, left_val, right_val = parse_array_from_array_node(type_node, symbol_table)
        return 'array', id_, index_type, element_type, left_val, right_val


def parse_type_decl_node(type_decl_node, symbol_table):
    """
    grammar rule:
        * type_decl         : simple_type_decl
                            | array_type_decl
                            | record_type_decl
        * simple_type_decl  :  SYS_TYPE
                            |  LP  name_list  RP (enum)
                            |  const_value  DOTDOT  const_value (range)
                            |  ID
        * array_type_decl   :  kARRAY  LB  simple_type_decl  RB  kOF  type_decl
    :param symbol_table:
    :param type_decl_node:
    :return: type(sys_type from [integer, real, char]) / array_type(Array Type instance) / None if not a valid type
    """
    if type_decl_node.type == 'sys_type':
        sys_type = type_decl_node.children[0]
        return sys_type
    elif type_decl_node.type == 'alias':
        # check whether the alias type exits
        alias_type = type_decl_node.children[0]
        ret_val = symbol_table.chain_look_up(alias_type)
        if not ret_val:
            SemanticLogger.error(type_decl_node.lineno, 'alias type: `{}` used before defined'.format(alias_type))
            return alias_type
            # raise Exception('alias type: `{}` used before defined'.format(alias_type))
        # return the true type
        if ret_val.type == 'sys_type':
            return ret_val.value['sys_type']
        else:  # array type
            return ret_val.value

    elif type_decl_node.type == 'array':
        index_type, element_type, left_val, right_val = parse_array_from_array_node(type_decl_node, symbol_table)
        return ArrayType(index_type, (left_val, right_val), element_type)

    elif type_decl_node.type == 'record':
        name_and_type_list = parse_record_node(type_decl_node, symbol_table)
        return RecordType(name_and_type_list)
    else:
        raise NotImplementedError('{}'.format(type_decl_node.type))


def parse_record_node(ast_node, symb_tab):
    name_and_type_list = parse_field_decl_list_node(ast_node.children[0], symb_tab)
    # 看看有无重复定义的 type
    return name_and_type_list


def parse_field_decl_list_node(ast_node, symb_tab):
    # SemanticLogger.info(None, ast_node.type)
    name_set = set()
    children = ast_node.children
    name_and_type_list = []
    if len(children) == 1:  # single field decl
        name_and_type_list = parse_field_decl_node(ast_node, symb_tab)
    else:
        ast_node._children = traverse_skew_tree(ast_node, 'field_decl')
        for child in ast_node.children:
            child_name_and_type_list = parse_field_decl_node(child, symb_tab)
            child_names = [item[0] for item in child_name_and_type_list]
            for child_name in child_names:
                if child_name in name_set:
                    SemanticLogger.error(child.lineno,
                                         '`{}` field is already declared'.format(child_name))
                else:
                    name_set.add(child_name)
            name_and_type_list.extend(child_name_and_type_list)
    return name_and_type_list


def parse_field_decl_node(ast_node, symb_tab):
    # SemanticLogger.info(None, ast_node.type)
    name_list_node, type_decl_node = ast_node.children
    flatten_name_list = parse_name_list(name_list_node)
    parsed_type = parse_type_decl_node(type_decl_node, symb_tab)
    parsed_type_list = [parsed_type] * len(flatten_name_list)
    return list(zip(flatten_name_list, parsed_type_list))


def parse_array_from_array_node(arr_node, symbol_table):
    """
    :param arr_node:
    :param symbol_table:
    :return: symb_tab_item to be inserted
    """
    assert arr_node.type == 'array', arr_node.type
    range_node, type_node = arr_node.children
    index_type, left_val, right_val = parse_range_from_range_node(range_node)
    element_type = parse_type_decl_node(type_node, symbol_table)
    return index_type, element_type, left_val, right_val


def parse_var_decl_from_node(var_decl_node, symbol_table):
    """
    parse var decl node,
    :param var_decl_node:
    :param symbol_table:
    :return: flatten name list and associated symb_tab_item
    """
    assert var_decl_node.type == 'var_decl', var_decl_node.type
    maybe_name_list_node, type_decl_node = var_decl_node.children

    flatten_name_list = parse_name_list(maybe_name_list_node)

    # get the var type
    assert type_decl_node.type in ['sys_type', 'array', 'alias'], type_decl_node.type
    if type_decl_node.type == 'sys_type':
        var_type, *_ = type_decl_node.children
        symb_tab_item = SymbolTableItem('var', {'var_type': var_type})
    elif type_decl_node.type == 'array':
        index_type, element_type, left_val, right_val = parse_array_from_array_node(type_decl_node, symbol_table)
        array_type = ArrayType(index_type, (left_val, right_val), element_type)
        symb_tab_item = SymbolTableItem('var',
                                        {'var_type': array_type})
    else:  # alias
        alias_type = type_decl_node.children[0]
        ret_val = symbol_table.chain_look_up(alias_type)
        if not ret_val:
            SemanticLogger.error(var_decl_node.lineno,
                                 'alias type: `{}` used before defined'.format(alias_type))
            symb_tab_item = None
        else:
            symb_tab_item = SymbolTableItem('var', {'var_type': ret_val.value})

    return flatten_name_list, symb_tab_item


def constant_folding(node, symbol_table):
    """
    一个整体逻辑是这样的
    如果返回值为 None, 证明这个节点不能完全的 const fold
    如果返回值不为 None, 那么这个节点可以完全的 const fold, caller 只需要让孩子变成这个值即可
    但是这个函数缺陷很大坑也很大，有机会要重新写一遍
    """
    return None

    # if not isinstance(node, Node):  # id (一般是 constant 的名字或者 function 的名字 / variable)
    #     id_ = node
    #     # 去 symbol table 查找, 这里需要 chain_lookup, 右值可存在于之前的 scope
    #     ret_val = symbol_table.chain_look_up(id_)
    #     if not ret_val:
    #         raise Exception('`{}` is not a function or a constant or variable'.format(id_))
    #     assert ret_val.type in ['const', 'var'], ret_val.type
    #     if ret_val.type == 'const':
    #         return ret_val.value['const_val']
    #     else:
    #         return None
    #
    # elif node.type == 'expression':  # bool const
    #     if len(node.children) == 1:
    #         val = constant_folding(node.children[0], symbol_table)
    #         # if val is not None:
    #         #     node._children = [val]
    #         return val
    #     else:
    #         left_val = constant_folding(node.children[0], symbol_table)
    #         right_val = constant_folding(node.children[2], symbol_table)
    #         if left_val is not None and right_val is not None:
    #             return bool_op_to_func[node.children[1]](left_val, right_val)
    #         else:
    #             return None
    #
    # elif node.type in ['integer', 'real', 'char', 'sys_con']:  # 直接的常数 1, 1.3, c, true
    #
    #     val = node.children[0]
    #     if node.type == 'sys_con':
    #         return bool_dict[val]
    #     else:
    #         return val
    # elif node.type == 'factor-arr':
    #
    #     arr_id, right_child = node.children
    #     # 需要进行 chain look up
    #     arr_id_lookup = symbol_table.chain_look_up(arr_id)
    #     if arr_id_lookup is None:
    #         raise Exception('{} used before declaration'.format(arr_id))
    #     right_val = constant_folding(right_child, symbol_table)
    #     if right_val is not None:
    #         node._children = (arr_id, right_val)
    #     return None  # return None, because the factor-arr is known to be non-const
    # elif node.type == 'factor-func':
    #     pass
    # elif node.type == 'factor':
    #     # kNOT factor
    #     # SUBSTRACT factor
    #     unary_op, right_child = node.children
    #     if unary_op == 'not':  # not true
    #         second_val = constant_folding(right_child, symbol_table)
    #         if second_val is not None:
    #             node._children = (unary_op, second_val)
    #             return not second_val
    #         else:
    #             return None
    #     elif unary_op == '-':
    #         second_val = constant_folding(right_child, symbol_table)
    #         if second_val is not None:
    #             node._children = (unary_op, second_val)
    #             return -second_val
    #         else:
    #             return None
    #     else:
    #         raise Exception('factor node with unknown unary op: {}'.format(unary_op))
    #
    # else:  # internal node, term  / expr
    #     node_type = node.type
    #
    #     arithmic_func = bin_op_to_func[type_to_bin_op[node_type]]
    #     children = node.children
    #     val_list = []
    #     can_const_fold = True
    #     new_children = []
    #
    #     for idx, child in enumerate(children):
    #         val = constant_folding(child, symbol_table)
    #         if val is None:
    #             can_const_fold = False
    #             new_children.append(child)
    #         else:
    #             val_list.append(val)
    #             new_children.append(val)
    #     node._children = tuple(new_children)
    #     if can_const_fold:
    #         return reduce(arithmic_func, val_list)
    #     else:
    #         return None


def parse_para_decl_list(ast_node, symb_tab_node):
    """
    需要建一个新的 symbol table
    :param node: ast node
    :param symbol_table_node: symb_tab node
    :return:
    """
    if ast_node.type == 'para_decl_list':
        # flatten
        ast_node._children = traverse_skew_tree(ast_node, ['val_para_type_list', 'var_para_type_list'])
        var_val_declare_list = []
        for child in ast_node.children:
            var_val_declare_list.append(parse_var_val_para_type_list(child, symb_tab_node))
        return var_val_declare_list
    else:  # 只有一个 para_decl 的情况
        return [parse_var_val_para_type_list(ast_node, symb_tab_node)]


def parse_var_val_para_type_list(ast_node, symb_tab_node):
    """
    需要在 symbtab 中插入这些 para declaration
    parse var_para_type_list|val_para_type_list
    :param ast_node:
    :param symb_tab_node:
    :return:
    """
    left_child, right_child = ast_node.children
    name_list = parse_name_list(left_child)
    type_ = parse_type_decl_node(right_child, symb_tab_node)
    for name in name_list:
        # TODO: 暂时把所有参数在新的 scope 下存成 var 型
        if symb_tab_node.lookup(name):
            SemanticLogger.error(left_child.lineno, "parameter `{}` is already defined".format(name))
            # raise Exception("parameter `{}` is already defined".format(name))
        else:
            symb_tab_item = SymbolTableItem('var', {'var_type': type_})
            symb_tab_node.insert(name, symb_tab_item)
    if ast_node.type == 'var_para_type_list':  # var_para_type_list

        return 'var', name_list, type_
    else:  # val_para_type_list
        return 'val', name_list, type_


# TODO: traverse_skew version
def parse_name_list(ast_node):
    """
    maybe name_list or just a str
    """
    if isinstance(ast_node, str):
        return [ast_node]

    elif ast_node.type == 'name_list':
        left_child, right_child = ast_node.children
        name_list = parse_name_list(left_child) + parse_name_list(right_child)
        return name_list

    else:
        raise NotImplementedError("{} is not supported when parsing name_list node".format(ast_node.type))


def parse_procedure_decl_node(ast_node, symb_tab_node):
    """
    parse procedure declaration
    """
    proc_head_node, routine_node = ast_node.children
    proc_id, para_decl_list_node = proc_head_node.children
    ret_val = symb_tab_node.lookup(proc_id)
    if ret_val is not None:  # 是否定义
        SemanticLogger.error(proc_head_node.lineno, 'procedure `{}` is already defined'.format(proc_id))
        # raise Exception('procedure `{}` is already defined'.format(proc_id))

    # parse para_decl_list

    new_symb_tab_node = SymbolTableNode(proc_id, None, None)
    make_parent_and_child(symb_tab_node, new_symb_tab_node)

    if para_decl_list_node:
        var_val_para_type_list = parse_para_decl_list(para_decl_list_node, new_symb_tab_node)
    else:
        var_val_para_type_list = []

    symb_tab_item = ProcedureItem(var_val_para_type_list)
    symb_tab_node.insert(proc_id, symb_tab_item)
    # parse routine_node

    parse_routine_node(routine_node, new_symb_tab_node)

    return proc_id, var_val_para_type_list


def parse_routine_head_node(ast_node, symb_tab_node):
    """
    routine_head : const_part type_part var_part routine_part
    routine_head 保证有四个孩子
    """
    const_part_node, type_part_node, var_part_node, routine_part_node = ast_node.children
    if const_part_node:
        parse_const_node(const_part_node, symb_tab_node)
    if type_part_node:
        parse_type_part_node(type_part_node, symb_tab_node)
    if var_part_node:
        parse_var_part_node(var_part_node, symb_tab_node)
    if routine_part_node:
        parse_routine_part_node(routine_part_node, symb_tab_node)


def parse_const_node(ast_node, symb_tab_node):
    """
    const declaration
    const_expr_list or const_expr
    """

    const_expr_node_list = []
    if ast_node.type == 'const_expr':
        const_expr_node_list.append(ast_node)
    else:
        # flatten the sub tree
        ast_node._children = traverse_skew_tree(ast_node, 'const_expr')
        const_expr_node_list.extend(ast_node.children)

    for child in const_expr_node_list:
        id_, const_val_node = child.children
        const_type = const_val_node.type
        const_val, *_ = const_val_node.children
        const_val = CONST_TYPE_TO_FUNC[const_type](const_val)
        symb_tab_item = SymbolTableItem('const', {'const_val': const_val, 'const_type': const_type})
        is_conflict, ret_val = symb_tab_node.insert(id_, symb_tab_item)
        if is_conflict:
            SemanticLogger.error(const_val_node.lineno,
                                 f'constant `{id_}` is already declared')
            # raise ConflictIDError(id_, ret_val)


def parse_type_part_node(ast_node, symb_tab_node):
    """
    type part declaration
    type_decl_list or type_definition
    """
    if ast_node.type == 'type_definition':
        type_definition_node_list = [ast_node]
    else:  # type_decl_list

        # flatten type definitions
        ast_node._children = traverse_skew_tree(ast_node, 'type_definition')
        type_definition_node_list = ast_node.children

    for child in type_definition_node_list:
        # parse type_definition
        type_, id_, *attributes = parse_type_definition_from_type_node(child, symb_tab_node)

        if type_ == 'alias':
            # check whether the alias type exist
            type_alias = attributes[0]
            ret_val = symb_tab_node.lookup(type_alias)
            if not ret_val:
                SemanticLogger.error(child.lineno, 'type alias: `{}` used before defined'.format(type_alias))
                # raise Exception('type alias: `{}` used before defined'.format(type_alias))
                symb_tab_item = None
            else:
                symb_tab_item = copy.deepcopy(ret_val)

        elif type_ == 'sys_type':
            sys_type = attributes[0]
            symb_tab_item = SymbolTableItem('sys_type', {'sys_type': sys_type})

        elif type_ == 'array':  # array type
            index_type, element_type, left_val, right_val = attributes
            array_type = ArrayType(index_type, (left_val, right_val), element_type)
            symb_tab_item = SymbolTableItem('arr_type',
                                            array_type)
        elif type_ == 'record':
            name_and_type_list, = attributes
            record_type = RecordType(name_and_type_list)
            symb_tab_item = SymbolTableItem('record_type', record_type)
        else:
            raise NotImplementedError

        # insert into symbol table
        if symb_tab_item is not None:
            is_conflict, ret_val = symb_tab_node.insert(id_, symb_tab_item)

            if is_conflict:
                SemanticLogger.error(child.lineno,
                                 f"type declare `{id_}` is duplicated")


def parse_var_part_node(ast_node, symb_tab_node):
    """
    var part declaration
    var_decl_list or var_decl
    """

    if ast_node.type == 'var_decl':
        flatten_name_list, symb_tab_item = parse_var_decl_from_node(ast_node, symb_tab_node)
        # insert (name, type) in symbol table
        for id_ in flatten_name_list:
            is_conflict, ret_val = symb_tab_node.insert(id_, symb_tab_item)
            if is_conflict:
                SemanticLogger.error(ast_node.lineno,
                        f'variable `{id_}` is already declared')
                # raise ConflictIDError(id_, symb_tab_item)
    else:
        # flatten var_decl

        ast_node._children = traverse_skew_tree(ast_node, 'var_decl')

        for child in ast_node.children:
            flatten_name_list, symb_tab_item = parse_var_decl_from_node(child, symb_tab_node)

            # insert (name, type) in symbol table
            for id_ in flatten_name_list:
                is_conflict, ret_val = symb_tab_node.insert(id_, symb_tab_item)
                if is_conflict:
                    SemanticLogger.error(child.lineno,
                                         f'variable `{id_}` is already declared')
                    # raise ConflictIDError(id_, symb_tab_item)


def parse_routine_part_node(ast_node, symb_tab_node):
    """
    parse routine part node
    return all (proc_id, var_val_para_type_list)
    一个 routine_part 里的 procedure 范围是同级的
    """
    # 如果只有一个 procedure, rountine_part 直接为一个 procedure_decl
    if ast_node.type == 'procedure_decl':
        parse_procedure_decl_node(ast_node, symb_tab_node)
    elif ast_node.type == 'function_decl':
        parse_func_decl_node(ast_node, symb_tab_node)
    elif ast_node.type == 'routine_part':
        flatten_proc_decl_nodes = traverse_skew_tree(ast_node, ['procedure_decl', 'function_decl'])
        ast_node._children = flatten_proc_decl_nodes
        for child in ast_node.children:
            if child.type == 'procedure_decl':
                parse_procedure_decl_node(child, symb_tab_node)
            else:  # function_decl
                parse_func_decl_node(child, symb_tab_node)


def parse_func_decl_node(ast_node, symb_tab_node):
    """
    function_decl : function_head  SEMICON  sub_routine  SEMICON
    """
    func_head_node, routine_node = ast_node.children
    func_id, para_decl_list_node, ret_type_decl_node = func_head_node.children
    func_ret_type = parse_type_decl_node(ret_type_decl_node, symb_tab_node)
    ret_val = symb_tab_node.lookup(func_id)
    if ret_val is not None:  # 是否定义
        SemanticLogger.error(ret_type_decl_node.lineno, 'function `{}` is already defined'.format(func_id))
        # raise Exception('procedure `{}` is already defined'.format(func_id))

    # parse para_decl_list

    new_symb_tab_node = SymbolTableNode(func_id, None, None)
    make_parent_and_child(symb_tab_node, new_symb_tab_node)

    # 插入 func id 作为一个 var
    ret_var_symb_tab_node = SymbolTableItem('var', {'var_type': func_ret_type})
    new_symb_tab_node.insert(func_id, ret_var_symb_tab_node)

    if para_decl_list_node:
        var_val_para_type_list = parse_para_decl_list(para_decl_list_node, new_symb_tab_node)
    else:
        var_val_para_type_list = []

    old_symb_tab_item = FunctionItem(var_val_para_type_list, func_ret_type)
    symb_tab_node.insert(func_id, old_symb_tab_item)

    # parse routine_node
    parse_routine_node(routine_node, new_symb_tab_node)

    return func_id, var_val_para_type_list


def parse_routine_node(ast_node, symb_tab_node):
    """
    routine : routine_head routine_body
    routine_body: compound_stmt : stmt_list
    routine_head 节点一定会存在
    routine_body 可能不存在
    """
    routine_head_node, routine_body_node = ast_node.children
    if routine_head_node:
        parse_routine_head_node(routine_head_node, symb_tab_node)
    if routine_body_node:
        parse_stmt_list_node(routine_body_node, symb_tab_node)


def parse_stmt_list_node(ast_node, symb_tab_node):
    """
    stmt_list : stmt_list stmt SEMICON | empty
    确保一定不为 None
    哪怕只有一个 stmt, 还是会有 stmt_list 作为一个父节点
    """
    flatten_stmt_node_list = traverse_skew_tree(ast_node, [
        'assign_stmt', 'assign_stmt-arr', 'assign_stmt-record',
        'proc_stmt', 'proc_stmt-simple',
        'if_stmt', 'repeat_stmt', 'while_stmt', 'for_stmt',
        'case_stmt'
    ])
    ast_node._children = flatten_stmt_node_list
    for child in ast_node.children:
        parse_stmt_node(child, symb_tab_node)


def parse_stmt_node(ast_node, symb_tab_node):
    """
    parse stmt node
    stmt :  INTEGER  COLON  non_label_stmt 这一情况的 node 叫 stmt-label
         |  non_label_stmt 这种情况的 node 直接叫 assgin 等
    """
    if ast_node.type == 'stmt-label':
        # TODO: add support for labeled statement
        raise NotImplementedError
    else:
        '''non_label_stmt :  assign_stmt 
                          | proc_stmt 
                          | compound_stmt 
                          | if_stmt 
                          | repeat_stmt 
                          | while_stmt 
                          | for_stmt 
                          | case_stmt 
                          | goto_stmt'''
        if ast_node.type.startswith('assign_stmt'):
            parse_assign_stmt_node(ast_node, symb_tab_node)
        elif ast_node.type.startswith('proc_stmt'):
            parse_proc_stmt_node(ast_node, symb_tab_node)
        elif ast_node.type == 'if_stmt':
            expression_node, stmt_node, else_clause_node = ast_node.children
            const_fold_ret,  const_fold_type = parse_expression_node(expression_node, symb_tab_node)
            parse_stmt_node(stmt_node, symb_tab_node)
            if else_clause_node is not None:
                parse_stmt_node(else_clause_node, symb_tab_node)
            if const_fold_ret is not None:
                ast_node._children = (bool(const_fold_ret), stmt_node, else_clause_node)
        elif ast_node.type == 'repeat_stmt':
            stmt_list_node, expression_node = ast_node.children
            parse_stmt_list_node(stmt_list_node, symb_tab_node)
            const_fold_ret,  const_fold_type = parse_expression_node(expression_node, symb_tab_node)
            if const_fold_ret is not None:
                ast_node._children = (stmt_list_node, bool(const_fold_ret))
        elif ast_node.type == 'while_stmt':
            expression_node, stmt_node = ast_node.children
            const_fold_ret,  const_fold_type = parse_expression_node(expression_node, symb_tab_node)
            parse_stmt_node(stmt_node, symb_tab_node)
            if const_fold_ret is not None:
                ast_node._children = (bool(const_fold_ret), stmt_node)
        elif ast_node.type == 'for_stmt':
            iterator, left_expression_node, direction_node, right_expression_node, stmt_node = ast_node.children
            ret_val = symb_tab_node.chain_look_up(iterator)
            if ret_val is None:
                SemanticLogger.error(iterator.lineno, f"var `{iterator}` used before declared")
                # raise Exception(f"var `{iterator}` used before declared")
            left_const_val, _ = parse_expression_node(left_expression_node, symb_tab_node)
            right_const_val, _ = parse_expression_node(right_expression_node, symb_tab_node)
            new_children = list(ast_node.children)
            if left_const_val is not None:
                new_children[1] = left_const_val
            if right_const_val is not None:
                new_children[3] = right_const_val
            ast_node._children = tuple(new_children)
        elif ast_node.type == 'case_stmt':
            expression_node, case_expr_list_node = ast_node.children
            const_fold_ret,  const_fold_type = parse_expression_node(expression_node, symb_tab_node)
            if const_fold_ret is not None:
                ast_node._children = (bool(const_fold_ret), case_expr_list_node)
        elif ast_node.type == 'stmt_list':
            parse_stmt_list_node(ast_node, symb_tab_node)
        else:
            # TODO: add goto support
            raise NotImplementedError(ast_node.type)


def parse_case_expr_list(ast_node, symb_tab_node):
    """
    case_expr_list :  case_expr_list  case_expr
                    |  case_expr
    """
    if ast_node.type == 'case_expr':
        parse_case_expr(ast_node, symb_tab_node)
    else:  # case_expr_list
        # traverse skew tree
        ast_node._children = traverse_skew_tree(ast_node, 'case_expr')
        for child in ast_node.children:
            parse_case_expr(child, symb_tab_node)


def parse_case_expr(ast_node, symb_tab_node):
    maybe_const_or_id, stmt_node = ast_node.children
    if not isinstance(maybe_const_or_id, Node):
        # id
        ret_val = symb_tab_node.chain_look_up(maybe_const_or_id)
        if ret_val is None:
            SemanticLogger.error(ast_node.lineno,
                                 '`{}` used before decalared in case statement'.format(maybe_const_or_id))
            # raise Exception('`{}` used before decalared in case statement')

    parse_stmt_node(stmt_node, symb_tab_node)


def parse_proc_stmt_node(ast_node, symb_tab_node):
    """
    pass proc_stmt
    proc_stmt :  ID             // proc_stmt-simple node
              |  SYS_PROC       // proc_stmt-simple node
              |  ID  LP  args_list  RP  // proc_stmt node
              |  SYS_PROC  LP  expression_list  RP
              |  kREAD  LP  factor  RP
    """
    if ast_node.type == 'proc_stmt-simple':
        proc_id_or_sys_func, = ast_node.children
        if proc_id_or_sys_func in SYS_PROC:  # sys proc
            pass
        else:
            # 检查该 procedure 是否定义过，chain look up
            ret_val = symb_tab_node.chain_look_up(proc_id_or_sys_func)
            if ret_val is None:
                SemanticLogger.error(ast_node.lineno, "procedure `{}` used before defined".format(proc_id_or_sys_func))
                # raise Exception("procedure `{}` used before defined".format(proc_id_or_sys_func))
            # 并且该 procedure 不接受任何参数，事实上 parse 直接替我们做了这件事情，所以不需要额外检查
    else:  # proc_stmt node
        proc_id, right_child = ast_node.children
        if proc_id == 'read':
            _ = parse_factor_node(right_child, symb_tab_node)
        elif proc_id in SYS_PROC:  # write/writeln
            parse_expression_list(right_child, symb_tab_node)
        else:  # user defind proc
            # proc_stmt: ID  LP  args_list  RP
            # 检查 proc_id 是否定义过, chain_look_up
            ret_val = symb_tab_node.chain_look_up(proc_id)
            if ret_val is None:
                SemanticLogger.error(right_child.lineno,
                                     "procedure `{}` used before declared".format(proc_id))
                # raise Exception("procedure `{}` used before declared".format(proc_id))
            else:
                # 检查变量个数是否合适
                # 用的变量是否定义过, 在 parse_args_list 中会自然调用 constant_folding, 会自动检查
                param_list = ret_val.para_list
                args_type_list = parse_args_list(right_child, symb_tab_node)
                # 检查变量个数是否合适
                if len(param_list) != len(args_type_list):
                    SemanticLogger.error(right_child.lineno,
                                         "procedure `{}` expect {} args, got {} args"
                                         .format(proc_id, len(param_list), len(args_type_list))
                                         )
                    # raise Exception("procedure `{}` expect {} args, got {} args"
                    #                 .format(proc_id, len(param_list), len(args_type_list)))
                # 检查变量类型是否合适
                for idx in range(len(param_list)):
                    _, arg_name, expect_type = param_list[idx]
                    given_type = args_type_list[idx]
                    if given_type != expect_type:
                        wrong_flag = False
                        if (expect_type != 'char' and given_type == 'char') or \
                                (isinstance(expect_type, dict) and expect_type != given_type):
                            wrong_flag = True
                        if wrong_flag:
                            SemanticLogger.error(right_child.lineno,
                                                 "procedure `{}` arg `{}` expect `{}` got `{}`"
                                                 .format(proc_id, arg_name, expect_type, given_type)
                                                 )

                            # raise Exception("procedure `{}` arg `{}` expect `{}` got `{}`"
                            #             .format(proc_id, arg_name, expect_type, given_type))
                        else:
                            SemanticLogger.warn(right_child.lineno,
                                                'procedure `{}` arg `{}` expect `{}` got `{}`'
                                  .format(proc_id, arg_name, expect_type, given_type))
                            # print('Warning, procedure `{}` arg `{}` expect `{}` got `{}`'
                            #       .format(proc_id, arg_name, expect_type, given_type))


def parse_args_list(ast_node, symb_tab_node):
    """
    args_list :  args_list  COMMA  expression
              |  expression
    :return number of args
    """
    if len(ast_node.children) == 2:
        # traverse skew tree
        ast_node._children = traverse_skew_tree(ast_node, 'expression')
        new_children = []
        args_type_list = []
        for child in ast_node.children:
            # fold constant
            const_fold_ret, const_fold_type = parse_expression_node(child, symb_tab_node)
            args_type_list.append(const_fold_type)
            if const_fold_ret is not None:
                new_children.append(const_fold_ret)
            else:
                new_children.append(child)
        ast_node._children = tuple(new_children)
        return args_type_list

    else:  # ast_node is an expression node
        const_fold_ret, const_fold_type = parse_expression_node(ast_node, symb_tab_node)
        return [const_fold_type]


def parse_assign_stmt_node(ast_node, symb_tab_node):

    """
    type checking and constant folding
    """

    children = ast_node.children
    if ast_node.type == 'assign_stmt':  # ID ASSIGN expression
        id_, expression_node = children
        ret_val = symb_tab_node.lookup(id_)
        if ret_val is None:
            SemanticLogger.error(ast_node.lineno, 'var {} assigned before declared'.format(id_))
            return
            # raise Exception('var {} assigned before declared'.format(id_))
        if ret_val.type == 'const':
            SemanticLogger.error(ast_node.lineno, 'const {} cannot be assigned!'.format(id_))
            return 
            # raise Exception('const {} cannot be assigned!'.format(id_))
        constant_fold_ret, constant_fold_type = parse_expression_node(expression_node, symb_tab_node)
        # 检查 type
        var_declare_type = ret_val.value['var_type']
        if constant_fold_type != var_declare_type:
            if var_declare_type == 'char':
                SemanticLogger.error(expression_node.lineno,
                                     "cannot cast `{}` type to char type in variable `{}`"
                                     .format(constant_fold_type, id_))
                # raise Exception("cannot cast `{}` type to char type in variable `{}`".format(constant_fold_type, id_))
        # 进行 type casting
        if constant_fold_ret is not None:
            new_constant_fold_ret = CONST_TYPE_TO_FUNC[var_declare_type](constant_fold_ret)
            if constant_fold_type != var_declare_type:
                SemanticLogger.warn(expression_node.lineno,
                                    "cast `{}` to `{}` for variable `{}`".format(constant_fold_ret, new_constant_fold_ret, id_))
            constant_fold_ret = new_constant_fold_ret
        if constant_fold_ret is not None:
            ast_node._children = (id_, constant_fold_ret)

    elif ast_node.type == 'assign_stmt-arr':  # ID LB expression RB ASSIGN expression
        id_, index_expression_node, expression_node = children
        ret_val = symb_tab_node.lookup(id_)
        if ret_val is None:
            SemanticLogger.error(ast_node.lineno, 'var {} assigned before declared'.format(id_))
            return
            # raise Exception('var {} assigned before declared'.format(id_))
        if ret_val.type == 'const':
            SemanticLogger.error(ast_node.lineno, 'const {} cannot be assigned!'.format(id_))
            return
            # raise Exception('const {} cannot be assigned!'.format(id_))
        constant_fold_ret, constant_fold_type = parse_expression_node(expression_node, symb_tab_node)
        index_fold_ret, index_fold_type = parse_expression_node(index_expression_node, symb_tab_node)

        var_type = ret_val.value['var_type']
        if not isinstance(var_type, ArrayType):
            SemanticLogger.error(ast_node.lineno,
                                 "`{}` is not an array variable".format(id_))
        else:

            # index type 可以直接进行检查
            if index_fold_type != var_type['index_type']:
                SemanticLogger.error(ast_node.lineno,
                                     'arr `{}` expect `{}` index, but got `{}`'.
                                     format(id_, var_type['index_type'], index_fold_type)
                                     )
                # raise Exception('arr `{}` expect `{}` index, but got `{}`'.
                #                 format(id_, var_type['index_type'], index_fold_type))
            # element type 可以直接进行检查
            if var_type['element_type'] != constant_fold_type:
                SemanticLogger.error(ast_node.lineno,
                                     'arr `{}` expect `{}` element but got `{}`'
                                     .format(id_, var_type['element_type'], constant_fold_type)
                                     )
                # raise Exception('arr `{}` expect `{}` element but got `{}`'
                #                 .format(id_, var_type['element_type'], constant_fold_type))
            # 如果 index_fold_ret 有效，可以进行范围检查
            if index_fold_ret is not None:
                left_range, right_range = var_type['index_range']
                if index_fold_ret < left_range or index_fold_ret > right_range:
                    SemanticLogger.error(index_expression_node.lineno,
                                         "arr `{}` has range `{}`, but got index {}"
                                         .format(id_, (left_range, right_range), index_fold_ret)
                                         )
                    # raise Exception("arr `{}` has range `{}`, but got index {}"
                    #                 .format(id_, (left_range, right_range), index_fold_ret))

            # 替换孩子
            ast_node._children = (id_, index_expression_node if index_fold_ret is None else index_fold_ret,
                                   expression_node if constant_fold_ret is None else constant_fold_ret)
    else:  # ID  DOT  ID  ASSIGN  expression assign_stmt-record
        record_var, record_field, expression_node = ast_node.children
        # 检查变量是否存在
        ret_val = symb_tab_node.chain_look_up(record_var)
        if ret_val is None:
            SemanticLogger.error(ast_node.lineno, '`{}` is not a record variable'.format(record_var))
        else:
            # 检查是否是 record 类型
            var_type = ret_val.value['var_type']
            if not isinstance(var_type, RecordType):
                SemanticLogger.error(ast_node.lineno, '`{}` is not a record variable'.format(record_var))
            else:
                # 检查 field 是否存在
                var_type_dict = var_type.to_dict()
                field_dtype = var_type_dict.get(record_field, None)
                if field_dtype is not None:
                    constant_fold_ret, constant_fold_type = parse_expression_node(expression_node, symb_tab_node)
                    if field_dtype == 'char' and constant_fold_type != 'char' or \
                        field_dtype != 'char' and constant_fold_type == 'char':
                        SemanticLogger.error(ast_node.lineno, 'cannot cast char type to `{}` type in field `{}`'
                                             .format(field_dtype, record_field))
                    else:
                        if constant_fold_ret is not None:  # 可以 const fold
                            const_fold_val = CONST_TYPE_TO_FUNC[constant_fold_type](constant_fold_ret)
                            ast_node._children = (record_var, record_field, const_fold_val)
                        else:  # 不能 const fold, 啥都不做
                            pass

                else:
                    SemanticLogger.error(ast_node.lineno, '`{}` is not a valid field for record variable `{}`'
                                         .format(record_field, ret_val))


def parse_expression_list(ast_node, symb_table):
    """
    expression_list :  expression_list  COMMA  expression
                    |  expression
    """
    if ast_node.type == 'expression':
        _ = parse_expression_node(ast_node, symb_table)
    else:
        ast_node._children = traverse_skew_tree(ast_node, 'expression')
        new_children = []
        for child in ast_node.children:
            const_fold_ret, const_fold_type = parse_expression_node(child, symb_table)
            if const_fold_ret is not None:
                new_children.append(const_fold_ret)
            else:
                new_children.append(child)
        ast_node._children = tuple(new_children)


def parse_expression_node(ast_node, symb_table):
    """
    parse expression node and constant folding&type checking at the same time
    expression :  expression  GE  expr
               |  expression  GT  expr
               |  expression  LE  expr
               |  expression  LT  expr
               |  expression  EQUAL  expr
               |  expression  UNEQUAL  expr
               |  expr

    """
    # 即便是 expr node, 也会建一个 expression 节点，也就是保证了 expression 节点一定出现
    children = ast_node.children
    if len(children) == 1:  # expr node
        return parse_expr_node(children[0], symb_table)

    else:
        # TODO traverse skew tree first
        # ast_node._chilren = traverse_skew_tree(ast_node, [
        #     'expr', 'term', ''
        # ])
        left_expression_child, bool_op, right_expr_child = ast_node.children
        new_chilren = [left_expression_child, bool_op, right_expr_child]
        expression_val, expression_type = parse_expression_node(left_expression_child, symb_table)
        expr_val, expr_type = parse_expr_node(right_expr_child, symb_table)
        # 依旧不支持 char, 这里要支持 char
        if (expression_type == 'char' and expr_type != 'char') or \
                (expr_type == 'char' and expression_type != 'char'):
            SemanticLogger.error(left_expression_child.lineno,
                                 "relation op `{}` is not supported betwwen `{}` and `{}`".
                                 format(bool_op, expression_type, expr_type))
            return None, 'real'
            # raise Exception("char value is not supported for relation op `{}`".format(bool_op))

        # 返回值的类型一定是 boolean
        ret_type = 'boolean'
        if expression_val is not None:
            new_chilren[0] = expression_val
        if expr_val is not None:
            new_chilren[2] = expr_val

        if expression_val is not None and expr_val is not None:
            bin_op_func = bin_op_to_func[bool_op]
            ret_val = bin_op_func(expression_val, expr_val)
        else:
            ret_val = None
        return ret_val, ret_type


def parse_expr_node(ast_node, symb_table):
    """
    parse expr node
    expr :  expr  ADD  term
         |  expr  SUBTRACT  term
         |  expr  kOR  term
         |  term
    前三种情况会建一个 expr node, 最后一种情况直接是 term node
    """
    if not isinstance(ast_node, Node):
        return parse_term_node(ast_node, symb_table)
    elif ast_node.type.startswith('expr') and ast_node.type != 'expression':  # expr node
        left_expr_child, right_term_child = ast_node.children
        expr_val, expr_type = parse_expr_node(left_expr_child, symb_table)
        term_val, term_type = parse_term_node(right_term_child, symb_table)

        node_op = type_to_bin_op[ast_node.type]
        new_children = []
        # 与 char 无瓜
        if expr_type == 'char' or term_type == 'char':
            SemanticLogger.error(left_expr_child.lineno,
                                 "char value is not supported for binary op: `{}`".format(node_op))
            return None, 'real'
            # raise Exception("char value is not supported for binary op: `{}`".format(node_op))

        # 判断节点返回值类型
        if ast_node.type == 'expr-OR':
            ret_val_type = 'boolean'
        else:
            # 只要有一个是 real 类型，结果就是 real 类型，不然就是 int 类型
            if term_type == 'real' or expr_val == 'real':
                ret_val_type = 'real'
            else:
                ret_val_type = 'integer'
                # 进行类型转化
        if expr_val is not None:  # not None, const-foldable
            new_children.append(expr_val)
        else:
            new_children.append(left_expr_child)
        if term_val is not None:
            new_children.append(term_val)
        else:
            new_children.append(right_term_child)

        # 如果可以 const fold, 进行计算
        if expr_val is not None and term_val is not None:
            bin_op_func = bin_op_to_func[node_op]
            ret_val = bin_op_func(expr_val, term_val)
            ret_val = CONST_TYPE_TO_FUNC[ret_val_type](ret_val)
        else:
            ret_val = None
        # 替换孩子
        ast_node._children = tuple(new_children)
        return ret_val, ret_val_type

    else:  # term node
        return parse_term_node(ast_node, symb_table)


def parse_term_node(ast_node, symb_table):
    """
    parse term node
    term :  term  MUL  factor
            |  term  kDIV factor
            |  term  DIV  factor
            |  term  kMOD  factor
            |  term  kAND  factor
            |  factor
    最后一种情况直接是 factor node
    """
    if not isinstance(ast_node, Node):
        return parse_factor_node(ast_node, symb_table)
    elif ast_node.type.startswith('term'):
        new_children = []
        left_term_child, right_factor_child = ast_node.children
        term_val, term_type = parse_term_node(left_term_child, symb_table)
        factor_val, factor_type = parse_factor_node(right_factor_child, symb_table)

        node_op = type_to_bin_op[ast_node.type]

        # 总之和 char 无瓜
        if term_type == 'char' or factor_type == 'char':
            SemanticLogger.error(left_term_child.lineno,
                                 'char value is not supported for binary op `{}`'.format(node_op))
            # raise Exception('char value is not supported for binary op `{}`'.format(node_op))

        # 以下的判断保证与 char 无瓜
        # 先把类型判断好
        if ast_node.type == 'term-AND':
            # 返回值一定是 sys_con 类型
            ret_val_type = 'boolean'
        elif ast_node.type == 'term-INTDIV' or ast_node.type == 'term-MOD':
            # 返回值一定是整数，且要求两个数字都是整数
            if term_type != 'integer' or factor_type != 'integer':
                SemanticLogger.error(left_term_child.lineno,
                                     "div and mod expect 2 integer, but got `{}` and `{}`"
                                     .format(term_type, factor_type))
                return None, 'integer'
                # raise Exception("div and mod expect 2 integer, but got `{}` and `{}`".format(term_type, factor_type))
            ret_val_type = 'integer'
        elif ast_node.type == 'term-DIV':
            ret_val_type = 'real'
        else:  # 返回值由两个 value 一起决定, MUL 乘法
            # 只要有一个是 real 类型，结果就是 real 类型，不然就是 int 类型

            if term_type == 'real' or factor_type == 'real':
                ret_val_type = 'real'
            else:
                ret_val_type = 'integer'

        # 进行类型转化
        if term_val is not None:  # not None, const-foldable
            new_children.append(term_val)
        else:
            new_children.append(left_term_child)
        if factor_val is not None:
            new_children.append(factor_val)
        else:
            new_children.append(right_factor_child)

        # 如果可以 const fold, 进行计算
        if factor_val is not None and term_val is not None:
            bin_op_func = bin_op_to_func[node_op]
            ret_val = bin_op_func(term_val, factor_val)
            ret_val = CONST_TYPE_TO_FUNC[ret_val_type](ret_val)
        else:
            ret_val = None
        # 替换孩子
        ast_node._children = tuple(new_children)
        return ret_val, ret_val_type

    else:  # factor node
        return parse_factor_node(ast_node, symb_table)


def parse_factor_node(ast_node, symb_table):
    """
    return None if not const-foldable
    factor  : ID  LP  args_list  RP
            | SYS_FUNCT  LP  args_list  RP   (factor-func node)
    factor  : ID  LB  expression  RB  (factor-arr node)
    factor :  ID  (str)
           |  SYS_FUNCT  (str)
           |  const_value  (const_value node)
           |  kNOT  factor  (factor node)
           |  SUBTRACT  factor  (factor node)
    factor : LP  expression  RP (expression node) 加了括号代表了优先级而已
    factor : ID  DOT  ID (factor-member node)
    """
    if not isinstance(ast_node, Node):  # ID / SYS_FUNCT
        if ast_node in SYS_FUNC:  # sys func
            raise NotImplementedError('sys func: {} is not supported currently'.format(SYS_FUNC))
        else:  # ID
            # must be const value or variable value
            ret_val = symb_table.chain_look_up(ast_node)
            if ret_val is None:
                SemanticLogger.error(None, "`{}` is not a const or variable or func".format(ast_node))
                # raise Exception("`{}` is not a const or variable or func".format(ast_node))
                return None, 'real'
            else:
                if ret_val.type == 'const':
                    const_val = ret_val.value['const_val']
                    const_type = ret_val.value['const_type']
                    return const_val, const_type
                else:  # variable
                    var_type = ret_val.value['var_type']
                    return None, var_type
    elif ast_node.type in CONST_VALUE_TYPE:  # const value / true / false / maxint
        const_val, = ast_node.children
        const_type = ast_node.type
        return const_val, const_type
        # return ConstantFoldItem(const_val, ast_node.type)
    elif ast_node.type.startswith('factor'):
        if ast_node.type == 'factor-arr':
            const_val, val_type = parse_factor_arr_node(ast_node, symb_table)
            return const_val, val_type
        elif ast_node.type == 'factor-func':
            return parse_factor_func_node(ast_node, symb_table)
        elif ast_node.type == 'factor':  # - factor / not factor
            unary_op, right_factor_child = ast_node.children
            const_val, val_type = parse_factor_node(right_factor_child, symb_table)
            if val_type == 'char':
                SemanticLogger.error(ast_node.lineno, 'char value `{}` is not supported for `-` op'.format(const_val))
                return None, 'integer'
            if const_val is not None:
                if unary_op == '-':
                    if val_type == 'boolean':
                        # const_val = ConstantFoldItem.eval_val_by_type(const_val, 'integer')
                        const_val = -const_val
                        val_type = 'integer'
                    else:  # integer / real
                        const_val = -const_val
                        # val type remains same
                else:  # not
                    if val_type != 'boolean':  # integer / real
                        val_type = 'boolean'
                        const_val = not const_val
                    else:
                        const_val = not const_val
                # 替换孩子
                ast_node._children = (const_val,)
            else:  # 只需要根据 unary op 来改变 val_type
                if unary_op == '-':
                    if val_type == 'boolean':
                        val_type = 'integer'
                        # val type remains same
                else:  # not
                    if val_type != 'boolean':  # integer / real
                        val_type = 'boolean'
            return const_val, val_type

        else:  # factor-member
            record_var, record_field = ast_node.children
            ret_val = symb_table.chain_look_up(record_var)
            record_type = ret_val.value['var_type']
            if not isinstance(record_type, RecordType):
                SemanticLogger.error(ast_node.lineno,
                                     '`{}` is not a record variable'.format(record_var))
                return None, 'real'
            else:
                # 检查 field
                record_type_dict = record_type.to_dict()
                field_dtype = record_type_dict.get(record_field, None)
                if field_dtype is None:
                    SemanticLogger.error(ast_node.lineno,
                                         "`{}` is not a field for variable `{}`".format(record_field, record_var))
                    return None, 'real'
                else:
                    return None, field_dtype
    else:  # LP expression RP 加了括号代表了优先级而已
        # 直接是一个 expression node
        return parse_expression_node(ast_node, symb_table)

# TODO: param val 归为 const
# TODO: var 归为 var


def parse_factor_func_node(ast_node, symb_tab_node):
    children = ast_node.children
    if len(children) == 1:  # factor-sys-func
        raise NotImplementedError
    else:  # factor-func
        id_or_sys_func, args_list_node = children
        if id_or_sys_func in SYS_FUNC:
            raise NotImplementedError
        else:
            # 检查函数是否定义过，参数是否给对（参数个数，参数类型）
            func_id = id_or_sys_func
            ret_val = symb_tab_node.chain_look_up(func_id)
            if ret_val is None or ret_val.type != 'function':
                SemanticLogger.error(ast_node.lineno, "func `{}` used before declared".format(func_id))
                return None, 'real'
                # raise Exception("func `{}` used before declared")
            # 检查变量个数是否合适
            # 用的变量是否定义过, 在 parse_args_list 中会自然调用 constant_folding, 会自动检查
            param_list = ret_val.para_list
            args_type_list = parse_args_list(args_list_node, symb_tab_node)
            # 检查变量个数是否合适
            if len(param_list) != len(args_type_list):
                SemanticLogger.error(args_list_node.lineno,
                                     "func `{}` expect {} args, got {} args"
                                     .format(func_id, len(param_list), len(args_type_list))
                                     )
                # raise Exception("func `{}` expect {} args, got {} args"
                #                 .format(func_id, len(param_list), len(args_type_list)))
            # 检查变量类型是否合适
            for idx in range(len(param_list)):
                _, arg_name, expect_type = param_list[idx]
                given_type = args_type_list[idx]
                if given_type != expect_type:
                    wrong_flag = False
                    if (expect_type != 'char' and given_type == 'char') or \
                            (isinstance(expect_type, dict) and expect_type != given_type):
                        wrong_flag = True
                    if wrong_flag:
                        SemanticLogger.error(args_list_node.lineno,
                                             "func `{}` arg `{}` expect `{}` got `{}`"
                                             .format(func_id, arg_name, expect_type, given_type)
                                             )
                        # raise Exception("func `{}` arg `{}` expect `{}` got `{}`"
                        #                 .format(func_id, arg_name, expect_type, given_type))
                    else:
                        SemanticLogger.warn(args_list_node.lineno,
                                             "func `{}` arg `{}` expect `{}` got `{}`"
                                             .format(func_id, arg_name, expect_type, given_type)
                                             )
                        # print('Warning, func `{}` arg `{}` expect `{}` got `{}`'
                        #       .format(func_id, arg_name, expect_type, given_type))
            return None, ret_val.ret_type


def parse_factor_arr_node(ast_node, symb_tab):
    """
    一定不可能 const fold, 直接返回 None
    parse factor-arr node
    factor  : ID  LB  expression  RB  (factor-arr node)
    """
    arr_id, index_expression_node = ast_node.children
    # arr_id 必须定义过
    ret_val = symb_tab.chain_look_up(arr_id)
    if ret_val is None:
        SemanticLogger.error(ast_node.lineno, 'array `{}` used before defined'.format(arr_id))
        return None, 'real'
    else:
        # parse index, 判断是否越界, 只有可以 const fold 的情况，才可以完全判断越界
        const_val, val_type = parse_expression_node(index_expression_node, symb_tab)
        arr_type = ret_val.value['var_type']
        if not isinstance(arr_type, ArrayType):
            SemanticLogger.error(ast_node.lineno, '`{}` is not an array'.format(arr_id))
            return None, 'real'
        else:
            if const_val is not None:  # 可以 const fold
                # 检查 index type 是否正确
                index_type = arr_type['index_type']
                if index_type != val_type:
                    SemanticLogger.error(index_expression_node.lineno,
                                         'illegal index `{}` for array `{}`'.format(const_val, arr_id))
                    # raise Exception('illegal index `{}` for array `{}`'.format(const_val, arr_id))
                # 检查是否越界
                left_range, right_range = arr_type['index_range']
                if const_val < left_range or const_val > right_range:
                    SemanticLogger.error(index_expression_node.lineno,
                                         'illegal index `{}` for array `{}` with index range: {}'
                                    .format(const_val, arr_id, (left_range, right_range)))
                    # raise Exception('illegal index `{}` for array `{}` with index range: {}'
                    #                 .format(const_val, arr_id, (left_range, right_range)))
                # 替换孩子
                ast_node._children = (arr_id, const_val)

                # 找到数组的类型
                arr_element_type = arr_type['element_type']
                return None, arr_element_type

            else:  # 不能 const fold
                # 什么都不做
                arr_element_type = arr_type['element_type']
                return None, arr_element_type


def graph(node, filename):
    edges = descend(node)
    g = pydot.graph_from_edges(edges)
    if filename:
        f = filename + ".png"
    else:
        f = "graph.png"
    g.write_png(f, prog='dot')


def descend(node):
    edges = []
    if node.__class__ != Node:
        return []

    for i in node.children:
        edges.append((s(node), s(i)))
        edges += descend(i)
    return edges


def s(node):
    if node.__class__ != Node:
        return "%s (%s)" % (node, random.uniform(0, 10))
    return "%s (%s)" % (node.type, id(node))


class ConstantFoldItem(object):
    """
    utility class for constant folding
    """
    _type_to_func = {'integer': int, 'real': float, 'sys_con': bool, 'char': str, 'boolean': bool}

    @staticmethod
    def eval_val_by_type(val, type):
        return ConstantFoldItem._type_to_func[type](val)