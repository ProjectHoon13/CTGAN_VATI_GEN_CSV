BCTC3_CDKT_A_1 = [
    # PROPERTIES 00
    # Discrete Columns
    ['STT',
     'CHỈ TIÊU',
     'Thuyết minh',
     'Số cuối năm',
     'Số đầu năm'],
    
    # PROPERTIES 01
    # Projected row header
    [0],

    # PROPERTIES 02
    # Spanning cell
    # Row index in bold data
    [],

    # PROPERTIES 03
    # Cell index in row have spanning cell
    [],

    # PROPERTIES 04
    # Content of spc
    [],

    # PROPERTIES 05
    # Alignment of text in spanning cell
    []
]

BCTC2_4C_1 = [
    # PROPERTIES 00
    # Discrete Columns
    ['A',
     'Tổng giá trị của hợp đồng (theo tỉ giá tại ngày hiệu lực)',
     'Tổng giá trị ghi sổ kế toán (theo tỷ giá tại ngày lập báo cáo tài chính)',
     'B',
     'C'],
    
    # PROPERTIES 01
    # Projected row header (index)
    [0, 1, 3, 4],

    # PROPERTIES 02
    # Spanning cell
    # Row index in bold data (not include header)
    [],

    # PROPERTIES 03
    # Cell index in row have spanning cell (not include header)
    [],

    # PROPERTIES 04
    # Content of spc (not include header)
    [],

    # PROPERTIES 05
    # Alignment of text in spanning cell (not include header)
    [] # Must have 2 arguments
]

BCTC2_4D_1 = [
    # PROPERTIES 00
    # Discrete Columns
    ['A',
     'Số dư đầu năm',
     'Phát sinh trong năm',
     'B',
     'Số dư cuối năm'
     ],
    
    # PROPERTIES 01
    # Projected row header (index)
    [],

    # PROPERTIES 02
    # Spanning cell
    # Row index in bold data (not include header)
    [],

    # PROPERTIES 03
    # Cell index in row have spanning cell (not include header)
    [],

    # PROPERTIES 04
    # Content of spc (not include header)
    [],

    # PROPERTIES 05
    # Alignment of text in spanning cell (not include header)
    []
]

DICT_DISCRETE_COLUMNS_TYPE = {
    'BCTC3_CDKT_A_1': BCTC3_CDKT_A_1,
    'BCTC2_4C_1': BCTC2_4C_1,
    'BCTC2_4D_1': BCTC2_4D_1
}
