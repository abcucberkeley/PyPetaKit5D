#!/bin/bash

# Directory containing the Python files
python_files_dir="/home/matt/PyLLSM5DTools/src"
output_file="/home/matt/PyLLSM5DTools/PyLLSM5DTools/__init__.py"

# Clear the output file
> "$output_file"

# Generate whitelist from function names in Python files
whitelist=()
for file in "$python_files_dir"/*.py; do
    # Get the base name of the file (without the extension)
    file_name=$(basename "$file" .py)
    # Get the function names from the file and add them to the whitelist
    functions=$(grep -oP 'def \K\w+' "$file")
    for function in $functions; do
        whitelist+=("$function")
    done


done

# Print the generated whitelist
printf -v whitelist_str "%s " "${whitelist[@]}"
echo "Whitelist: $whitelist_str"

for file in /home/matt/LLSM_Processing_GUI/LLSM5DTools/mcc/*_parser.m; do
	file_name=$(basename "$file" .m)

    # Check if the function name contains any of the whitelisted patterns
    valid=false
    for pattern in "${whitelist[@]}"; do
        if [[ $file_name= == *"$pattern"* ]]; then
            valid=true
            break
        fi
    done

    if $valid; then
        echo "Processing function: $file_name"

        # Write the file name (function name) to the output file
        function_name=$(echo "$file_name" | sed 's/_parser//')
        echo "from .$function_name import $function_name" >> "$output_file"

        # Call your Python script here with the file path
        python PyLLSM5DTools/generatePythonWrapper.py "$file"
    else
        echo "Ignoring function: $file_name"
    fi
done

