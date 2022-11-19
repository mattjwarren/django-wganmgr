SHELL_GET_NEWEST_CKPT_FILE="ls -ltr --full-time %s | grep ckpt | grep -v _temp | tail -1"
SHELL_TOUCH_HALT="touch %shalt"
SHELL_DOES_PATH_EXIST='[[ -d %s ]] && echo True || echo False'
SHELL_MKDIR_P="mkdir -p %s && echo True || echo False"
SHELL_MV="mv %s %s && echo True || echo False"