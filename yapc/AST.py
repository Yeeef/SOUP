import pydot
from ErrorHandler import *
from SymbolTable import *
import copy
from functools import reduce
from utils import *
import random


def traverse_skew_tree(node, stop_node_type=None):
    # TODO: find bug
    """
    遍历一种很特殊但是在我们的 parse tree 中频繁出现的一种结构（左递归导致的）
    能不能顺便做一个 compress ✅
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


class Node(object):

    def __init__(self, t, *args):
        self._type = t
        self._children = args

    @property
    def children(self):
        return self._children

    @property
    def type(self):
        return self._type

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
    # semantic error
    if left_type != right_type:
        raise Exception('left range type: `{}`, right range type: `{}`'.format(left_type, right_type))

    if left_type not in ['integer', 'char']:
        raise Exception('arr only supprt integer / char indices, not {}'.format(left_type))

    left_val, *_ = left_range_node.children
    right_val, *_ = right_range_node.children

    if left_val > right_val:
        raise Exception('left range val `{}` > right range val `{}`'.format(left_val, right_val))
    return left_type, left_val, right_val


def parse_type_definition_from_type_node(node, symbol_table):
    """
    parse type_definition node, only return information
    :param node:
    :return:
    """
    assert node.type == 'type_definition', node.type
    children = node.children
    assert len(children) == 2, children
    id_, type_node = children
    assert type_node.type in ['alias', 'sys_type', 'array']
    if type_node.type == 'alias':
        # most simple
        type_alias, *_ = type_node.children
        return 'alias', id_, type_alias
    elif type_node.type == 'sys_type':
        sys_type, *_ = type_node.children
        return 'sys_type', id_, sys_type
    else:
        # 1d array, compicated
        index_type, element_type, left_val, right_val = parse_array_from_array_node(type_node, symbol_table)
        return 'array', id_, index_type, element_type, left_val, right_val


def parse_type_decl_node(type_decl_node, symbol_table):
    """
    grammar rule:
        * type_decl         : simple_type_decl
                            | array_type_decl
        * simple_type_decl  :  SYS_TYPE
                            |  LP  name_list  RP (enum)
                            |  const_value  DOTDOT  const_value (range)
                            |  ID
        * array_type_decl   :  kARRAY  LB  simple_type_decl  RB  kOF  type_decl
    :param type_decl_node:
    :return: type(sys_type from [integer, real, char]) / array_type(Array Type instance)
    """
    if type_decl_node.type == 'sys_type':
        sys_type = type_decl_node.children[0]
        return sys_type
    elif type_decl_node.type == 'alias':
        # check whether the alias type exits
        alias_type = type_decl_node.children[0]
        ret_val = symbol_table.lookup(alias_type)
        if not ret_val:
            raise Exception('alias type: `{}` used before defined'.format(alias_type))
        # return the true type
        if ret_val.type == 'sys_type':
            return ret_val.value['sys_type']
        else:  # array type
            return ret_val.value

    elif type_decl_node.type == 'array':
        index_type, element_type, left_val, right_val = parse_array_from_array_node(type_decl_node, symbol_table)
        return ArrayType(index_type, (left_val, right_val), element_type)

    else:
        raise NotImplementedError('{}'.format(type_decl_node.type))


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

    flatten_name_list = parse_name_list(maybe_name_list_node, symbol_table)
    # get name_list
    # if isinstance(maybe_name_list_node, Node):
    #     # traverse name_list
    #     flatten_name_list = traverse_skew_tree(maybe_name_list_node)
    #     # flatten the subtree for future use
    #     maybe_name_list_node._children = flatten_name_list
    # else:
    #     # just a leaf node
    #     flatten_name_list = [maybe_name_list_node]

    # get the var type
    assert type_decl_node.type in ['sys_type', 'array', 'alias'], type_decl_node.type
    if type_decl_node.type == 'sys_type':
        var_type, *_ = type_decl_node.children
        symb_tab_item = SymbolTableItem('var', {'var_type': var_type})
    elif type_decl_node.type == 'array':
        index_type, element_type, left_val, right_val = parse_array_from_array_node(type_decl_node, symbol_table)
        array_type = ArrayType(index_type, (left_val, right_val), element_type)
        symb_tab_item = SymbolTableItem('arr_var',
                                        array_type)
    else:  # alias
        alias_type = type_decl_node.children[0]
        ret_val = symbol_table.lookup(alias_type)
        if not ret_val:
            raise Exception('alias type {} used before defined'.format(alias_type))
        else:
            symb_tab_item = ret_val

    return flatten_name_list, symb_tab_item


def constant_folding(node, symbol_table):
    global bin_op_to_func, type_to_bin_op, bool_dict

    if not isinstance(node, Node):  # id (一般是 constant 的名字或者 function 的名字 / variable)
        id_ = node
        # 去 symbol table 查找
        ret_val = symbol_table.lookup(id_)
        if not ret_val:
            raise Exception('{} is not a function or a constant'.format(id_))
        assert ret_val.type in ['const', 'var'], ret_val.type
        if ret_val.type == 'const':
            return ret_val.value
        else:
            return None

    elif node.type in ['integer', 'real', 'char', 'sys_con']:  # 直接的常数 1, 1.3, c, true

        val = node.children[0]
        if node.type == 'sys_con':
            return bool_dict[val]
        else:
            return val
    elif node.type == 'factor-arr':

        arr_id, right_child = node.children
        arr_id_lookup = symbol_table.lookup(arr_id)
        if arr_id_lookup is None:
            raise Exception('{} used before declaration'.format(arr_id))
        right_val = constant_folding(right_child, symbol_table)
        if right_val is not None:
            node._children = (arr_id, right_val)
        return None  # return None, because the factor-arr is known to be non-const
    elif node.type == 'factor-func':
        pass
    elif node.type == 'factor':
        # kNOT factor
        # SUBSTRACT factor
        unary_op, right_child = node.children
        if unary_op == 'not':  # not true
            second_val = constant_folding(right_child, symbol_table)
            if second_val is not None:
                node._children = (unary_op, second_val)
                return not second_val
            else:
                return None
        elif unary_op == '-':
            second_val = constant_folding(right_child, symbol_table)
            if second_val is not None:
                node._children = (unary_op, second_val)
                return -second_val
            else:
                return None
        else:
            raise Exception('factor node with unknown unary op: {}'.format(unary_op))

    else:  # internal node, term  / expr
        node_type = node.type

        arithmic_func = bin_op_to_func[type_to_bin_op[node_type]]
        children = node.children
        val_list = []
        can_const_fold = True
        new_children = []

        for idx, child in enumerate(children):
            val = constant_folding(child, symbol_table)
            if val is None:
                can_const_fold = False
                new_children.append(child)
            else:
                val_list.append(val)
                new_children.append(val)
        node._children = tuple(new_children)
        if can_const_fold:
            return reduce(arithmic_func, val_list)
        else:
            return None


def parse_para_decl_list(proc_id, ast_node, symb_tab_node):
    """
    需要建一个新的 symbol table
    :param node: ast node
    :param symbol_table_node: symb_tab node
    :return:
    """
    new_symb_tab_node = SymbolTableNode(proc_id, None, None)
    make_parent_and_child(symb_tab_node, new_symb_tab_node)
    if ast_node.type == 'para_decl_list':
        left_child, right_child = ast_node.children
        return [parse_var_val_para_type_list(left_child, new_symb_tab_node),
               parse_var_val_para_type_list(right_child, new_symb_tab_node)]
    else:  # 只有一个 para_decl 的情况
        return [parse_var_val_para_type_list(ast_node, new_symb_tab_node)]


def parse_var_val_para_type_list(ast_node, symb_tab_node):
    """
    需要在 symbtab 中插入这些 para declaration
    parse var_para_type_list|val_para_type_list
    :param ast_node:
    :param symb_tab_node:
    :return:
    """
    left_child, right_child = ast_node.children
    name_list = parse_name_list(left_child, symb_tab_node)
    type_ = parse_type_decl_node(right_child, symb_tab_node)
    for name in name_list:
        # TODO: 暂时把所有参数在新的 scope 下存成 var 型
        symb_tab_item = SymbolTableItem('var', {'var_type': type_})
        symb_tab_node.insert(name, symb_tab_item)
    if ast_node.type == 'var_para_type_list':  # var_para_type_list

        return 'var', name_list, type_
    else:  # val_para_type_list
        return 'val', name_list, type_


def parse_name_list(ast_node, symb_tab_node):
    """
    maybe name_list or just a str
    """
    if isinstance(ast_node, str):
        if symb_tab_node.lookup(ast_node) is not None:
            raise Exception('variable {} is already defined'.format(ast_node))
        return [ast_node]

    elif ast_node.type == 'name_list':
        left_child, right_child = ast_node.children
        name_list = parse_name_list(left_child, symb_tab_node) + parse_name_list(right_child, symb_tab_node)
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
    if ret_val is not None:
        raise Exception('procedure `{}` is already defined'.format(proc_id))

    # parse para_decl_list

    var_val_para_type_list = parse_para_decl_list(proc_id, para_decl_list_node, symb_tab_node)

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
        print(const_expr_node_list)

    for child in const_expr_node_list:
        id_, const_val_node = child.children
        const_val, *_ = const_val_node.children
        symb_tab_item = SymbolTableItem('const', {'const_val': const_val})
        is_conflict, ret_val = symb_tab_node.insert(id_, symb_tab_item)
        if is_conflict:
            raise ConflictIDError(id_, ret_val)


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
                raise Exception('type alias: `{}` used before defined'.format(type_alias))
            symb_tab_item = copy.deepcopy(ret_val)

        elif type_ == 'sys_type':
            sys_type = attributes[0]
            symb_tab_item = SymbolTableItem('sys_type', {'sys_type': sys_type})

        elif type_ == 'array':  # array type
            index_type, element_type, left_val, right_val = attributes
            array_type = ArrayType(index_type, (left_val, right_val), element_type)
            symb_tab_item = SymbolTableItem('arr_var',
                                            array_type)
        else:  # TODO: add record support
            raise NotImplementedError

        # insert into symbol table
        is_conflict, ret_val = symb_tab_node.insert(id_, symb_tab_item)

        if is_conflict:
            raise ConflictIDError(id_, symb_tab_item)


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
                raise ConflictIDError(id_, symb_tab_item)
    else:
        # flatten var_decl

        ast_node._children = traverse_skew_tree(ast_node, 'var_decl')

        for child in ast_node.children:
            flatten_name_list, symb_tab_item = parse_var_decl_from_node(child, symb_tab_node)

            # insert (name, type) in symbol table
            for id_ in flatten_name_list:
                is_conflict, ret_val = symb_tab_node.insert(id_, symb_tab_item)
                if is_conflict:
                    raise ConflictIDError(id_, symb_tab_item)


def parse_routine_part_node(ast_node, symb_tab_node):
    """
    parse routine part node
    return all (proc_id, var_val_para_type_list)
    一个 routine_part 里的 procedure 范围是同级的
    """
    proc_info_list = []
    # 如果只有一个 procedure, rountine_part 直接为一个 procedure_decl
    if ast_node.type == 'procedure_decl':
        proc_id, var_val_para_type_list = parse_procedure_decl_node(ast_node, symb_tab_node)
        proc_info_list.append((proc_id, var_val_para_type_list))
    elif ast_node.type == 'routine_part':
        flatten_proc_decl_nodes = traverse_skew_tree(ast_node, 'procedure_decl')
        ast_node._children = flatten_proc_decl_nodes
        proc_info_list = []
        for child in ast_node.children:
            proc_id, var_val_para_type_list = parse_procedure_decl_node(child, symb_tab_node)
            proc_info_list.append((proc_id, var_val_para_type_list))

    else:
        raise NotImplementedError

    for proc_id, var_val_para_type_list in proc_info_list:
        symb_tab_item = ProcedureItem(var_val_para_type_list, [])
        symb_tab_node.insert(proc_id, symb_tab_item)


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
    # TODO: make a flatten version
    flatten_stmt_node_list = traverse_skew_tree(ast_node, [
        'assign_stmt', 'assign_stmt-arr', 'assign_stmt-record',
        'proc_stmt', 'proc_stmt-simple',
        'if_stmt', 'repeat_stmt', 'while_stmt', 'for_stmt'
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
        else:
            raise NotImplementedError(ast_node.type)


def parse_assign_stmt_node(ast_node, symb_tab_node):

    """
    type checking and constant folding
    """

    children = ast_node.children
    if ast_node.type == 'assign_stmt':  # ID ASSIGN expression
        id_, expression_node = children
        ret_val = symb_tab_node.lookup(id_)
        if ret_val is None:
            raise Exception('var {} assigned before declared'.format(id_))
        if ret_val.type == 'const':
            raise Exception('const {} cannot be assigned!'.format(id_))

        constant_fold_ret = constant_folding(expression_node, symb_tab_node)
        if constant_fold_ret is not None:
            ast_node._children = (id_, constant_fold_ret)

    elif ast_node.type == 'assign_stmt-arr':  # ID LB expression RB ASSIGN expression
        id_, index_expression_node, expression_node = children
        ret_val = symb_tab_node.lookup(id_)
        if ret_val is None:
            raise Exception('var {} assigned before declared'.format(id_))
        if ret_val.type == 'const':
            raise Exception('const {} cannot be assigned!'.format(id_))
        constant_fold_ret = constant_folding(expression_node, symb_tab_node)
        index_fold_ret = constant_folding(index_expression_node, symb_tab_node)
        ast_node._children = (id_, index_expression_node if index_fold_ret is None else index_fold_ret,
                               expression_node if constant_fold_ret is None else constant_fold_ret)
    else:  # ID  DOT  ID  ASSIGN  expression
        raise NotImplementedError
        pass


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
