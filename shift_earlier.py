import datetime
import sys

def parse_srt_time(time_str):
    return datetime.datetime.strptime(time_str.strip(), '%H:%M:%S,%f')

def format_srt_time(time_obj):
    return time_obj.strftime('%H:%M:%S,%f')[:-3]

def shift_srt_time_earlier(filename, shift_seconds):
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    new_lines = []
    for line in lines:
        if '-->' in line:
            start_time, end_time = line.split(' --> ')
            new_start_time = parse_srt_time(start_time) - datetime.timedelta(seconds=shift_seconds)
            new_end_time = parse_srt_time(end_time) - datetime.timedelta(seconds=shift_seconds)
            new_lines.append(f"{format_srt_time(new_start_time)} --> {format_srt_time(new_end_time)}\n")
        else:
            new_lines.append(line)
    
    new_filename = filename.replace('.srt', f'_shifted_{-shift_seconds}s.srt')
    with open(new_filename, 'w') as file:
        file.writelines(new_lines)
    
    return new_filename

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python shift_earlier.py <filename> <shift_seconds>")
    else:
        filename = sys.argv[1]
        shift_seconds = float(sys.argv[2])
        new_filename = shift_srt_time_earlier(filename, shift_seconds)
        print(f"New file created: {new_filename}")
