
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftADDSUBTRACTleftMULDIVkDIVkMODADD ASSIGN CHAR COLON COMMA DIV DOT DOUBLEDOT EQUAL GE GT ID INTEGER LB LE LP LT MOD MUL RB REAL RP SEMICON STRING SUBTRACT SYS_CON SYS_FUNCT SYS_PROC SYS_TYPE UNEQUAL kAND kARRAY kBEGIN kCASE kCONST kDIV kDO kDOWNTO kELSE kEND kFOR kFUNCTION kGOTO kIF kIN kLABEL kMOD kNOT kOF kOR kPACKED kPROCEDURE kPROGRAM kREAD kRECORD kREPEAT kSET kTHEN kTO kTYPE kUNTIL kVAR kWHILE kWITHprogram :  program_head  routine  DOTprogram_head : kPROGRAM ID SEMICONroutine : routine_head routine_bodyroutine_head : const_part type_part var_part routine_partconst_part : kCONST const_expr_list\n                  | emptyconst_expr_list :  const_expr_list  const_expr\n                    |  const_exprconst_expr : ID EQUAL const_value SEMICONconst_value : INTEGERconst_value : REALconst_value : CHARconst_value : STRINGconst_value : SYS_CONtype_part : kTYPE type_decl_list\n                             | emptytype_decl_list :  type_decl_list  type_definition  \n                    |  type_definitiontype_definition :  ID  EQUAL  type_decl  SEMICONtype_decl :  simple_type_decl  \n                    |  array_type_decl  \n                    |  record_type_declsimple_type_decl : SYS_TYPEsimple_type_decl : LP name_list RPsimple_type_decl : const_value DOUBLEDOT const_valuesimple_type_decl : IDarray_type_decl :  kARRAY  LB  simple_type_decl  RB  kOF  type_declrecord_type_decl :  kRECORD  field_decl_list  kENDfield_decl_list :  field_decl_list  field_decl  \n                    |  field_declfield_decl :  name_list  COLON  type_decl  SEMICONname_list :  name_list  COMMA  ID  \n                    |  IDvar_part :  kVAR  var_decl_list  \n                    |  emptyvar_decl_list :  var_decl_list  var_decl  \n                    |  var_declvar_decl :  name_list  COLON  type_decl  SEMICONroutine_part :  routine_part  function_decl  \n                    |  routine_part  procedure_decl\n                    |  function_decl  \n                    |  procedure_decl  \n                    | emptysub_routine : routinefunction_decl : function_head  SEMICON  sub_routine  SEMICONfunction_head :  kFUNCTION  ID  parameters  COLON  simple_type_decl procedure_decl :  procedure_head  SEMICON  sub_routine  SEMICONprocedure_head :  kPROCEDURE ID parameters parameters :  LP  para_decl_list  RP  \n                    |  emptypara_decl_list :  para_decl_list  SEMICON  para_type_list \n                    | para_type_listpara_type_list :  var_para_list COLON  simple_type_declvar_para_list :  kVAR  name_listval_para_list :  name_listroutine_body :  compound_stmtcompound_stmt :  kBEGIN  stmt_list  kENDstmt_list :  stmt_list  stmt  SEMICON  \n                    |  emptystmt :  INTEGER  COLON  non_label_stmt  \n                    |  non_label_stmtnon_label_stmt :  assign_stmt \n                    | proc_stmt \n                    | compound_stmt \n                    | if_stmt \n                    | repeat_stmt \n                    | while_stmt \n                    | for_stmt \n                    | case_stmt \n                    | goto_stmtassign_stmt :  ID  ASSIGN  expression\n                    | ID LB expression RB ASSIGN expression\n                    | ID  DOT  ID  ASSIGN  expressionproc_stmt :  ID\n                    |  ID  LP  args_list  RP\n                    |  SYS_PROC\n                    |  SYS_PROC  LP  expression_list  RP\n                    |  kREAD  LP  factor  RPif_stmt :  kIF  expression  kTHEN  stmt  else_clauseelse_clause :  kELSE stmt \n                    |  emptyrepeat_stmt :  kREPEAT  stmt_list  kUNTIL  expressionwhile_stmt :  kWHILE  expression  kDO stmtfor_stmt :  kFOR  ID  ASSIGN  expression  direction  expression  kDO stmtdirection :  kTO \n                    | kDOWNTOcase_stmt : kCASE expression kOF case_expr_list kENDcase_expr_list :  case_expr_list  case_expr  \n                    |  case_exprcase_expr :  const_value  COLON  stmt  SEMICON\n                    |  ID  COLON  stmt  SEMICONgoto_stmt :  kGOTO  INTEGERexpression_list :  expression_list  COMMA  expression\n                    |  expressionexpression :  expression  GE  expr  \n                    |  expression  GT  expr  \n                    |  expression  LE  expr\n                    |  expression  LT  expr  \n                    |  expression  EQUAL  expr  \n                    |  expression  UNEQUAL  expr  \n                    |  exprexpr :  expr  ADD  term  \n                    |  expr  SUBTRACT  term  \n                    |  expr  kOR  term  \n                    |  termterm :  term  MUL  factor  \n                    |  term  DIV  factor  \n                    |  term  MOD  factor \n                    |  term  kAND  factor  \n                    |  factorfactor :  ID  \n                    |  ID  LP  args_list  RP  \n                    |  SYS_FUNCT  \n                    |  SYS_FUNCT  LP  args_list  RP  \n                    |  const_value  \n                    |  kNOT  factor\n                    |  SUBTRACT  factor  \n                    |  ID  LB  expression  RBfactor : LP  expression  RPfactor : ID  DOT  IDargs_list :  args_list  COMMA  expression  \n            |  expressionempty :'
    
_lr_action_items = {'kPROGRAM':([0,],[3,]),'$end':([1,10,],[0,-1,]),'kCONST':([2,20,98,99,],[7,-2,7,7,]),'kTYPE':([2,6,8,17,18,20,29,98,99,115,],[-123,15,-6,-5,-8,-2,-7,-123,-123,-9,]),'kVAR':([2,6,8,14,16,17,18,20,26,27,29,65,98,99,115,154,159,232,],[-123,-123,-6,24,-16,-5,-8,-2,-15,-18,-7,-17,-123,-123,-9,205,-19,205,]),'kFUNCTION':([2,6,8,14,16,17,18,20,23,25,26,27,29,53,54,55,56,61,62,65,96,97,98,99,102,115,159,199,200,206,],[-123,-123,-6,-123,-16,-5,-8,-2,59,-35,-15,-18,-7,59,-41,-42,-43,-34,-37,-17,-39,-40,-123,-123,-36,-9,-19,-45,-47,-38,]),'kPROCEDURE':([2,6,8,14,16,17,18,20,23,25,26,27,29,53,54,55,56,61,62,65,96,97,98,99,102,115,159,199,200,206,],[-123,-123,-6,-123,-16,-5,-8,-2,60,-35,-15,-18,-7,60,-41,-42,-43,-34,-37,-17,-39,-40,-123,-123,-36,-9,-19,-45,-47,-38,]),'kBEGIN':([2,5,6,8,13,14,16,17,18,20,21,22,23,25,26,27,29,48,53,54,55,56,61,62,65,73,74,91,96,97,98,99,102,115,125,147,159,199,200,206,218,228,229,246,],[-123,13,-123,-6,-123,-123,-16,-5,-8,-2,13,-59,-123,-35,-15,-18,-7,-123,-4,-41,-42,-43,-34,-37,-17,-58,13,13,-39,-40,-123,-123,-36,-9,13,13,-19,-45,-47,-38,13,13,13,13,]),'ID':([3,7,13,15,17,18,21,22,24,26,27,29,47,48,49,50,51,59,60,61,62,65,66,73,74,75,76,77,78,79,80,84,87,90,91,102,103,104,111,114,115,125,126,127,128,129,130,131,132,133,134,135,136,137,138,140,141,142,144,146,147,148,149,159,162,163,164,167,169,171,195,196,201,205,206,211,212,213,218,223,224,225,227,228,229,233,244,245,246,247,248,],[9,19,-123,28,19,-8,44,-59,64,28,-18,-7,86,-123,86,93,86,100,101,64,-37,-17,105,-58,44,86,86,119,86,86,86,86,86,86,44,-36,105,158,64,64,-9,44,86,86,86,86,86,86,86,86,86,86,86,86,86,86,86,189,86,86,44,86,198,-19,105,64,-30,86,86,86,198,-89,105,64,-38,-29,105,86,44,86,-85,-86,-88,44,44,105,105,-31,44,-90,-91,]),'DOT':([4,11,12,31,44,86,],[10,-3,-56,-57,77,142,]),'SEMICON':([9,11,12,31,32,34,35,36,37,38,39,40,41,42,43,44,45,57,58,67,68,69,70,71,72,82,83,85,86,88,89,95,101,105,106,107,108,109,110,116,117,139,145,150,151,152,155,156,157,168,170,172,173,174,175,176,177,178,179,180,181,182,183,184,185,186,189,190,192,193,202,203,207,208,210,214,217,219,220,221,222,226,230,231,236,237,238,240,241,242,243,249,250,],[20,-3,-56,-57,73,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,-74,-76,98,99,115,-10,-11,-12,-13,-14,-101,-105,-110,-111,-113,-115,-92,-123,-26,159,-20,-21,-22,-23,-60,-71,-117,-116,199,-44,200,-50,-48,206,-75,-77,-78,-123,-95,-96,-97,-98,-99,-100,-102,-103,-104,-106,-107,-108,-109,-120,-119,-82,-83,232,-52,-24,-25,-28,-73,-79,-81,-112,-118,-114,-87,-46,-49,245,-72,-80,247,248,-51,-53,-27,-84,]),'kEND':([13,21,22,73,163,164,195,196,211,227,245,247,248,],[-123,31,-59,-58,210,-30,226,-89,-29,-88,-31,-90,-91,]),'INTEGER':([13,21,22,30,47,48,49,51,52,66,73,75,76,78,79,80,84,87,90,91,103,125,126,127,128,129,130,131,132,133,134,135,136,137,138,140,141,144,146,147,148,149,161,162,167,169,171,195,196,201,212,213,218,223,224,225,227,228,229,233,244,246,247,248,],[-123,33,-59,68,68,-123,68,68,95,68,-58,68,68,68,68,68,68,68,68,33,68,33,68,68,68,68,68,68,68,68,68,68,68,68,68,68,68,68,68,33,68,68,68,68,68,68,68,68,-89,68,68,68,33,68,-85,-86,-88,33,33,68,68,33,-90,-91,]),'SYS_PROC':([13,21,22,48,73,74,91,125,147,218,228,229,246,],[-123,45,-59,-123,-58,45,45,45,45,45,45,45,45,]),'kREAD':([13,21,22,48,73,74,91,125,147,218,228,229,246,],[-123,46,-59,-123,-58,46,46,46,46,46,46,46,46,]),'kIF':([13,21,22,48,73,74,91,125,147,218,228,229,246,],[-123,47,-59,-123,-58,47,47,47,47,47,47,47,47,]),'kREPEAT':([13,21,22,48,73,74,91,125,147,218,228,229,246,],[-123,48,-59,-123,-58,48,48,48,48,48,48,48,48,]),'kWHILE':([13,21,22,48,73,74,91,125,147,218,228,229,246,],[-123,49,-59,-123,-58,49,49,49,49,49,49,49,49,]),'kFOR':([13,21,22,48,73,74,91,125,147,218,228,229,246,],[-123,50,-59,-123,-58,50,50,50,50,50,50,50,50,]),'kCASE':([13,21,22,48,73,74,91,125,147,218,228,229,246,],[-123,51,-59,-123,-58,51,51,51,51,51,51,51,51,]),'kGOTO':([13,21,22,48,73,74,91,125,147,218,228,229,246,],[-123,52,-59,-123,-58,52,52,52,52,52,52,52,52,]),'EQUAL':([19,28,68,69,70,71,72,81,82,83,85,86,88,89,92,94,117,118,121,123,139,143,145,174,175,176,177,178,179,180,181,182,183,184,185,186,188,189,190,192,194,214,215,216,220,221,222,237,239,],[30,66,-10,-11,-12,-13,-14,130,-101,-105,-110,-111,-113,-115,130,130,130,130,130,130,-117,130,-116,-95,-96,-97,-98,-99,-100,-102,-103,-104,-106,-107,-108,-109,130,-120,-119,130,130,130,130,130,-112,-118,-114,130,130,]),'kUNTIL':([22,48,73,91,],[-59,-123,-58,146,]),'REAL':([30,47,49,51,66,75,76,78,79,80,84,87,90,103,126,127,128,129,130,131,132,133,134,135,136,137,138,140,141,144,146,148,149,161,162,167,169,171,195,196,201,212,213,223,224,225,227,233,244,247,248,],[69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,-89,69,69,69,69,-85,-86,-88,69,69,-90,-91,]),'CHAR':([30,47,49,51,66,75,76,78,79,80,84,87,90,103,126,127,128,129,130,131,132,133,134,135,136,137,138,140,141,144,146,148,149,161,162,167,169,171,195,196,201,212,213,223,224,225,227,233,244,247,248,],[70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,-89,70,70,70,70,-85,-86,-88,70,70,-90,-91,]),'STRING':([30,47,49,51,66,75,76,78,79,80,84,87,90,103,126,127,128,129,130,131,132,133,134,135,136,137,138,140,141,144,146,148,149,161,162,167,169,171,195,196,201,212,213,223,224,225,227,233,244,247,248,],[71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,-89,71,71,71,71,-85,-86,-88,71,71,-90,-91,]),'SYS_CON':([30,47,49,51,66,75,76,78,79,80,84,87,90,103,126,127,128,129,130,131,132,133,134,135,136,137,138,140,141,144,146,148,149,161,162,167,169,171,195,196,201,212,213,223,224,225,227,233,244,247,248,],[72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,-89,72,72,72,72,-85,-86,-88,72,72,-90,-91,]),'kELSE':([31,34,35,36,37,38,39,40,41,42,43,44,45,68,69,70,71,72,82,83,85,86,88,89,95,116,117,139,145,168,170,172,173,174,175,176,177,178,179,180,181,182,183,184,185,186,189,190,192,193,214,217,219,220,221,222,226,237,238,250,],[-57,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,-74,-76,-10,-11,-12,-13,-14,-101,-105,-110,-111,-113,-115,-92,-60,-71,-117,-116,-75,-77,-78,218,-95,-96,-97,-98,-99,-100,-102,-103,-104,-106,-107,-108,-109,-120,-119,-82,-83,-73,-79,-81,-112,-118,-114,-87,-72,-80,-84,]),'COLON':([33,63,64,68,69,70,71,72,100,153,155,158,165,197,198,204,231,234,],[74,103,-33,-10,-11,-12,-13,-14,-123,201,-50,-32,212,228,229,233,-49,-54,]),'ASSIGN':([44,93,119,166,],[75,148,167,213,]),'LB':([44,86,113,],[76,141,162,]),'LP':([44,45,46,47,49,51,66,75,76,78,79,80,84,86,87,88,90,100,101,103,126,127,128,129,130,131,132,133,134,135,136,137,138,140,141,144,146,148,162,167,169,171,201,212,213,223,224,225,233,244,],[78,79,80,87,87,87,111,87,87,87,87,87,87,140,87,144,87,154,154,111,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,111,87,87,87,111,111,87,87,-85,-86,111,111,]),'SYS_FUNCT':([47,49,51,75,76,78,79,80,84,87,90,126,127,128,129,130,131,132,133,134,135,136,137,138,140,141,144,146,148,167,169,171,213,223,224,225,],[88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,-85,-86,]),'kNOT':([47,49,51,75,76,78,79,80,84,87,90,126,127,128,129,130,131,132,133,134,135,136,137,138,140,141,144,146,148,167,169,171,213,223,224,225,],[90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,-85,-86,]),'SUBTRACT':([47,49,51,68,69,70,71,72,75,76,78,79,80,82,83,84,85,86,87,88,89,90,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,144,145,146,148,167,169,171,174,175,176,177,178,179,180,181,182,183,184,185,186,189,190,213,220,221,222,223,224,225,],[84,84,84,-10,-11,-12,-13,-14,84,84,84,84,84,133,-105,84,-110,-111,84,-113,-115,84,84,84,84,84,84,84,84,84,84,84,84,84,84,-117,84,84,84,-116,84,84,84,84,84,133,133,133,133,133,133,-102,-103,-104,-106,-107,-108,-109,-120,-119,84,-112,-118,-114,84,-85,-86,]),'COMMA':([63,64,68,69,70,71,72,82,83,85,86,88,89,120,121,122,123,139,145,158,160,165,174,175,176,177,178,179,180,181,182,183,184,185,186,187,189,190,191,215,216,220,221,222,234,],[104,-33,-10,-11,-12,-13,-14,-101,-105,-110,-111,-113,-115,169,-122,171,-94,-117,-116,-32,104,104,-95,-96,-97,-98,-99,-100,-102,-103,-104,-106,-107,-108,-109,169,-120,-119,169,-121,-93,-112,-118,-114,104,]),'RP':([64,68,69,70,71,72,82,83,85,86,88,89,105,110,120,121,122,123,124,139,143,145,158,160,174,175,176,177,178,179,180,181,182,183,184,185,186,187,189,190,191,202,203,207,208,215,216,220,221,222,242,243,],[-33,-10,-11,-12,-13,-14,-101,-105,-110,-111,-113,-115,-26,-23,168,-122,170,-94,172,-117,190,-116,-32,207,-95,-96,-97,-98,-99,-100,-102,-103,-104,-106,-107,-108,-109,220,-120,-119,222,231,-52,-24,-25,-121,-93,-112,-118,-114,-51,-53,]),'SYS_TYPE':([66,103,162,201,212,233,244,],[110,110,110,110,110,110,110,]),'kARRAY':([66,103,212,244,],[113,113,113,113,]),'kRECORD':([66,103,212,244,],[114,114,114,114,]),'MUL':([68,69,70,71,72,83,85,86,88,89,139,145,180,181,182,183,184,185,186,189,190,220,221,222,],[-10,-11,-12,-13,-14,135,-110,-111,-113,-115,-117,-116,135,135,135,-106,-107,-108,-109,-120,-119,-112,-118,-114,]),'DIV':([68,69,70,71,72,83,85,86,88,89,139,145,180,181,182,183,184,185,186,189,190,220,221,222,],[-10,-11,-12,-13,-14,136,-110,-111,-113,-115,-117,-116,136,136,136,-106,-107,-108,-109,-120,-119,-112,-118,-114,]),'MOD':([68,69,70,71,72,83,85,86,88,89,139,145,180,181,182,183,184,185,186,189,190,220,221,222,],[-10,-11,-12,-13,-14,137,-110,-111,-113,-115,-117,-116,137,137,137,-106,-107,-108,-109,-120,-119,-112,-118,-114,]),'kAND':([68,69,70,71,72,83,85,86,88,89,139,145,180,181,182,183,184,185,186,189,190,220,221,222,],[-10,-11,-12,-13,-14,138,-110,-111,-113,-115,-117,-116,138,138,138,-106,-107,-108,-109,-120,-119,-112,-118,-114,]),'ADD':([68,69,70,71,72,82,83,85,86,88,89,139,145,174,175,176,177,178,179,180,181,182,183,184,185,186,189,190,220,221,222,],[-10,-11,-12,-13,-14,132,-105,-110,-111,-113,-115,-117,-116,132,132,132,132,132,132,-102,-103,-104,-106,-107,-108,-109,-120,-119,-112,-118,-114,]),'kOR':([68,69,70,71,72,82,83,85,86,88,89,139,145,174,175,176,177,178,179,180,181,182,183,184,185,186,189,190,220,221,222,],[-10,-11,-12,-13,-14,134,-105,-110,-111,-113,-115,-117,-116,134,134,134,134,134,134,-102,-103,-104,-106,-107,-108,-109,-120,-119,-112,-118,-114,]),'kTHEN':([68,69,70,71,72,81,82,83,85,86,88,89,139,145,174,175,176,177,178,179,180,181,182,183,184,185,186,189,190,220,221,222,],[-10,-11,-12,-13,-14,125,-101,-105,-110,-111,-113,-115,-117,-116,-95,-96,-97,-98,-99,-100,-102,-103,-104,-106,-107,-108,-109,-120,-119,-112,-118,-114,]),'GE':([68,69,70,71,72,81,82,83,85,86,88,89,92,94,117,118,121,123,139,143,145,174,175,176,177,178,179,180,181,182,183,184,185,186,188,189,190,192,194,214,215,216,220,221,222,237,239,],[-10,-11,-12,-13,-14,126,-101,-105,-110,-111,-113,-115,126,126,126,126,126,126,-117,126,-116,-95,-96,-97,-98,-99,-100,-102,-103,-104,-106,-107,-108,-109,126,-120,-119,126,126,126,126,126,-112,-118,-114,126,126,]),'GT':([68,69,70,71,72,81,82,83,85,86,88,89,92,94,117,118,121,123,139,143,145,174,175,176,177,178,179,180,181,182,183,184,185,186,188,189,190,192,194,214,215,216,220,221,222,237,239,],[-10,-11,-12,-13,-14,127,-101,-105,-110,-111,-113,-115,127,127,127,127,127,127,-117,127,-116,-95,-96,-97,-98,-99,-100,-102,-103,-104,-106,-107,-108,-109,127,-120,-119,127,127,127,127,127,-112,-118,-114,127,127,]),'LE':([68,69,70,71,72,81,82,83,85,86,88,89,92,94,117,118,121,123,139,143,145,174,175,176,177,178,179,180,181,182,183,184,185,186,188,189,190,192,194,214,215,216,220,221,222,237,239,],[-10,-11,-12,-13,-14,128,-101,-105,-110,-111,-113,-115,128,128,128,128,128,128,-117,128,-116,-95,-96,-97,-98,-99,-100,-102,-103,-104,-106,-107,-108,-109,128,-120,-119,128,128,128,128,128,-112,-118,-114,128,128,]),'LT':([68,69,70,71,72,81,82,83,85,86,88,89,92,94,117,118,121,123,139,143,145,174,175,176,177,178,179,180,181,182,183,184,185,186,188,189,190,192,194,214,215,216,220,221,222,237,239,],[-10,-11,-12,-13,-14,129,-101,-105,-110,-111,-113,-115,129,129,129,129,129,129,-117,129,-116,-95,-96,-97,-98,-99,-100,-102,-103,-104,-106,-107,-108,-109,129,-120,-119,129,129,129,129,129,-112,-118,-114,129,129,]),'UNEQUAL':([68,69,70,71,72,81,82,83,85,86,88,89,92,94,117,118,121,123,139,143,145,174,175,176,177,178,179,180,181,182,183,184,185,186,188,189,190,192,194,214,215,216,220,221,222,237,239,],[-10,-11,-12,-13,-14,131,-101,-105,-110,-111,-113,-115,131,131,131,131,131,131,-117,131,-116,-95,-96,-97,-98,-99,-100,-102,-103,-104,-106,-107,-108,-109,131,-120,-119,131,131,131,131,131,-112,-118,-114,131,131,]),'kDO':([68,69,70,71,72,82,83,85,86,88,89,92,139,145,174,175,176,177,178,179,180,181,182,183,184,185,186,189,190,220,221,222,239,],[-10,-11,-12,-13,-14,-101,-105,-110,-111,-113,-115,147,-117,-116,-95,-96,-97,-98,-99,-100,-102,-103,-104,-106,-107,-108,-109,-120,-119,-112,-118,-114,246,]),'kOF':([68,69,70,71,72,82,83,85,86,88,89,94,139,145,174,175,176,177,178,179,180,181,182,183,184,185,186,189,190,220,221,222,235,],[-10,-11,-12,-13,-14,-101,-105,-110,-111,-113,-115,149,-117,-116,-95,-96,-97,-98,-99,-100,-102,-103,-104,-106,-107,-108,-109,-120,-119,-112,-118,-114,244,]),'DOUBLEDOT':([68,69,70,71,72,112,],[-10,-11,-12,-13,-14,161,]),'RB':([68,69,70,71,72,82,83,85,86,88,89,105,110,118,139,145,174,175,176,177,178,179,180,181,182,183,184,185,186,188,189,190,207,208,209,220,221,222,],[-10,-11,-12,-13,-14,-101,-105,-110,-111,-113,-115,-26,-23,166,-117,-116,-95,-96,-97,-98,-99,-100,-102,-103,-104,-106,-107,-108,-109,221,-120,-119,-24,-25,235,-112,-118,-114,]),'kTO':([68,69,70,71,72,82,83,85,86,88,89,139,145,174,175,176,177,178,179,180,181,182,183,184,185,186,189,190,194,220,221,222,],[-10,-11,-12,-13,-14,-101,-105,-110,-111,-113,-115,-117,-116,-95,-96,-97,-98,-99,-100,-102,-103,-104,-106,-107,-108,-109,-120,-119,224,-112,-118,-114,]),'kDOWNTO':([68,69,70,71,72,82,83,85,86,88,89,139,145,174,175,176,177,178,179,180,181,182,183,184,185,186,189,190,194,220,221,222,],[-10,-11,-12,-13,-14,-101,-105,-110,-111,-113,-115,-117,-116,-95,-96,-97,-98,-99,-100,-102,-103,-104,-106,-107,-108,-109,-120,-119,225,-112,-118,-114,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'program_head':([0,],[2,]),'routine':([2,98,99,],[4,151,151,]),'routine_head':([2,98,99,],[5,5,5,]),'const_part':([2,98,99,],[6,6,6,]),'empty':([2,6,13,14,23,48,98,99,100,101,173,],[8,16,22,25,56,22,8,8,155,155,219,]),'routine_body':([5,],[11,]),'compound_stmt':([5,21,74,91,125,147,218,228,229,246,],[12,37,37,37,37,37,37,37,37,37,]),'type_part':([6,],[14,]),'const_expr_list':([7,],[17,]),'const_expr':([7,17,],[18,29,]),'stmt_list':([13,48,],[21,91,]),'var_part':([14,],[23,]),'type_decl_list':([15,],[26,]),'type_definition':([15,26,],[27,65,]),'stmt':([21,91,125,147,218,228,229,246,],[32,32,173,193,238,240,241,250,]),'non_label_stmt':([21,74,91,125,147,218,228,229,246,],[34,116,34,34,34,34,34,34,34,]),'assign_stmt':([21,74,91,125,147,218,228,229,246,],[35,35,35,35,35,35,35,35,35,]),'proc_stmt':([21,74,91,125,147,218,228,229,246,],[36,36,36,36,36,36,36,36,36,]),'if_stmt':([21,74,91,125,147,218,228,229,246,],[38,38,38,38,38,38,38,38,38,]),'repeat_stmt':([21,74,91,125,147,218,228,229,246,],[39,39,39,39,39,39,39,39,39,]),'while_stmt':([21,74,91,125,147,218,228,229,246,],[40,40,40,40,40,40,40,40,40,]),'for_stmt':([21,74,91,125,147,218,228,229,246,],[41,41,41,41,41,41,41,41,41,]),'case_stmt':([21,74,91,125,147,218,228,229,246,],[42,42,42,42,42,42,42,42,42,]),'goto_stmt':([21,74,91,125,147,218,228,229,246,],[43,43,43,43,43,43,43,43,43,]),'routine_part':([23,],[53,]),'function_decl':([23,53,],[54,96,]),'procedure_decl':([23,53,],[55,97,]),'function_head':([23,53,],[57,57,]),'procedure_head':([23,53,],[58,58,]),'var_decl_list':([24,],[61,]),'var_decl':([24,61,],[62,102,]),'name_list':([24,61,111,114,163,205,],[63,63,160,165,165,234,]),'const_value':([30,47,49,51,66,75,76,78,79,80,84,87,90,103,126,127,128,129,130,131,132,133,134,135,136,137,138,140,141,144,146,148,149,161,162,167,169,171,195,201,212,213,223,233,244,],[67,89,89,89,112,89,89,89,89,89,89,89,89,112,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,197,208,112,89,89,89,197,112,112,89,89,112,112,]),'expression':([47,49,51,75,76,78,79,87,140,141,144,146,148,167,169,171,213,223,],[81,92,94,117,118,121,123,143,121,188,121,192,194,214,215,216,237,239,]),'expr':([47,49,51,75,76,78,79,87,126,127,128,129,130,131,140,141,144,146,148,167,169,171,213,223,],[82,82,82,82,82,82,82,82,174,175,176,177,178,179,82,82,82,82,82,82,82,82,82,82,]),'term':([47,49,51,75,76,78,79,87,126,127,128,129,130,131,132,133,134,140,141,144,146,148,167,169,171,213,223,],[83,83,83,83,83,83,83,83,83,83,83,83,83,83,180,181,182,83,83,83,83,83,83,83,83,83,83,]),'factor':([47,49,51,75,76,78,79,80,84,87,90,126,127,128,129,130,131,132,133,134,135,136,137,138,140,141,144,146,148,167,169,171,213,223,],[85,85,85,85,85,85,85,124,139,85,145,85,85,85,85,85,85,85,85,85,183,184,185,186,85,85,85,85,85,85,85,85,85,85,]),'type_decl':([66,103,212,244,],[106,157,236,249,]),'simple_type_decl':([66,103,162,201,212,233,244,],[107,107,209,230,107,243,107,]),'array_type_decl':([66,103,212,244,],[108,108,108,108,]),'record_type_decl':([66,103,212,244,],[109,109,109,109,]),'args_list':([78,140,144,],[120,187,191,]),'expression_list':([79,],[122,]),'sub_routine':([98,99,],[150,152,]),'parameters':([100,101,],[153,156,]),'field_decl_list':([114,],[163,]),'field_decl':([114,163,],[164,211,]),'case_expr_list':([149,],[195,]),'case_expr':([149,195,],[196,227,]),'para_decl_list':([154,],[202,]),'para_type_list':([154,232,],[203,242,]),'var_para_list':([154,232,],[204,204,]),'else_clause':([173,],[217,]),'direction':([194,],[223,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> program_head routine DOT','program',3,'p_program','yacc_pas.py',16),
  ('program_head -> kPROGRAM ID SEMICON','program_head',3,'p_program_head','yacc_pas.py',21),
  ('routine -> routine_head routine_body','routine',2,'p_routine','yacc_pas.py',26),
  ('routine_head -> const_part type_part var_part routine_part','routine_head',4,'p_routine_head','yacc_pas.py',31),
  ('const_part -> kCONST const_expr_list','const_part',2,'p_const_part','yacc_pas.py',36),
  ('const_part -> empty','const_part',1,'p_const_part','yacc_pas.py',37),
  ('const_expr_list -> const_expr_list const_expr','const_expr_list',2,'p_const_expr_list','yacc_pas.py',43),
  ('const_expr_list -> const_expr','const_expr_list',1,'p_const_expr_list','yacc_pas.py',44),
  ('const_expr -> ID EQUAL const_value SEMICON','const_expr',4,'p_const_expr','yacc_pas.py',52),
  ('const_value -> INTEGER','const_value',1,'p_const_value_1','yacc_pas.py',59),
  ('const_value -> REAL','const_value',1,'p_const_value_2','yacc_pas.py',64),
  ('const_value -> CHAR','const_value',1,'p_const_value_3','yacc_pas.py',69),
  ('const_value -> STRING','const_value',1,'p_const_value_4','yacc_pas.py',75),
  ('const_value -> SYS_CON','const_value',1,'p_const_value_5','yacc_pas.py',80),
  ('type_part -> kTYPE type_decl_list','type_part',2,'p_type_part','yacc_pas.py',86),
  ('type_part -> empty','type_part',1,'p_type_part','yacc_pas.py',87),
  ('type_decl_list -> type_decl_list type_definition','type_decl_list',2,'p_type_decl_list','yacc_pas.py',93),
  ('type_decl_list -> type_definition','type_decl_list',1,'p_type_decl_list','yacc_pas.py',94),
  ('type_definition -> ID EQUAL type_decl SEMICON','type_definition',4,'p_type_definition','yacc_pas.py',102),
  ('type_decl -> simple_type_decl','type_decl',1,'p_type_decl','yacc_pas.py',107),
  ('type_decl -> array_type_decl','type_decl',1,'p_type_decl','yacc_pas.py',108),
  ('type_decl -> record_type_decl','type_decl',1,'p_type_decl','yacc_pas.py',109),
  ('simple_type_decl -> SYS_TYPE','simple_type_decl',1,'p_simple_type_decl_1','yacc_pas.py',124),
  ('simple_type_decl -> LP name_list RP','simple_type_decl',3,'p_simple_type_decl_2','yacc_pas.py',130),
  ('simple_type_decl -> const_value DOUBLEDOT const_value','simple_type_decl',3,'p_simple_type_decl_3','yacc_pas.py',135),
  ('simple_type_decl -> ID','simple_type_decl',1,'p_simple_type_decl_4','yacc_pas.py',141),
  ('array_type_decl -> kARRAY LB simple_type_decl RB kOF type_decl','array_type_decl',6,'p_array_type_decl','yacc_pas.py',147),
  ('record_type_decl -> kRECORD field_decl_list kEND','record_type_decl',3,'p_record_type_decl','yacc_pas.py',152),
  ('field_decl_list -> field_decl_list field_decl','field_decl_list',2,'p_field_decl_list','yacc_pas.py',157),
  ('field_decl_list -> field_decl','field_decl_list',1,'p_field_decl_list','yacc_pas.py',158),
  ('field_decl -> name_list COLON type_decl SEMICON','field_decl',4,'p_field_decl','yacc_pas.py',166),
  ('name_list -> name_list COMMA ID','name_list',3,'p_name_list','yacc_pas.py',171),
  ('name_list -> ID','name_list',1,'p_name_list','yacc_pas.py',172),
  ('var_part -> kVAR var_decl_list','var_part',2,'p_var_part','yacc_pas.py',181),
  ('var_part -> empty','var_part',1,'p_var_part','yacc_pas.py',182),
  ('var_decl_list -> var_decl_list var_decl','var_decl_list',2,'p_var_decl_list','yacc_pas.py',188),
  ('var_decl_list -> var_decl','var_decl_list',1,'p_var_decl_list','yacc_pas.py',189),
  ('var_decl -> name_list COLON type_decl SEMICON','var_decl',4,'p_var_decl','yacc_pas.py',197),
  ('routine_part -> routine_part function_decl','routine_part',2,'p_routine_part','yacc_pas.py',203),
  ('routine_part -> routine_part procedure_decl','routine_part',2,'p_routine_part','yacc_pas.py',204),
  ('routine_part -> function_decl','routine_part',1,'p_routine_part','yacc_pas.py',205),
  ('routine_part -> procedure_decl','routine_part',1,'p_routine_part','yacc_pas.py',206),
  ('routine_part -> empty','routine_part',1,'p_routine_part','yacc_pas.py',207),
  ('sub_routine -> routine','sub_routine',1,'p_sub_routine','yacc_pas.py',216),
  ('function_decl -> function_head SEMICON sub_routine SEMICON','function_decl',4,'p_function_decl','yacc_pas.py',221),
  ('function_head -> kFUNCTION ID parameters COLON simple_type_decl','function_head',5,'p_function_head','yacc_pas.py',226),
  ('procedure_decl -> procedure_head SEMICON sub_routine SEMICON','procedure_decl',4,'p_procedure_decl','yacc_pas.py',231),
  ('procedure_head -> kPROCEDURE ID parameters','procedure_head',3,'p_procedure_head','yacc_pas.py',236),
  ('parameters -> LP para_decl_list RP','parameters',3,'p_parameters','yacc_pas.py',241),
  ('parameters -> empty','parameters',1,'p_parameters','yacc_pas.py',242),
  ('para_decl_list -> para_decl_list SEMICON para_type_list','para_decl_list',3,'p_para_decl_list','yacc_pas.py',248),
  ('para_decl_list -> para_type_list','para_decl_list',1,'p_para_decl_list','yacc_pas.py',249),
  ('para_type_list -> var_para_list COLON simple_type_decl','para_type_list',3,'p_para_type_list','yacc_pas.py',257),
  ('var_para_list -> kVAR name_list','var_para_list',2,'p_var_para_list','yacc_pas.py',264),
  ('val_para_list -> name_list','val_para_list',1,'p_val_para_list','yacc_pas.py',269),
  ('routine_body -> compound_stmt','routine_body',1,'p_routine_body','yacc_pas.py',274),
  ('compound_stmt -> kBEGIN stmt_list kEND','compound_stmt',3,'p_compound_stmt','yacc_pas.py',279),
  ('stmt_list -> stmt_list stmt SEMICON','stmt_list',3,'p_stmt_list','yacc_pas.py',284),
  ('stmt_list -> empty','stmt_list',1,'p_stmt_list','yacc_pas.py',285),
  ('stmt -> INTEGER COLON non_label_stmt','stmt',3,'p_stmt','yacc_pas.py',293),
  ('stmt -> non_label_stmt','stmt',1,'p_stmt','yacc_pas.py',294),
  ('non_label_stmt -> assign_stmt','non_label_stmt',1,'p_non_label_stmt','yacc_pas.py',303),
  ('non_label_stmt -> proc_stmt','non_label_stmt',1,'p_non_label_stmt','yacc_pas.py',304),
  ('non_label_stmt -> compound_stmt','non_label_stmt',1,'p_non_label_stmt','yacc_pas.py',305),
  ('non_label_stmt -> if_stmt','non_label_stmt',1,'p_non_label_stmt','yacc_pas.py',306),
  ('non_label_stmt -> repeat_stmt','non_label_stmt',1,'p_non_label_stmt','yacc_pas.py',307),
  ('non_label_stmt -> while_stmt','non_label_stmt',1,'p_non_label_stmt','yacc_pas.py',308),
  ('non_label_stmt -> for_stmt','non_label_stmt',1,'p_non_label_stmt','yacc_pas.py',309),
  ('non_label_stmt -> case_stmt','non_label_stmt',1,'p_non_label_stmt','yacc_pas.py',310),
  ('non_label_stmt -> goto_stmt','non_label_stmt',1,'p_non_label_stmt','yacc_pas.py',311),
  ('assign_stmt -> ID ASSIGN expression','assign_stmt',3,'p_assign_stmt','yacc_pas.py',316),
  ('assign_stmt -> ID LB expression RB ASSIGN expression','assign_stmt',6,'p_assign_stmt','yacc_pas.py',317),
  ('assign_stmt -> ID DOT ID ASSIGN expression','assign_stmt',5,'p_assign_stmt','yacc_pas.py',318),
  ('proc_stmt -> ID','proc_stmt',1,'p_proc_stmt','yacc_pas.py',330),
  ('proc_stmt -> ID LP args_list RP','proc_stmt',4,'p_proc_stmt','yacc_pas.py',331),
  ('proc_stmt -> SYS_PROC','proc_stmt',1,'p_proc_stmt','yacc_pas.py',332),
  ('proc_stmt -> SYS_PROC LP expression_list RP','proc_stmt',4,'p_proc_stmt','yacc_pas.py',333),
  ('proc_stmt -> kREAD LP factor RP','proc_stmt',4,'p_proc_stmt','yacc_pas.py',334),
  ('if_stmt -> kIF expression kTHEN stmt else_clause','if_stmt',5,'p_if_stmt','yacc_pas.py',342),
  ('else_clause -> kELSE stmt','else_clause',2,'p_else_clause','yacc_pas.py',347),
  ('else_clause -> empty','else_clause',1,'p_else_clause','yacc_pas.py',348),
  ('repeat_stmt -> kREPEAT stmt_list kUNTIL expression','repeat_stmt',4,'p_repeat_stmt','yacc_pas.py',354),
  ('while_stmt -> kWHILE expression kDO stmt','while_stmt',4,'p_while_stmt','yacc_pas.py',359),
  ('for_stmt -> kFOR ID ASSIGN expression direction expression kDO stmt','for_stmt',8,'p_for_stmt','yacc_pas.py',364),
  ('direction -> kTO','direction',1,'p_direction','yacc_pas.py',369),
  ('direction -> kDOWNTO','direction',1,'p_direction','yacc_pas.py',370),
  ('case_stmt -> kCASE expression kOF case_expr_list kEND','case_stmt',5,'p_case_stmt','yacc_pas.py',375),
  ('case_expr_list -> case_expr_list case_expr','case_expr_list',2,'p_case_expr_list','yacc_pas.py',380),
  ('case_expr_list -> case_expr','case_expr_list',1,'p_case_expr_list','yacc_pas.py',381),
  ('case_expr -> const_value COLON stmt SEMICON','case_expr',4,'p_case_expr','yacc_pas.py',389),
  ('case_expr -> ID COLON stmt SEMICON','case_expr',4,'p_case_expr','yacc_pas.py',390),
  ('goto_stmt -> kGOTO INTEGER','goto_stmt',2,'p_goto_stmt','yacc_pas.py',395),
  ('expression_list -> expression_list COMMA expression','expression_list',3,'p_expression_list','yacc_pas.py',400),
  ('expression_list -> expression','expression_list',1,'p_expression_list','yacc_pas.py',401),
  ('expression -> expression GE expr','expression',3,'p_expression','yacc_pas.py',409),
  ('expression -> expression GT expr','expression',3,'p_expression','yacc_pas.py',410),
  ('expression -> expression LE expr','expression',3,'p_expression','yacc_pas.py',411),
  ('expression -> expression LT expr','expression',3,'p_expression','yacc_pas.py',412),
  ('expression -> expression EQUAL expr','expression',3,'p_expression','yacc_pas.py',413),
  ('expression -> expression UNEQUAL expr','expression',3,'p_expression','yacc_pas.py',414),
  ('expression -> expr','expression',1,'p_expression','yacc_pas.py',415),
  ('expr -> expr ADD term','expr',3,'p_expr','yacc_pas.py',425),
  ('expr -> expr SUBTRACT term','expr',3,'p_expr','yacc_pas.py',426),
  ('expr -> expr kOR term','expr',3,'p_expr','yacc_pas.py',427),
  ('expr -> term','expr',1,'p_expr','yacc_pas.py',428),
  ('term -> term MUL factor','term',3,'p_term','yacc_pas.py',440),
  ('term -> term DIV factor','term',3,'p_term','yacc_pas.py',441),
  ('term -> term MOD factor','term',3,'p_term','yacc_pas.py',442),
  ('term -> term kAND factor','term',3,'p_term','yacc_pas.py',443),
  ('term -> factor','term',1,'p_term','yacc_pas.py',444),
  ('factor -> ID','factor',1,'p_factor_1','yacc_pas.py',458),
  ('factor -> ID LP args_list RP','factor',4,'p_factor_1','yacc_pas.py',459),
  ('factor -> SYS_FUNCT','factor',1,'p_factor_1','yacc_pas.py',460),
  ('factor -> SYS_FUNCT LP args_list RP','factor',4,'p_factor_1','yacc_pas.py',461),
  ('factor -> const_value','factor',1,'p_factor_1','yacc_pas.py',462),
  ('factor -> kNOT factor','factor',2,'p_factor_1','yacc_pas.py',463),
  ('factor -> SUBTRACT factor','factor',2,'p_factor_1','yacc_pas.py',464),
  ('factor -> ID LB expression RB','factor',4,'p_factor_1','yacc_pas.py',465),
  ('factor -> LP expression RP','factor',3,'p_factor_2','yacc_pas.py',476),
  ('factor -> ID DOT ID','factor',3,'p_factor3','yacc_pas.py',481),
  ('args_list -> args_list COMMA expression','args_list',3,'p_args_list','yacc_pas.py',486),
  ('args_list -> expression','args_list',1,'p_args_list','yacc_pas.py',487),
  ('empty -> <empty>','empty',0,'p_empty','yacc_pas.py',497),
]
