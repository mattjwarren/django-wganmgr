#modelrun.full_path
SHELL_GET_NEWEST_CKPT_FILE="ls -ltr --full-time %s | grep ckpt | grep -v _temp | tail -1"
#modelrun.full_path
SHELL_TOUCH_HALT="touch %shalt"
#modelrun.full_path
SHELL_TOUCH_UPLOAD_MODEL="touch %supload_model"
#any directory
SHELL_DOES_PATH_EXIST='[[ -d %s ]] && echo True || echo False'
#any directory
SHELL_MKDIR_P="mkdir -p %s && echo True || echo False"
#any valid bash mv pair
SHELL_MV="mv %s %s && echo True || echo False"
#get dataset file after upload to node TODO: sort out settings parameters properly
SHELL_GET_DATASET_BUNDLE_AND_UNPACK="mkdir -p %s && scp ubuntu-1:/tmp/%s %s/ && cd %s/ && tar -xzvf %s && rm %s/%s && echo True || echo False"
