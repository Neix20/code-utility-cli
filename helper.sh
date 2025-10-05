
file_ls=(
    "txt_read_strategy.py"
    "json_read_strategy.py"
    "txt_write_strategy.py"
    "json_write_strategy.py"
)

for file in "${file_ls[@]}"; do
    touch "app/strategy/file_handler/$file"
done