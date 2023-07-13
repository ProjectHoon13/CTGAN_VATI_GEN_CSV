import csv
import numpy as np
from utils import rand_date, rand_sub_arr, rand_string_number

def clear_header(nrh, nums_of_columns, lines):
    for element in range(nrh + 1):
        for index in range(nums_of_columns):
            lines[element][index] = ''

def overwrite_bold_data(nums_of_columns, nrbs, lines, nrh, bd_data, nrbe, nums_rows_bold_rest, nums_of_rows, prh_idx, spc_idx, cell_spc_idx, content_spc, alignment_spc):
    # List all bold rows index in GEN CSV
    all_bd_row_arr = []
    # List all space rows index in GEN CSV
    space_row_arr = []
    # List all prh in GEN CSV
    prh_row_arr = []
    # List all spc in GEN CSV
    spc_row_arr = []
    # List all space row in GEN CSV
    space_row_arr = []
    # List all content of spc in GEN CSV
    content_spc_arr = []
    # List all aligment of spc in GEN CSV
    aligment_spc_arr = []

    # List all bold rows index used in INPUT CSV
    original_bd_idx = []
    
    # Overwrite fixed bold row data
    if len(bd_data) > 0:
        for idx in range(nrbs):
            all_bd_row_arr.append(idx + nrh + 1)
            original_bd_idx.append(idx)
            for cell in range(nums_of_columns):
                lines[idx + nrh + 1][cell] = bd_data[idx][cell]
        for idx in range(nrbe):
            all_bd_row_arr.append(nums_of_rows -(idx + 1))
            original_bd_idx.append(nums_of_rows -(idx + 1))
            for cell in range(nums_of_columns):
                lines[-(idx + 1)][cell] = bd_data[-(idx + 1)][cell]
    
    # # Calculate nums of bold rows rest
    # nums_rows_bold_rest = nums_rows_bold_rest - nrbs - nrbe

    if nums_rows_bold_rest > 0:
        # RANDOM_RANGE nums of bold rows
        rand_bd_start = nrbs
        rand_bd_stop = len(bd_data) - nrbe

        # Create list bold rows
        bd_arr = list(range(rand_bd_start, rand_bd_stop))
        sub_bd_arr = rand_sub_arr(bd_arr, nums_rows_bold_rest)

        # RANDOM_RANGE order of bold rows
        rand_row_start = nrh + nrbs + 1
        rand_row_stop = nums_of_rows - nrbe

        row_arr = list(range(rand_row_start, rand_row_stop))
        sub_row_arr = rand_sub_arr(row_arr, nums_rows_bold_rest)

        # Overwrite rest bold row data
        for bd_row_idx in range(len(sub_bd_arr)):
            all_bd_row_arr.append(sub_row_arr[bd_row_idx])
            original_bd_idx.append(sub_bd_arr[bd_row_idx])
            for bd_cell_idx in range(nums_of_columns):
                lines[sub_row_arr[bd_row_idx]][bd_cell_idx] = bd_data[sub_bd_arr[bd_row_idx]][bd_cell_idx]

    if len(all_bd_row_arr) > 0:        
        for pos in all_bd_row_arr:
            space_row_arr.append(pos - 1)
        if nrh not in space_row_arr:
            space_row_arr.append(nrh)
        if (nums_of_rows - 2) not in space_row_arr:
            space_row_arr.append(nums_of_rows - 2)
        space_row_arr.append(nums_of_rows - 1)
        space_row_arr.sort()

        new_prh_idx = np.where(np.in1d(original_bd_idx, prh_idx))[0]
        prh_row_idx = np.array(all_bd_row_arr)[new_prh_idx]
        for element in prh_row_idx:
            sub_prh_arr = []
            for i in range(nums_of_columns):
                sub_prh_arr.append(nums_of_columns * element + i)
            prh_row_arr.append(sub_prh_arr)

        new_spc_idx = np.where(np.in1d(original_bd_idx, spc_idx))[0]
        spc_row_idx = np.array(all_bd_row_arr)[new_spc_idx]
        for loop_count, element in enumerate(spc_row_idx):
            sub_spc_arr = []
            for i in cell_spc_idx[loop_count]:
                sub_spc_arr.append(nums_of_columns * element + i)
            spc_row_arr.append(sub_spc_arr)
        
        new_cont_spc_idx = np.where(np.in1d(spc_idx, new_spc_idx))[0]
        cont_spc = np.array(content_spc)[new_cont_spc_idx]
        for loop_count, element in enumerate(cont_spc):
            sub_cont_spc_arr = element.tolist()
            content_spc_arr.append(sub_cont_spc_arr)

        # new_alig_spc_idx = np.where(np.in1d(spc_idx, new_spc_idx))[0]
        alig_spc = np.array(alignment_spc)[new_cont_spc_idx]
        for loop_count, element in enumerate(alig_spc):
            sub_alig_spc_arr = element.tolist()
            aligment_spc_arr.append(sub_alig_spc_arr)
        
        all_bd_row_arr.sort()             

    return [all_bd_row_arr, space_row_arr, prh_row_arr, spc_row_arr, content_spc_arr, aligment_spc_arr]

def rand_number_columns(list_index_of_columns_rand_number, nrh, nums_of_rows, lines):
    for row_idx in range(nrh + 1, nums_of_rows):
        for col_idx in list_index_of_columns_rand_number:
            lines[row_idx][col_idx] = rand_string_number(lines[row_idx][col_idx])

def changed_function(nrh, nums_of_columns, lines, bd_data, nums_rows_bold_rest, nums_of_rows, file_csv_dir, nrbs, nrbe, prh_idx, spc_idx, cell_spc_idx, content_spc, alignment_spc):
    # Clear header
    clear_header(nrh, nums_of_columns, lines)
    
    # Refix header
    # FIXME: NEED CHANGE value of text in header per table type
    lines[0][3] = "Tại ngày"
    lines[1][3] = rand_date()
    lines[1][4] = rand_date()
    lines[2][3] = "Triệu VND"
    lines[2][4] = "Triệu VND"

    # Overwrite bold row data
    pos_info_arr = overwrite_bold_data(nums_of_columns, nrbs, lines, nrh, bd_data, nrbe, nums_rows_bold_rest, nums_of_rows, prh_idx, spc_idx, cell_spc_idx, content_spc, alignment_spc)

    # Index of columns need random number
    # FIXME: NEED CHANGE index of columns random number per table type
    list_index_of_columns_rand_number = [-2, -1]

    # RANDOM NUMBER columns
    rand_number_columns(list_index_of_columns_rand_number, nrh, nums_of_rows, lines)

    # Rewrite .csv file
    writer = csv.writer(open(file_csv_dir, 'w', encoding='utf-8-sig', newline=''))
    writer.writerows(lines)

    # Write info to .txt file
    with open(f'{file_csv_dir[:-4]}.txt', 'w') as txt_file:
        for element in pos_info_arr:
            txt_file.write("%s\n" % element)
