from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
from io import StringIO
import glob

app = Flask(__name__)

# Configuration
DATA_DIR = './data'
MERGED_DIR = os.path.join(DATA_DIR, 'merged')
ALLOWED_EXTENSIONS = {'conll'}

# Create necessary directories
os.makedirs(MERGED_DIR, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_next_file_number():
    existing_files = glob.glob(os.path.join(MERGED_DIR, 'merged_*.conll'))
    if not existing_files:
        return 1
    numbers = [int(f.split('_')[-1].split('.')[0]) for f in existing_files]
    return max(numbers) + 1

def merge_conll_contents(contents):
    def process_content(content, output_buffer, is_first_file=False):
        previous_line_empty = True if is_first_file else False
        for line in content.split('\n'):
            line = line.rstrip()
            if line.startswith('-DOCSTART-'):
                continue
            if line or not previous_line_empty:
                output_buffer.write(line + '\n')
                previous_line_empty = (line == '')

    output_buffer = StringIO()
    output_buffer.write('-DOCSTART- -X- O O\n\n')
    
    for i, content in enumerate(contents):
        process_content(content, output_buffer, is_first_file=(i==0))
    
    return output_buffer.getvalue()

@app.route('/merge', methods=['POST'])
def merge_files():
    files = request.files.getlist('files')
    
    if not files or len(files) < 2:
        return jsonify({
            'success': False,
            'error': 'At least two files are required'
        }), 400
    
    if any(file.filename == '' for file in files):
        return jsonify({
            'success': False,
            'error': 'Empty filename detected'
        }), 400
    
    if not all(allowed_file(file.filename) for file in files):
        return jsonify({
            'success': False,
            'error': 'Invalid file type. Only .conll files are allowed'
        }), 400
    
    try:
        # Read the content of all files
        contents = [file.read().decode('utf-8') for file in files]
        
        # Merge the contents
        merged_content = merge_conll_contents(contents)
        
        # Get next file number and create formatted number string
        file_number = get_next_file_number()
        formatted_number = f"{file_number:04d}"
        
        # Create output filename and path
        output_filename = f"merged_{formatted_number}.conll"
        output_path = os.path.join(MERGED_DIR, output_filename)
        
        # Save the merged content
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(merged_content)
        
        # Return success response with file information
        return jsonify({
            'success': True,
            'message': 'Files merged successfully',
            'file_path': output_path,
            'file_name': output_filename,
            'merged_files': [file.filename for file in files],
            'number_of_files_merged': len(files),
            'status': 'Merged successfully'
        })
    
    except UnicodeDecodeError:
        return jsonify({
            'success': False,
            'error': 'Invalid file encoding. Files must be UTF-8 encoded'
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

@app.route('/list-merged', methods=['GET'])
def list_merged_files():
    merged_files = glob.glob(os.path.join(MERGED_DIR, 'merged_*.conll'))
    merged_files = [os.path.basename(f) for f in merged_files]
    return jsonify({
        'success': True,
        'merged_files': sorted(merged_files)
    })

if __name__ == '__main__':
    app.run(debug=True, port=5004)