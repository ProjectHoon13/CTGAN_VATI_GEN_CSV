import time

from utils import *
from multiprocessing.pool import ThreadPool
from dict_discrete_columns_type import DICT_DISCRETE_COLUMNS_TYPE
from changed_function_per_table_type import changed_function


## CHANGED PARAMS ##
# FIXME: Change the below parameters according to the generated table type

# PARAMS 00 - Table Type
# Name of table type
TABLE_TYPE = 'BCTC3_CDKT_A_2'

# PARAMS 01 - OUTPUT FOLDER
OUTPUT_FOLDER = 'VATI_GEN_CSV' + '/' + TABLE_TYPE

# PARAMS 02 - Nums of Rows Header
# NOT include first row of header
NRH = 2

# PARAMS 03
# NUMS_ROWS_BOLD_START
NRBS = 2

# PARAMS 04
# NUMS_ROWS_BOLD_END
NRBE = 1

# PARAMS 05 - Range Nums of Bold Rows Rest
# NOT include START ROWS BOLD & END ROW
# RANGE_NBRR = [min, max]
RANGE_NBRR = [2, 6]

# PARAMS 06 - Range Nums of Rows in Normal
# RANGE_NRN = [min, max]
RANGE_NRN = [18, 26]

# PARAMS 07 - Nums of CSV Samples Output
NCSO = 500


## FIXED PARAMS ##
# NOTE: No need to adjust the parameters below, except for special cases

FOLDER_CSV = './type'
NR_CSV_DIR = FOLDER_CSV + '/' + TABLE_TYPE + '_NR.csv'
BD_CSV_DIR = FOLDER_CSV + '/' + TABLE_TYPE + '_BD.csv'

BASE_ADDR = os.getcwd()
FOLDER_OUTPUT_DIR = join_path(BASE_ADDR, OUTPUT_FOLDER)

# NFR - Nums Fixed Rows
NFR = NRH + NRBS + NRBE

# START_INDEX
START_IDX = 0

# STOP_INDEX
STOP_IDX = START_IDX + NCSO

# INDEX_RANGE
INDEX_RANGE = [START_IDX, STOP_IDX]

# RANGE_ROWS
RANGE_ROWS = [RANGE_NBRR, RANGE_NRN, NFR]

# Number of parallel processes
NUMS_PROCESSES = 4

# Number of epochs
NUMS_EPOCHS = 300

# SUB_CONSTANT
TIME = '1'


def gen_csv(range_nbrr, range_nrn, nums_fixed_rows, ctgan, index, folder_csv_dir, bd_data, prh_idx, spc_idx, cell_spc_idx, content_spc, alignment_spc):
    # Random nums of rows
    nums_rows_bold_rest = random.randint(range_nbrr[0], range_nbrr[1])
    nums_rows_normal = random.randint(range_nrn[0], range_nrn[1])
    nums_of_rows = nums_rows_bold_rest + nums_rows_normal + nums_fixed_rows
    
    # Create synthetic data
    synthetic_data = ctgan.sample(nums_of_rows - 1)
    file_name_csv = TABLE_TYPE + '_' + str(index + 1) + ".csv"
    file_csv_dir = folder_csv_dir + '/' + file_name_csv
    synthetic_data.to_csv(file_csv_dir, index=False, encoding='utf-8-sig')
    
    # Read file csv
    read_csv = csv.reader(open(file_csv_dir, encoding='utf-8-sig'))
    lines = list(read_csv)
    nums_of_columns = len(lines[0])

    changed_function(NRH, nums_of_columns, lines, bd_data, nums_rows_bold_rest, nums_of_rows, file_csv_dir, NRBS, NRBE, prh_idx, spc_idx, cell_spc_idx, content_spc, alignment_spc)

    print('Successfully generated csv file and txt file {:03}'.format(index + 1))

def make_csv(ctgan, range_rows, index_range, bd_data, merged_cell_data_idx):
    prh_idx, spc_idx, cell_spc_idx, content_spc, alignment_spc = merged_cell_data_idx
    range_nbrr, range_nrn, nums_fixed_rows = range_rows
    start_index, stop_index = index_range
    folder_csv_dir = './' + OUTPUT_FOLDER
    make_dirs_or_format_dir(folder_csv_dir)

    with ThreadPool(processes=NUMS_PROCESSES) as pool:
        for index in range(start_index, stop_index):
            pool.apply_async(gen_csv, args=(range_nbrr, range_nrn, nums_fixed_rows, ctgan, index, folder_csv_dir, bd_data, prh_idx, spc_idx, cell_spc_idx, content_spc, alignment_spc))
        pool.close()
        pool.join()

def main():
    # START
    print('Program start !!!')
    start_time_program = time.time()

    # Create or Refresh output folder
    make_dirs_or_format_dir(FOLDER_OUTPUT_DIR)

    # Get list of bold data
    bd_data = list(read_bd_csv(BD_CSV_DIR))

    try:
        assert (NRBS + NRBE) <= len(bd_data)
    except AssertionError:
        print('The NBR (nums bold rows) start & end constant is set to a value greater than the NBR in the input CSV_BD file ({} > {}) !!!'.format(NRBS + NRBE, len(bd_data)))
    
    # Get list of projected row header
    prh_idx = DICT_DISCRETE_COLUMNS_TYPE[TABLE_TYPE][1]
    
    # Get list of spanning cell
    spc_idx = DICT_DISCRETE_COLUMNS_TYPE[TABLE_TYPE][2]
    # Get cell index in spanning cell
    cell_spc_idx = DICT_DISCRETE_COLUMNS_TYPE[TABLE_TYPE][3]
    # Get content of spc list
    content_spc = DICT_DISCRETE_COLUMNS_TYPE[TABLE_TYPE][4]
    # Get alignment of text in spc list
    alignment_spc = DICT_DISCRETE_COLUMNS_TYPE[TABLE_TYPE][5]

    # PACKET_CONSTANT
    MERGED_CELL_DATA_IDX = [prh_idx, spc_idx, cell_spc_idx, content_spc, alignment_spc]

    # Names of the columns that are discrete
    discrete_columns = DICT_DISCRETE_COLUMNS_TYPE[TABLE_TYPE][0]
    
    # Load data from CSV INPUT
    data = my_load_data(NR_CSV_DIR)
    
    # LEARNING TASK
    start_time_task_learning = time.time()
    ctgan = learning_data(data, discrete_columns, epochs=NUMS_EPOCHS)
    end_time_task_normalize = time.time()
    total_time_task_learning = end_time_task_normalize - start_time_task_learning
    mean_times_per_epoch = total_time_task_learning / NUMS_EPOCHS
    mean_epoch_per_sec = 1 / mean_times_per_epoch

    # MAKE CSV TASK
    start_time_task_make_csv = time.time()
    make_csv(ctgan, RANGE_ROWS, INDEX_RANGE, bd_data, MERGED_CELL_DATA_IDX)
    end_time_task_make_csv = time.time()
    total_time_task_make_csv = end_time_task_make_csv - start_time_task_make_csv
    mean_times_per_csv = total_time_task_make_csv / NCSO
    mean_csv_and_txt_per_sec = 1 / mean_times_per_csv
    print('Average time per csv file generated:', round(mean_times_per_csv, 5), '(s)')
    print('Average csv file generated per second: {:.3f}'.format(round(mean_csv_and_txt_per_sec, 3)), '(csv/s)')
    print('Total running time of task make csv:', round(total_time_task_make_csv, 5), '(s)')
    print('Average run time per epoch:', round(mean_times_per_epoch, 5), '(s)')
    print('Average number of completed epochs per second: {:.3f}'.format(round(mean_epoch_per_sec, 3)), '(epoch/s)')
    print('Total running time of task learning:', round(total_time_task_learning, 5), '(s)')

    end_time_program = time.time()
    total_time_program = end_time_program - start_time_program
    print('Total running time:', round(total_time_program, 5), '(s)')

    # END
    print('Program run successfully !!!')
    print("Copyright @ProjectHoon")

if __name__ == "__main__":
    main()
