import jaclang.compiler.absyntree as ast
from _typeshed import Incomplete
from jaclang.compiler.absyntree import AstNode as AstNode
from jaclang.compiler.passes import Pass as Pass
from jaclang.settings import settings as settings

class JacFormatPass(Pass):
    comments: Incomplete
    indent_size: int
    indent_level: int
    MAX_LINE_LENGTH: Incomplete
    def before_pass(self) -> None: ...
    def enter_node(self, node: ast.AstNode) -> None: ...
    def token_before(self, node: ast.Token) -> ast.Token | None: ...
    def token_after(self, node: ast.Token) -> ast.Token | None: ...
    def indent_str(self) -> str: ...
    def emit(self, node: ast.AstNode, s: str, strip_mode: bool = True) -> None: ...
    def emit_ln(self, node: ast.AstNode, s: str) -> None: ...
    def comma_sep_node_list(self, node: ast.SubNodeList) -> str: ...
    def dot_sep_node_list(self, node: ast.SubNodeList) -> str: ...
    def nl_sep_node_list(self, node: ast.SubNodeList) -> str: ...
    def sep_node_list(self, node: ast.SubNodeList, delim: str = " ") -> str: ...
    def enter_module(self, node: ast.Module) -> None: ...
    def exit_module(self, node: ast.Module) -> None: ...
    def exit_global_vars(self, node: ast.GlobalVars) -> None: ...
    def exit_module_code(self, node: ast.ModuleCode) -> None: ...
    def exit_sub_node_list(self, node: ast.SubNodeList) -> None: ...
    def exit_sub_tag(self, node: ast.SubTag) -> None: ...
    def exit_func_call(self, node: ast.FuncCall) -> None: ...
    def exit_multi_string(self, node: ast.MultiString) -> None: ...
    def exit_module_path(self, node: ast.ModulePath) -> None: ...
    def exit_tuple_val(self, node: ast.TupleVal) -> None: ...
    def exit_special_var_ref(self, node: ast.SpecialVarRef) -> None: ...
    def exit_ability_def(self, node: ast.AbilityDef) -> None: ...
    def exit_event_signature(self, node: ast.EventSignature) -> None: ...
    def exit_import(self, node: ast.Import) -> None: ...
    def exit_arch_def(self, node: ast.ArchDef) -> None: ...
    def exit_ability(self, node: ast.Ability) -> None: ...
    def exit_func_signature(self, node: ast.FuncSignature) -> None: ...
    def exit_arch_has(self, node: ast.ArchHas) -> None: ...
    def exit_arch_ref(self, node: ast.ArchRef) -> None: ...
    def exit_param_var(self, node: ast.ParamVar) -> None: ...
    def exit_enum(self, node: ast.Enum) -> None: ...
    def exit_enum_def(self, node: ast.EnumDef) -> None: ...
    def exit_atom_trailer(self, node: ast.AtomTrailer) -> None: ...
    def exit_atom_unit(self, node: ast.AtomUnit) -> None: ...
    def exit_yield_expr(self, node: ast.YieldExpr) -> None: ...
    def is_line_break_needed(self, content: str, max_line_length: int = 0) -> bool: ...
    def exit_binary_expr(self, node: ast.BinaryExpr) -> None: ...
    def exit_compare_expr(self, node: ast.CompareExpr) -> None: ...
    def exit_has_var(self, node: ast.HasVar) -> None: ...
    def exit_if_stmt(self, node: ast.IfStmt) -> None: ...
    def exit_else_if(self, node: ast.ElseIf) -> None: ...
    def exit_disengage_stmt(self, node: ast.DisengageStmt) -> None: ...
    def exit_else_stmt(self, node: ast.ElseStmt) -> None: ...
    def exit_expr_stmt(self, node: ast.ExprStmt) -> None: ...
    def exit_iter_for_stmt(self, node: ast.IterForStmt) -> None: ...
    def exit_try_stmt(self, node: ast.TryStmt) -> None: ...
    def exit_except(self, node: ast.Except) -> None: ...
    def exit_finally_stmt(self, node: ast.FinallyStmt) -> None: ...
    def exit_while_stmt(self, node: ast.WhileStmt) -> None: ...
    def exit_with_stmt(self, node: ast.WithStmt) -> None: ...
    def exit_module_item(self, node: ast.ModuleItem) -> None: ...
    def exit_global_stmt(self, node: ast.GlobalStmt) -> None: ...
    def exit_non_local_stmt(self, node: ast.GlobalStmt) -> None: ...
    def handle_long_assignment(
        self, node: ast.Assignment, kid: ast.AstNode
    ) -> None: ...
    def handle_long_expression(self, node: ast.AstNode, kid: ast.AstNode) -> None: ...
    def exit_assignment(self, node: ast.Assignment) -> None: ...
    def exit_architype(self, node: ast.Architype) -> None: ...
    def exit_f_string(self, node: ast.FString) -> None: ...
    def exit_if_else_expr(self, node: ast.IfElseExpr) -> None: ...
    def decl_def_missing(self, decl: str = "this") -> None: ...
    def exit_bool_expr(self, node: ast.BoolExpr) -> None: ...
    def exit_lambda_expr(self, node: ast.LambdaExpr) -> None: ...
    def exit_unary_expr(self, node: ast.UnaryExpr) -> None: ...
    def exit_raise_stmt(self, node: ast.RaiseStmt) -> None: ...
    def exit_edge_ref_trailer(self, node: ast.EdgeRefTrailer) -> None: ...
    def exit_edge_op_ref(self, node: ast.EdgeOpRef) -> None: ...
    def exit_index_slice(self, node: ast.IndexSlice) -> None: ...
    def exit_list_val(self, node: ast.ListVal) -> None: ...
    def exit_set_val(self, node: ast.ListVal) -> None: ...
    def exit_dict_val(self, node: ast.DictVal) -> None: ...
    def exit_inner_compr(self, node: ast.InnerCompr) -> None: ...
    def exit_list_compr(self, node: ast.ListCompr) -> None: ...
    def exit_gen_compr(self, node: ast.GenCompr) -> None: ...
    def exit_set_compr(self, node: ast.SetCompr) -> None: ...
    def exit_dict_compr(self, node: ast.DictCompr) -> None: ...
    def exit_k_v_pair(self, node: ast.KVPair) -> None: ...
    def exit_k_w_pair(self, node: ast.KWPair) -> None: ...
    def exit_disconnect_op(self, node: ast.DisconnectOp) -> None: ...
    def exit_connect_op(self, node: ast.ConnectOp) -> None: ...
    def exit_filter_compr(self, node: ast.FilterCompr) -> None: ...
    def exit_assign_compr(self, node: ast.AssignCompr) -> None: ...
    def exit_await_expr(self, node: ast.AwaitExpr) -> None: ...
    def exit_revisit_stmt(self, node: ast.RevisitStmt) -> None: ...
    def exit_visit_stmt(self, node: ast.VisitStmt) -> None: ...
    def exit_ignore_stmt(self, node: ast.IgnoreStmt) -> None: ...
    def exit_return_stmt(self, node: ast.ReturnStmt) -> None: ...
    def exit_assert_stmt(self, node: ast.AssertStmt) -> None: ...
    def exit_check_stmt(self, node: ast.CheckStmt) -> None: ...
    def exit_ctrl_stmt(self, node: ast.CtrlStmt) -> None: ...
    def exit_delete_stmt(self, node: ast.DeleteStmt) -> None: ...
    def exit_report_stmt(self, node: ast.ReportStmt) -> None: ...
    def exit_expr_as_item(self, node: ast.ExprAsItem) -> None: ...
    def exit_in_for_stmt(self, node: ast.InForStmt) -> None: ...
    def exit_test(self, node: ast.Test) -> None: ...
    def exit_py_inline_code(self, node: ast.PyInlineCode) -> None: ...
    def exit_arch_ref_chain(self, node: ast.ArchRefChain) -> None: ...
    def exit_typed_ctx_block(self, node: ast.TypedCtxBlock) -> None: ...
    def exit_match_stmt(self, node: ast.MatchStmt) -> None: ...
    def exit_match_case(self, node: ast.MatchCase) -> None: ...
    def exit_match_or(self, node: ast.MatchOr) -> None: ...
    def exit_match_as(self, node: ast.MatchAs) -> None: ...
    def exit_match_wild(self, node: ast.MatchWild) -> None: ...
    def exit_match_value(self, node: ast.MatchValue) -> None: ...
    def exit_match_singleton(self, node: ast.MatchSingleton) -> None: ...
    def exit_match_sequence(self, node: ast.MatchSequence) -> None: ...
    def exit_match_mapping(self, node: ast.MatchMapping) -> None: ...
    def exit_match_k_v_pair(self, node: ast.MatchKVPair) -> None: ...
    def exit_match_star(self, node: ast.MatchStar) -> None: ...
    def exit_match_arch(self, node: ast.MatchArch) -> None: ...
    def exit_token(self, node: ast.Token) -> None: ...
    def exit_name(self, node: ast.Name) -> None: ...
    def enter_float(self, node: ast.Float) -> None: ...
    def enter_int(self, node: ast.Int) -> None: ...
    def enter_string(self, node: ast.String) -> None: ...
    def enter_bool(self, node: ast.Bool) -> None: ...
    def exit_builtin_type(self, node: ast.BuiltinType) -> None: ...
    def exit_null(self, node: ast.Null) -> None: ...
    def exit_ellipsis(self, node: ast.Ellipsis) -> None: ...
    def exit_semi(self, node: ast.Semi) -> None: ...
    def exit_comment_token(self, node: ast.CommentToken) -> None: ...